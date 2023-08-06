#!/usr/bin/env python3

"""Test module for pygwin.

Provides function go that launches a simple test application.

"""

import sys
import logging
import pygame as pg

from pygwin import mdata, StyleClass, WindowSystem, Keys, Media
from .main import main_panel
from . import glob


def go():
    """Launch the test."""

    #  default key bindings:
    #    * escape => close window
    #    * tab => move focus forward
    #    * lshift + tab => move focus backward
    #    * enter => activate element with focus
    Keys.bind(pg.K_RETURN, 'activate')
    Keys.bind(pg.K_ESCAPE, 'close-window')
    Keys.bind(pg.K_TAB, 'move-focus-forward')
    Keys.bind(pg.K_TAB, 'move-focus-backward', pressed=[pg.K_LSHIFT])

    #  configure logging
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    stdout_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s;%(module)s;%(message)s')
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)

    #  pygame initialisation stuff
    pg.init()
    pg.mixer.init()
    pg.font.init()

    screen = pg.display.set_mode((1200, 820))
    pg.display.set_caption(f'pygwin v{mdata.VERSION} - test application')
    StyleClass.load_default()
    Media.add_media_path(glob.MEDIA_DIR)
    win_sys = WindowSystem(screen)
    p = main_panel(win_sys)
    p.open(pos=(0, 0))
    pg.key.set_repeat(200, 100)
    clock = pg.time.Clock()
    win_sys.draw(update=True)

    #  main loop
    while not win_sys.closed:
        for pgevt in pg.event.get():
            if pgevt.type == pg.QUIT:
                win_sys.set_closed(True)
            win_sys.process_pg_event(pgevt)
        win_sys.refresh()
        clock.tick(glob.FPS)

    pg.quit()
    sys.exit(0)


if __name__ == '__main__':
    go()
