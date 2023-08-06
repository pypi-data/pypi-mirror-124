#!/usr/bin/env python3

"""Definition of class GrowAnimation."""

from typing import Any, Tuple, Optional, TYPE_CHECKING

from .node_animation import NodeAnimation
if TYPE_CHECKING:
    from .. import Node


class GrowAnimation(NodeAnimation):
    """A GrowAnimation updates periodically the scale style of a node."""

    def __init__(self, node: 'Node', **kwargs: Any):
        """Initialise a GrowAnimation for node.

        kwarg step indicates how much the scale is modified at each
        execution of self (default = 0.1).

        kwarg min_scale (resp. max_scale) is the minimal scale below
        (resp. above) which self won't modify node's scale (default =
        1.1 (resp. 1.0)).  If this bound is reached then self stops.

        If kwarg loop is True, then self won't stop automatically and
        will keep changing node's scale within range [min_scale,
        max_scale].

        For example, the code below creates a GrowAnimation that will
        keep updating the label's scale within range [0.8, 1.2].  The
        scale is incremented/decremented at each iteration of the game
        loop by 0.05.

        GrowAnimation(
           Label('this is a test'),
           loop=True,
           step=0.05,
           min_scale=0.8,
           max_scale=1.2
        ))

        """
        prog_t = Tuple[float, float]

        def handler(scale_step: prog_t) -> Optional[prog_t]:
            scale, step = scale_step
            scale += step
            if scale >= max_scale:
                scale = max_scale
                end_reached = True
            elif scale <= min_scale:
                scale = min_scale
                end_reached = True
            else:
                end_reached = False
            result: Optional[prog_t]
            if end_reached:
                if loop:
                    result = scale, - step
                else:
                    result = None
            else:
                result = scale, step
            node.set_style('scale', scale, cname=self.tmp_class)
            node._update_manager()
            return result

        max_scale = kwargs.pop('max_scale', 1.1)
        min_scale = kwargs.pop('min_scale', 1.0)
        loop = kwargs.pop('loop', True)
        style_scale = node.get_style('scale')
        if style_scale is None:
            scale = 1.0
        else:
            scale = style_scale
        NodeAnimation.__init__(
            self,
            node,
            (scale, kwargs.get('step', 0.01)),
            handler,
            **kwargs
        )


class PopInAnimation(GrowAnimation):
    """A PopInAnimation makes a node progressively pop in."""

    def __init__(self, node: 'Node', **kwargs: Any):
        """Initialise a PopInAnimation for node."""
        kwargs.setdefault('max_scale', 1.0)
        kwargs.setdefault('min_scale', 0.0)
        kwargs.setdefault('loop', False)
        kwargs.setdefault('persistent', True)
        kwargs.setdefault('step', 0.1)
        node.set_style('scale', 0.0)
        super().__init__(node, **kwargs)


class PopOutAnimation(GrowAnimation):
    """A PopOutAnimation makes a node progressively pop out."""

    def __init__(self, node: 'Node', **kwargs: Any):
        """Initialise a PopOutAnimation for node."""
        kwargs.setdefault('max_scale', 1.0)
        kwargs.setdefault('min_scale', 0.0)
        kwargs.setdefault('loop', False)
        kwargs.setdefault('persistent', True)
        kwargs.setdefault('step', - 0.1)
        node.set_style('scale', 1.0)
        super().__init__(node, **kwargs)
