#!/usr/bin/env python3

"""Provides mk_runtime_checked_dict to create runtime checked TypedDict."""

import typing as tp
import collections
import logging

T = tp.TypeVar('T')  # pylint: disable=invalid-name


def mk_runtime_checked_dict(  # pylint: disable=too-many-statements
        typed_dict: tp.Type[T],
        default: tp.Optional[tp.Mapping[tp.Any, tp.Any]] = None,
        type_check: bool = True,
        fail_method: tp.Literal['exception', 'logging'] = 'exception',
        log_level: int = logging.WARNING
) -> tp.Callable[[T], T]:
    """Return a function that creates a TypedDict with runtime checks.

    >>> import typing as tp
    >>> td = tp.TypedDict('td', {
    ...    'x': int,
    ...    'y': tp.Literal[0, 1, 2],
    ...    'z': tp.Union[str, int]
    ... }, total=False)
    >>> td_dict = mk_runtime_checked_dict(tp.cast(tp.Type[td], td), {'y': 2})
    >>> d = td_dict({'y': 132})  #  value of 'y' must be in {0, 1, 2}
    Traceback (most recent call last):
    ValueError: ...
    >>> d = td_dict({})
    >>> d['x'] = 'test'  #  value of 'x' key must be an int
    Traceback (most recent call last):
    ValueError: ...
    >>> d['w']  # 'w' is not a valid key
    Traceback (most recent call last):
    KeyError: ...
    >>> d['z'] = 'test' # OK
    >>> d['y']  # check default value
    2

    """
    class RuntimeCheckedDict(collections.UserDict[tp.Any, tp.Any]):
        """Provides dictionaries of type typed_dict with runtime checks."""

        c_keys = set(tp.get_type_hints(typed_dict).keys())
        c_default = dict(default if default is not None else ())
        c_types = dict(tp.get_type_hints(typed_dict))

        def __setitem__(self, key: tp.Any, val: tp.Any) -> None:
            if not RuntimeCheckedDict.__check_key(key):
                return
            if val is not None and type_check:
                try:
                    RuntimeCheckedDict.__check(key, val)
                except ValueError as e:
                    if fail_method == 'logging':
                        logging.log(log_level, e.args[0])
                    else:
                        raise e
            super().__setitem__(key, val)

        def __getitem__(self, key: tp.Any) -> tp.Any:
            if not RuntimeCheckedDict.__check_key(key):
                return None
            if key not in self and key in RuntimeCheckedDict.c_default:
                return RuntimeCheckedDict.c_default.get(key)
            return super().__getitem__(key)

        @classmethod
        def __check_key(cls, key: tp.Any) -> bool:
            if key in RuntimeCheckedDict.c_keys:
                return True
            msg = f'invalid key: {key}'
            if fail_method == 'exception':
                raise KeyError(msg)
            if fail_method == 'logging':
                logging.log(log_level, msg)
            return False

        @classmethod
        def __check(cls, key: tp.Any, val: tp.Any) -> None:
            def c(cond: bool) -> None:
                if not cond:
                    raise ValueError(
                        f'invalid value for key {key}: {val}'
                    )

            def check_literal(val: tp.Any, typedef: tp.Any) -> None:
                c(val in tp.get_args(typedef))

            def check_union(val: tp.Any, typedef: tp.Any) -> None:
                for t in tp.get_args(typedef):
                    try:
                        rec(val, t)
                        return
                    except ValueError:
                        pass
                c(False)

            def check_tuple(val: tp.Any, typedef: tp.Any) -> None:
                try:
                    args = tp.get_args(typedef)
                    c(len(args) == len(val))
                    for arg, tuple_val in zip(args, val):
                        rec(tuple_val, arg)
                except TypeError:
                    c(False)

            def check_list(val: tp.Any, typedef: tp.Any) -> None:
                typ = tp.get_origin(typedef)
                assert isinstance(typ, type)
                c(isinstance(val, typ))
                if tp.get_args(typedef)[0] is not None:
                    for item in val:
                        rec(item, tp.get_args(typedef)[0])

            def rec(val: tp.Any, typedef: tp.Any) -> None:
                if isinstance(typedef, type):
                    c(isinstance(val, typedef))
                else:
                    checker = {
                        tp.Literal: check_literal,
                        tuple: check_tuple,
                        tp.Union: check_union,
                        list: check_list,
                        set: check_list
                    }
                    try:
                        checker[tp.get_origin(typedef)](val, typedef)
                    except KeyError:
                        pass
            typedef = RuntimeCheckedDict.c_types[key]
            if typedef is not None and val is not None:
                rec(val, typedef)

    return lambda x: tp.cast(
        T, RuntimeCheckedDict(tp.cast(tp.Mapping[tp.Any, tp.Any], x))
    )
