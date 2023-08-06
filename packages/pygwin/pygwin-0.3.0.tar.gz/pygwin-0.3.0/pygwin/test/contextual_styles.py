#!/usr/bin/env python3

"""Document this method."""

from pygwin import Box, Window, InputText, Checkbox, TextBoard


TITLE = 'contextual styles'.title()


def get_window(win_sys):
    """contextual styles window"""
    board = TextBoard(
        """Elements can have styles which depend on the current value of the
element.  For example, the border of the checkbox will become <color
rgb="0,255,0">green</color> if you select it or the background of the
input text will become <color rgb="255,0,0">red</color> if you type
the word wrong it.""",
        style={'size': ('100%', None)}
    )
    cb = Checkbox()
    cb.set_style(
        'border-color', (0, 255, 0),
        context={'value': True}
    )
    it = InputText()
    it.set_style('background', 'color', context={'value': 'wrong'})
    it.set_style('background-color', (255, 0, 0), context={'value': 'wrong'})
    return Window(
        win_sys,
        Box(board, cb, it, style={'size': ('100%', None)}),
        title=TITLE,
        style={'size': (600, None)}
    )
