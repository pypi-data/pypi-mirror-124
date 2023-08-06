#!/usr/bin/env python3

"""Definition of class Grid."""

import logging
from typing import Any, Tuple

from pygwin import types, Box, Pos, Node


class Grid(Box):
    """A Grid is a Box of which one of the two dimensions is bounded.

    The width or height of the grid can be set via the size style or
    the grid-row-size style.

    For example, this create a vertical grid of which each row can
    contain at most four nodes.  So when packing a fifth node in the
    grid, this fifth node is automatically put in a second row:
    >>> g = Grid(style={'orientation': 'vertical', 'grid-row-size': 4})

    This is an example of a 100 pixel wide grid:
    >>> g = Grid(style={'orientation': 'vertical', 'size': (100, None)})

    Only vertical grids (that grow vertically) are supported for now.

    """

    AVAILABLE_STYLES = {
        'grid-row-size'
    }

    def __init__(self, *nodes: Node, **kwargs: Any):
        """Initialise a Grid node with nodes inside."""
        Box.__init__(self, *nodes, **kwargs)
        if self.get_style('orientation') == 'horizontal':
            logging.warning('unimplemented feature: horizontal grids')
            self.set_style('orientation', 'vertical')

    def _compute_inner_size(self) -> types.pos_t:
        def update_result(result: Tuple[int, int]) -> Tuple[int, int]:
            if result == (0, 0):
                return rw, rh
            return max(result[0], rw), result[1] + spacing[1] + rh

        w, h = self._precompute_inner_size()
        sizes = list(map(lambda child: child._compute_size(), self.children))
        if w is not None and h is not None:
            return w, h

        orientation = self.get_style('orientation')
        spacing = self.get_style('hspacing'), self.get_style('vspacing')
        row_size = self.get_style('grid-row-size')

        #  check that the size of component grids could have been
        #  computed
        try:
            for cw, ch in sizes:
                assert isinstance(cw, int) and isinstance(ch, int)
        except (AssertionError, TypeError) as e:
            raise ValueError(
                'cannot determine size of a grid component'
            ) from e

        rw = 0  # row width
        rh = 0  # row height
        rs = 0  # row size

        result = 0, 0
        for cw, ch in sizes:
            if orientation == 'vertical':
                if (row_size is not None and rs >= row_size) or (
                        w is not None and rw is not None and rw + cw > w
                ):
                    result = update_result(result)
                    rw = 0
                    rs = 0
                if rs == 0:
                    rw = cw
                    rh = ch
                else:
                    rw += spacing[0] + cw
                    rh = max(rh, ch)
                rs += 1
        result = update_result(result)

        if orientation == 'vertical':
            return Pos.check(Pos.combine((w, h), result))
        raise ValueError('unimplemented feature: horizontal grids')

    def _position(self, pos: types.pos_t) -> None:
        width, height = self.get_inner_size_()
        spacing = self.get_style('hspacing'), self.get_style('vspacing')
        orientation = self.get_style('orientation')
        w = 0
        h = 0
        rw = 0
        rh = 0
        for child in self.children:
            cw, ch = child.size_
            if orientation == 'vertical':
                if w + cw > width:
                    h += spacing[1] + ch
                    w = 0
                    rh = 0
                rh = max(rh, ch)
            else:
                if h + ch > height:
                    w += spacing[0] + cw
                    h = 0
                    rw = 0
                rw = max(rw, cw)
            child.position(Pos.sum(pos, (w, h)))
            if orientation == 'vertical':
                w += spacing[1] + cw
            else:
                h += spacing[0] + ch
