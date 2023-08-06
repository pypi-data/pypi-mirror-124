#!/usr/bin/env python3

"""Definition of class ScrollAnimation."""

import logging
from typing import Any, Optional, TYPE_CHECKING

from .node_animation import NodeAnimation
if TYPE_CHECKING:
    from .. import Frame


class ScrollAnimation(NodeAnimation):
    """A ScrollAnimation updates periodically the scrolling of a Frame."""

    def __init__(self, frame: 'Frame', **kwargs: Any):
        """Initialise a ScrollAnimation for frame.

        kwarg move is the number of pixels the scrolling is updated at
        each execution of the animation.

        """
        def handler(_: bool) -> Optional[bool]:
            try:
                frame.vscroll_move(move)
                if frame.at_bottom() or frame.at_top():
                    return None
                return True
            except AttributeError:
                logging.error(
                    'scrollable node expected, got a %s node.',
                    type(frame).__name__
                )
                raise
        move = kwargs.pop('move', 1)
        kwargs.setdefault('period', 5)
        NodeAnimation.__init__(
            self,
            frame,
            True,
            handler,
            **{**kwargs, 'persistent': False}
        )
