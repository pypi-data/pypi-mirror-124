#!/usr/bin/env python3
# pylint: disable=too-many-lines

"""Definition of class Node."""

from __future__ import annotations
from typing import Tuple, Optional, List, Iterator, TYPE_CHECKING
from typing import Union, Any, Dict, Type
import re
import inspect
import logging
import pygame as pg

from .animations import FadeAnimation, FadeInAnimation, FadeOutAnimation
from .animations import FillAnimation, GlowAnimation, GrowAnimation
from .animations import PopInAnimation, PopOutAnimation, ScrollAnimation
from .style import INHERITED, DEFAULT
from . import types, Media, Pos, Draw, Util, NodeType, StyleClass

if TYPE_CHECKING:
    from .event_manager import _EventManager
    from . import Animation, Window


class Node(metaclass=NodeType):  # pylint: disable=R0904,R0902
    """Node is the base class of all window elements (labels, boxes, ...)."""

    HIDDEN = 1
    FOCUS = 2
    SELECTED = 4
    DISABLED = 8
    OVERED = 16
    CLICKED = 32

    __PERCENT_EXPR = re.compile(r'\d+%')

    AVAILABLE_STYLES = {
        'animation',
        'animation-arguments',
        'background',
        'background-color',
        'background-image',
        'border',
        'border-color',
        'border-images',
        'border-width',
        'corner',
        'cursor-image',
        'expand',
        'font',
        'font-size',
        'halign',
        'opacity',
        'padding',
        'pos',
        'pos-list',
        'scale',
        'size',
        'sound',
        'valign'
    }

    def __init__(self, **kwargs: Any):
        """Initialise node self.

        kwarg style is the (dictionary) style of the node (default =
        None).

        kwarg stc is the list of style class names that this node has
        (default = []).

        kwarg link is a function (with type [] -> bool) that is called
        when the node is clicked or activated (with self.activate())
        (default = None).

        """
        self.__flags: int = 0
        self.__depth: int = 1
        self.__pos: types.opt_pos_t = None
        self.__size: types.opt_pos_opt_t = None
        self.__parent: Optional[Node] = None
        self.__container_size: types.opt_pos_t = None
        self.__events: Dict[types.event_t, List[types.event_proc_t]] = dict()
        self.__style_procs: Dict[types.event_t, List[types.event_proc_t]]
        self.__style_procs = dict()
        self.__link: Optional[types.link_t] = None
        self.__link_proc: Optional[types.event_proc_t] = None
        self.__manager: Optional['_EventManager'] = None
        self.__prev_flags: int = 0
        self.__style_cache: types.style_t = dict()
        self.__has_ctx_menu: bool = False
        self.__animation: Optional['Animation'] = None

        #  build node style classes
        style = kwargs.get('style')
        my_stc = StyleClass(self, register=False, style=style)
        stc = kwargs.get('stc', list())
        if stc is None:
            stc = list()
        elif not isinstance(stc, list):
            stc = [stc]
        self.__stc = list()
        for c in stc:
            if c in StyleClass:
                self.__stc.append(StyleClass[c])
            else:
                logging.warning('style class "%s" does not exist', c)
        self.__stc.insert(0, my_stc)
        self.set_link(kwargs.get('link'), update_style_procs=False)

        #  the node inherits from all the style classes of its parent
        #  classes
        for c in inspect.getmro(type(self))[:-1]:
            cname = c.__name__
            if cname in StyleClass:
                self.__stc.append(StyleClass[cname])

        self.__update_style_procs()

    @property
    def parent(self) -> Optional[Node]:
        """Get the parent node of self, None if no parent."""
        return self.__parent

    @property
    def manager(self) -> Optional[_EventManager]:
        """Get the event manager of self."""
        return self.__manager

    @property
    def manager_(self) -> _EventManager:
        """Get the event manager of self + check result is not None."""
        assert self.__manager is not None
        return self.__manager

    @property
    def container_size(self) -> types.opt_pos_t:
        """Get the container size of self."""
        return self.__container_size

    @property
    def container_size_(self) -> types.pos_t:
        """Get the container size of self + check result is not None."""
        return Pos.check(self.__container_size)

    @property
    def pos(self) -> types.opt_pos_t:
        """Get the position of self in its event manager."""
        return self.__pos

    @property
    def pos_(self) -> types.pos_t:
        """Get the position of self + check result is not None."""
        return Pos.check(self.__pos)

    @property
    def depth(self) -> int:
        """Get the depth of self."""
        return self.__depth

    @property
    def stc(self) -> List[StyleClass]:
        """Get all style classes that apply to the node."""
        return self.__stc

    @property
    def size(self) -> types.opt_pos_opt_t:
        """Get the total size of self (i.e., border + padding included)."""
        return self.__size

    @property
    def size_(self) -> types.pos_t:
        """Get the total size of self + check result is not None."""
        return Pos.check(self.__size)

    @property
    def value(self) -> Any:
        """Get the current value of self, None if it is not valued."""
        return None

    @property
    def animation(self) -> Optional['Animation']:
        """Get the animation currently running on the node."""
        return self.__animation

    def has_value(self) -> bool:  # pylint: disable=no-self-use
        """Check if the node is valued."""
        return False

    def get_window(self) -> Window:
        """Get the window to which the node belongs."""
        return self.manager_.get_window()

    def get_inner_size(self) -> types.opt_pos_opt_t:
        """Get the inner size of Node (size - (padding + border))."""
        if self.size is None:
            return None
        w, h = self.size
        wdiff, hdiff = self._get_inner_diff()
        result = (
            None if w is None else w - wdiff,
            None if h is None else h - hdiff
        )
        return result

    def get_inner_size_(self) -> types.pos_t:
        """Get the inner size of Node + check result is not None."""
        return Pos.check(self.get_inner_size())

    def get_inner_pos(self) -> types.opt_pos_t:
        """Get the inner position of self in its event manager.

        The inner position is obtained by adding the node padding and
        border to its position.

        """
        if self.pos is None:
            return None
        return Pos.sum(self.pos_, self._get_inner_shift())

    def get_inner_pos_(self) -> types.pos_t:
        """Get the inner position of self + check result is not None."""
        return Pos.check(self.get_inner_pos())

    def get_absolute_pos(self) -> types.pos_t:
        """Get the position of self in the window system."""
        result = Pos.sum(self.pos_, self.manager_.get_absolute_pos())
        result = Pos.diff(result, self.manager_._get_scroll())
        return result

    def get_window_pos(self) -> types.pos_t:
        """Get the position of self in its window."""
        result = self.manager_.get_window_pos()
        result = Pos.sum(result, self.pos_)
        result = Pos.diff(result, self.manager_._get_scroll())
        return result

    def get_bg_img(self) -> Optional[pg.surface.Surface]:
        """Get the background image of self set via its style."""
        if self.get_style('background') == 'image':
            return Media.get_image(self.get_style('background-image'))
        return None

    def get_width(self) -> Optional[int]:
        """Get the width of self."""
        if self.__size is None:
            return None
        return self.__size[0]

    def get_height(self) -> Optional[int]:
        """Get the height of self."""
        if self.__size is None:
            return None
        return self.__size[1]

    def get_rect(self) -> types.rect_t:
        """Get the rectangle occupied by the node in its manager."""
        return Pos.rect(self.pos_, self.size_)

    def get_absolute_rect(self) -> types.rect_t:
        """Get the rectangle occupied by the node in its window system."""
        return Pos.rect(self.get_absolute_pos(), self.size_)

    def set_parent(self, parent: Optional[Node]) -> None:
        """Set the parent Node of self."""
        self.__parent = parent

    def set_depth(self, depth: int) -> None:
        """Set the depth of self."""
        self.__depth = depth

    def _set_container_size(self, size: types.pos_t) -> None:
        if size != self.__container_size:
            self.__container_size = size
            if self.has_relative_size():
                for node in self.iter_tree():
                    node._reset_size()
                self._compute_size()

    def set_link(
            self,
            link: Optional[types.link_t],
            update_style_procs: bool = True
    ) -> None:
        """Update node so that when it is clicked, link() -> bool is called.

        If a previous link was associated to the node it is discarded.

        """
        self.__link = link
        if self.__link_proc is not None:
            self.del_processor('on-click-up', self.__link_proc)
        if link is not None:
            def event(_: pg.event.Event) -> bool:
                if self.is_clicked():
                    return self.activate()
                return False
            self.add_processor('on-click-up', event)
            self.__link_proc = event
            if 'link' in StyleClass:
                self.stc.append(StyleClass['link'])
                if update_style_procs:
                    self.__update_style_procs()

    def _reset_position(self) -> None:
        self.__pos = None

    def _reset_size(self) -> None:
        if self.parent is not None:
            self.parent._reset_size()
        else:
            #  the root node resets the position of its sub-tree
            for node in self.iter_tree():
                node._reset_position()
            self._update_manager()

        self.__size = None

    def _set_flag(self, val: bool, flag: int) -> None:
        if val:
            self.__flags |= flag
        else:
            self.__flags = self.__flags & ~flag

    def __set_flag_tree(self, val: bool, flag: int) -> None:
        for child in self.iter_tree():
            child._set_flag(val, flag)

    def set_hidden(self, hidden: bool) -> None:
        """Hide/show self."""
        self.__set_flag_tree(hidden, Node.HIDDEN)

    def set_selected(self, selected: bool) -> None:
        """Select/unselect self."""
        self.__set_flag_tree(selected, Node.SELECTED)

    def _set_focus(self, focus: bool) -> None:
        self.__set_flag_tree(focus, Node.FOCUS)

    def _set_disabled(self, disabled: bool) -> None:
        self.__set_flag_tree(disabled, Node.DISABLED)

    def _set_overed(self, overed: bool) -> bool:
        result = self.is_overed() != overed
        if result:
            self._set_flag(overed, Node.OVERED)
        return result

    def _set_clicked(self, clicked: bool) -> bool:
        result = self.is_clicked() != clicked
        if result:
            self._set_flag(clicked, Node.CLICKED)
        return result

    def is_hidden(self) -> bool:
        """Check if self is hidden."""
        return self.__flags & Node.HIDDEN == Node.HIDDEN

    def is_selected(self) -> bool:
        """Check if self is selected."""
        return self.__flags & Node.SELECTED == Node.SELECTED

    def has_focus(self) -> bool:
        """Check if self has the focus."""
        return self.__flags & Node.FOCUS == Node.FOCUS

    def is_disabled(self) -> bool:
        """Check if self is disabled."""
        return self.__flags & Node.DISABLED == Node.DISABLED

    def is_clicked(self) -> bool:
        """Check if self is clicked."""
        return self.__flags & Node.CLICKED == Node.CLICKED

    def is_overed(self) -> bool:
        """Check if the cursor is over self."""
        return self.__flags & Node.OVERED == Node.OVERED

    def _unref(self) -> None:
        for node in self.iter_tree():
            node._reset_manager()

    def _add_child(self, node: Node) -> None:
        if node.parent == self:
            return
        if node.parent is not None:
            node.parent._del_child(node)
        node.set_parent(self)
        if self.manager is not None:
            self.manager._set_updated(True)
        for child in node.iter_tree():
            child._set_manager(self.manager)

    def _del_child(self, node: Node) -> None:
        if node.parent == self:
            node.set_parent(None)
            if self.manager is not None:
                self.manager._set_updated(True)
            node._unref()

    def set_animation(self, animation: Optional['Animation']) -> None:
        """Set and start an animation running on self.

        If an animation was already running on self it is stopped.

        """
        old_animation = self.__animation
        self.__animation = animation
        if old_animation is not None:
            old_animation.stop()
        if animation is not None:
            animation.start()

    def stop_animation(self) -> None:
        """Stop the animation set on self with set_animation."""
        self.set_animation(None)

    def set_tooltip(
            self,
            tooltip: Node
    ) -> None:
        """Set the tooltip of self.

        A tooltip is a Node that will pop if the cursor is over self
        or if self has the focus.  The tooltip disappears when the
        opposite event occurs.

        The pos style of the tooltip may be set to indicate where it
        will appear.  Alternatively, if the pos-list style of tooltip
        is set, it must be a list of candidate positions: tooltip will
        appear at the first position of the list so that that makes it
        fully visible in the window.

        """
        def pop(_: pg.event.Event) -> bool:
            self.get_window()._set_popup(self, tooltip)
            return True

        def clear(_: pg.event.Event) -> bool:
            self.get_window()._clear_popup()
            return True
        self.add_processor('on-over', pop)
        self.add_processor('on-focus', pop)
        self.add_processor('on-unover', clear)
        self.add_processor('on-unfocus', clear)

    def set_ctx_menu(
            self,
            menu: Node,
            button: int = Util.MOUSEBUTTON_RIGHT
    ) -> None:
        """Set the contextual menu of the node.

        A contextual menu is a node that appears when self has the
        focus or when the cursor is over self and button is clicked.

        Pygwin does not manage the closing of the contextual menu.

        See help(Node.set_tooltip) to have a description on how to
        place the contextual menu.

        """
        def pop(_: pg.event.Event) -> bool:
            self.get_window()._set_popup(self, menu)
            return True
        if button == Util.MOUSEBUTTON_LEFT:
            self.add_processor('on-click-up', pop)
        elif button == Util.MOUSEBUTTON_RIGHT:
            self.add_processor('on-click-up-right', pop)
        self.add_processor('on-focus', pop)
        self.__has_ctx_menu = True

    def clear_tooltip(self) -> None:
        """Make the tooltip of self disappear."""
        self.get_window()._clear_popup()

    def clear_ctx_menu(self) -> None:
        """Make the contextual menu of self disappear."""
        self.get_window()._clear_popup()

    def _open(self) -> None:
        if self.manager is not None:
            self.manager_._trigger('on-open', None, self)

    def _close(self) -> None:
        if self.manager is not None:
            self.manager_._trigger('on-close', None, self)

    def _reset_manager(self) -> None:
        if self.__manager is not None:
            self.__manager._unref_node(self)
        self.__manager = None

    def _set_manager(self, manager: Optional[_EventManager]) -> None:
        if self.__manager == manager:
            return
        if self.__manager is not None:
            self.__manager._unref_node(self)
        self.__manager = manager
        if manager is not None:
            for evt, funs in self.__events.items():
                for fun in funs:
                    self.manager_._register(evt, self, fun)

    def _update_manager(self) -> None:
        if self.manager is not None:
            self.manager._set_updated(True)

    def _compute_size(self) -> types.pos_t:
        def norm_dim(val: Union[None, int, str], dim: int) -> Optional[int]:
            if val is None or isinstance(val, int):
                return val

            #  check available size.  return None if unknown
            avail_size: types.opt_pos_opt_t
            avail_size = self.container_size
            if avail_size is None and self.parent is None:
                manager = self.manager
                if manager is not None:
                    avail_size = manager.available_size()
            if avail_size is None:
                return None
            avail = avail_size[dim]
            if avail is None:
                return None

            #  size is expressed as a percentage of avail_size
            m = Node.__PERCENT_EXPR.fullmatch(val)
            if not m:
                raise ValueError(f'could not parse size {val}')
            percent = int(val[:len(val) - 1])
            result = int(avail * percent / 100)
            return result

        def norm_style_size() -> types.opt_pos_opt_t:
            img = self.get_bg_img()
            size: types.opt_pos_opt_t
            if img is not None:
                size = img.get_size()
            else:
                size = self.get_style('size')
            if size is None:
                return None
            return norm_dim(size[0], 0), norm_dim(size[1], 1)

        #  size does not need to be recomputed
        if self.__size is not None:
            return Pos.check(self.__size)

        size = norm_style_size()
        self.__size = size
        inner_size = self._compute_inner_size()
        self.__size = Pos.combine(
            size, Pos.sum(inner_size, self._get_inner_diff())
        )
        self.__size = Pos.check(self.__size)
        return self.__size

    def position(self, pos: types.pos_t) -> None:
        """Position self at pos."""
        #  change the node position according to its alignment
        new_pos = Pos.align(
            pos,
            self.size_,
            self.container_size,
            self.get_style('halign'),
            self.get_style('valign')
        )

        #  check if position must be recomputed
        if new_pos != self.__pos:
            self.__pos = new_pos
            self._position(self.get_inner_pos_())

    def __fill_background(
            self,
            surface: pg.surface.Surface,
            pos: types.pos_t
    ) -> None:
        bg = self.get_style('background')
        if bg is None:
            return
        if bg == 'image':
            bg_img = self.get_bg_img()
            if bg_img is None:
                msg = 'node has background style "image" but its '
                msg += 'background image could not be found'
                raise ValueError(msg)
            surface.blit(bg_img, pos)
        elif bg == 'color':
            corner = self.get_style('corner')
            bg_color = self.get_style('background-color')
            rect = Pos.rect(pos, self.size_)
            if corner is None or corner == 0:
                Draw.rectangle(surface, bg_color, rect)
            else:
                Draw.rectangle_rounded(surface, bg_color, rect, corner)
        else:
            raise ValueError(f'undefined background type: {bg}')

    def __draw_border_images(
            self,
            surface: pg.surface.Surface,
            pos: types.pos_t
    ) -> None:

        def draw_horizontal_bars() -> None:
            w = size[0] - (tl.get_width() + tr.get_width())
            x = tl.get_width()
            while w > 0:
                if hb.get_width() <= w:
                    rect = None
                else:
                    rect = pg.Rect((0, 0), (w, hb.get_height()))
                surface.blit(
                    hb, Pos.sum(pos, (x, 0)), rect
                )
                surface.blit(
                    hb, Pos.sum(pos, (x, size[1] - hb.get_height())), rect
                )
                w -= hb.get_width()
                x += hb.get_width()

        def draw_vertical_bars() -> None:
            h = size[1] - (tl.get_height() + tr.get_height())
            y = tl.get_height()
            while h > 0:
                if vb.get_height() <= h:
                    rect = None
                else:
                    rect = pg.Rect((0, 0), (vb.get_width(), h))
                surface.blit(
                    vb, Pos.sum(pos, (0, y)), rect
                )
                surface.blit(
                    vb, Pos.sum(pos, (size[0] - vb.get_width(), y)), rect
                )
                h -= hb.get_height()
                y += hb.get_height()

        def draw_corners() -> None:
            w, h = size
            for img, corner in [
                    (tl, (0, 0)),
                    (tr, (w, 0)),
                    (bl, (w, h)),
                    (br, (0, h))
            ]:
                x, y = corner
                if x > 0:
                    x -= img.get_width()
                if y > 0:
                    y -= img.get_width()
                surface.blit(img, Pos.sum((x, y), pos))

        tl, tr, bl, br, hb, vb = [
            Media.get_image_(img) for img in self.get_style('border-images')
        ]
        size = self.size_
        draw_horizontal_bars()
        draw_vertical_bars()
        draw_corners()

    def __draw_border_color(
            self, surface: pg.surface.Surface, pos: types.pos_t
    ) -> None:
        corner = self.get_style('corner')
        color = self.get_style('border-color')
        width = self.get_style('border-width')
        rect = Pos.rect(pos, self.size_)
        if width > 0:
            if corner is not None and corner > 0:
                Draw.rectangle_rounded(
                    surface, color, rect, corner, width
                )
            else:
                Draw.rectangle(
                    surface, color, rect, width
                )

    def __draw_border(
            self, surface: pg.surface.Surface, pos: types.pos_t
    ) -> None:
        border = self.get_style('border')
        if border == 'image':
            self.__draw_border_images(surface, pos)
        elif border == 'color':
            self.__draw_border_color(surface, pos)
        elif border is not None:
            raise ValueError(f'invalid border type: {border}')

    def draw(
            self,
            surface: pg.surface.Surface,
            pos: types.opt_pos_t = None
    ) -> None:
        """Draw self on the surface at position pos.

        If pos is None, self is drawn at position self.pos_.

        """
        if self.is_hidden():
            return
        scale = self.get_style('scale')
        opacity = self.get_style('opacity')
        scaled = scale is not None and scale != 1
        alphaed = opacity is not None and opacity != 1
        apos = self.pos_ if pos is None else pos
        work_on_tmp_surface = scaled or alphaed
        if not work_on_tmp_surface:
            s = surface
            dpos = apos
        else:
            s = pg.surface.Surface(self.size_).convert_alpha()
            s.fill((0, 0, 0, 0))
            dpos = (0, 0)
        self.__fill_background(s, dpos)
        self.__draw_border(s, dpos)
        self._draw(s, Pos.sum(dpos, self._get_inner_shift()))

        #  draw children nodes
        for child in self.iter_tree(rec=False):
            if child != self:
                cpos: Optional[types.pos_t]
                if work_on_tmp_surface:
                    cpos = Pos.diff(child.pos_, dpos)
                else:
                    cpos = (
                        None if pos is None
                        else Pos.sum(child.pos_, Pos.diff(self.pos_, pos))
                    )
                child.draw(s, pos=cpos)

        if scaled:
            new_size = Pos.mult(self.size_, scale)
            s = pg.transform.scale(s, new_size)
            apos = Pos.align(apos, new_size, self.size_, 'center', 'center')

        if alphaed:
            s.set_alpha(int(opacity * 255))

        # if we have worked on a temporary surface blit it on surface
        if work_on_tmp_surface:
            surface.blit(s, apos)

    def iter_tree(
            self,
            rec: bool = True,
            traverse: bool = False
    ) -> Iterator[Node]:
        """Yield self and all its sub-tree.

        If traverse is True, children nodes of _EventManager nodes
        inside self sub-tree are also traversed.

        """
        yield self
        yield from self._iter_tree(rec=rec, traverse=traverse)

    def is_over(self, pos: types.pos_t) -> bool:
        """Check if pos is inside self.get_absolute_rect()."""
        return (
            self.__pos is not None
            and self.__size is not None
            and self.__manager is not None
            and Pos.in_rect(self.get_absolute_rect(), pos)
        )

    def disable(self) -> None:
        """Disable self.

        self loses the focus if it has it.  The on-disable event is
        called on self and all its sub-tree.

        """
        self._set_disabled(True)
        if self.has_focus():
            self.lose_focus()
        for node in self.iter_tree():
            if node.manager is not None:
                node.manager._trigger('on-disable', None, node)

    def enable(self) -> None:
        """Enable self.

        The on-enable event is called on self and all its sub-tree.

        """
        self._set_disabled(False)
        for node in self.iter_tree():
            if node.manager is not None:
                node.manager._trigger('on-enable', None, node)

    def can_grab_focus(self) -> bool:
        """Check if the node can get the focus."""
        return self.__link is not None or self.__has_ctx_menu

    def can_grab_focus_now(self) -> bool:
        """Check if the node can get the focus now.

        Return true if self.can_grab_focus() + its current status
        allows it (i.e., visible and not disabled).

        """
        return (
            self.can_grab_focus()
            and not self.is_hidden()
            and not self.is_disabled()
        )

    def get_focus(self) -> None:
        """Node self gets the focus and the on-focus event is triggered.

        Method has no effect if the node already has the focus.

        """
        if self.has_focus() or not self.can_grab_focus_now():
            return
        self._set_focus(True)
        if self.manager is not None:
            self._update_manager()
            self.manager._trigger('on-focus', None, self)
            self.get_window().give_focus(self)

    def lose_focus(self) -> None:
        """Node self loses the focus and the on-unfocus event is triggered.

        Method has no effect if the node does not have the focus.

        """
        if not self.has_focus():
            return
        self._set_focus(False)
        if self.manager is not None:
            self._update_manager()
            self.manager._trigger('on-unfocus', None, self)
            self.get_window().remove_focus()

    def _has_focusable_content(self) -> bool:
        return self.can_grab_focus_now()

    def _receive_focus_from_direction(
            self, direction: types.pos_t  # pylint: disable=unused-argument
    ) -> Node:
        assert self.can_grab_focus_now()
        return self

    def activate(self) -> bool:
        """Activate self.

        If self is enabled, the on-activate event is triggered on it
        and its link is called (see help(pygwin.Node.__init__)).

        Return True if self has been activated, False otherwise (e.g.,
        if its disabled or if its _EventManager is not set.

        """
        if self.manager is None:
            return False
        if not self.is_disabled():
            result = self.manager._trigger('on-activate', None, self)
            result = self._activate() or result
            return result
        return False

    def _activate(self) -> bool:
        if self.__link is not None:
            self.get_focus()
            self.__link()
            return True
        return False

    def add_processor(
            self,
            evt: types.event_t,
            proc: types.event_proc_t
    ) -> None:
        """Add processor function proc for event evt.

        Function proc must have type pg.event.Event -> bool.  It will
        be called each time event evt will be triggered on self.  The
        pygame event parameter of the function is the one that
        generated the pygwin event or None if the pygwin event does
        not have an equivalent.  Function proc must return True if the
        event has been handled.  This result is used to determine if
        self's manager must be redrawned.

        """
        if evt not in types.all_events:
            logging.warning('event "%s" does not exist', evt)
        else:
            if evt not in self.__events:
                self.__events[evt] = list()
            self.__events[evt].append(proc)
            if self.__manager is not None:
                self.__manager._register(evt, self, proc)

    def del_processor(
            self,
            evt: types.event_t,
            proc: types.event_proc_t
    ) -> None:
        """Delete processor function proc for event evt.

        The method has no effect if the processor had not been
        previously added by add_processor.

        """
        self.__events[evt] = [p for p in self.__events[evt] if p != proc]
        if self.__manager is not None:
            self.__manager._unregister(evt, self, proc)

    def get_style(
            self,
            attr: types.style_attr_t
    ) -> Any:
        """Get the style of self for attribute attr.

        The result of the method is context dependent.  So, for
        example, if self has a color xx defined for the overed status
        and if the cursor is currently over self, then
        self.get_style('color') will return xx.

        """
        def get(node: Node) -> Tuple[bool, Any]:
            for c in node.stc:
                for pred, style in c._iter_styles():
                    if attr in style and all(pr(node) for pr in pred):
                        return True, style[attr]
            return False, None

        #  node status has changed => clear cache
        if self.__prev_flags != self.__flags:
            self.__style_cache = dict()
        self.__prev_flags = self.__flags

        #  look in cache
        try:
            result = self.__style_cache[attr]
            return result
        except KeyError:
            pass

        #  check if self has the attribute defined in one of its
        #  classes.  if so cache the result
        found, result = get(self)
        if found:
            self.__style_cache[attr] = result
            return result

        #  for inherited attributes check if one of the ancestors has
        #  this attribute defined
        if attr in INHERITED:
            parent = self.parent
            while parent is not None:
                found, result = get(parent)
                if found:
                    return result
                parent = parent.parent

        #  in any other case, return the default style
        try:
            self.__style_cache[attr] = DEFAULT[attr]
            return self.__style_cache[attr]
        except KeyError:
            return None

    def set_style(
            self,
            attr: types.style_attr_t,
            value: Any,
            context: Optional[types.sc_context_t] = None,
            cname: Optional[Any] = None,
            update: bool = True
    ) -> bool:
        """Set the value of a style attribute for self.

        If update is True, the style attribute for the context is
        updated.  Otherwise if self already has a style for that
        context, the method has no effect.

        If cname is not None, then it must be one of the style classes
        of self.  Then this style class is updated.

        Return True if the style has been modified, False otherwise.

        >>> n = Node()
        >>> n.set_style('background', 'color')
        True
        >>> n.set_style('color', (0, 0, 255))
        True
        >>> n.set_style('color', (255, 0, 0), context={'status': 'overed'})
        True
        >>> n.set_style(
        ...   'color', (0, 255, 0),
        ...   context={'status': 'overed'},
        ...   update=False
        ... )
        False

        """
        #  by default the modified style class is the private class of
        #  the node (i.e., the one that has self as name)
        if cname is None:
            cname = self

        #  change the attribute in the class
        c = next(c for c in self.stc if c.name == cname)
        if not c.add(attr, value, update=update, context=context):
            return False

        #  clear cache
        if attr in self.__style_cache:
            del self.__style_cache[attr]

        self.__update_style_procs()
        self._reset_size()
        return True

    def _clear_style_cache(self) -> None:
        self.__style_cache = dict()

    def _does_process_key(self, _: str) -> bool:  # pylint: disable=R0201
        return False

    def _compute_inner_size(self) -> types.pos_t:  # pylint: disable=R0201
        return 0, 0

    def _position(self, pos: types.pos_t) -> None:
        pass

    def _iter_tree(  # pylint: disable=R0201,W0613
            self, rec: bool = True, traverse: bool = False
    ) -> Iterator[Node]:
        yield from []

    def _draw(self, surface: pg.surface.Surface, pos: types.pos_t) -> None:
        pass

    def _get_inner_shift(self) -> types.pos_t:
        w, h = self._get_inner_diff()
        return int(w / 2), int(h / 2)

    def _get_inner_diff(self) -> types.pos_t:
        padding = self.get_style('padding')
        border = self.get_style('border')
        if border == 'image':
            img = Media.get_image_(self.get_style('border-images')[4])
            border = img.get_height()
        elif border == 'color':
            border = self.get_style('border-width')
        elif border is not None:
            raise ValueError(f'invalid border type: {border}')
        else:
            border = 0
        if isinstance(padding, int):
            diff = 2 * (border + padding)
            result = diff, diff
        else:
            left, top = padding
            result = 2 * (border + left), 2 * (border + top)
        return result

    def has_relative_size(self) -> bool:
        """Check if the size of self is defined relatively to its container.

        Return True if the 'size' style of self includes a percentage
        string, e.g. ('100%', 10) or (None, '100%').

        """
        s = self.get_style('size')
        return s is not None and (
            isinstance(s[0], str) or isinstance(s[1], str)
        )

    def get_font(self) -> pg.font.Font:
        """Get the pygame font that must be used to draw the node.

        The font returned depends on the 'font' and 'font-size' styles
        of self.

        """
        font = self.get_style('font')
        font_size = self.get_style('font-size')
        if isinstance(font_size, str):
            size = Media.get_font_size(font)
            try:
                mult = {
                    'xx-small': 0.4,
                    'x-small': 0.6,
                    'small': 0.8,
                    'normal': 1.0,
                    'large': 1.4,
                    'x-large': 1.8,
                    'xx-large': 2.2
                }[font_size]
            except KeyError:
                logging.warning('undefined font-size: %s', font_size)
                mult = 1
            font_size = int(mult * size)
        return Media.get_font_(font, size=font_size)

    __STYLE_ANIMATIONS: Dict[types.animation_t, Type[Animation]] = {
        'fade': FadeAnimation,
        'fadein': FadeInAnimation,
        'fadeout': FadeOutAnimation,
        'fill': FillAnimation,
        'glow': GlowAnimation,
        'grow': GrowAnimation,
        'popin': PopInAnimation,
        'popout': PopOutAnimation,
        'scroll': ScrollAnimation
    }

    __STATUS_ON: Dict[types.status_t, types.event_t] = {
        'base': 'on-open',
        'clicked': 'on-clicked',
        'disabled': 'on-disable',
        'focus': 'on-focus',
        'overed': 'on-over',
        'selected': 'on-select'
    }
    __STATUS_OFF: Dict[types.status_t, types.event_t] = {
        'base': 'on-close',
        'clicked': 'on-unclicked',
        'disabled': 'on-enable',
        'focus': 'on-unfocus',
        'overed': 'on-unover',
        'selected': 'on-unselect'
    }

    def __update_style_procs(self) -> None:
        def play_animation(
                animation: Optional[types.animation_t],
                animation_args: Dict[str, Any]
        ) -> bool:
            if animation is None:
                return False
            try:
                cls = Node.__STYLE_ANIMATIONS[animation]
            except KeyError:
                logging.warning('undefined animation: %s', animation)
                return False
            if self.__animation is not None:
                self.__animation.stop()
                self.__animation = None
            if animation_args is None:
                args = dict()
            else:
                args = animation_args
            cls(self, **args)
            return True

        #  delete previous style-related processors
        for evt, procs in self.__style_procs.items():
            for proc in procs:
                self.del_processor(evt, proc)
        self.__style_procs = dict()

        #  add processors to change style (the on-change event is
        #  always considered if the node has value dependent styles)
        changing_events = {
            evt
            for c in self.stc
            for _, status in c._get_checked_status()
            for evt in [Node.__STATUS_ON[status], Node.__STATUS_OFF[status]]
        }
        if any(c.does_check_value() for c in self.stc):
            changing_events.add('on-change')
        for evt in changing_events:
            def change_style(_: types.event_t) -> types.event_proc_t:
                def do(_: pg.event.Event) -> bool:
                    return True
                return do
            proc = change_style(evt)
            self.add_processor(evt, proc)
            self.__style_procs[evt] = [proc]

        #  add processors for event styles
        for evt, pred, style in [
                (evt, pred, style)
                for c in self.stc
                for evt in types.all_events
                for pred, style in c._iter_events(evt)
        ]:
            def handle_event(
                    evt: types.event_t,
                    pred: List[types.node_pred_t],
                    style: types.style_t
            ) -> types.event_proc_t:
                def do(pgevt: pg.event.Event) -> bool:
                    if not all(pr(self) for pr in pred):
                        return False
                    sound = style.get('sound')
                    if (sound is not None
                        and (evt != 'on-key'
                             or (self.has_focus() and
                                 self._does_process_key(pgevt.unicode)))):
                        Media.play_sound(sound)
                    return play_animation(
                        style.get('animation'),
                        style.get('animation-arguments', dict())
                    )
                return do
            proc = handle_event(evt, pred, style)
            self.add_processor(evt, proc)
            li = self.__style_procs.get(evt, list())
            li.append(proc)
            self.__style_procs[evt] = li

        #  add processors for animations
        for status in [
                status
                for c in self.stc
                for style, status in c._get_checked_status()
                if 'animation' in style
        ]:
            def start(_: pg.event.Event) -> bool:
                return play_animation(
                    self.get_style('animation'),
                    self.get_style('animation-arguments')
                )

            def stop(_: pg.event.Event) -> bool:
                if self.__animation is not None:
                    self.__animation.stop()
                    self.__animation = None
                    return True
                return False
            for evt, fun in [
                    (Node.__STATUS_ON[status], start),
                    (Node.__STATUS_OFF[status], stop)
            ]:
                self.add_processor(evt, fun)
                self.__style_procs[evt].append(fun)

    def _new_tmp_style_class(self) -> str:
        result = StyleClass('tmp', register=False)
        self.stc.insert(0, result)
        return 'tmp'

    def _del_tmp_style_class(self, cname: str) -> None:
        self.__stc = [sc for sc in self.stc if sc.name != cname]
