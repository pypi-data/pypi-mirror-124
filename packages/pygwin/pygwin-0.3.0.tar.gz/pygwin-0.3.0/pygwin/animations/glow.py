#!/usr/bin/env python3

"""Definition of class GlowAnimation."""

from typing import Any, Tuple, TYPE_CHECKING

from .node_animation import NodeAnimation
if TYPE_CHECKING:
    from .. import Node


class GlowAnimation(NodeAnimation):
    """A GlowAnimation updates periodically the color of a node."""

    def __init__(self, node: 'Node', **kwargs: Any):
        """Initialise a GlowAnimation for node.

        kwarg color_attrs is the list of color style attributes
        (default is ['border-color', 'background-color']) that are
        updated by the animation.

        kwarg amplitude is an integer specifying how far the color(s)
        can get from the initial color value(s) of the node (default =
        20).

        kwarg step indicates how much the color(s) is (are) modified
        each time the animation is run (default = 10).

        For example, if color_attrs=['color'], amplitude=20 and
        step=10 and if node.get_style('color') = (100, 100, 100).
        Then the successive executions of the animation will produce:
        node.get_style('color') = (110, 110, 110)
        node.get_style('color') = (120, 120, 120)
        node.get_style('color') = (110, 110, 110)
        node.get_style('color') = (100, 100, 100)
        node.get_style('color') = (90, 90, 90)
        node.get_style('color') = (80, 80, 80)
        node.get_style('color') = (90, 90, 90)
        node.get_style('color') = (100, 100, 100)
        ...

        """
        def handler(prog: Tuple[int, int]) -> Tuple[int, int]:
            add, mult = prog
            if mult < 0:
                add -= step
            else:
                add += step
            for attr in color_attrs:
                color = attrs[attr]
                nr = max(min(color[0] + add, 255), 0)
                ng = max(min(color[1] + add, 255), 0)
                nb = max(min(color[2] + add, 255), 0)
                node.set_style(attr, (nr, ng, nb), cname=self.tmp_class)
            if add < - amplitude or add > amplitude:
                mult = mult * (- 1)
            node._update_manager()
            return add, mult

        amplitude = kwargs.pop('amplitude', 20)
        step = kwargs.pop('step', 10)
        color_attrs = kwargs.pop(
            'color_attrs', ['border-color', 'background-color']
        )
        attrs = {attr: node.get_style(attr) for attr in color_attrs}
        kwargs.setdefault('period', 5)
        NodeAnimation.__init__(
            self,
            node,
            (0, 1),
            handler,
            **kwargs
        )
