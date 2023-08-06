#!/usr/bin/env python3

"""Document this method."""

from pygwin import Label, Window, Box, Button, Frame, InputText


TITLE = 'frames'.title()


def get_window(win_sys):
    """frames window"""
    def push():
        if ip.value != '':
            board.pack(Label(ip.value))
        return True
    centered = {'halign': 'center'}
    ip = InputText(
        style={
            'input-text-placeholder': 'type something and validate...',
            'size': (400, None),
            **centered
        }
    )
    btn = Button('validate', link=push, style=centered)
    board = Box(
        'Enter text and validate.',
        'Text will be added below but the window won\'t grow.'
    )
    frame = Frame(board, style={'expand': True, 'size': ('100%', '100%')})
    box = Box(
        ip, btn, frame,
        style={'expand': True, 'size': ('100%', '100%')}
    )
    result = Window(win_sys, box, title=TITLE, style={'size': (600, 400)})
    return result
