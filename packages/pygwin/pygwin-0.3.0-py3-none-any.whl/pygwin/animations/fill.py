#!/usr/bin/env python3

"""Definition of class FillAnimation."""

from typing import Any, Optional, TYPE_CHECKING

from .node_animation import NodeAnimation
if TYPE_CHECKING:
    from .. import ValuedNode
    from ..min_max import _MinMax

    class _MinMaxNode(ValuedNode, _MinMax):
        pass


class FillAnimation(NodeAnimation):
    """A FillAnimation increases/decreases a Range or Gauge value."""

    def __init__(self, node: '_MinMaxNode', **kwargs: Any):
        """Initialise a FillAnimation for node.

        kwarg step (default = 1) specifies how the value of the node
        is increased.

        """
        def handler(_: bool) -> Optional[bool]:
            value = node.value + step
            value = min(node.max_value, max(node.min_value, value))
            result: Optional[bool] = True
            if not node.min_value < value < node.max_value:
                result = None
            node.set_value(value)
            return result
        step = kwargs.get('step', 1)
        NodeAnimation.__init__(self, node, True, handler, **kwargs)
