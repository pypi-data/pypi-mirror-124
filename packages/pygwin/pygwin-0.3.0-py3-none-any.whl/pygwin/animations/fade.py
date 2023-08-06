#!/usr/bin/env python3

"""Definition of class FadeAnimation."""

from typing import Any, Optional, TYPE_CHECKING

from .node_animation import NodeAnimation
if TYPE_CHECKING:
    from .. import Node


class FadeAnimation(NodeAnimation):
    """A FadeAnimation makes a node progressively appear or disappear."""

    def __init__(self, node: 'Node', **kwargs: Any):
        """Initialise a FadeAnimation for node.

        kwarg step (default = -0.02) specifies how the opacity is
        modified at each execution of the animation.

        """
        def handler(_: bool) -> Optional[bool]:
            opacity = node.get_style('opacity')
            if opacity is None:
                opacity = 1.0
            opacity += step
            opacity = min(1.0, max(0.0, opacity))
            result: Optional[bool] = True
            if opacity in (0, 1):
                result = None
            if opacity == 1:
                opacity = None
            node.set_style('opacity', opacity, cname=self.tmp_class)
            return result
        step = kwargs.get('step', -0.02)
        NodeAnimation.__init__(self, node, True, handler, **kwargs)


class FadeInAnimation(FadeAnimation):
    """A FadeAnimation makes a node progressively appear."""

    def __init__(self, node: 'Node', **kwargs: Any):
        """Initialise a FadeInAnimation for node."""
        kwargs.setdefault('step', 0.1)
        kwargs.setdefault('persistent', True)
        node.set_style('opacity', 0.0)
        super().__init__(node, **kwargs)


class FadeOutAnimation(FadeAnimation):
    """A FadeAnimation makes a node progressively disappear."""

    def __init__(self, node: 'Node', **kwargs: Any):
        """Initialise a FadeOutAnimation for node."""
        kwargs.setdefault('step', -0.1)
        kwargs.setdefault('persistent', True)
        node.set_style('opacity', 1.0)
        super().__init__(node, **kwargs)
