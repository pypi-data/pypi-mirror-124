#!/usr/bin/env python3

"""Definition of class NodeType."""

from typing import Any

from . import StyleClass


class NodeType(type):
    """A NodeType class is any class that has the Node class as ancestor."""

    def __init__(cls, name: Any, bases: Any, dic: Any):
        """Initialise NodeType class cls.

        A new style class is created for cls of which the name is
        cls.__name__.

        """
        type.__init__(cls, name, bases, dic)
        StyleClass(cls.__name__)
