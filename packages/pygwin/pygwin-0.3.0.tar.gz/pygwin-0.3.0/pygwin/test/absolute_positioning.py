#!/usr/bin/env python3

"""Document this method."""

import random

from pygwin import Animation, Media, Window, Box, Button, Pos, Image
from . import glob


TITLE = 'absolute positioning'.title()


def get_window(win_sys):
    """absolute positioning window"""
    def handler(directions):
        size = win.size
        result = []
        for i, img in enumerate(imgs):
            direction = directions[i]
            pos = img.pos
            if pos is None:  # pos is None <=> window closed
                return None
            pos = Pos.sum(pos, direction)
            style_pos = ('absolute', ('left', 'top'), (pos[0], pos[1]))
            img.set_style('pos', style_pos)
            next_pos = Pos.sum(pos, direction)
            if next_pos[1] + img_size > size[1] or next_pos[1] < 0:
                direction = (direction[0], -direction[1])
            if next_pos[0] + img_size > size[0] or next_pos[0] < 0:
                direction = (-direction[0], direction[1])
            result.append(direction)
        return result

    def start_or_stop():
        if btn.node.text == 'stop':
            anim.pause()
            btn.node.set_text('start')
        else:
            anim.start()
            btn.node.set_text('stop')

    def random_pos():
        return (
            'absolute',
            ('left', 'top'),
            (random.randint(0, 400 - img_size),
             random.randint(0, 400 - img_size))
        )
    btn = Button(
        'start',
        link=start_or_stop,
        style={'expand': True, 'halign': 'center', 'valign': 'center'}
    )
    box = Box(btn, style={'expand': True, 'size': ('100%', '100%')})
    win = Window(win_sys, box, title=TITLE, style={'size': (600, 400)})
    result = win
    img_size = 128
    directions = []
    imgs = [
        Image(
            Media.get_image(mdata[0], scale=(img_size, img_size)),
            style={'pos': random_pos()}
        )
        for m, mdata in glob.MONSTERS.items()
    ]
    for img in imgs:
        directions.append((random.choice([5, -5]), random.choice([5, -5])))
        result.add_floating_node(img)
    anim = Animation(directions, handler, result)
    return result
