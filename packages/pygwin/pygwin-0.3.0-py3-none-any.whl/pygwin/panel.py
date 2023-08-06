#!/usr/bin/env python3

"""Definition of class Panel."""

from typing import Optional

from . import types, Window


class Panel(Window):
    """Document this method."""

    def open(self, pos: Optional[types.pos_t] = None) -> None:
        """Open self at the given position."""
        assert pos is not None
        self.window_system.open_panel(self, pos=pos)
