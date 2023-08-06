#!/usr/bin/env python3

"""Document this method."""

from pygwin import Label, Window, Table, Image, Media
from . import glob


TITLE = 'tables'.title()


def get_window(win_sys):
    """tables window"""
    center = {'halign': 'center'}
    right = {'halign': 'right'}
    tbl = Table()
    tbl.new_row({0: Label('monster', style=center),
                 2: Label('characteristics', style=center)},
                colspan={0: 2, 2: 4})
    tbl.new_row({2: Label('health', style=center),
                 4: Label('magic', style=center)},
                colspan={2: 2, 4: 2})
    tbl.new_row({2: Label('min'),
                 3: Label('max'),
                 4: Label('min'),
                 5: Label('max')})
    for m, mdata in glob.MONSTERS.items():
        cells = {
            j + 2: Label(data, style=right)
            for j, data in enumerate(mdata[1:])
        }
        cells[0] = Label(m)
        cells[1] = Image(Media.get_image(mdata[0]))
        tbl.new_row(cells)
    return Window(win_sys, tbl, title=TITLE)
