#!/usr/bin/env python3

"""Definition of class StyleClass."""

from __future__ import annotations
from typing import Dict, Tuple, Iterator, Any, Optional, List, Pattern
from typing import Callable, Sequence, cast, TYPE_CHECKING
import re
import logging
import os
import pkg_resources

from .style import Style
from . import types, SubscriptableType, Util, Media
if TYPE_CHECKING:
    from . import Node


class StyleClass(metaclass=SubscriptableType):
    """StyleClass objects are similar to HTML classes.

    A StyleClass is identified by a name.  It consists of a set of
    styles that can be context dependent (e.g., depend on the value or
    the status of the node).  A StyleClass can then be applied to nodes.

    >>> sc = StyleClass('my-class')
    >>> _ = sc.add('size', (100, 100))
    >>> _ = sc.add('color', (255, 0, 0))
    >>> _ = sc.add('border', 'color')
    >>> _ = sc.add('border-color', (255, 255, 0))
    >>> _ = sc.add('color', (0, 255, 0), context={'status': 'overed'})
    >>> _ = sc.add('sound', 'test.wav', context={'event': 'on-over'})
    >>> _ = sc.add('color', (255, 0, 0), context={'value': 'x'})
    >>> print(sc)
    my-class:status=overed {
       color: (0, 255, 0)
    }
    my-class:value=x {
       color: (255, 0, 0)
    }
    my-class {
       size: (100, 100)
       color: (255, 0, 0)
       border: color
       border-color: (255, 255, 0)
    }
    my-class:event=on-over {
       sound: test.wav
    }

    """

    __RE_CLS_NAME = re.compile(r'(\w+)(:.+)?')

    ctx_t = Sequence[Tuple[types.sc_context_type_t, Any]]
    def_t = Tuple[ctx_t, List[types.node_pred_t], types.style_t, int]

    def __init__(
            self,
            name: Any,
            register: bool = True,
            style: Optional[types.style_t] = None
    ):
        """Initialize self with the given name and an empty set of styles.

        If register == True, the style class is inserted in StyleClass
        and can then be given to any Node.

        """
        self.__name = name
        self.__styles: List[StyleClass.def_t] = list()
        self.__events: Dict[types.event_t, List[StyleClass.def_t]] = dict()
        if register:
            StyleClass[name] = self
        if style is not None:
            self.__styles.append(
                ((), [lambda node: True], style, 0)
            )

    @property
    def name(self) -> Any:
        """Get the name of the class."""
        return self.__name

    def __str__(self) -> str:
        def pred_to_str(preds: StyleClass.ctx_t) -> str:
            if preds == ():
                return ''
            return ':' + ','.join(var + '=' + str(val) for var, val in preds)
        return '\n'.join([
            str(self.name) + pred_to_str(context) + ' {\n' +
            '\n'.join(
                ['   ' + att + ': ' + str(val) for att, val in style.items()]
            ) + '\n}'
            for context, _, style, _ in self.__styles +
            [item for li in self.__events.values() for item in li]
        ])

    @classmethod
    def __iter_list(
            cls,
            li: List[StyleClass.def_t]
    ) -> Iterator[Tuple[List[types.node_pred_t], types.style_t]]:
        for _, check, style, _ in li:
            yield check, style

    def _iter_events(
            self,
            event: types.event_t
    ) -> Iterator[Tuple[List[types.node_pred_t], types.style_t]]:
        yield from StyleClass.__iter_list(self.__events.get(event, []))

    def _iter_styles(
            self
    ) -> Iterator[Tuple[List[types.node_pred_t], types.style_t]]:
        yield from StyleClass.__iter_list(self.__styles)

    def _get_checked_status(
            self
    ) -> Iterator[Tuple[types.style_t, types.status_t]]:
        for context, _, style, _ in self.__styles:
            status = next(
                (val for var, val in context if var == 'status'), None
            )
            if status is not None:
                yield style, status

    def does_check_value(self) -> bool:
        """Check if self has value dependent styles."""
        for context, _, _, _ in self.__styles:
            value = next(
                (val for var, val in context if var == 'value'), None
            )
            if value is not None:
                return True
        return False

    @classmethod
    def __get_funs_and_priority(
            cls,
            context: types.sc_context_t
    ) -> Optional[Tuple[Tuple[Tuple[types.sc_context_type_t, Any], ...],
                        List[types.node_pred_t], int]]:
        funs = []
        prio = 0
        filtered_context = list()
        for var, val in context.items():
            fun = None
            append_context = True
            if var == 'event':
                pass
            elif var == 'value':
                def get_check_value(val: Any) -> types.node_pred_t:
                    def fun(node: 'Node') -> bool:
                        return node.has_value() and node.value == val
                    return fun
                fun = get_check_value(val)
                prio += 100
            elif var == 'parentclass':
                def get_check_type(name: str) -> types.node_pred_t:
                    def fun(node: 'Node') -> bool:
                        parent = node.parent
                        if parent is None:
                            return False
                        return any(c.name == name for c in parent.stc)
                    return fun
                fun = get_check_type(val)
                prio += 10
            elif var == 'class':
                def get_check_class(name: str) -> types.node_pred_t:
                    def fun(node: 'Node') -> bool:
                        return any(c.name == name for c in node.stc)
                    return fun
                fun = get_check_class(val)
                prio += 10
            elif var == 'status':
                append_context = val != 'base'
                status = {
                    'base': (
                        None, 0
                    ),
                    'selected': (
                        lambda n: n.is_selected(), 1000
                    ),
                    'overed': (
                        lambda n: n.is_overed(), 2000
                    ),
                    'focus': (
                        lambda n: n.has_focus(), 3000
                    ),
                    'clicked': (
                        lambda n: (n.is_clicked() and n.is_overed()), 4000
                    ),
                    'disabled': (
                        lambda n: n.is_disabled(), 5000
                    )
                }
                if val not in status:
                    logging.warning('undefined status: "%s"', val)
                    return None
                fun, to_add = status[val]
                prio += to_add
            else:
                logging.warning('undefined attribute: "%s"', var)
                return None
            if fun is not None:
                funs.append(fun)
            if append_context:
                filtered_context.append((var, val))
        filtered_context_tuple = tuple(sorted(
            filtered_context, key=lambda var_val: var_val[0]
        ))
        return filtered_context_tuple, funs, prio

    def add(
            self,
            attr: types.style_attr_t,
            value: Any,
            context: Optional[types.sc_context_t] = None,
            update: bool = True
    ) -> bool:
        """Add set a style attribute to self.

        See help(StyleClass) for examples.

        If update is True, the current style associated to the
        context is updated.  Else the method as no effect.

        Return True if the style class has been updated, False
        otherwise.

        """
        if context is None:
            context = dict()
        event = context.get('event')
        if event is not None:
            if event not in self.__events:
                self.__events[event] = list()
            li = self.__events[event]
        else:
            li = self.__styles

        funs_and_priority = StyleClass.__get_funs_and_priority(context)
        if funs_and_priority is None:
            return False
        tuple_context, funs, prio = funs_and_priority

        #  check if the context already exists in the class
        cond_style = next((st for st in li if st[0] == tuple_context), None)
        result = False
        if cond_style is not None:
            if update or attr not in cond_style[2]:
                cond_style[2][attr] = value
                result = True
        else:
            style = Style({attr: value})  # type: ignore
            li.append((tuple_context, funs, style, prio))
            li.sort(key=lambda style: - style[3])
            result = True
        return result

    @classmethod
    def load(cls, json_file: str) -> None:
        """Load all style classes from file json_file."""
        def parse_context(
                ctx: str
        ) -> Tuple[bool, Optional[types.sc_context_t]]:
            result: types.sc_context_t = dict()
            for cond in ctx[1:].split(','):
                try:
                    var, val = tuple(x.strip() for x in cond.split('='))
                except ValueError:
                    logging.warning('cannot parse context "%s"', cond)
                    return False, None
                if var == 'value':
                    x = StyleClass.parse_constant(val)
                    if x is None:
                        logging.warning('cannot parse constant "%s"', val)
                        return False, None
                    val = x
                elif var not in types.all_sc_contexts:
                    logging.warning('invalid context type "%s"', var)
                    return False, None
                result[cast(types.sc_context_type_t, var)] = val
            return True, result
        data = Util.load_json_file(json_file)
        if data is None:
            return
        loaded = set()
        for name, style in data.items():
            match = StyleClass.__RE_CLS_NAME.fullmatch(name)
            if match is None:
                logging.warning('invalid style class name: "%s"', name)
                continue
            grps = match.groups()
            if grps[1] is None:
                context: Optional[types.sc_context_t] = dict()
            else:
                style_ok, context = parse_context(grps[1])
                if not style_ok:
                    continue
            name = grps[0]
            if name not in StyleClass:
                StyleClass(name)
            elif name not in loaded:
                del StyleClass[name]
                StyleClass(name)
            c: StyleClass = StyleClass[name]
            for attr, value in style.items():
                c.add(attr, value, context=context)
            loaded.add(name)

    __parse_constant_pred: List[Tuple[Pattern[str], Callable[[Any], Any]]] = [
        (re.compile(r'(true)', re.IGNORECASE), lambda _: True),
        (re.compile(r'(false)', re.IGNORECASE), lambda _: False),
        (re.compile(r'\'(.*)\''), str),
        (re.compile(r'([0-9]+)'), int),
        (re.compile(r'([0-9]+\.[0-9]+)'), float)
    ]

    @classmethod
    def parse_constant(cls, constant: str) -> Any:
        """Parse and return a constant str, or None in case of parse error.

        >>> StyleClass.parse_constant('this is not valid')
        >>> StyleClass.parse_constant('TrUe')
        True
        >>> StyleClass.parse_constant('fAlSe')
        False
        >>> StyleClass.parse_constant('123')
        123
        >>> StyleClass.parse_constant('123.132')
        123.132
        >>> StyleClass.parse_constant("'this is a string'")
        'this is a string'

        """
        for reg, get_val in StyleClass.__parse_constant_pred:
            match = reg.fullmatch(constant)
            if match is not None:
                return get_val(match.groups()[0])
        return None

    @classmethod
    def load_default(cls) -> None:
        """Load style classes and fonts from the package data directory."""
        data_dir = pkg_resources.resource_filename('pygwin', 'data')

        #  load fonts
        json = os.path.join(data_dir, 'fonts.json')
        Media.load_fonts(json)

        #  load default style
        json = os.path.join(data_dir, 'default-style.json')
        StyleClass.load(json)
