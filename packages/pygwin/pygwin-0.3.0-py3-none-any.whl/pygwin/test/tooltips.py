#!/usr/bin/env python3

"""Document this method."""

from pygwin import Label, Window, Table, Image, Media, Box
from . import glob


TITLE = 'tooltips'.title()


def get_window(win_sys):
    """tooltips window"""
    def tooltip(pos):
        result = Box(style={**glob.TOOLTIP_STYLE, 'pos': pos})
        result.pack(Label('this is the tooltip'))
        for f in ['dragon.png', 'elf.png']:
            result.pack(Image(Media.get_image(f, scale=(64, 64))))
        return result

    def new_label(lbl, pos):
        result = Label(lbl, style={'halign': 'center'})
        result.set_tooltip(tooltip(pos))
        return result
    vpos = [
        ('top', 'top'),
        ('center', 'center'),
        ('bottom', 'bottom')
    ]
    hpos = [
        ('left', 'left'),
        ('center', 'center'),
        ('right', 'right')
    ]
    coord_sys = [
        ('absolute', 'absolute'),
        ('relative', 'relative')
    ]

    tbl = Table(style={'halign': 'center'})
    tbl.new_row(
        {0: Label('tooltips can pop when overing an item')},
        colspan={0: 3}
    )
    for clbl, ct in coord_sys:
        tbl.new_row({0: Label(f'{clbl} positioning',
                              style={'halign': 'center'})},
                    colspan={0: 3})
        for vlbl, v in vpos:
            tbl.new_row(
                {
                    i: new_label(f'{vlbl}{hlbl}', (ct, (h, v), (0, 0)))
                    for i, (hlbl, h) in enumerate(hpos)
                }
            )
    return Window(win_sys, tbl, title=TITLE, style={'size': (800, 600)})
