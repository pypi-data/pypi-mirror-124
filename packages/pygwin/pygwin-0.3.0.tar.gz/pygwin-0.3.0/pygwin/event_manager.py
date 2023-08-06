#!/usr/bin/env python3

"""Definition of class EventManager."""

from __future__ import annotations
from typing import Tuple, Any, Iterator, Optional, Set, Dict, List
import pygame as pg

from . import types, Util, Pos, Node


class _EventManager(Node):  # pylint: disable=R0904,R0902
    """An _EventManager is some node that can catch and process elements.

    Frame and Window nodes are examples of _EventManager nodes.

    Each _EventManager is associated with a surface on which it is
    drawn.

    _EventManager objects are hierarchically organised.  Each can have
    children and a parent.  An _EventManager that does not have a
    parent is called a root _EventManager.  It usually is a Window
    node.

    """

    def __init__(self, **kwargs: Any) -> None:
        """Initialise self."""
        Node.__init__(self, **kwargs)
        self.__updated: bool = True
        self.__surface: Optional[pg.surface.Surface] = None
        self.__children: List[_EventManager] = list()
        self.__overed: Set[Node] = set()
        self.__clicked: Set[Node] = set()
        self.__floating: Set[Node] = set()
        self.__registered: Dict[
            types.event_t, List[Tuple[Node, types.event_proc_t]]
        ] = {
            evt: list() for evt in types.all_events
        }

    @property
    def surface(self) -> Optional[pg.surface.Surface]:
        """Get the surface of self."""
        return self.__surface

    @property
    def surface_(self) -> pg.surface.Surface:
        """Get the surface of self (+ check it is not None)."""
        assert self.__surface is not None
        return self.__surface

    def make_visible(self, node: Node) -> None:  # pylint: disable=R0201
        """Update self's scrolling so that node becomes fully visible."""

    def _get_scroll(self) -> types.pos_t:  # pylint: disable=R0201
        return 0, 0

    def set_surface(self, surface: pg.surface.Surface) -> None:
        """Set the surface of self."""
        self.__surface = surface

    def _add_child_manager(self, child: _EventManager) -> None:
        if child not in self.__children and child != self:
            self.__children.append(child)

    def _del_child_manager(self, child: _EventManager) -> None:
        self.__children.remove(child)

    def _set_manager(self, manager: Optional[_EventManager]) -> None:
        if manager is not None:
            manager._add_child_manager(self)
        super()._set_manager(manager)

    def is_root(self) -> bool:
        """Check if self is a root _EventManager (with no parent manager)."""
        return self.manager is None or self.manager == self

    def _update_manager(self) -> None:
        if not self.is_root():
            self.manager_._update_manager()
        super()._update_manager()

    def _reset_manager(self) -> None:
        if not self.is_root():
            self.manager_._del_child_manager(self)
        super()._reset_manager()

    def _set_updated(self, updated: bool) -> None:
        self.__updated = updated

    def _recompute_sizes_and_positions(self) -> None:
        #  position main node
        self.content._compute_size()
        self.content.position((0, 0))

        #  and floating nodes
        size = self.content.size_
        for node in self.__floating:
            nsize = node._compute_size()
            pos_style = node.get_style('pos')
            if pos_style is None:
                pos = 0, 0
            else:
                pos = Pos.floating_to_pos(pos_style, nsize, size)
            node.position(pos)

        for child_manager in self.__children:
            child_manager._recompute_sizes_and_positions()

    def _draw_content(self) -> None:
        if self.__updated:

            self._recompute_sizes_and_positions()

            #  reinitialise the surface if needed
            size = self.content.size_
            if self.surface is None or self.surface.get_size() != size:
                self.set_surface(pg.Surface(size).convert_alpha())

            self.surface_.fill((0, 0, 0, 0))
            self._set_updated(False)

            #  draw all children nodes
            for node in self.iter_nodes(rec=False):
                # if node != self:
                #     node._set_manager(self)
                node.draw(self.surface_)

    def add_floating_node(self, node: Node) -> None:
        """Add a floating node to self.

        Node is positionned with style pos.  If style pos is not
        defined, node is positionned at (0, 0) in self.

        """
        node._set_manager(self)
        self.__floating.add(node)
        for child in node.iter_tree():
            child.set_depth(0)
        self._set_updated(True)

    def del_floating_node(self, node: Node) -> None:
        """Remove floating node node from self."""
        if node in self.__floating:
            node._unref()
            self.__floating.remove(node)
        self._set_updated(True)

    def _register(
            self,
            evt: types.event_t,
            proc: Node,
            fun: types.event_proc_t
    ) -> None:
        self.__registered[evt].append((proc, fun))

    def _unregister(
            self,
            evt: types.event_t,
            proc: Node,
            fun: types.event_proc_t
    ) -> None:
        self.__registered[evt] = [
            pf
            for pf in self.__registered[evt]
            if pf != (proc, fun)
        ]

    def _unref_node(self, node: Node) -> None:
        win = self.get_window()
        if win != self:
            win._unref_node(node)
        for evt in self.__registered:
            self.__registered[evt] = [
                pf
                for pf in self.__registered[evt]
                if pf[0] != node
            ]

    def _trigger(
            self,
            evt: types.event_t,
            pgevt: Optional[pg.event.Event],
            proc: Node
    ) -> bool:
        return self.__event(evt, pgevt, check_pos=False, incl={proc})

    def __check_pos_over(self, pos: types.pos_t, node: Node) -> bool:
        return node.is_over(pos) and all(
            f.depth >= node.depth
            or not f.is_over(pos)
            for f in self.__floating
        )

    def __event(
            self,
            evt: types.event_t,
            pgevt: Optional[pg.event.Event],
            **kwargs: Any
    ) -> bool:
        result = False
        check_pos = kwargs.get('check_pos', True)
        incl = kwargs.get('incl', None)
        if pgevt is None:
            pgevt = pg.event.Event(0)

        for proc, fun in self.__registered[evt]:

            #  it may be the case that the manager of proc is not self
            #  anymore if a processor in self.__registered[evt]
            #  removed it (call to fun in this loop).  if so we skip
            #  it
            # if proc.manager != self:
            #    continue

            #  the event has a position and this one is not inside the
            #  node => skip it
            if (
                    check_pos
                    and pgevt is not None
                    and hasattr(pgevt, 'pos')
                    and not self.__check_pos_over(pgevt.pos, proc)
            ):
                continue

            #  the node is not in included => skip it
            if incl is not None and proc not in incl:
                continue

            #  the node is hidden => skip it
            if proc.is_hidden():
                continue

            if fun(pgevt):
                result = True

        return result

    def __pg_mouse_motion(self, pgevt: pg.event.Event) -> bool:
        result = False

        #  check which nodes are not overed anymore and which are
        #  newly overed.  set the overed flag of these and trigger the
        #  on-clicked and on-unclicked events if needed
        not_overed_anymore = {
            n for n in self.__overed
            if not self.__check_pos_over(pgevt.pos, n)
        }
        newly_overed = {
            n for n in self.iter_nodes()
            if self.__check_pos_over(pgevt.pos, n)
            and n not in self.__overed
        }
        self.__overed = self.__overed - not_overed_anymore
        for n in not_overed_anymore:
            n._set_overed(False)
            if n.is_clicked():
                result = self._trigger('on-unclicked', pgevt, n) or result
        for n in newly_overed:
            n._set_overed(True)
            if n.is_clicked():
                result = self._trigger('on-clicked', pgevt, n) or result

        #  trigger events
        events: List[Tuple[types.event_t, Set[Node]]] = [
            ('on-unover', not_overed_anymore),
            ('on-over-again', self.__overed),
            ('on-over', newly_overed)
        ]
        for evt, node_set in events:
            result = self.__event(
                evt, pgevt, check_pos=False, incl=node_set
            ) or result

        self.__overed |= set(newly_overed)

        return result

    def __pg_mouse_button_up(self, pgevt: pg.event.Event) -> bool:
        if pgevt.button == Util.MOUSEBUTTON_LEFT:
            result = self.__event('on-click-up', pgevt)
            result = self.__event(
                'on-unclicked', pgevt, check_pos=False, incl=self.__clicked
            ) or result
            for n in self.__clicked:
                n._set_clicked(False)
            self.__clicked = set()
            return result
        if pgevt.button == Util.MOUSEBUTTON_RIGHT:
            return self.__event('on-click-up-right', pgevt)
        if pgevt.button in [
                Util.MOUSEBUTTON_WHEEL_DOWN,
                Util.MOUSEBUTTON_WHEEL_UP
        ]:
            return self.__event('on-mouse-wheel', pgevt)
        return False

    def __pg_mouse_button_down(self, pgevt: pg.event.Event) -> bool:
        evt: Optional[types.event_t] = None
        result = False
        if pgevt.button == Util.MOUSEBUTTON_LEFT:
            evt = 'on-click-down'
            self.__clicked = {
                n for n in self.iter_nodes()
                if self.__check_pos_over(pgevt.pos, n)
            }
            result = self.__event(
                'on-clicked', pgevt, check_pos=False, incl=self.__clicked
            ) or result
            for n in self.__clicked:
                n._set_clicked(True)
        elif pgevt.button == Util.MOUSEBUTTON_RIGHT:
            evt = 'on-click-down-right'
        else:
            return False

        result = self.__event(evt, pgevt) or result

        return result

    def _get_cursor_image(self) -> Optional[Any]:
        for node in self.iter_tree(traverse=True):
            result = node.get_style('cursor-image')
            if result is not None:
                return result
        return None

    def __pg_key_down(self, pgevt: pg.event.Event) -> bool:
        return self.__event('on-key', pgevt)

    def process_pg_event(self, pgevt: pg.event.Event) -> bool:
        """Process pygame event pgevt.

        Return True if the event has been processed by some node
        inside self, False otherwise.

        """
        try:
            proc: Optional[types.event_proc_t] = {
                pg.MOUSEBUTTONDOWN: self.__pg_mouse_button_down,
                pg.MOUSEBUTTONUP: self.__pg_mouse_button_up,
                pg.MOUSEMOTION: self.__pg_mouse_motion,
                pg.KEYDOWN: self.__pg_key_down
            }[pgevt.type]
        except KeyError:
            result = False
            proc = None

        if proc is not None:
            result = proc(pgevt)

        for child_manager in self.__children:
            if not hasattr(pgevt, 'pos') or child_manager.is_over(pgevt.pos):
                result = child_manager.process_pg_event(pgevt) or result

        if result:
            self._set_updated(True)

            #  since sizes and positions may have changed we recompute
            #  them
            if self.is_root():
                self._recompute_sizes_and_positions()

        return result

    def iter_nodes(self, rec: bool = True) -> Iterator[Node]:
        """Iterate on all the nodes of the manager."""
        if not rec:
            yield self.content
            yield from self.__floating
        else:
            yield from self.content.iter_tree()
            for floating in self.__floating:
                for node in floating.iter_tree():
                    yield node

    def _clear(self) -> bool:
        result = self.__event(
            'on-unover', None, check_pos=False, incl=self.__overed
        )
        for n in self.__clicked:
            result = n._set_clicked(False) or result
        for n in self.__overed:
            result = n._set_overed(False) or result
        self.__clicked = set()
        self.__overed = set()
        return result

    @property
    def content(  # pylint: disable=C0116,R0201
            self
    ) -> Node:
        assert False

    def available_size(  # pylint: disable=C0116,R0201
            self
    ) -> types.opt_pos_opt_t:
        assert False
