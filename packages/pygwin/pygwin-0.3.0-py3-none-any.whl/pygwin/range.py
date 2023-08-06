#!/usr/bin/env python3

"""Definition of class Range."""

from typing import Any, Tuple, Optional, Union, Iterator
import math
import pygame as pg

from . import Node, ValuedNode, Label, Draw, Pos, Util, types
from .min_max import _MinMax


class Range(_MinMax, ValuedNode):
    """Range nodes are similar to <input type="range"> HTML elements."""

    AVAILABLE_STYLES = {
        'range-acceleration',
        'range-bar-color',
        'range-bar-corner',
        'range-bar-size',
        'range-bullet-color',
        'range-bullet-radius',
        'range-label-class',
        'range-label-distance',
        'range-label-format',
        'range-step'
    }

    KEY_ADD = pg.K_RIGHT
    KEY_REM = pg.K_LEFT
    KEY_FIRST = pg.K_PAGEDOWN
    KEY_LAST = pg.K_PAGEUP

    def __init__(self, min_value: int, max_value: int, **kwargs: Any):
        """Initialise a Range node with values in [min_value, max_value].

        Kwarg value is the initial value of the range (default =
        min_value).

        """
        value = kwargs.pop('value', min_value)
        ValuedNode.__init__(self, **kwargs, value=value)
        _MinMax.__init__(self, min_value, max_value)
        step: int = self.get_style('range-step')
        self.__label: Optional[Label]
        self.__speed = step
        self.__ctr = 0
        self.__last = pg.time.get_ticks()
        if not self.get_style('range-label-format'):
            self.__label = None
        else:
            self.__label = Label('', stc=self.get_style('range-label-class'))
            self.__set_label()
            self._add_child(self.__label)

        def click_down(pgevt: pg.event.Event) -> bool:
            if not self.is_disabled():
                self.get_focus()
                self.set_value(self.__x_to_value(pgevt.pos))
                return True
            return False

        def slide(pgevt: pg.event.Event) -> bool:
            if self.is_disabled() or not pg.mouse.get_pressed(3)[0]:
                return False
            self.set_value(self.__x_to_value(pgevt.pos))
            return True

        def move(pts: Optional[Union[int, float]]) -> bool:
            if pts is None:
                return False
            new_value = int(self.__fix_value(self.value + pts))
            result: bool = new_value != self.value
            if result:
                self.set_value(new_value)
            return result

        def key(pgevt: pg.event.Event) -> bool:
            if not self.has_focus() or self.is_disabled():
                return False
            try:
                now = pg.time.get_ticks()
                if now - self.__last <= 200:
                    self.__ctr += 1
                    if self.__ctr == 10:
                        self.__ctr = 0
                        self.__speed *= self.get_style('range-acceleration')
                else:
                    self.__ctr = 0
                    self.__speed = step
                self.__last = now
                return move({
                    Range.KEY_ADD: int(self.__speed),
                    Range.KEY_REM: - int(self.__speed),
                    Range.KEY_FIRST: - math.inf,
                    Range.KEY_LAST: math.inf
                }[pgevt.key])
            except KeyError:
                return False

        def mouse_wheel(pgevt: pg.event.Event) -> bool:
            self.get_focus()
            try:
                return move({
                    Util.MOUSEBUTTON_WHEEL_UP: int(step),
                    Util.MOUSEBUTTON_WHEEL_DOWN: - int(step),
                }[pgevt.button])
            except KeyError:
                return False

        self.add_processor('on-click-down', click_down)
        self.add_processor('on-over', slide)
        self.add_processor('on-over-again', slide)
        self.add_processor('on-key', key)
        self.add_processor('on-mouse-wheel', mouse_wheel)

    def can_grab_focus(self) -> bool:
        return True

    def set_value(self, value: Any, trigger: bool = True) -> None:
        ValuedNode.set_value(self, value, trigger=trigger)
        self.__set_label()

    def __set_label(self) -> None:
        if self.__label is not None:
            self.__label.set_text(
                self.get_style('range-label-format').format(
                    max=self.max_value, min=self.min_value, value=self.value
                )
            )

    def __fix_value(self, value: int) -> int:
        return max(self.min_value, min(self.max_value, value))

    def __value_to_x(self, x0: int) -> int:
        br = self.get_style('range-bullet-radius')
        w = self.get_style('range-bar-size')[0]
        result = int(
            x0 + br + w * (self.value - self.min_value) /
            (self.max_value - self.min_value)
        )
        return result

    def __x_to_value(self, pos: types.pos_t) -> int:
        br = self.get_style('range-bullet-radius')
        w = self.get_style('range-bar-size')[0]
        step = self.get_style('range-step')
        pos = Pos.diff(pos, self.get_absolute_pos())
        x = Pos.sum(pos, self._get_inner_shift())[0]
        x0 = br + self._get_inner_shift()[0]
        units = round(
            (x - x0) / (w / ((self.max_value - self.min_value) / step))
        )
        return self.__fix_value(int(self.min_value + units * step))

    def _compute_inner_size(self) -> Tuple[int, int]:
        br = self.get_style('range-bullet-radius')
        w, h = self.get_style('range-bar-size')
        h = max(h, br * 2)
        w = w + br * 2
        if self.__label is not None:
            self.__label._compute_size()
            h += self.__label.size_[1] + self.get_style('range-label-distance')
        return w, h

    def _position(self, pos: types.pos_t) -> None:
        if self.__label is not None:
            x, y = pos
            x += int((self.size_[0] - self.__label.size_[0]) / 2)
            self.__label.position((x, y))

    def _draw(self, surface: pg.surface.Surface, pos: types.pos_t) -> None:
        br = self.get_style('range-bullet-radius')
        w, h = self.get_style('range-bar-size')
        x, y = pos
        if self.__label is not None:
            y += self.__label.size_[1] + self.get_style('range-label-distance')
        x += br
        Draw.rectangle_rounded(
            surface,
            self.get_style('range-bar-color'),
            Pos.rect((x, y), (w, h)),
            self.get_style('range-bar-corner')
        )
        Draw.circle(
            surface,
            self.get_style('range-bullet-color'),
            (self.__value_to_x(pos[0]), int(y + h / 2)),
            br
        )

    def _iter_tree(
            self, rec: bool = True, traverse: bool = False
    ) -> Iterator[Node]:
        if self.__label is not None:
            yield from self.__label.iter_tree(rec=rec, traverse=traverse)
