#!/usr/bin/env python3

"""Definition of class AnimationSequence."""

import typing as tp
from typing import TYPE_CHECKING

from .. import Animation
if TYPE_CHECKING:
    from .. import Window


class AnimationSequence(Animation):
    """An AnimationSequence can be used to chain several animations."""

    def __init__(
            self,
            sequence: tp.Sequence[Animation],
            win: 'Window'
    ):
        def handler(prog: int) -> tp.Optional[int]:
            if prog == -1:
                sequence[0].start(start_now=True)
                return 0
            if sequence[prog].stopped:
                prog += 1
                if prog >= len(sequence):
                    return None
                sequence[prog].start(start_now=True)
            return prog
        super().__init__(- 1, handler, win, period=1)
