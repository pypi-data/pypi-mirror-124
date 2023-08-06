#!/usr/bin/env python3

"""Document this method."""

import webbrowser

from pygwin import Button, Grid, Panel, Box, HorizontalRule, Label, Window
from pygwin import Frame
from .all import all_tests
from . import glob


def main_panel(win_sys):
    """main panel of the test application"""
    def open_win(test):
        return lambda: test.get_window(win_sys).open()

    def show_credits():
        def open_url(url):
            def fun():
                webbrowser.open(url)
            return fun
        txt = 'Many thanks to the authors of the media used in this test app:'
        box = Box(Label(txt))
        for who, url in glob.CREDITS.items():
            box.pack(Label('- ' + who))
            box.pack(Label(url, link=open_url(url)))
        frame = Frame(box, style={'size': (600, 400)})
        Window(win_sys, frame, title='Credits').open()
        return True

    def quit_test():
        win_sys.set_closed(True)
        return True
    grid = Grid(style={'halign': 'center', 'grid-row-size': 5})
    for test in all_tests:
        grid.pack(Button(test.TITLE.title(), link=open_win(test)))
    quit_button = Button('Quit', link=quit_test)
    credits_button = Button('Credits', link=show_credits)
    box = Box(
        credits_button,
        quit_button,
        style={'orientation': 'horizontal', 'halign': 'center'}
    )
    box = Box(
        grid,
        HorizontalRule(style={'size': ('80%', 4)}),
        box,
        style={'halign': 'center'}
    )
    return Panel(win_sys, box, style={'size': ('100%', '100%')})
