#!/usr/bin/env python3

"""Document this method."""

from pygwin import Label, Window, Box, Cursor, Image, Media


TITLE = 'cursor'.title()


def get_window(win_sys):
    """cursor window"""
    def close(_):
        Cursor.deactivate()
    Cursor.set_default('cursor-base.png')
    Cursor.activate()
    elf = Image(Media.get_image('elf.png', scale=(128, 128)))
    elf.set_style(
        'cursor-image', 'cursor-overed.png', context={'status': 'overed'}
    )
    elf.set_style(
        'cursor-image', 'cursor-clicked.png', context={'status': 'clicked'}
    )
    box = Box(
        Label('move over/click the image to change the cursor'),
        elf
    )
    result = Window(win_sys, box, title=TITLE)
    result.add_processor('on-close', close)
    return result
