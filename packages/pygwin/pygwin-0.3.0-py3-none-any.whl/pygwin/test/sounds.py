#!/usr/bin/env python3

"""Document this method."""

from pygwin import Label, Window
from pygwin import Checkbox, InputText, Table


TITLE = 'sounds'.title()


def get_window(win_sys):
    """sounds window"""
    click_check_box = 'click_checkbox.wav'
    key_input_text = 'key_inputtext.wav'
    over_link = 'over_link.wav'

    tbl = Table()
    lbl = Label('label')
    lbl.set_style('sound', over_link, context={'event': 'on-over'})
    tbl.new_row({0: lbl, 1: Label('move over the label to play sound')})
    cb = Checkbox()
    cb.set_style('sound', click_check_box, context={'event': 'on-activate'})
    it = InputText()
    it.set_style('sound', key_input_text, context={'event': 'on-key'})
    tbl.new_row({0: cb, 1: Label('check to play sound')})
    tbl.new_row({0: it, 1: Label('type key to play sound')})
    return Window(win_sys, tbl, title=TITLE)
