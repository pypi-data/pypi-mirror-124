#!/usr/bin/env python3

"""Definition of global variables and helper functions for the test package."""

import os
import pkg_resources

from pygwin import Label, Gauge, Table, TextBoard, Empty


def monster_table(m):
    """Create and return a table containing monster attributes."""
    result = Table()
    data = MONSTERS[m]
    result.new_row({
        0: Label('name'),
        1: Label(m)
    })
    result.new_row({
        0: Label('health'),
        1: Gauge(0, int(data[2]), int(data[1]))
    })
    result.new_row({
        0: Label('magic'),
        1: Gauge(0, int(data[4]), int(data[3]))
    })
    return result


def lorem_ipsum_textboard():
    """Generate a TextBoard containing lorem_ipsum.txt of the MEDIA_DIR."""
    result = TextBoard(style={'size': ('100%', None)})
    path = os.path.join(MEDIA_DIR, 'lorem_ipsum.txt')
    with open(path, encoding="utf8") as f:
        for paragraph in f.read().split('\n\n'):
            result.push_text(paragraph)
            result.pack(Empty())
    return result


FPS = 50
MEDIA_DIR = pkg_resources.resource_filename(
    'pygwin.test', os.path.join('data', 'media')
)
DATA_DIR = pkg_resources.resource_filename(
    'pygwin.test', 'data'
)
MONSTERS = {
    'orc': ('orc.png', '10', '20', '0', '10'),
    'elf': ('elf.png', '5', '15', '30', '50'),
    'dragon': ('dragon.png', '70', '100', '50', '200')
}
ITEMS = {
    item: (item + '.png', name, descr)
    for item, name, descr in [
        ('axe', 'axe', 'damage: 1D12'),
        ('club', 'club', 'damage: 1D6'),
        ('dagger', 'dagger', 'damage: 1D4'),
        ('flail', 'flail', 'damage: 1D8'),
        ('hammer', 'hammer', 'damage: 1D8'),
        ('long-sword', 'long sword', 'damage: 1D10'),
        ('mace', 'mace', 'damage: 1D8'),
        ('potion-blue', 'magic potion', 'MP: 2D10'),
        ('potion-clear', 'cure paralysis potion', 'success chance: 90%'),
        ('potion-white', 'cure disease potion', 'success chance: 80%')
    ]
}
TOOLTIP_STYLE = {
    'corner': 8,
    'border': 'color',
    'border-width': 4,
    'padding': 10,
    'orientation': 'vertical',
    'background': 'color',
    'background-color': (20, 20, 100),
    'pos-list': [
        ('relative', ('right', 'bottom'), (0, 0)),
        ('relative', ('right', 'top'), (0, 0)),
        ('relative', ('left', 'bottom'), (0, 0)),
        ('relative', ('left', 'top'), (0, 0))
    ]
}

CREDITS = {
    'Daniel Lyons (for the "ltinternet" font)':
    'https://www.dafont.com/lt-internet.font',
    'team of dungeon crawl stop soup for their monster images':
    'https://crawl.develz.org/',
    'Lamoot for its RPG GUI contruction kit':
    'https://opengameart.org/content/rpg-gui-construction-kit-v10',
    'Kenney for its RPG GUI contruction kit':
    'https://www.kenney.nl',
    'rhodesmas (for the "click on checkbox" sound)':
    'https://freesound.org/people/rhodesmas/sounds/380291/',
    'gamedevc (for the "over link" sound)':
    'https://freesound.org/people/GameDevC/sounds/422830/',
    'complex_waveform (for the "key" sound)':
    'https://freesound.org/people/complex_waveform/sounds/213148/',
    'FontBlast Design (for the "monaco" font)':
    'https://www.dafont.com/monaco.font',
    'Dieter Steffmann (for the "cardinal" font)':
    'https://www.1001freefonts.com/cardinal.font',
    'James Grieshaber (for the "metamorphous" font)':
    'https://www.1001freefonts.com/metamorphous.font',
    'Dharma Type (for the "bebas-neue" font)':
    'https://www.dafont.com/fr/bebas-neue.font'
}
