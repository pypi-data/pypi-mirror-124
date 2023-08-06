#!/usr/bin/env python3

"""Document this method."""

from pygwin import Menu, Window, Box, Frame, Image, Media
from . import glob


TITLE = 'maximised menu'.title()


def get_window(win_sys):
    """maximised menu"""
    items = dict()
    boards = {
        m: glob.lorem_ipsum_textboard()
        for m in glob.MONSTERS
    }
    for m, mdata in glob.MONSTERS.items():
        box = Box(
            glob.monster_table(m),
            boards[m],
            style={'size': ('100%', None)}
        )
        frame = Frame(
            box,
            style={'expand': True, 'size': ('100%', '100%')}
        )
        img = Image(Media.get_image(mdata[0], scale=(64, 64)))
        items[img] = frame
    node = Menu(items, style={'expand': True, 'size': ('100%', '100%')})
    return Window(
        win_sys,
        node,
        title=TITLE,
        style={'size': ('100%', '100%')}
    )
