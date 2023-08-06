#!/usr/bin/env python3

"""Definition of class Style."""

from typing import Callable, Set, Type, cast
import pygame as pg

from . import types
from .runtime_checked_dict import mk_runtime_checked_dict


INHERITED: Set[types.style_attr_t] = {
    'font',
    'font-size'
}

DEFAULT: types.style_t = {
    'background-color': (0, 0, 0),
    'border-color': (100, 100, 100),
    'border-width': 0,
    'color': (255, 255, 255),
    'expand': False,
    'font': pg.font.get_default_font(),
    'font-size': 16,
    'frame-bar-background-color': (100, 100, 100, 150),
    'frame-bar-color': (150, 150, 150, 150),
    'frame-bar-corner': 4,
    'frame-bar-width': 8,
    'gauge-label-format': '{value} / {max}',
    'halign': 'left',
    'hspacing': 10,
    'input-text-allowed': r'A-Za-z\d \_\-\'\"\.',
    'input-text-max-size': 20,
    'orientation': 'vertical',
    'padding': 0,
    'range-acceleration': 10,
    'range-bar-color': (150, 150, 150, 150),
    'range-bar-corner': 0,
    'range-bar-size': (200, 4),
    'range-bullet-color': (150, 150, 150, 150),
    'range-bullet-radius': 6,
    'range-label-distance': 6,
    'range-label-format': '{value}',
    'range-step': 1,
    'select-cyclic': False,
    'select-hide-links': True,
    'select-next-label': '&gt;&gt;',
    'select-prev-label': '&lt;&lt;',
    'select-wheel-units': 1,
    'text-board-push-dest': 'bottom',
    'underline': False,
    'valign': 'top',
    'vspacing': 10
}

Style: Callable[[types.style_t], types.style_t] = mk_runtime_checked_dict(
    cast(Type[types.style_t], types.style_t),
    default=DEFAULT,
    fail_method='logging'
)
