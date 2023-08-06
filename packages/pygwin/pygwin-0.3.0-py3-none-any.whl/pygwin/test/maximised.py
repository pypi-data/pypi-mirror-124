#!/usr/bin/env python3

"""Document this method."""

from pygwin import Window, Frame
from . import glob


TITLE = 'maximised window'.title()


def get_window(win_sys):
    """maximised window"""
    board = glob.lorem_ipsum_textboard()
    result = Window(
        win_sys,
        Frame(board, style={'expand': True, 'size': ('100%', '100%')}),
        title=TITLE,
        style={'size': ('100%', '100%')}
    )
    return result
