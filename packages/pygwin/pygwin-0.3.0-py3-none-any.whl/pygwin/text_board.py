#!/usr/bin/env python3

"""Definition of class TextBoard."""

from typing import Any, List, Optional

from . import types, Box, Util, Image


class TextBoard(Box):
    """TextBoard nodes are boxes that contains text.

    The text in a TextBoard is always split in several Label nodes
    such that each of these Labels does not exceed the width of the
    board.  A TextBoard can grow dynamically with new text using the
    push_text method.

    """

    AVAILABLE_STYLES = {
        'color',
        'text-board-push-dest',
        'text-board-rows'
    }

    def __init__(self, text: Optional[str] = None, **kwargs: Any):
        """Initialise a TextBoard containing optional string text."""
        Box.__init__(self, **kwargs)
        self.__text: List[str] = list()
        self.__pending: List[str] = list()
        self.__text_width: Optional[int] = None
        if text is not None:
            self.push_text(text)

    @property
    def text(self) -> List[str]:
        """Get texts pushed on the board."""
        return self.__text

    def push_text(self, text: str) -> None:
        """Push a new text string on the board."""
        self.__text.append(text)
        self.__pending.append(text)
        self._reset_size()

    def _compute_inner_size(self) -> types.pos_t:
        width = self.get_width()
        if width is None:
            return 0, 0
        if self.__text_width != width:
            self.__text_width = width
            self.empty()
            text_list = self.__text
        elif self.__pending != []:
            text_list = self.__pending
        else:
            text_list = []
        self.__pending = []

        for text in text_list:
            lines = list(
                Util.split_lines(
                    text, self.get_font(), self.get_style('color'),
                    width=self.__text_width
                )
            )
            dest = self.get_style('text-board-push-dest')
            if dest == 'top':
                lines.reverse()
            for line in lines:
                lbl = Image(line)
                if dest == 'top':
                    self.insert(0, lbl)
                else:
                    self.pack(lbl)

        self.__remove_overflowing_lines()
        return Box._compute_inner_size(self)

    def __remove_overflowing_lines(self) -> None:
        rows = self.get_style('text-board-rows')
        if rows is not None:
            dest = self.get_style('text-board-push-dest')
            while len(self.children) > rows:
                if dest == 'top':
                    self.remove(rows)
                else:
                    self.remove(0)
