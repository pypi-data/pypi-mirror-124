#!/usr/bin/env python3

"""Definition of class Gauge."""

from typing import Iterator, Any
import pygame as pg

from . import types, Draw, ValuedNode, Label, Node
from .min_max import _MinMax


class Gauge(_MinMax, ValuedNode):
    """Gauge nodes are used to draw status bars (e.g., health bars in RPGs)."""

    AVAILABLE_STYLES = {
        'color',
        'gauge-label-class',
        'gauge-label-format'
    }

    def __init__(
            self,
            min_value: int,
            max_value: int,
            value: int,
            **kwargs: Any
    ):
        """Initialise a Gauge node.

        The value of the gauge ranges from min_value to max_value and
        is initialised to value.

        """
        ValuedNode.__init__(self, value=value, **kwargs)
        _MinMax.__init__(self, min_value, max_value)
        label_format = self.get_style('gauge-label-format')
        if label_format is None:
            self.__label = None
        else:
            self.__label = Label('', stc=self.get_style('gauge-label-class'))
            self.__set_label()
            self._add_child(self.__label)

    def set_value(self, value: int, trigger: bool = True) -> None:
        """Update the current value of the gauge."""
        ValuedNode.set_value(self, value, trigger=trigger)
        self.__set_label()

    def __set_label(self) -> None:
        if self.__label is not None:
            label_format = self.get_style('gauge-label-format')
            label = label_format.format(
                min=self.min_value, value=self.value, max=self.max_value
            )
            self.__label.set_text(label)

    def _compute_inner_size(self) -> types.pos_t:
        if self.__label is not None:
            self.__label._compute_size()
        return (200, 40)

    def _position(self, pos: types.pos_t) -> None:
        if self.__label is not None:
            self.__label._set_container_size(self.get_inner_size_())
            self.__label.position(pos)

    def _draw(self, surface: pg.surface.Surface, pos: types.pos_t) -> None:
        w, h = self.get_inner_size_()
        color = self.get_style('color')
        pts = int(self.value * w / (self.max_value - self.min_value))
        rect = (pos[0], pos[1], pts, h)
        Draw.rectangle(surface, color, rect)

    def _iter_tree(
            self, rec: bool = True, traverse: bool = False
    ) -> Iterator[Node]:
        if self.__label is not None:
            yield from self.__label.iter_tree(traverse=traverse)
