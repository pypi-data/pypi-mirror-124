#!/usr/bin/env python3

"""Definition of class Label."""

from typing import Optional, Any
import functools
import pygame as pg

from . import types, Node, Util


class Label(Node):
    """Label nodes are used to draw texts."""

    AVAILABLE_STYLES = {
        'color',
        'underline'
    }

    def __init__(
            self,
            text: str,
            **kwargs: Any
    ) -> None:
        """Initialise a label with the given text.

        If not None, kwarg label_for must be a Node object.  If the
        label is clicked or activated then node label_for is activated.

        """
        Node.__init__(self, **kwargs)
        self.__text: str
        label_for: Optional[Node] = kwargs.get('label_for')
        if label_for is not None:
            def link() -> bool:
                assert label_for is not None
                label_for.activate()
                return True
            self.set_link(link)
        self.set_text(text)

    @property
    def text(self) -> str:
        """Text of the label."""
        return self.__text

    def set_text(self, text: str) -> None:
        """Set the text of the label."""
        self.__text = text
        self._reset_size()

    @classmethod
    def node_of(cls, value: Any, **kwargs: Any) -> Node:
        """Return value if it is a Node, or Label(value, **kwargs) else."""
        if isinstance(value, Node):
            result = value
        else:
            result = Label(str(value), **kwargs)
        return result

    @classmethod
    @functools.lru_cache(maxsize=10000)
    def __render_cache(
            cls,
            text: str,
            font: pg.font.Font,
            color: types.color_t,
            **kwargs: Any
    ) -> pg.surface.Surface:
        font.set_underline(kwargs.get('underline', False))
        result = next(Util.split_lines(text, font, color))
        font.set_underline(False)
        return result

    @classmethod
    def __render(
            cls,
            text: str,
            font: pg.font.Font,
            color: Any,
            **kwargs: Any
    ) -> pg.surface.Surface:
        return Label.__render_cache(text, font, tuple(color), **kwargs)

    def __redraw(self) -> pg.surface.Surface:
        return Label.__render(
            self.__text,
            self.get_font(),
            self.get_style('color'),
            underline=self.get_style('underline')
        )

    def _compute_inner_size(self) -> types.pos_t:
        return self.__redraw().get_size()

    def _draw(self, surface: pg.surface.Surface, pos: types.pos_t) -> None:
        surface.blit(self.__redraw(), pos)
