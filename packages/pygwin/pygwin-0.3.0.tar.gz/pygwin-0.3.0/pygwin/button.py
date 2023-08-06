#!/usr/bin/env python3

"""Definition of class Button."""

from typing import Any

from . import Box, Label, Node


class Button(Box):  # pylint: disable=R0904,R0902
    """Button nodes are boxes with a single clickable Node inside it."""

    def __init__(self, node: Node, **kwargs: Any):
        """Initialise a Button node with the Node node packed in it."""
        Box.__init__(self, Label.node_of(node), **kwargs)

    @property
    def node(self) -> Node:
        """Get the node inside the button."""
        return self.children[0]
