#!/usr/bin/env python3

"""Document this method."""

import os

from pygwin import Box, Label, Window, Table
from pygwin import ItemSelect
from pygwin.style import DEFAULT
from . import glob


TITLE = 'fonts'.title()


def get_window(win_sys):
    """fonts window"""
    def change_name(_):
        lbl.set_style('font', name_select.value)
        return True

    def change_size(_):
        lbl.set_style('font-size', size_select.value)
        return True
    lbl = Label('hey, change my font!', style={'halign': 'center'})
    select = dict()
    select[DEFAULT['font']] = 'default'
    for f in os.listdir(glob.MEDIA_DIR):
        name, ext = os.path.splitext(f)
        if ext == '.ttf':
            select[f] = name
    tbl = Table(style={'halign': 'center'})
    name_select = ItemSelect(select)
    size_select = ItemSelect({s: s for s in range(8, 42, 2)}, value=24)
    name_select.add_processor('on-change', change_name)
    size_select.add_processor('on-change', change_size)
    tbl.new_row({0: Label('font name'), 1: name_select})
    tbl.new_row({0: Label('font size'), 1: size_select})
    box = Box(tbl, lbl, style={'expand': True, 'size': ('100%', '100%')})
    return Window(win_sys, box, title=TITLE, style={'size': (500, 200)})
