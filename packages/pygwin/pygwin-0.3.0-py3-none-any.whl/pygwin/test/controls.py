#!/usr/bin/env python3

"""Document this method."""

import string

from pygwin import Box, IntSelect, Label, Window, ItemSelect, Radiobox, Table
from pygwin import Checkbox, InputText, RadioboxGroup, Button, Range


TITLE = 'controls'.title()


def get_window(win_sys):
    """controls window"""
    def check():
        tbl = Table()
        for i, ip in enumerate(ips):
            tbl.new_row({
                0: Label(f'text written {i}'),
                1: Label(ip.value)
            })
        tbl.new_row({
            0: Label('checkbox checked'),
            1: Label('yes' if cb.value else 'no')
        })
        tbl.new_row(
            {0: Label('you are feeling'), 1: Label(str(grp.value))}
        )
        tbl.new_row(
            {0: Label('fruit selected'), 1: Label(str(fruits.value))}
        )
        tbl.new_row(
            {0: Label('your age'), 1: Label(str(ages.value))}
        )
        tbl.new_row(
            {0: Label('number chosen'), 1: Label(str(rng.value))}
        )
        Window(win_sys, tbl, title='Results').open()
        return True

    def disable():
        if btn_disable.node.text == 'disable controls':
            btn_disable.node.set_text('enable controls')
            tbl.disable()
        else:
            btn_disable.node.set_text('disable controls')
            tbl.enable()
        btn_disable.enable()
        return True
    tbl = Table()
    ips = [
        InputText(
            style={
                'input-text-placeholder': 'An input text'
            }
        ),
        InputText(
            style={
                'input-text-placeholder': 'A larger input text',
                'size': (300, None)
            }
        ),
        InputText(
            style={
                'input-text-placeholder': 'An input text occupying all space',
                'size': ('100%', None)
            }
        ),
        InputText(
            prompt='prompt> ',
            style={
                'input-text-placeholder': 'An input text with a prompt',
                'size': ('100%', None)
            }
        ),
        InputText(
            style={
                'input-text-placeholder': '4-digit',
                'input-text-max-size': 4,
                'input-text-allowed': string.digits,
                'size': (70, None)
            }
        )
    ]
    cb = Checkbox(value=True)
    grp = RadioboxGroup()
    fruits = ItemSelect({fruit: fruit for fruit in [
        'apple', 'banana', 'chocolate', 'pear']})
    ages = IntSelect(0, 100, init=20, steps=[1, 5])
    btn_check = Button('check data', link=check)
    btn_disable = Button('disable controls', link=disable)
    rng = Range(1, 10_000)
    tbl.new_row(
        {0: Label('to navigate between controls: TAB or SHIFT+TAB')},
        colspan={0: 2}
    )
    for ip in ips:
        tbl.new_row({0: ip}, colspan={0: 2})
    tbl.new_row({0: cb, 1: Label('a checkbox', label_for=cb)})
    tbl.new_row(
        {0: Label('how are you?')},
        colspan={0: 2}
    )
    for how in ['fine', 'ok', 'not great']:
        cb = Radiobox(grp, how)
        tbl.new_row({0: cb, 1: Label(how, label_for=cb)})
    tbl.new_row(
        {0: Label('select a fruit (mousewheel can be used)')},
        colspan={0: 2}
    )
    tbl.new_row(
        {0: fruits},
        colspan={0: 2}
    )
    tbl.new_row(
        {0: Label('what\'s your age? (mousewheel can be used)')},
        colspan={0: 2}
    )
    tbl.new_row(
        {0: ages},
        colspan={0: 2}
    )
    tbl.new_row(
        {0: Label(
            'choose a number between 1 and 10000 (mousewheel can be used)'
        )},
        colspan={0: 2}
    )
    tbl.new_row(
        {0: rng},
        colspan={0: 2}
    )
    tbl.new_row(
        {0: Box(
            btn_disable, btn_check,
            style={
                'halign': 'center',
                'orientation': 'horizontal'
            })
         },
        colspan={0: 2}
    )
    return Window(win_sys, tbl, title=TITLE)
