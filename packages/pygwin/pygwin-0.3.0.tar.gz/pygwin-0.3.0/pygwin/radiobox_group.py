#!/usr/bin/env python3

"""Definition of class RadioboxGroup."""

from typing import Any, Optional, Dict

from . import Radiobox


class RadioboxGroup:
    """A RadioboxGroup groups Radiobox nodes that are mutually exclusive.

    If a Radiobox is selected among the group, then others become
    deselected.  RadioboxGroups are not visible on the screen, they
    are just logical groups of Radiobox nodes.

    """

    def __init__(self) -> None:
        """Initialise a group with an empty set of radioboxes."""
        self.__selected: Optional[Radiobox] = None
        self.__values: Dict[Radiobox, Any] = dict()

    @property
    def value(self) -> Any:
        """Get the value associated to the currently checked box of the group.

        Returns None if no box is currently checked.

        """
        if self.__selected is None:
            result = None
        else:
            result = self.__values[self.__selected]
        return result

    def add_radiobox(self, box: Radiobox, value: Any) -> None:
        """Add Radiobox box to the group and associate the given value."""
        self.__values[box] = value

    def select(self, box: Radiobox) -> None:
        """Radiobox box becomes the selected Radiobox of the group.

        Raises ValueError is raised if the box does not belong to the
        group.

        """
        if box not in self.__values:
            raise ValueError('box does not belong to the group values')
        if box != self.__selected:
            if self.__selected is not None:
                self.__selected.set_value(False)
            self.__selected = box
            self.__selected.set_value(True)
