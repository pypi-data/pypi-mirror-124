#!/usr/bin/env python3

"""Definition of class Select."""

from __future__ import annotations
from typing import Callable, Any, Dict, Iterator, Optional, cast

from . import Box, Label, Util, ValuedNode, Node, Empty, types


class Select(Box, ValuedNode):  # pylint: disable=R0902
    """Select nodes are comparable to HTML <select> elements.

    Select nodes contain a fixed list of items the user can navigate
    through.  a select consists of a node and two links allowing to
    navigate backward or forward in the list.  unlike select elements,
    it is only possible to navigate sequentially through the list.

    Note that the IntSelect and ItemSelect classes inheriting from Select
    should be prefered for most cases.

    """

    AVAILABLE_STYLES = {
        'select-cyclic',
        'select-hide-links',
        'select-next-class',
        'select-next-label',
        'select-prev-class',
        'select-prev-label',
        'select-wheel-units'
    }

    NEXT: int = 1
    PREV: int = -1

    def __init__(
            self,
            first: Any,
            last: Any,
            get_prev: Callable[[Any], Any],
            get_next: Callable[[Any], Any],
            **kwargs: Any
    ) -> None:
        """Initialize a Select node ranging from first to last.

        get_prev and get_next are mapping from a select value to its
        predecessor or successor.

        kwarg value is the initial value of the select.  default is
        first.

        kwarg get_node is a function from select values to anything
        that can str-ed.

        if not None, kwarg prev_node (resp. next_node) is the node
        that will be the navigation link to move to the previous
        (resp. next) value of the select.

        for instance:
        Select(0, 100, lambda n: n - 1, lambda n: n + 1, value=50)
        creates a list with values ranging from 0 to 100 and
        initialised to 50.  (note that for int Select, IntSelect
        should be used instead)

        """
        def create_navigation_links() -> Iterator[Node]:
            def get_link(name: str) -> Node:
                c = self.get_style(
                    cast(types.style_attr_t, f'select-{name}-class')
                )
                lbl = self.get_style(
                    cast(types.style_attr_t, f'select-{name}-label')
                )
                if lbl != '' and lbl is not None:
                    return Label(lbl, stc=c)
                return Empty(stc=c)
            for name in ['prev', 'next']:
                node: Optional[Node] = kwargs.get(name + '_node')
                if node is None:
                    node = get_link(name)
                yield node
        value = kwargs.get('value', first)
        kwargs['value'] = value
        Box.__init__(self, **kwargs)
        ValuedNode.__init__(self, **kwargs)
        self.__first: Any = first
        self.__last: Any = last
        self.__get_prev: Callable[[Any], Any] = get_prev
        self.__get_next: Callable[[Any], Any] = get_next
        self.__get_node: Callable[[Any], Any] = kwargs.get('get_node', str)
        self.__lbl: Label = Label(str(self.__get_node(value)))
        lbl_box = Box(self.__lbl)
        nav_nodes = tuple(create_navigation_links())
        nav_nodes[0].set_link(lambda: self.__move(Select.PREV))
        nav_nodes[1].set_link(lambda: self.__move(Select.NEXT))
        self.__links: Dict[int, Node] = {
            Select.PREV: nav_nodes[0],
            Select.NEXT: nav_nodes[1]
        }
        self.pack(self.__links[Select.PREV])
        self.pack(lbl_box)
        self.pack(self.__links[Select.NEXT])
        self.set_value(value, trigger=False)
        self.add_processor('on-mouse-wheel', self.__mouse_wheel_event)

    def set_value(self, value: Any, trigger: bool = True) -> None:
        """Set value of the select to value.

        If trigger is True, the ON_CHANGE event of the select is
        triggered.

        """
        ValuedNode.set_value(self, value, trigger=trigger)
        self.__lbl.set_text(str(self.__get_node(value)))
        if not self.__is_cyclic():
            if value != self.__first:
                self.enable_move(Select.PREV)
            if value != self.__last:
                self.enable_move(Select.NEXT)
            if value == self.__first:
                self.disable_move(Select.PREV)
            if value == self.__last:
                self.disable_move(Select.NEXT)

    def disable_move(self, move: int) -> None:
        """Disable a navigation link of the select.

        Raise ValueError if move does not belong to {Select.NEXT,
        Select.PREV}.  If the disabled link had the focus, give focus
        to the other navigation link (if it's enabled).

        """
        if move not in [Select.NEXT, Select.PREV]:
            raise ValueError(f'move must be in {[Select.NEXT, Select.PREV]}')
        has_focus = self.__links[move].has_focus()
        if self.__hide_links():
            self.__links[move].set_hidden(True)
        self.__links[move].disable()
        if has_focus and self.__links[-move].can_grab_focus_now():
            self.__links[-move].get_focus()

    def enable_move(self, move: int) -> None:
        """Enable a navigation link of the select.

        Raise ValueError if move does not belong to {Select.NEXT,
        Select.PREV}.

        """
        if move not in [Select.NEXT, Select.PREV]:
            raise ValueError(f'move must be in {[Select.NEXT, Select.PREV]}')
        if self.__hide_links():
            self.__links[move].set_hidden(False)
        self.__links[move].enable()

    def reset(self, first: Any, last: Any, value: Any) -> None:
        """Set the first, last and current value of the select."""
        self.__first = first
        self.__last = last
        self.set_value(value)

    def __is_cyclic(self) -> bool:
        return bool(self.get_style('select-cyclic'))

    def __hide_links(self) -> bool:
        return bool(self.get_style('select-hide-links'))

    def __move(self, move: int) -> bool:
        if self.__links[move].is_disabled():
            return False
        if move == Select.PREV:
            if self.value == self.__first:
                new = self.__last if self.__is_cyclic() else None
            else:
                new = self.__get_prev(self.value)
        else:
            if self.value == self.__last:
                new = self.__first if self.__is_cyclic() else None
            else:
                new = self.__get_next(self.value)
        if new is not None:
            self.set_value(new)
        return new is not None

    def __mouse_wheel_event(self, pgevt: Any) -> bool:
        if pgevt.button == Util.MOUSEBUTTON_WHEEL_DOWN:
            move = Select.NEXT
        elif pgevt.button == Util.MOUSEBUTTON_WHEEL_UP:
            move = Select.PREV
        if move is not None:
            for _ in range(self.get_style('select-wheel-units')):
                self.__move(move)
        return True
