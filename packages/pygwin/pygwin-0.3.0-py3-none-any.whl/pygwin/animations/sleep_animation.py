#!/usr/bin/env python3

"""Definition of class SleepAnimation."""

import typing as tp
from typing import TYPE_CHECKING
import pygame as pg

from .. import Animation
if TYPE_CHECKING:
    from .. import Window


class SleepAnimation(Animation):
    """A SleepAnimation only wait some time and terminate."""

    def __init__(self, win: 'Window', sleep_time: int):
        def sleep(_: bool) -> tp.Optional[bool]:
            if pg.time.get_ticks() - start_time <= sleep_time:
                return True
            return None
        start_time = pg.time.get_ticks()
        super().__init__(True, sleep, win, period=1)
