#!/usr/bin/env python3

"""Definition of class VerticalRule."""

from . import types, Rule, Media


class VerticalRule(Rule):
    """VerticalRule nodes are vertical lines."""

    def _compute_inner_size(self) -> types.pos_t:
        imgs = self.get_style('rule-images')
        if imgs is None:
            w = 4
        else:
            w = max(Media.get_image_(img).get_width() for img in imgs)
        return w, 100

    def get_dim(self) -> int:
        return 1
