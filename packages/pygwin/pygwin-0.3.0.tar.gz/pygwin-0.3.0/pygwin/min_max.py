#!/usr/bin/env python3

"""Definition of class MinMax."""


class _MinMax:
    """A _MinMax is any object which is associated a min and a max value.

    Examples are Gauge and Range nodes.

    """

    def __init__(self, min_value: int, max_value: int) -> None:
        """Initialise a MinMax object with min_value and max_value."""
        self.__min_value: int = min_value
        self.__max_value: int = max_value

    @property
    def min_value(self) -> int:
        """Get the min value of the object."""
        return self.__min_value

    @property
    def max_value(self) -> int:
        """Get the max value of the object."""
        return self.__max_value
