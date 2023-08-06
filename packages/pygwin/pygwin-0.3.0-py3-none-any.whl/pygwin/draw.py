#!/usr/bin/env python3

"""Definition of class Draw."""

from typing import Any
import pygame as pg

from . import types, Pos


class Draw:
    """Class Draw provides several drawing functions."""

    BLACK = (0, 0, 0, 0)

    @classmethod
    def rectangle(
            cls,
            surface: pg.surface.Surface,
            color: Any,
            rect: Any,
            width: int = 0
    ) -> None:
        """Draw a rectangle rect."""
        x, y, w, h = rect
        if w == 0 or h == 0:
            return
        if width == 0 or width is None:
            pg.draw.rect(surface, color, rect, width)
        else:
            if width > 2 * w or width > 2 * h:
                msg = f'incorrect width for a ({w}, {h}) rectangle: {width}'
                raise ValueError(msg)
            pg.draw.rect(surface, color, (x, y, w, width))
            pg.draw.rect(surface, color, (x, y, width, h))
            pg.draw.rect(surface, color, (x + w - width, y, width, h))
            pg.draw.rect(surface, color, (x, y + h - width, w, width))

    @classmethod
    def rectangle_rounded(
            cls,
            surface: pg.surface.Surface,
            color: Any,
            rect: Any,
            radius: int,
            width: int = 0
    ) -> None:  # pylint: disable=R0913
        """Draw a rounded rectangle rect."""

        def draw_sub_rects() -> None:
            #  draw sub rectangles
            if width == 0 or width is None:
                rects = [
                    (x + radius, y, w - 2 * radius + 1, radius),
                    (x, y + radius, w, h - 2 * radius),
                    (x + radius, y + h - radius, w - 2 * radius + 1, radius)
                ]
            else:
                rects = [
                    (x + radius, y, w - 2 * radius + 1, width),
                    (x + radius, y + h - width, w - 2 * radius + 1, width),
                    (x, y + radius, width, h - 2 * radius),
                    (x + w - width, y + radius, width, h - 2 * radius)
                ]
            for r in rects:
                Draw.rectangle(surface, color, r)

        def draw_angles() -> None:
            #  draw rounded angles
            circle = pg.Surface((radius * 2, radius * 2)).convert_alpha()
            circle.fill(Draw.BLACK)
            pg.draw.circle(
                circle, color, (radius, radius), radius
            )
            if not (width == 0 or width is None):
                pg.draw.circle(
                    circle, Draw.BLACK, (radius, radius), radius - width
                )
            cs = (radius, radius)
            for pos, area in [
                    ((x, y), Pos.rect((0, 0), cs)),
                    ((x + w - radius, y), Pos.rect((radius, 0), cs)),
                    ((x, y + h - radius), Pos.rect((0, radius), cs)),
                    ((x + w - radius, y + h - radius), Pos.rect(cs, cs))
            ]:
                surface.blit(circle, pos, area=pg.Rect(area))

        x, y, w, h = rect
        radius = min(radius, int(w / 2), int(h / 2))

        #  no radius => simple rectangle drawing
        if radius == 0 or radius is None:
            Draw.rectangle(surface, color, rect, width)
            return

        draw_sub_rects()
        draw_angles()

    @classmethod
    def circle(
            cls,
            surface: pg.surface.Surface,
            color: Any,
            origin: types.pos_t,
            radius: int,
            width: int = 0
    ) -> None:  # pylint: disable=R0913
        """Draw a circle."""
        if width == 0:
            pg.draw.circle(surface, color, origin, radius)
        else:
            circle = pg.Surface((radius * 2, radius * 2)).convert_alpha()
            circle.fill(Draw.BLACK)
            pg.draw.circle(
                circle, color, (radius, radius), radius)
            pg.draw.circle(
                circle, Draw.BLACK, (radius, radius), radius - width)
            surface.blit(circle, (origin[0] - radius, origin[1] - radius))
