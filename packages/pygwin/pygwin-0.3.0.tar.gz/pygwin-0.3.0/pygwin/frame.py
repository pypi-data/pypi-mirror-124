#!/usr/bin/env python3

"""Definition of class Frame."""

from typing import Tuple, Any, List, Iterator, Dict
import math
import pygame as pg

from . import types, Pos, Draw, Node, Util, Media
from .event_manager import _EventManager


class Frame(_EventManager):
    """Frame nodes are wrappers for other nodes.

    The content of a frame can grow but the frame will keep a constant
    size.

    For instance to create a frame of size (100, 100) containing a box:
    >>> from . import Box
    >>> Frame(Box(), style={'size': (100, 100)})
    <pygwin.frame.Frame object at ...>

    """

    AVAILABLE_STYLES = {
        'frame-bar-background-color',
        'frame-bar-color',
        'frame-bar-corner',
        'frame-bar-width',
        'frame-vbar-images'
    }

    #  how much do we scroll (in points) when using the mouse wheel
    WHEEL_SCROLL_PTS = 20

    KEY_SCROLL_DOWN = pg.K_PAGEDOWN
    KEY_SCROLL_UP = pg.K_PAGEUP

    def __init__(self, node: Node, **kwargs: Any):
        """Initialise a Frame with content Node node."""

        def click_down(pgevt: pg.event.Event) -> bool:
            if self.__scroll_vertical(pgevt.pos, True):
                self.__vscrolling = True
                return True
            return False

        def click_up(_: pg.event.Event) -> bool:
            if self.__vscrolling:
                self.__vscrolling = False
                return True
            return False

        def slide(pgevt: pg.event.Event) -> bool:
            if self.__vscrolling:
                self.get_focus()
                return self.__scroll_vertical(pgevt.pos, False)
            return False

        def key(pgevt: pg.event.Event) -> bool:
            pts = None
            if pgevt.key == Frame.KEY_SCROLL_DOWN:
                pts = 10 * Frame.WHEEL_SCROLL_PTS
            elif pgevt.key == Frame.KEY_SCROLL_UP:
                pts = - 10 * Frame.WHEEL_SCROLL_PTS
            if pts is not None:
                return self.__vertical_scroll(pts)
            return False

        def mouse_wheel(pgevt: pg.event.Event) -> bool:
            if not self.__has_vertical_scroll_bar():
                return False
            move = None
            pts = Frame.WHEEL_SCROLL_PTS
            if pgevt.button == Util.MOUSEBUTTON_WHEEL_DOWN:
                move = pts * - 1
            elif pgevt.button == Util.MOUSEBUTTON_WHEEL_UP:
                move = pts
            result = move is not None and self.__vertical_scroll(move)
            self.get_focus()
            return result

        def unover(_: pg.event.Event) -> bool:
            return self._clear()

        _EventManager.__init__(self, **kwargs)
        self.__scroll = 0, 0
        self.__vscrolling = False
        self.__node = node
        self.__align_shift = 0, 0
        processed: Dict[types.event_t, types.event_proc_t] = {
            'on-click-down': click_down,
            'on-click-up': click_up,
            'on-mouse-wheel': mouse_wheel,
            'on-over': slide,
            'on-over-again': slide,
            'on-key': key,
            'on-unover': unover
        }
        for evt, proc in processed.items():
            self.add_processor(evt, proc)
        for child in node.iter_tree():
            child._set_manager(self)

    @property
    def content(self) -> Node:
        """Get the node inside the frame."""
        return self.__node

    @property
    def hscroll(self) -> int:
        """Get the horizontal scrolling in pixels."""
        return self.__scroll[0]

    @property
    def vscroll(self) -> int:
        """Get the vertical scrolling in pixels."""
        return self.__scroll[1]

    def vscroll_move(self, move: int) -> None:
        """Increase the vertical scrolling by move pixels."""
        h, v = self.__scroll
        self.__scroll = h, v + move

    def set_vscroll(self, vscroll: int) -> None:
        """Set the vertical scrolling."""
        self.__scroll = self.__scroll[0], vscroll
        self._update_manager()

    def scroll_bottom(self) -> None:
        """Scroll to the bottom of the frame."""
        self.set_vscroll(self.__vscroll_bounds()[1])

    def scroll_top(self) -> None:
        """Scroll to the top of the frame."""
        self.set_vscroll(self.__vscroll_bounds()[0])

    def at_bottom(self) -> bool:
        """Check if the vertical scroll bar is at bottom."""
        return self.vscroll == self.__vscroll_bounds()[1]

    def at_top(self) -> bool:
        """Check if the vertical scroll bar is at top."""
        return self.vscroll == 0

    def _get_scroll(self) -> types.pos_t:
        wd, hd = self._get_inner_diff()
        result = self.__scroll
        result = Pos.diff(result, (int(wd / 2), int(hd / 2)))
        result = Pos.sum(result, self.__align_shift)
        return result

    def available_size(self) -> types.opt_pos_opt_t:
        """Get the available size inside the frame."""
        return self.get_inner_size()

    def _compute_size(self) -> types.pos_t:
        if self.size is None:
            Node._compute_size(self)
            if self.content.has_relative_size():
                self.content._reset_size()
                self.content._compute_size()
        return self.size_

    def make_visible(self, node: Node) -> None:
        assert node.manager == self
        try:
            Pos.check(node.pos_)
            Pos.check(node.size_)
            Pos.check(self.pos_)
            Pos.check(self.size_)
        except AssertionError:
            return
        _, y = node.pos_
        _, h = node.size_
        _, ph = self.get_inner_size_()
        if y + h > self.vscroll + ph:
            self.set_vscroll(y + h - ph)
        if y < self.vscroll:
            self.set_vscroll(y)

    def _compute_inner_size(self) -> types.pos_t:
        return self.content._compute_size()

    def _draw(self, surface: pg.surface.Surface, pos: types.pos_t) -> None:
        inner_size = self.get_inner_size_()
        self._draw_content()
        self.set_vscroll(
            Util.in_range(self.vscroll, self.__vscroll_bounds())
        )
        cpos = Pos.align(
            pos, self.content.size_, inner_size,
            self.content.get_style('halign'), self.content.get_style('valign')
        )
        self.__align_shift = Pos.diff(pos, cpos)
        surface.blit(
            self.surface_, cpos,
            area=pg.Rect(self.__scroll, inner_size)
        )
        self.__draw_scroll_bars(surface, pos)

    def __scroll_vertical(
            self,
            pos: types.pos_t,
            check_in_bar: bool
    ) -> bool:
        if not self.__has_vertical_scroll_bar():
            return False
        pos = Pos.diff(pos, self.get_absolute_pos())
        pos = Pos.diff(pos, self._get_inner_shift())
        rect_container, _ = self.__get_vscroll_bar_rects()
        if not check_in_bar or Pos.in_rect(rect_container, pos):
            _, y, _, h = rect_container
            y = pos[1] - y
            _, h = self.get_inner_size_()
            _, rh = self.content.size_
            newvscroll = math.ceil(rh / h * y)
            newvscroll = Util.in_range(newvscroll, self.__vscroll_bounds())
            self.set_vscroll(newvscroll)
            return True
        return False

    def __vscroll_bounds(self) -> types.pos_t:
        inner_size = self.get_inner_size()
        if inner_size is None:
            max_height = None
        else:
            max_height = inner_size[1]
        if max_height is None:
            result = 0, 0
        else:
            _, ymax = self.content.size_
            result = 0, max(0, ymax - max_height)
        return result

    def __has_vertical_scroll_bar(self) -> bool:
        size = self.get_inner_size()
        max_height = None if size is None else size[1]
        return max_height is not None and self.content.size_[1] > max_height

    def __get_scroll_bar_sizes(self) -> types.pos_opt_t:
        w, h = self.get_inner_size_()
        rw, rh = self.content.size_
        resultw, resulth = None, None
        if rh >= h and rh > 0:
            resulth = int(h * h / rh)
        if rw >= w and rw > 0:
            resultw = int(w * w / rw)
        return resultw, resulth

    def __get_vscroll_bar_rects(
            self
    ) -> Tuple[types.rect_t, types.rect_t]:
        imgs = self.get_style('frame-vbar-images')
        bar_width: int
        if imgs is None:
            bar_width = self.get_style('frame-bar-width')
            if not isinstance(bar_width, int):
                raise ValueError('integer expected for style frame-bar-width')
        else:
            img = Media.get_image_(imgs[0])
            bar_width = img.get_width()
        w, h = self.get_inner_size_()
        _, rh = self.content.size_
        _, scrollh = self.__get_scroll_bar_sizes()
        assert scrollh is not None
        x = w - bar_width
        ystart = math.ceil(self.vscroll * h / rh)
        return (
            (x, 0, bar_width, h),
            (x, ystart, bar_width, scrollh)
        )

    def __draw_vscroll_bar_color(
            self,
            surface: pg.surface.Surface,
            rect_cont: types.rect_t,
            rect_bar: types.rect_t
    ) -> None:
        col = self.get_style('frame-bar-background-color')
        corner = self.get_style('frame-bar-corner')

        #  draw the scrollbar container
        _, _, w, h = rect_cont
        Draw.rectangle_rounded(surface, col, (0, 0, w, h), corner)

        #  draw the scrollbar
        _, y, w, h = rect_bar
        col = self.get_style('frame-bar-color')
        Draw.rectangle_rounded(surface, col, (0, y, w, h), corner)

    def __draw_vscroll_bar_image(
            self,
            surface: pg.surface.Surface,
            rect_cont: types.rect_t,
            rect_bar: types.rect_t
    ) -> None:
        def draw(
                ystart: int,
                yend: int,
                imgs: List[pg.surface.Surface]
        ) -> None:
            top, middle, bottom = imgs
            y = ystart
            surface.blit(top, (0, ystart))
            y += top.get_height()
            while y < yend:
                rect = None
                if middle.get_height() + y > yend:
                    rect = pg.Rect(0, 0, middle.get_width(), yend - y)
                surface.blit(middle, (0, y), rect)
                y += middle.get_height()
            surface.blit(bottom, (0, yend - bottom.get_height()))

        #  draw the container
        imgs = self.get_style('frame-vbar-images')
        draw(0, rect_cont[3], list(map(Media.get_image_, imgs))[0:3])

        #  draw the scrollbar
        _, y, _, h = rect_bar
        draw(y, y + h, list(map(Media.get_image_, imgs))[3:6])

    def __draw_scroll_bars(
            self,
            surface: pg.surface.Surface,
            pos: types.pos_t
    ) -> None:
        if self.__has_vertical_scroll_bar():
            rect_cont, rect_bar = self.__get_vscroll_bar_rects()
            x0, y0, w, h = rect_cont
            s = pg.Surface((w, h)).convert_alpha()
            s.fill((0, 0, 0, 0))
            if self.get_style('frame-vbar-images') is None:
                self.__draw_vscroll_bar_color(s, rect_cont, rect_bar)
            else:
                self.__draw_vscroll_bar_image(s, rect_cont, rect_bar)
            surface.blit(s, (pos[0] + x0, pos[1] + y0))

    def __vertical_scroll(self, pts: int) -> bool:
        newvscroll = self.vscroll + pts
        newvscroll = Util.in_range(newvscroll, self.__vscroll_bounds())
        result = self.vscroll != newvscroll
        if result:
            self.set_vscroll(newvscroll)
        return result

    def _iter_tree(
            self, rec: bool = True, traverse: bool = False
    ) -> Iterator[Node]:
        if traverse:
            yield from self.content.iter_tree(rec=rec, traverse=True)

    def _has_focusable_content(self) -> bool:
        return any(
            node._has_focusable_content()
            for node in self.content.iter_tree()
        )

    def _receive_focus_from_direction(self, direction: types.pos_t) -> Node:
        w = self.content.get_width()
        h = self.content.get_height()
        assert w is not None and h is not None

        from_pos = {
            (0, 1): (int(w / 2), 0),
            (0, -1): (int(w / 2), h),
            (1, 0): (0, int(h / 2)),
            (-1, 0): (w, int(h / 2))
        }[direction]
        candidates = list()
        for node in self.content.iter_tree():
            if node._has_focusable_content():
                node_center = Pos.center(node.get_rect())
                diff = Pos.diff(from_pos, node_center)
                move = diff[0] * direction[0], diff[1] * direction[1]
                if Pos.gt((0, 0), move):
                    candidates.append(node)

        candidates.sort(key=lambda node: Pos.distance(node.pos_, from_pos))
        for new_focus in candidates:
            if new_focus.can_grab_focus_now():
                return new_focus
            node = new_focus._receive_focus_from_direction(direction)
            if node is not None:
                return node
        return node
