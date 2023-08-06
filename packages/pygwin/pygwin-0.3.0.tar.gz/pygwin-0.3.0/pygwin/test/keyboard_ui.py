#!/usr/bin/env python3

"""Document this method."""

import random
import pygame as pg

from pygwin import Button, Grid, Window, Frame, Box, Image, Media, StyleClass
from pygwin import Label, Keys
from . import glob


TITLE = 'keyboard UI'.title()


def get_window(win_sys):  # pylint: disable=too-many-locals
    """keyboard ui window"""
    def close(_):
        del StyleClass['item-image']
        win_sys.enable_mouse()
        Keys.bind(pg.K_DOWN, None)
        Keys.bind(pg.K_UP, None)
        Keys.bind(pg.K_LEFT, None)
        Keys.bind(pg.K_RIGHT, None)

    def take_everything():
        to_move = list(grid_left.children)
        for item in to_move:
            grid_right.pack(item)
        return True

    def drop_everything():
        to_move = list(grid_right.children)
        for item in to_move:
            grid_left.pack(item)
        return True

    def link_image(item):
        def fun():
            def move(grid_from, grid_to):
                index = grid_from.children.index(item)
                if index == len(grid_from.children) - 1:
                    index = len(grid_from.children) - 2
                grid_from.remove_node(item)
                grid_to.pack(item)
            if item in grid_left:
                move(grid_left, grid_right)
            else:
                move(grid_right, grid_left)
            return True
        return fun

    win_sys.disable_mouse()

    Keys.bind(pg.K_DOWN, 'move-focus-south')
    Keys.bind(pg.K_UP, 'move-focus-north')
    Keys.bind(pg.K_LEFT, 'move-focus-west')
    Keys.bind(pg.K_RIGHT, 'move-focus-east')

    no_items = 100
    grid_left = Grid(style={'grid-row-size': 5})
    grid_right = Grid(style={'grid-row-size': 5})

    sc = StyleClass('item-image')
    ctx = {'status': 'focus'}
    sc.add('background', 'color', context=ctx)
    sc.add('background-color', (70, 130, 180), context=ctx)
    sc.add('corner', 8, context=ctx)
    items = [
        random.choice(list(glob.ITEMS))
        for _ in range(no_items)
    ]
    for item in items:
        img = Image(
            Media.get_image(glob.ITEMS[item][0], scale=(64, 64)),
            stc='item-image'
        )
        img.set_link(link_image(img))
        tooltip = Box(
            Label(glob.ITEMS[item][1]),
            Label(glob.ITEMS[item][2]),
            style=glob.TOOLTIP_STYLE
        )
        img.set_tooltip(tooltip)
        grid_left.pack(img)

    box_center = Box(
        Button('take everything', link=take_everything),
        Button('drop everything', link=drop_everything),
        Button('close', link=lambda: result.close()),  # pylint: disable=W0108
        style={'valign': 'center'}
    )
    main_box = Box(
        Frame(grid_left, style={'size': (440, 400)}),
        box_center,
        Frame(grid_right, style={'size': (440, 400)}),
        style={'orientation': 'horizontal'}
    )
    result = Window(win_sys, main_box, title=TITLE)
    result.add_processor('on-close', close)
    return result
