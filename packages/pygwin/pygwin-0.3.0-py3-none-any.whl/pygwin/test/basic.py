#!/usr/bin/env python3

"""Document this method."""

from pygwin import Window, Box


TITLE = 'basic window'.title()


def get_window(win_sys):
    """test window"""
    box = Box(
        'The window can be moved by',
        'drag and dropping its title.',
        'Escape closes the window.'
    )
    return Window(win_sys, box, title=TITLE)
