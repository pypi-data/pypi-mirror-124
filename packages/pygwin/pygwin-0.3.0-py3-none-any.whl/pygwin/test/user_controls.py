#!/usr/bin/env python3

"""Document this method."""

import os

from pygwin import Label, Window, Box, Frame, IntSelect, Radiobox
from pygwin import Checkbox, RadioboxGroup, InputText, Table, StyleClass
from pygwin import Button, ItemSelect, HorizontalRule
from . import glob


TITLE = 'user controls'.title()


def get_window(win_sys):
    """user controls window"""
    def close(_):
        del StyleClass['window']
        del StyleClass['frame']
        del StyleClass['item_select']
        del StyleClass['int_select']
        del StyleClass['checkbox']
        del StyleClass['radiobox']
        del StyleClass['img_button']
        del StyleClass['input_text']
        StyleClass.load_default()

    StyleClass.load(os.path.join(glob.DATA_DIR, 'style.json'))

    tbl = Table()

    #  name input text
    ctrl = InputText(stc='input_text')
    tbl.new_row({0: Label('name'), 1: ctrl})
    tbl.new_row({1: HorizontalRule()})

    #  class radioboxes
    class_grp = RadioboxGroup()
    ctrl = {
        c: Box(
            Radiobox(
                class_grp, c, value=c == 'warrior', stc='radiobox',
                style={'valign': 'center'}
            ),
            Label(c, style={'valign': 'center'}),
            style={'orientation': 'horizontal'}
        )
        for c in ['warrior', 'wizard', 'thief']
    }
    tbl.new_row({0: Label('class'), 1: ctrl['warrior']})
    tbl.new_row({1: ctrl['wizard']})
    tbl.new_row({1: ctrl['thief']})
    tbl.new_row({1: HorizontalRule()})

    #  level int select
    tbl.new_row({0: Label('level'), 1: IntSelect(1, 10, stc='int_select')})
    tbl.new_row({1: HorizontalRule()})

    #  weapon select
    tbl.new_row({
        0: Label('weapon'),
        1: ItemSelect(
            {weapon: weapon for weapon in ['sword', 'axe', 'bow', 'staff']},
            stc=['item_select']
        )})
    tbl.new_row({1: HorizontalRule()})

    #  skill checkboxes
    skills = [
        'long sword', 'axe', 'bow', 'magic', 'dodge',
        'lockpicking', 'cartography', 'kung-fu', 'yoyo',
        'gaming'
    ]
    ctrl = {
        skill: Box(
            Checkbox(stc='checkbox', style={'valign': 'center'}),
            Label(skill, style={'valign': 'center'}),
            style={'orientation': 'horizontal'}
        )
        for skill in skills
    }
    tbl.new_row({
        0: Label('skills', style={'valign': 'top'}),
        1: Frame(
            Box(*ctrl.values()), stc=['frame'], style={'size': (300, 200)}
        )
    })

    #  button
    tbl.new_row(
        {0: Button('start', stc=['img_button'], style={'halign': 'center'})},
        colspan={0: 2}
    )

    result = Window(win_sys, tbl, title=TITLE, stc=['window'])
    result.add_processor('on-close', close)
    return result
