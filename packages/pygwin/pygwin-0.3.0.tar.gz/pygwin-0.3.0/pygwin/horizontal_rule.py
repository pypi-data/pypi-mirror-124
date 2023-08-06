#!/usr/bin/env python3

"""Definition of class HorizontalRule."""

from . import types, Rule, Media


class HorizontalRule(Rule):
    """HorizontalRule nodes are horizontal lines."""

    def _compute_inner_size(self) -> types.pos_t:
        imgs = self.get_style('rule-images')
        if imgs is None:
            h = 4
        else:
            h = max(Media.get_image_(img).get_height() for img in imgs)
        return 100, h
