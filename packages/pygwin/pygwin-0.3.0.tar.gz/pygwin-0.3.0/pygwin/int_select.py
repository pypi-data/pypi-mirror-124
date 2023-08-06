#!/usr/bin/env python3

"""Definition of class IntSelect."""

from typing import Any

from . import Select


class IntSelect(Select):
    """IntSelect nodes are Select nodes containing integer values."""

    def __init__(
            self,
            min_value: int,
            max_value: int,
            **kwargs: Any
    ):
        """Initialise an IntSelect node.

        Values of the select values range from min_val to max_val.

        Kwarg value is the initial value of the IntSelect (default =
        min_val).

        """
        def get_prev(n: int) -> int:
            return n - 1

        def get_next(n: int) -> int:
            return n + 1
        Select.__init__(
            self, min_value, max_value, get_prev, get_next, **kwargs
        )
