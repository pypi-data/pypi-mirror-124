#!/usr/bin/env python3

"""Definition of class SubscriptableType."""

from typing import Any, Iterator, Dict

from . import Util


class SubscriptableType(type):
    """A SubscriptableType class can be accessed like dictionaries.

    >>> class Constants(metaclass=SubscriptableType):
    ...    ALL = {
    ...       'i': 0,
    ...       'j': True,
    ...       'k': 'ok'
    ...    }
    >>> Constants['k']
    'ok'
    >>> Constants['j'] = 2
    >>> Constants['j']
    2
    >>> for cst in Constants:
    ...    cst
    'i'
    'j'
    'k'

    """

    def __init__(cls, name: Any, bases: Any, dic: Any):
        """Initialise the SubscriptableType cls.

        cls.ALL is initialised if cls does not have such an
        attribute.

        """
        type.__init__(cls, name, bases, dic)
        if not hasattr(cls, 'ALL'):
            cls.ALL: Dict[Any, Any] = dict()

    def __getitem__(cls, i: Any) -> Any:
        return cls.ALL[i]

    def __setitem__(cls, i: Any, val: Any) -> None:
        cls.ALL[i] = val

    def __delitem__(cls, i: Any) -> None:
        del cls.ALL[i]

    def __iter__(cls) -> Iterator[Any]:
        yield from cls.ALL

    def save(cls, json_file: str) -> None:
        """Save cls.ALL in json file json_file."""
        Util.save_json_file(json_file, cls.ALL)

    def load(cls, json_file: str) -> None:
        """Load cls.ALL from file json_file.

        The method has no effect if json_file does not contain a
        dictionnary.

        """
        data = Util.load_json_file(json_file)
        if data is not None:
            for key, val in data.items():
                if key in cls.ALL:
                    cls.ALL[key] = type(cls.ALL[key])(val)
