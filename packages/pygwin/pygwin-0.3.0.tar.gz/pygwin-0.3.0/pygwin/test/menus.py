#!/usr/bin/env python3

"""Document this method."""

from pygwin import Menu, Window, Image, Media
from . import glob


TITLE = 'menus'.title()


def get_window(win_sys):
    """menus window"""
    items = {
        Image(Media.get_image(mdata[0], scale=(64, 64))): glob.monster_table(m)
        for m, mdata in glob.MONSTERS.items()
    }
    menu = Menu(items, style={'orientation': 'horizontal'})
    return Window(win_sys, menu, title=TITLE)
