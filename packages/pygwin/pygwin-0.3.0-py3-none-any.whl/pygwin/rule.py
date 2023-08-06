#!/usr/bin/env python3

"""Definition of class Rule."""

import pygame as pg

from . import Draw, Node, Pos, Media, types


class Rule(Node):
    """Rule nodes are horizontal or vertical lines."""

    AVAILABLE_STYLES = {
        'rule-images'
    }

    def get_dim(self) -> int:  # pylint: disable=no-self-use
        """Get the dimension of the rule (0 = horizontal, 1 = vertical)."""
        return 0

    def _draw(self, surface: pg.surface.Surface, pos: types.pos_t) -> None:
        imgs = self.get_style('rule-images')
        size = self.get_inner_size_()
        dim = self.get_dim()
        if imgs is None:
            Draw.rectangle(
                surface,
                self.get_style('color'),
                Pos.rect(pos, size)
            )
        else:
            lpos = list(pos)
            start, middle, end = (Media.get_image_(img) for img in imgs)
            surface.blit(start, lpos)
            shift = start.get_size()[dim]
            middle_size = middle.get_size()[dim]
            while shift < size[dim]:
                rect = None
                if middle_size + shift > size[dim]:
                    rect_size = {
                        dim: size[dim] - shift,
                        (dim + 1) % 2: middle_size
                    }
                    rect = pg.rect.Rect(0, 0, rect_size[0], rect_size[1])
                lpos[dim] += shift
                surface.blit(middle, lpos, rect)
                lpos[dim] -= shift
                shift += middle_size
            lpos[dim] += size[dim] - end.get_size()[dim]
            surface.blit(end, lpos)
