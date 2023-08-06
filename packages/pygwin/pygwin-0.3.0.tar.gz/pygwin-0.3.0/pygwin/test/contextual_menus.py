#!/usr/bin/env python3

"""Document this method."""

from pygwin import Box, Label, Window, Image, Media
from . import glob


TITLE = 'contextual menus'.title()


def get_window(win_sys):
    """contextual menus window"""
    def delete(m):
        def do():
            box.remove(monsters.index(m) + 1)
            monsters.remove(m)
            return True
        return do

    def show(m):
        def do():
            Window(win_sys, glob.monster_table(m), title=m).open()
            return True
        return do

    def close(img):
        def fun():
            img.clear_ctx_menu()
            return True
        return fun
    box = Box()
    box.pack(Label('right-click on a monster to open a contextual menu'))
    monsters = list()
    centered = {'halign': 'center'}
    for m, mdata in glob.MONSTERS.items():
        monsters.append(m)
        img = Image(Media.get_image(mdata[0], scale=(128, 128)))
        menu = Box(
            Label('menu', style={'halign': 'center'}),
            Label(f'delete {m}', link=delete(m), style=centered),
            Label(f'show {m}', link=show(m), style=centered),
            Label('close', link=close(img), style=centered),
            style=glob.TOOLTIP_STYLE
        )
        img.set_ctx_menu(menu)
        box.pack(img)
    return Window(win_sys, box, title=TITLE)
