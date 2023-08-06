#!/usr/bin/env python3

"""Definition of class Keys."""

from typing import Dict, Tuple, Optional, Sequence
import logging

from . import types


class Keys:
    """The Keys class provides mechanisms to associate keys to actions.

    For example, we can associate the escape key to the action of
    closing the top window of the window system. A number of
    predefined action are available: closing the top window, moving
    the focus...  (see types.key_action_t). It is also possible to
    define new action as functions to call when specific keys are
    pressed (the 'user-defined' action).

    For instance this associates the RETURN key to the action of
    activating the node that now has the focus:
    >>> import pygame as pg
    >>> Keys.bind(pg.K_RETURN, 'activate')

    This associate the F1 key to the action of calling method
    print_help:
    >>> def print_help():
    ...    print('typing F1 prints this help message')
    >>> Keys.bind(pg.K_F1, 'user-defined', fun=print_help)

    This associate Ctrl+C to the action of closing the top window:
    >>> Keys.bind(pg.K_F1, 'close-window', pressed=[pg.K_LCTRL])

    """

    __MAP: Dict[
        int,
        Dict[Sequence[int],
             Tuple[types.key_action_t,
                   Optional[types.user_key_proc_t]]]] = dict()

    @classmethod
    def bind(
            cls,
            key: int,
            action: Optional[types.key_action_t],
            pressed: Optional[Sequence[int]] = None,
            fun: Optional[types.user_key_proc_t] = None
    ) -> None:
        """Associate an action to a key.

        The method has no effect if action is not in
        types.all_keys_actions.  If not None, pressed is the list of
        pygame keys that must be already pressed when key is pressed
        for the action to be triggered.  If action == 'user-defined',
        fun must not be None and is the function associated to the
        action.

        """
        if action is not None and action not in types.all_key_actions:
            logging.warning('undefined action: %s', action)
            return
        p: Tuple[int, ...]
        if pressed is None:
            p = tuple()
        else:
            p = tuple(sorted(pressed))
        if action is None:
            if key in Keys.__MAP:
                if p in Keys.__MAP[key]:
                    del Keys.__MAP[key][p]
                if len(Keys.__MAP[key]) == 0:
                    del Keys.__MAP[key]
        else:
            if key not in Keys.__MAP:
                Keys.__MAP[key] = dict()
            Keys.__MAP[key][p] = action, fun

    @classmethod
    def action(
            cls,
            key: int,
            pressed: Sequence[bool]
    ) -> Optional[Tuple[types.key_action_t, Optional[types.user_key_proc_t]]]:
        """Get an action associated to a key.

        pressed is an array of booleans specifying which keys are
        currently pressed, as returned e.g., by pg.key.get_pressed().
        Return None if no action must be triggered or a couple (act,
        fun) with act the action to be triggered and, if act ==
        'user-defined', fun is the user function associated to the
        key.

        """
        acts = Keys.__MAP.get(key)
        if acts is not None:
            best: Optional[Sequence[int]] = None
            for keys in acts:
                if (
                        all(pressed[key] for key in keys) and
                        (best is None or len(best) < len(keys))
                ):
                    best = keys
            if best is not None:
                return acts[best]
        return None
