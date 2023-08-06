#!/usr/bin/env python3

"""Definition of class ValuedNode."""

from typing import Any

from . import Node


class ValuedNode(Node):
    """A ValuedNode is any node that is associated a value.

    Examples are Checkbox, or InputText nodes.

    """

    def __init__(self, **kwargs: Any):
        """Initialise a ValuedNode initialised with kwarg value."""
        Node.__init__(self, **kwargs)
        self.__value = kwargs.get('value')

    @property
    def value(self) -> Any:
        """Get the current value of the node."""
        return self.__value

    def has_value(self) -> bool:
        return True

    def set_value(self, value: Any, trigger: bool = True) -> None:
        """Update the value of the node.

        If trigger is True, the on-change event of the node is
        triggered.

        """
        self.__value = value
        if trigger:
            self.trigger_on_change()
        self._update_manager()

    def trigger_on_change(self) -> None:
        """Trigger the on-change event of the node."""
        if self.manager is not None:
            self.manager._trigger('on-change', None, self)

            #  we must clear the style cache of the node since the
            #  node may have value dependant styles
            self._clear_style_cache()
