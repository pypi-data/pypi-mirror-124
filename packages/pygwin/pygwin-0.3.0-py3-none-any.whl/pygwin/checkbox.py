#!/usr/bin/env python3

"""Definition of class Checkbox."""

from typing import Any
import pygame as pg

from . import types, Draw, ValuedNode, Pos


class Checkbox(ValuedNode):
    """Checkbox are square boxes used to select options."""

    AVAILABLE_STYLES = {
        'color'
    }

    def __init__(self, **kwargs: Any):
        """Initialise a Checkbox node.

        Kwarg value is True if the checkbox is initially checked
        (default is False).

        """
        def click_event(_: pg.event.Event) -> bool:
            if self.is_clicked():
                return self.activate()
            return False
        kwargs.setdefault('value', False)
        ValuedNode.__init__(self, **kwargs)
        self.add_processor('on-click-up', click_event)

    def can_grab_focus(self) -> bool:
        return True

    def _activate(self) -> bool:
        self.get_focus()
        self.set_value(not self.value)
        return True

    def _compute_inner_size(self) -> types.pos_t:
        return 20, 20

    def _draw(self, surface: pg.surface.Surface, pos: types.pos_t) -> None:
        #  if the checkbox has a background image we don't draw anything
        img = self.get_style('background-image')
        if img is None and self.value:
            color = self.get_style('color')
            Draw.rectangle(
                surface, color, Pos.rect(pos, self.get_inner_size_())
            )
