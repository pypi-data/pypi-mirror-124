#!/usr/bin/env python3

"""Definition of class Radiobox."""

from typing import Any, TYPE_CHECKING

from . import Checkbox
if TYPE_CHECKING:
    from . import RadioboxGroup


class Radiobox(Checkbox):
    """Radiobox nodes are similar to HTML <input type="radio">."""

    def __init__(
            self,
            group: 'RadioboxGroup',
            group_value: Any,
            **kwargs: Any
    ):
        """Initialise a radiobox put in group and associated with group_value.

        kwarg group_value is the value that will be associated to this
        radiobox in the group.  This means that if the radiobox is
        checked, then group.value will return group_value.

        kwarg value is True if the radiobox is initially checked.

        >>> from pygwin import RadioboxGroup
        >>> grp_grade = RadioboxGroup()
        >>> box_a = Radiobox(grp_grade, 'A')
        >>> box_b = Radiobox(grp_grade, 'B', value=True)
        >>> box_c = Radiobox(grp_grade, 'C')
        >>> box_d = Radiobox(grp_grade, 'D')
        >>> box_e = Radiobox(grp_grade, 'E')
        >>> grp_grade.value
        'B'
        >>> box_b.value
        True
        >>> _ = box_e.set_value(True)
        >>> grp_grade.value
        'E'
        >>> box_b.value
        False

        """
        Checkbox.__init__(self, **kwargs)
        self.__group = group
        self.__group.add_radiobox(self, group_value)
        if self.value:
            self.__group.select(self)

    def set_value(self, value: Any, trigger: bool = True) -> None:
        super().set_value(value, trigger=trigger)
        if self.value:
            self.__group.select(self)

    def _activate(self) -> bool:
        self.get_focus()
        if not self.value:
            self.set_value(True)
        return True
