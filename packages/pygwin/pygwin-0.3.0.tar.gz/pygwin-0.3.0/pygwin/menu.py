#!/usr/bin/env python3

"""Definition of class Menu."""

from typing import Any, Dict, Optional
import pygame as pg

from . import Rule, HorizontalRule, VerticalRule, Util, Box, Empty, Node, types


class Menu(Box):
    """Menu nodes are collection of item nodes.

    Each item node is associated with one header node.  Only one item
    is visible at any time.  Activation of one of the headers shows
    its associated item and hides the others.

    """

    def __init__(self, items: Dict[Node, Node], **kwargs: Any):
        """Initialise a Menu node.

        Items is a dictionary mapping header nodes to children nodes.

        """
        def on_mouse_wheel(pgevt: pg.event.Event) -> bool:
            if pgevt.button is Util.MOUSEBUTTON_WHEEL_DOWN:
                self.__prev_tab()
            elif pgevt.button is Util.MOUSEBUTTON_WHEEL_UP:
                self.__next_tab()
            return True

        def switch_tab(i: int) -> types.link_t:
            def result(i: int) -> bool:
                self.switch_tab(i)
                return True
            return lambda: result(i)

        Box.__init__(self, **kwargs)
        self.__items: Dict[Node, Node] = dict()
        self.__curr: Optional[Node] = None

        for i, item in enumerate(items):
            item.set_link(switch_tab(i))
            self.__items[item] = items[item]
        rule: Rule
        if self.get_style('orientation') == 'vertical':
            rule = HorizontalRule()
            orientation = 'horizontal'
        else:
            rule = VerticalRule()
            orientation = 'vertical'
        style = {
            'orientation': orientation,
            'halign': 'center',
            'valign': 'center'
        }
        head_box = Box(style=style)
        for item in self.__items:
            head_box.pack(item)
        self.pack(head_box)
        self.pack(rule)
        self.pack(Empty())

        head_box.add_processor('on-mouse-wheel', on_mouse_wheel)
        self.switch_tab(0)

    @property
    def items(self) -> Dict[Node, Node]:
        """Get the items of the menu."""
        return self.__items

    def switch_tab(self, i: int) -> None:
        """Switch the visible item node to the ith one."""
        if self.__curr is not None:
            self.__curr.set_selected(False)
            if self.manager is not None:
                self.manager._trigger('on-unselect', None, self.__curr)
        self.__curr = self.__item_at_index(i)
        self.__curr.set_selected(True)
        node = self.__items[self.__curr]
        self.replace(2, node)
        if self.manager is not None:
            self.manager._trigger('on-select', None, self.__curr)
        self._update_manager()

    def __item_at_index(self, idx: int) -> Node:
        for i, item in enumerate(self.__items):
            if i == idx:
                return item
        raise IndexError('item not found')

    def __item_index(self, item: Node) -> int:
        for i, it in enumerate(self.__items):
            if it == item:
                return i
        raise IndexError('item not found')

    def __next_tab(self) -> None:
        if self.__curr is None:
            idx = 0
        else:
            idx = (self.__item_index(self.__curr) + 1) % len(self.__items)
        self.switch_tab(idx)

    def __prev_tab(self) -> None:
        if self.__curr is None:
            idx = 0
        else:
            idx = (self.__item_index(self.__curr) - 1) % len(self.__items)
        self.switch_tab(idx)
