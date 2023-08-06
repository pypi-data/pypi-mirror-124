#!/usr/bin/env python3

"""Definition of class Pos."""

from typing import Optional
import math

from . import types


class Pos:
    """Class Pos defines basic class methods to work with (x, y) positions."""

    @classmethod
    def diff(cls, c1: types.pos_t, c2: types.pos_t) -> types.pos_t:
        """
        Get the difference between two coordinates.

        >>> Pos.diff((4, 3), (2, 5))
        (2, -2)

        """
        return c1[0] - c2[0], c1[1] - c2[1]

    @classmethod
    def sum(cls, c1: types.pos_t, c2: types.pos_t) -> types.pos_t:
        """Get the sum of two coordinates.

        >>> Pos.sum((4, 3), (2, 5))
        (6, 8)

        """
        return c1[0] + c2[0], c1[1] + c2[1]

    @classmethod
    def mult(cls, c: types.pos_t, mult: int) -> types.pos_t:
        """Multiply the coordinate by mult.

        >>> Pos.mult((4, 3), 2.5)
        (10, 7)

        """
        return int(c[0] * mult), int(c[1] * mult)

    @classmethod
    def in_rect(cls, rect: types.rect_t, pt: types.pos_t) -> bool:
        """Check if point pt is in rect.

        >>> Pos.in_rect((1, 0, 4, 8), (1, 1))
        True
        >>> Pos.in_rect((1, 0, 4, 8), (4, 0))
        True
        >>> Pos.in_rect((1, 0, 4, 8), (5, 10))
        False

        """
        x, y = pt
        xr, yr, w, h = rect
        return xr <= x < xr + w and yr <= y < yr + h

    @classmethod
    def rect(cls, pos: types.pos_t, size: types.pos_t) -> types.rect_t:
        """Get a rectangle from position pos and size size.

        >>> Pos.rect((100, 100), (200, 200))
        (100, 100, 200, 200)

        """
        return pos[0], pos[1], size[0], size[1]

    @classmethod
    def center(cls, rect: types.rect_t) -> types.pos_t:
        """Get the center point of rectangle rect.

        >>> Pos.center(Pos.rect((100, 100), (400, 300)))
        (300, 250)

        """
        return rect[0] + int(rect[2] / 2), rect[1] + int(rect[3] / 2)

    @classmethod
    def ge(cls, pt1: types.pos_t, pt2: types.pos_t) -> bool:
        """Check if point pt1 is greater than or equal to point pt2.

        >>> Pos.ge((2, 3), (1, 0))
        True
        >>> Pos.ge((1, 1), (1, 0))
        True
        >>> Pos.ge((1, 1), (1, 1))
        True
        >>> Pos.ge((1, 1), (1, 2))
        False

        """
        return pt1[0] >= pt2[0] and pt1[1] >= pt2[1]

    @classmethod
    def gt(cls, pt1: types.pos_t, pt2: types.pos_t) -> bool:
        """Check if point pt1 is strictly greater than pt2.

        >>> Pos.gt((2, 3), (1, 0))
        True
        >>> Pos.gt((0, 1), (0, 0))
        True
        >>> Pos.gt((1, 0), (1, 0))
        False

        """
        return Pos.ge(pt1, pt2) and pt1 != pt2

    @classmethod
    def distance(cls, pt1: types.pos_t, pt2: types.pos_t) -> float:
        """Compute the distance between points pt1 and pt2.

        >>> '%.2f' % Pos.distance((1, 1), (1, 0))
        '1.00'
        >>> '%.2f' % Pos.distance((0, 0), (-1, -1))
        '1.41'

        """
        return math.sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)

    @classmethod
    def floating_to_pos(
            cls,
            pos: types.floating_pos_t,
            node_size: types.pos_t,
            cont_size: Optional[types.pos_t] = None,
            rect: Optional[types.rect_t] = None
    ) -> types.pos_t:
        """Compute an (x, y) position from a floating position pos.

        node_size is the size of the node of which we compute the
        positions.  If the floating position is an absolute one,
        cont_size may not be None and is the size of the container
        (e.g., a window) this node is put into.  If the floating
        position is a relative one, rect may not be None and is the
        rectangle to which the floating position is defined relatively.

        >>> Pos.floating_to_pos(
        ...    ('absolute', ('left', 'top'), (10, 10)),
        ...    (100, 100), cont_size=(1000, 1000))
        (10, 10)
        >>> Pos.floating_to_pos(
        ...    ('absolute', ('right', 'bottom'), (10, 10)), (100, 100),
        ...    cont_size=(1000, 1000))
        (890, 890)
        >>> Pos.floating_to_pos(
        ...    ('relative', ('left', 'top'), (0, 0)),
        ...    (100, 100), rect=(100, 100, 1000, 1000))
        (0, 0)
        >>> Pos.floating_to_pos(
        ...    ('relative', ('right', 'bottom'), (0, 0)),
        ...    (100, 100), rect=(100, 100, 200, 200))
        (300, 300)

        """
        xanchor, yanchor = pos[1]
        x, y = pos[2]
        if pos[0] == 'absolute':
            if cont_size is None:
                raise ValueError('cont_size expected')
            if xanchor == 'right':
                x = - x
            if yanchor == 'bottom':
                y = - y
            return Pos.align(
                (x, y), node_size, cont_size, xanchor, yanchor
            )
        if pos[0] == 'relative':
            if rect is None:
                raise ValueError('rect expected')
            nw, nh = node_size
            rx, ry, rw, rh = rect
            if xanchor == 'right':
                x = rx + rw
            elif xanchor == 'center':
                x = rx + int((rw - nw) / 2)
            else:
                x = rx - nw
            if yanchor == 'bottom':
                y = ry + rh
            elif yanchor == 'center':
                y = ry + int((rh - nh) / 2)
            else:
                y = ry - nh
            return x, y
        raise ValueError('undefined positioning type: {pos[0]}')

    @classmethod
    def combine(
            cls,
            c0: types.opt_pos_opt_t,
            *c1: types.pos_opt_t
    ) -> types.pos_opt_t:
        """Take components of c0 if not None or otherwise positions of c1.

        >>> Pos.combine(None, (1, 2))
        (1, 2)
        >>> Pos.combine((None, None), (1, 4))
        (1, 4)
        >>> Pos.combine((3, None), (1, 2))
        (3, 2)
        >>> Pos.combine((3, None), (1, None), (1, 4))
        (3, 4)

        """
        result = c0
        for c in c1:
            if result is None:
                result = c
            else:
                if result[0] is None and c[0] is not None:
                    result = c[0], result[1]
                if result[1] is None and c[1] is not None:
                    result = result[0], c[1]
        return Pos.check(result)

    @classmethod
    def check(cls, c: types.opt_pos_opt_t) -> types.pos_t:
        """Check if position c if fully defined (without None in it).

        Return c is the c is fully defined or raise AssertionError
        otherwise.

        >>> Pos.check((1, 1))
        (1, 1)
        >>> Pos.check(None)
        Traceback (most recent call last):
        AssertionError
        >>> Pos.check((2, None))
        Traceback (most recent call last):
        AssertionError

        """
        assert c is not None
        x, y = c
        assert x is not None
        assert y is not None
        return x, y

    @classmethod
    def align(
            cls,
            pos: types.pos_t,
            size: types.pos_t,
            cont_size: types.opt_pos_t,
            halign: types.halign_t,
            valign: types.valign_t
    ) -> types.pos_t:  # pylint: disable=R0913
        """Compute a position according to some aligment.

        If pos is the position of a node with the given size and
        container size, then align returns this position modified
        according to horizontal and vertical aligments halign and
        valign.

        >>> Pos.align((0, 0), (10, 10), (100, 100), 'left', 'top')
        (0, 0)
        >>> Pos.align((0, 0), (10, 10), (100, 100), 'center', 'center')
        (45, 45)
        >>> Pos.align((0, 0), (10, 10), (100, 100), 'right', 'bottom')
        (90, 90)

        """
        if cont_size is None:
            return pos
        x, y = pos
        w, h = size
        cw, ch = cont_size
        if halign == 'center':
            x += int((cw - w) / 2)
        elif halign == 'right':
            x += cw - w
        if valign == 'center':
            y += int((ch - h) / 2)
        elif valign == 'bottom':
            y += ch - h
        return x, y
