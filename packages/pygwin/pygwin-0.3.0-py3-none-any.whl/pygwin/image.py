#!/usr/bin/env python3

"""Definition of class Image."""

from typing import Any
import pygame as pg

from . import types, Node


class Image(Node):
    """Image nodes are placeholders for pygame surfaces."""

    def __init__(self, surface: pg.surface.Surface, **kwargs: Any):
        """Initialise an Image node holding the given surface."""
        Node.__init__(self, **kwargs)
        self.__surface = surface

    @property
    def surface(self) -> pg.surface.Surface:
        """Get the pygame surface of the image."""
        return self.__surface

    def set_surface(self, surface: pg.surface.Surface) -> None:
        """Update the pygame surface of the image."""
        self.__surface = surface
        self._reset_size()

    def _compute_inner_size(self) -> types.pos_t:
        return self.__surface.get_size()

    def _draw(self, surface: pg.surface.Surface, pos: types.pos_t) -> None:
        surface.blit(self.__surface, pos)
