#!/usr/bin/env python3

"""Definition of class InputText."""

import re
from typing import Tuple, List, Optional, Any
import pygame as pg

from . import types, Util, ValuedNode, Pos


class InputText(ValuedNode):  # pylint: disable=R0902
    """InputText nodes are similar to <input type="text"> HTML elements."""

    AVAILABLE_STYLES = {
        'color',
        'input-text-allowed',
        'input-text-max-size',
        'input-text-placeholder'
    }

    def __init__(self, **kwargs: Any):
        """Initialise a new InputText.

        Kwarg value is the initial value of the input text.  default
        is ''.

        Kwarg prompt is a string displayed at the beginning of the
        input text.  Default is ''.

        """
        def click_event(_: pg.event.Event) -> bool:
            if not self.is_disabled():
                self.get_focus()
                return True
            return False

        def key_event(evt: pg.event.Event) -> bool:
            if not self.has_focus() or self.is_disabled():
                result = False
            else:
                result = self.new_key(evt.key, evt.unicode)
            return result
        kwargs.setdefault('value', '')
        ValuedNode.__init__(self, **kwargs)
        self.__prompt: Optional[str] = kwargs.get('prompt')
        self.__cursor: int = len(kwargs['value'])
        self.__xshift: int = 0
        self.__prev: Optional[Tuple[
            bool, Optional[str], str, int, types.color_t, pg.font.Font]] = None
        self.__prompt_surface: Optional[pg.surface.Surface] = None
        self.__surface: pg.surface.Surface = self.__redraw()
        self.add_processor('on-click-up', click_event)
        self.add_processor('on-key', key_event)

    def can_grab_focus(self) -> bool:
        return True

    def _does_process_key(self, uni: str) -> bool:
        return self.is_char_allowed(uni)

    def is_char_allowed(self, char: str) -> bool:
        """Check is char is allowed to be typed in the input text."""
        allowed = self.get_style('input-text-allowed')
        reg_exp = r'[' + str(allowed) + ']+'
        return char != '' and re.fullmatch(reg_exp, char) is not None

    def set_value(self, value: str, trigger: bool = True) -> None:
        """Change the value of the input text.

        If trigger is True, the on-change event of the input text is
        triggered.

        """
        ValuedNode.set_value(self, value, trigger=trigger)
        self.__cursor = Util.in_range(self.__cursor, (0, len(value)))
        self.__redraw()

    def append_value(self, value: str) -> None:
        """Concatenate value to the current value of the input text."""
        self.set_value(self.value + value)

    def set_cursor_at_end(self) -> None:
        """Place the cursor at the end of the input text."""
        self.__cursor = len(self.value)

    def set_prompt(self, prompt: str) -> None:
        """Change the prompt of the input text."""
        self.__prompt = prompt
        self.__redraw()

    def _activate(self) -> bool:
        """Activate the input text.

        If the input text has the focus then it loses it, otherwise it
        gets it.

        """
        if self.has_focus():
            self.lose_focus()
        else:
            self.get_focus()
        return True

    def new_key(self, key: int, uni: str) -> bool:
        """Key is pressed when the input text has the focus."""
        result = True
        val = self.value
        if key == pg.K_RETURN:
            self.lose_focus()
        elif key == pg.K_BACKSPACE:
            if self.__cursor > 0:
                self.__cursor -= 1
                self.set_value(val[:self.__cursor] + val[self.__cursor + 1:])
        elif key == pg.K_DELETE:
            if self.__cursor < len(val):
                self.set_value(val[:self.__cursor] + val[self.__cursor + 1:])
        elif key == pg.K_LEFT:
            self.__cursor = max(0, self.__cursor - 1)
        elif key == pg.K_RIGHT:
            self.__cursor = min(len(val), self.__cursor + 1)
        elif self.is_char_allowed(uni):
            max_size = self.get_style('input-text-max-size')
            if max_size is None or len(val) < max_size:
                char = uni
                self.set_value(
                    val[:self.__cursor] + char + val[self.__cursor:]
                )
                self.__cursor += 1
        else:
            result = False
        if result:
            self.__redraw()
        return result

    def __drawn_text(self) -> str:
        ph = self.get_style('input-text-placeholder')
        if (
                self.value == ''
                and not self.has_focus()
                and ph is not None
        ):
            result = ph
        else:
            result = self.value
        return str(result)

    def __max_text_width(self) -> int:
        result = self.get_inner_size_()[0]
        if self.__prompt_surface is not None:
            result = max(0, result - self.__prompt_surface.get_width())
        return result

    def __redraw(self) -> pg.surface.Surface:
        def draw_cursor(w: int, h: int) -> int:
            pg.draw.line(result, color, (w, 0), (w, h), 1)
            return w

        color = self.get_style('color')
        font = self.get_font()

        #  everything unchanged => exit
        if self.__prev == (
                self.has_focus(), self.__prompt, self.value,
                self.__cursor, color, font
        ):
            return self.__surface

        #  draw the prompt
        if self.__prompt is not None:
            lbl = font.render(self.__prompt, True, color)
            self.__prompt_surface = pg.Surface(lbl.get_size()).convert_alpha()
            self.__prompt_surface.fill((0, 0, 0, 0))
            self.__prompt_surface.blit(lbl, (0, 0))

        self.__prev = (
            self.has_focus(), self.__prompt, self.value,
            self.__cursor, color, font
        )
        cursor = self.__cursor

        #  create a surface for each letter in the text to draw and
        #  compute the width of the node surface (its width is the sum
        #  of all letter surface widths + 1 if the cursor is at the
        #  end of the text)
        w = 0
        h = self.get_font().get_height()
        letters: List[pg.surface.Surface] = list()
        for letter in self.__drawn_text():
            s = font.render(letter, True, color)
            letters.append(s)
            w += s.get_width()
        if cursor == len(letters):
            w += 1
        result = pg.Surface((w, h)).convert_alpha()
        result.fill((0, 0, 0, 0))

        #  copy all letter surfaces on the node surface and also draw
        #  the cursor on it
        w = 0
        cursor_pos = None
        for i, l in enumerate(letters):
            if i == cursor and self.has_focus():
                cursor_pos = draw_cursor(w, h)
            result.blit(l, (w, 0))
            w += l.get_width()
        if cursor == len(letters) and self.has_focus():
            cursor_pos = draw_cursor(w, h)

        #  adjust the xshift so that cursor remains visible
        if cursor_pos is None:
            self.__xshift = 0
        elif cursor_pos < self.__xshift:
            self.__xshift = cursor_pos
        elif cursor_pos > self.__xshift + self.__max_text_width():
            self.__xshift = cursor_pos - self.__max_text_width() + 1

        self._update_manager()
        self.__surface = result
        return result

    def _compute_inner_size(self) -> types.pos_t:
        return 200, self.get_font().get_height()

    def _draw(self, surface: pg.surface.Surface, pos: types.pos_t) -> None:
        self.__redraw()
        assert self.__surface is not None
        sh = self.__surface.get_height()
        if self.__prompt_surface is None:
            x = 0
        else:
            surface.blit(self.__prompt_surface, pos)
            x = self.__prompt_surface.get_width()
        y = int(
            (self.size_[1] - self.get_font().get_height() -
             self._get_inner_diff()[1]) / 2
        )
        surface.blit(
            self.__surface,
            Pos.sum(pos, (x, y)),
            area=pg.Rect(self.__xshift, 0, self.__max_text_width(), sh)
        )
