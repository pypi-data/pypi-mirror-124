#!/usr/bin/env python3

"""Definition of class Window."""

from __future__ import annotations
from typing import Any, Optional, Tuple, Iterator, List, TYPE_CHECKING
import logging
import pygame as pg

from . import types, Box, Pos, Label, Image, Media, Node, Keys, HorizontalRule
from .event_manager import _EventManager
if TYPE_CHECKING:
    from . import WindowSystem


class Window(_EventManager, Box):  # pylint: disable=R0902,R0904
    """Defines Window objects."""

    AVAILABLE_STYLES = {
        'window-cross-image'
    }

    def __init__(
            self,
            win_sys: WindowSystem,
            node: Node,
            **kwargs: Any
    ):
        """Initialize a Window in win_sys WindowSystem with node as content.

        If not None, kwarg title is the window title node.

        Kwarg modal specifies if the window is modal (i.e. no other
        window can be accessed as long as this window is opened).
        only modal windows are supported for now.

        """
        self.__win_sys: 'WindowSystem' = win_sys
        self.__modal: bool = kwargs.get('modal', True)
        self.__absolute_pos: types.pos_t = 0, 0
        self.__popup: Optional[Tuple[Node, Node]] = None
        self.__title_node: Optional[Node] = None
        self.__focus: Optional[Node] = None
        self.__closed: bool = False
        title = kwargs.get('title')

        _EventManager.__init__(self)
        Box.__init__(self, **kwargs)
        if title is not None:
            sliding = False
            sliding_init_pos = 0, 0

            def start_sliding(pgevt: pg.event.Event) -> bool:
                nonlocal sliding_init_pos, sliding
                sliding_init_pos = Pos.diff(pgevt.pos, self.get_absolute_pos())
                sliding = True
                return True

            def stop_sliding(_: pg.event.Event) -> bool:
                nonlocal sliding
                sliding = False
                return True

            def move(pgevt: pg.event.Event) -> bool:
                if sliding:
                    new_pos = Pos.diff(pgevt.pos, sliding_init_pos)
                    self.set_absolute_pos(new_pos)
                    return True
                return False
            self.add_processor('on-over', move)
            self.add_processor('on-over-again', move)
            self.__title_node = Label.node_of(title, stc='window_title')
            self.__title_node.add_processor('on-click-down', start_sliding)
            self.__title_node.add_processor('on-click-up', stop_sliding)
            cross = self.__cross_image()
            if cross is None:
                title_box = self.__title_node
            else:
                cross.set_style('valign', 'center')
                cross.can_grab_focus = lambda: False  # type: ignore
                title_box = Box(
                    self.__title_node, cross,
                    style={'orientation': 'horizontal'}
                )
            title_box.set_style('halign', 'center')
            self.pack(title_box)
            self.pack(HorizontalRule())
        self.pack(node)
        for child in self.iter_nodes():
            child._set_manager(self)
        self._set_container_size(self.__win_sys.screen.get_size())
        self._recompute_sizes_and_positions()

    def __cross_image(self) -> Optional[Image]:
        def click_cross() -> bool:
            self.close()
            return True
        cross = Media.get_image(self.get_style('window-cross-image'))
        if cross is None:
            result = None
        else:
            result = Image(cross, link=click_cross)
        return result

    @property
    def focus(self) -> Optional[Node]:
        """Get the node that currently has the focus in self."""
        return self.__focus

    @property
    def window_system(self) -> WindowSystem:
        """Get the window system of self."""
        return self.__win_sys

    @property
    def modal(self) -> bool:
        """Check if self is modal."""
        return self.__modal

    @property
    def content(self) -> Node:
        return self

    @property
    def title_node(self) -> Optional[Node]:
        """Get the title Node of self."""
        return self.__title_node

    @property
    def absolute_pos(self) -> types.pos_t:
        """Get the position of the self in its window system."""
        return self.__absolute_pos

    def get_window(self) -> Window:
        return self

    def get_window_pos(self) -> types.pos_t:
        return (0, 0)

    def available_size(self) -> types.opt_pos_opt_t:
        return self.get_inner_size()

    def get_absolute_pos(self) -> types.pos_t:
        return self.absolute_pos

    def set_absolute_pos(self, pos: types.pos_t) -> None:
        """Set the position of self in its window system."""
        self.__absolute_pos = pos

    def blit(self, surface: pg.surface.Surface) -> None:
        """Blit the window surface on surface at self.get_absolute_pos()."""
        self._draw_content()
        surface.blit(self.surface_, self.get_absolute_pos())

    def open(self, pos: Optional[types.pos_t] = None) -> None:
        """Open self.

        The on-open event is triggered on all nodes of the window.

        """
        for node in self.iter_tree(traverse=True):
            node._open()
        self.__win_sys.open_window(self, pos=pos)

    def close(self) -> None:
        """Close self.

        The on-close event is triggered on all nodes of the window.

        """
        def close_for_real() -> None:
            self.__win_sys.close_window(self)
        if self.__closed:
            return
        self.__closed = True
        for node in self.iter_tree(traverse=True):
            node._close()
        if self.animation is not None:
            self.animation.set_callback(close_for_real)
        else:
            close_for_real()

    def move(self, move: types.pos_t) -> None:
        """Move self according to the move xy couple."""
        self.set_absolute_pos(Pos.sum(self.get_absolute_pos(), move))

    def _recompute_sizes_and_positions(self) -> None:
        super()._recompute_sizes_and_positions()

        if self.__popup is None:
            return

        node, popped = self.__popup
        size = popped._compute_size()
        rect = Pos.rect(node.get_window_pos(), node.size_)

        #  find valid position for the popped node: check all
        #  candidate positions (style pos-list) and take the first one
        #  for which the top-left and bottom-right corners of the
        #  popped node are in the window and not over node
        pos = popped.get_style('pos')
        lpos: Optional[List[types.floating_pos_t]]
        if pos is not None:
            lpos = [pos]
        else:
            lpos = popped.get_style('pos-list')
        if lpos is None:
            lpos = [
                ('relative', ('right', 'bottom'), (0, 0)),
                ('relative', ('right', 'top'), (0, 0)),
                ('absolute', ('left', 'top'), (0, 0))
            ]
        for p in lpos:
            pos = Pos.floating_to_pos(p, size, rect=rect, cont_size=self.size_)
            popped_rect = pg.rect.Rect(pos, size)
            if (
                    Pos.ge(pos, (0, 0))
                    and Pos.ge(self.size_, Pos.sum(pos, size))
                    and not pg.rect.Rect(rect).colliderect(popped_rect)
            ):
                popped.position(pos)
                return

        #  the first position of the list is the fallback solution
        popped.position(
            Pos.floating_to_pos(lpos[0], size, rect=rect, cont_size=self.size_)
        )

    def iter_nodes(self, rec: bool = True) -> Iterator[Node]:
        yield from super().iter_nodes(rec=rec)
        if self.__popup is not None:
            if not rec:
                yield self.__popup[1]
            else:
                yield from self.__popup[1].iter_tree(rec=True)

    def _set_popup(
            self,
            node: Node,
            popped: Node
    ) -> None:
        self._add_child(popped)
        self.__popup = node, popped

    def _clear_popup(self) -> None:
        if self.__popup is not None:
            #  self._del_child would call Box._del_child which would
            #  cause an error since the popup is not in self.children
            Node._del_child(self, self.__popup[1])
        self.__popup = None

    def remove_focus(self) -> None:
        """Remove the focus from the node that currently has it.

        The method has no effect if no node has the focus.

        """
        focus = self.__focus
        self.__focus = None
        if focus is not None:
            focus.lose_focus()

    def give_focus(self, node: Node) -> None:
        """Give the focus to Node node.

        self.remove_focus() is called to remove the focus that
        currently has it.  The method has no effect if node already
        has the focus.

        """
        if node == self.__focus or not node.can_grab_focus():
            return
        self.remove_focus()
        self.__focus = node
        if node is not None:
            node.get_focus()
            node._update_manager()
            manager = node.manager
            while manager is not None and not manager.is_root():
                manager.make_visible(node)
                node = manager.content
                manager = manager.manager

    def activate_focus(self) -> bool:
        """Active the node that currently has the focus.

        The method has no effect if no node has the focus.

        """
        if self.__focus is None:
            return False
        result = self.__focus.activate()
        self._set_updated(result)
        return result

    def move_focus_sequential(self, forward: bool) -> bool:
        """Traverse self's content to give the focus to the next node.

        The search starts from the node that currently has the focus.
        From this node, the focus is given to the first node for which
        node.can_grab_focus_now() == True.  If forward = False, the
        search is performed backward.

        """
        old_focus = self.__focus
        prev: Optional[Node] = None
        for node in self.content.iter_tree(traverse=True):
            if node.can_grab_focus_now():
                if forward and prev == old_focus:
                    self.give_focus(node)
                    return node != old_focus
                if not forward and node == old_focus and prev is not None:
                    self.give_focus(prev)
                    return prev != old_focus
                prev = node
        if forward:
            for node in self.content.iter_tree(traverse=True):
                if node.can_grab_focus_now():
                    self.give_focus(node)
                    return node != old_focus
        else:
            if prev is not None:
                self.give_focus(prev)
                return prev != old_focus
        return False

    def move_focus_direction(self, direction: types.pos_t) -> bool:
        """Move the focus according to the given direction.

        The search starts from the node that currently has the focus.
        From this node, the focus is given to the next node on the
        direction for which node.can_grab_focus_now() == True.
        Parameter direction must be either (0, -1) for north, or
        either (0, 1) for south and so on.

        """
        #  no node has the focus.  whathever the direction, give the
        #  focus to the first one
        if self.__focus is None:
            return self.move_focus_sequential(True)

        manager = self.__focus.manager_
        from_node = self.__focus
        while True:
            from_center = Pos.center(from_node.get_rect())

            #  find all nodes reachable from from_node that are in the
            #  right direction and that contain a focusable node and put
            #  these in candidates list
            candidates = []
            for node in manager.content.iter_tree():
                if node._has_focusable_content():
                    node_center = Pos.center(node.get_rect())
                    diff = Pos.diff(from_center, node_center)
                    move = diff[0] * direction[0], diff[1] * direction[1]
                    if Pos.gt((0, 0), move):
                        candidates.append(node)

            #  if any candidate found, sort the list according to the
            #  distance
            if candidates != []:
                candidates.sort(
                    key=lambda node: Pos.distance(node.pos_, from_node.pos_)
                )
                for new_focus in candidates:
                    if new_focus.can_grab_focus_now():
                        self.give_focus(new_focus)
                        return True
                    node = new_focus._receive_focus_from_direction(direction)
                    if node is not None:
                        self.give_focus(node)
                        return True

                #  at least one candidate must have been chosen for
                #  the focus
                assert False, 'unreachable code'

            if manager.is_root():
                return False
            from_node = manager
            manager = manager.manager_
        assert False, 'unreachable code'

    def __bind_key(self, pgevt: pg.event.Event) -> bool:
        bind = Keys.action(pgevt.key, pg.key.get_pressed())
        if bind is None:
            return False

        def activate_focus() -> bool:
            return self.activate_focus()

        def close_window() -> bool:
            win = self.window_system.top_window()
            if win is not None:
                win.close()
            return True

        def move_focus_forward() -> bool:
            return self.move_focus_sequential(True)

        def move_focus_backward() -> bool:
            return self.move_focus_sequential(False)

        def move_focus_direction(direction: Tuple[int, int]) -> types.link_t:
            def fun() -> bool:
                return self.move_focus_direction(direction)
            return fun

        def user_defined(fun: Optional[types.user_key_proc_t]) -> types.link_t:
            def do() -> bool:
                if fun is not None:
                    fun()
                return True
            return do
        act, ufun = bind
        try:
            fun = {
                'activate': activate_focus,
                'close-window': close_window,
                'move-focus-forward': move_focus_forward,
                'move-focus-backward': move_focus_backward,
                'move-focus-north': move_focus_direction((0, -1)),
                'move-focus-east': move_focus_direction((1, 0)),
                'move-focus-south': move_focus_direction((0, 1)),
                'move-focus-west': move_focus_direction((-1, 0)),
                'user-defined': user_defined(ufun)
            }[act]
        except KeyError:
            logging.error('undefined action: "%s"', act)
            return False
        return fun()

    def process_pg_event(self, pgevt: pg.event.Event) -> bool:
        if pgevt.type == pg.MOUSEMOTION and pgevt.pos == pg.mouse.get_pos():
            return False
        result = False
        if pgevt.type == pg.KEYDOWN:
            result = self.__bind_key(pgevt)
        return super().process_pg_event(pgevt) or result

    def _unref_node(self, node: Node) -> None:
        super()._unref_node(node)

        #  the unreferenced node has the focus => clear the focus node
        #  of the window
        if node == self.__focus:
            node.lose_focus()

        #  same if the unreferenced node had an associated popup
        if self.__popup is not None and node == self.__popup[0]:
            self._clear_popup()
