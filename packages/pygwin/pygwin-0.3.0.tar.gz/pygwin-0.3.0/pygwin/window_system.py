#!/usr/bin/env python3

"""Definition of class WindowSystem."""

from typing import TYPE_CHECKING, Optional, List, Set
import time
import pygame as pg

from . import types, Animation, Cursor, Media
if TYPE_CHECKING:
    from . import Window, Panel


class WindowSystem:  # pylint: disable=R0902
    """WindowSystem is pygwin's main class."""

    def __init__(self, screen: pg.surface.Surface):
        """Initialize a window system in the given screen surface.

        >>> import pygame as pg
        >>> from pygwin import WindowSystem
        >>> _ = pg.init()
        >>> screen = pg.display.set_mode((800, 600))
        >>> win_sys = WindowSystem(screen)
        >>> win_sys.draw()

        """
        self.__surface = pg.Surface(screen.get_size())
        self.__screen = screen
        self.__windows: List['Window'] = list()
        self.__panels: Set['Panel'] = set()
        self.__redraw_all = True
        self.__redraw_cursor = True
        self.__closed = False
        self.__mouse = True
        self.__last_redraw: Optional[float] = None
        self.__frozen = False

    @property
    def screen(self) -> pg.surface.Surface:
        """Get the screen surface self is attached to."""
        return self.__screen

    @property
    def closed(self) -> bool:
        """Check if self has been closed."""
        return self.__closed

    def set_frozen(self, frozen: bool) -> None:
        """Freeze/unfreeze self.

        When frozen, pygame events are ignored.

        """
        self.__frozen = frozen

    def set_closed(self, closed: bool) -> None:
        """Close/open the window system."""
        self.__closed = closed

    def top_window(self) -> Optional['Window']:
        """Get the top window of self (i.e., the last opened window).

        Return None if no window is currently opened.

        """
        if self.__windows == []:
            result = None
        else:
            result = self.__windows[0]
        return result

    def center_window(self, win: 'Window') -> None:
        """Center window object win in self."""
        sw, sh = self.__surface.get_size()
        win._compute_size()
        w, h = win.size_
        win.set_absolute_pos((int((sw - w) / 2), int((sh - h) / 2)))

    def open_window(
            self,
            win: 'Window',
            pos: types.opt_pos_t = None
    ) -> None:
        """Open Window win in self.

        Win is position at position pos if not None or otherwise centered.

        """
        self.__windows.insert(0, win)
        if pos is None:
            self.center_window(win)
        else:
            win.set_absolute_pos(pos)

    def window_opened(self, win: 'Window') -> bool:
        """Check if window win has been opened in self."""
        return win in self.__windows or win in self.__panels

    def close_window(self, win: Optional['Window']) -> None:
        """Close window win of self.

        If win is None, the top window is closed.

        """
        if win is None:
            if self.__windows == []:
                return
            win = self.__windows[0]
        if win in self.__windows:
            self.__windows.remove(win)
            Animation.stop_all(wins=[win])

    def close_all_windows(self) -> None:
        """Close all the windows of self."""
        while self.__windows != []:
            self.close_window(self.__windows[0])

    def center_all_windows(self) -> None:
        """Center all windows of self."""
        for win in self.__windows:
            self.center_window(win)

    def open_panel(self, panel: 'Panel', pos: types.pos_t) -> None:
        """Open Panel panel in self at position pos."""
        self.__panels.add(panel)
        panel.set_absolute_pos(pos)

    def close_panel(self, panel: 'Panel') -> None:
        """Close Panel panel of self."""
        if panel in self.__panels:
            self.__panels.remove(panel)

    def process_pg_event(self, pgevt: pg.event.Event) -> bool:
        """Process pygame event pgevt.

        Return True if the event has been processed, False
        otherwise.

        """
        def dispatch() -> bool:
            result = False
            for win in self.__windows + list(self.__panels):
                result = win.process_pg_event(pgevt)
                if result or win.modal:
                    break
            return result

        #  self is frozen => event is ignored
        if self.__frozen:
            return False

        #  if mouse is disabled, several event types are ignored
        if not self.__mouse and pgevt.type in [
                pg.MOUSEBUTTONDOWN,
                pg.MOUSEBUTTONUP,
                pg.MOUSEMOTION,
                pg.MOUSEWHEEL
        ]:
            return False

        result = dispatch()
        self.__redraw_all = self.__redraw_all or result
        self.__redraw_cursor = (
            self.__redraw_cursor or
            Cursor.activated() and pgevt.type in [
                pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP, pg.MOUSEMOTION
            ]
        )
        return result

    def draw(self, update: bool = False) -> None:
        """Draw self (i.e., all its windows and panels) in its screen surface.

        If update == True, pygame.display.update is called after
        drawing.

        """
        #  if we have not redrawn for 1 second => force redraw
        now = time.time()
        if not self.__redraw_all:
            if self.__last_redraw is None:
                self.__redraw_all = True
            elif now - self.__last_redraw >= 1:
                self.__redraw_all = True

        if self.__redraw_all:
            self.__last_redraw = now
            self.__surface.fill((0, 0, 0))
            for panel in list(self.__panels):
                panel.blit(self.__surface)
            for win in self.__windows[::-1]:  # last window opened first
                win.blit(self.__surface)
            self.__screen.blit(self.__surface, (0, 0))
            self.__draw_cursor()
            if update:
                pg.display.update()
        elif self.__redraw_cursor:
            self.__screen.blit(self.__surface, (0, 0))
            self.__draw_cursor()
            pg.display.update()
        self.__redraw_all = False
        self.__redraw_cursor = False

    def __active(self) -> List['Window']:
        if self.__windows != []:
            result = [self.__windows[0]]
        else:
            result = list(self.__panels)
        return result

    def refresh(self, force_redraw: bool = False) -> None:
        """Redraw self.

        Run all animations of the top window or of all panels if no
        window is opened.

        The window system is then redrawned if something has been
        updated in it (e.g., the size of one window) or if
        force_redraw is True.

        """
        self.__redraw_all = (
            Animation.run_all(wins=self.__active()) or self.__redraw_all
        )
        self.__redraw_all = self.__redraw_all or force_redraw
        self.draw(update=True)

    def __draw_cursor(self) -> None:
        if not Cursor.activated():
            return

        #  check if some node overrides the cursor image
        for win in self.__active():
            img = win._get_cursor_image()
            if img is not None:
                media = Media.get_image(img)
                if media is not None:
                    self.__screen.blit(media, pg.mouse.get_pos())
                    return

        #  otherwise get the default cursor image
        img = None
        if pg.mouse.get_pressed(num_buttons=3)[0]:
            img = Cursor.get_default(status='clicked')
        if img is None:
            img = Cursor.get_default()
        if img is not None:
            self.__screen.blit(img, pg.mouse.get_pos())

    def disable_mouse(self) -> None:
        """Totally disable the mouse for self.

        After the call, no cursor appears at all and mouse related
        events are not processed anymore.

        """
        self.__mouse = False
        Cursor.deactivate()
        pg.mouse.set_visible(False)

    def enable_mouse(self) -> None:
        """Enable the mouse for self.

        Mouse cursor becomes visible and mouse related events are
        processed again.

        """
        self.__mouse = True
        pg.mouse.set_visible(True)
