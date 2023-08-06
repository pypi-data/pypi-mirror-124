#!/usr/bin/env python3

"""export all test packages here in list all_tests.  each package in
all_tests defines:

* `get_window(win_sys: WindowSystem) -> None`: creates a test window
  in system win_sys

* `TITLE: str`: title of the test window
"""

from . import absolute_positioning
from . import animations
from . import basic
from . import contextual_styles
from . import contextual_menus
from . import controls
from . import cursor
from . import fonts
from . import frames
from . import grids
from . import keyboard_ui
from . import maximised
from . import maximised_menu
from . import menus
from . import sounds
from . import tables
from . import text_boards
from . import tooltips
from . import user_controls


all_tests = [
    basic,
    tables,
    controls,
    fonts,
    sounds,
    cursor,
    frames,
    menus,
    tooltips,
    text_boards,
    maximised,
    maximised_menu,
    contextual_menus,
    animations,
    absolute_positioning,
    user_controls,
    contextual_styles,
    keyboard_ui,
    grids
]
