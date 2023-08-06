#!/usr/bin/env python3

"""Definition of class ItemSelect."""

from typing import Any, Dict, List

from . import Select


class ItemSelect(Select):
    """An ItemSelect is a Select with values in a set of dictionary keys."""

    def __init__(
            self,
            items: Dict[Any, str],
            **kwargs: Any):
        """Initialise an ItemSelect node containing items.

        Items must be a dictionary mapping ItemSelect values (which
        can be of any type) to str-able values.  If not None, kwarg
        value (the initial value of the select) must be in items.

        For instance, this creates an ItemSelect nodes with 3 values.
        Initially, s.value == (0, 10):

        s = ItemSelect({
          (0, 10): "child",
          (10, 20): "teenager",
          (21, 120): "grown up"
        })

        """
        self.__items = list(items)

        def get_node(item: Any) -> str:
            return items[item]

        def get_prev(item: Any) -> Any:
            return self.__items[self.__items.index(item) - 1]

        def get_next(item: Any) -> Any:
            return self.__items[self.__items.index(item) + 1]

        Select.__init__(
            self,
            self.__items[0],
            self.__items[-1],
            get_prev,
            get_next,
            get_node=get_node,
            **kwargs
        )

    @property
    def items(self) -> List[Any]:
        """Get the items of the select."""
        return self.__items
