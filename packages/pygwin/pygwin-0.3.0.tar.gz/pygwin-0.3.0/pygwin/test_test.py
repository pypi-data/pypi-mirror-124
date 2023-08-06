#!/usr/bin/env python3

"""
Document this method.
"""

import pygame as pg

from . import WindowSystem, StyleClass, Media
from .test.all import all_tests
from .test import glob


def test_test():
    """Open all test windows of pygwin.test."""
    pg.init()
    pg.font.init()
    screen = pg.display.set_mode((1200, 800))
    Media.add_media_path(glob.MEDIA_DIR)
    StyleClass.load_default()
    screen = pg.display.set_mode((1200, 800))
    win_sys = WindowSystem(screen)
    for test in all_tests:
        win = test.get_window(win_sys)
        win.open()
        win_sys.refresh(force_redraw=True)
        win.close()
    pg.quit()
