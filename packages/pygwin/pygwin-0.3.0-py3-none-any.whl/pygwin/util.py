#!/usr/bin/env python3

"""Definition of class Util."""

import re
import logging
import json
from typing import Tuple, Iterator, List, Optional, Dict, Any
import xml.etree.ElementTree as ET
import pygame as pg

from . import types


class Util:
    """Class Util defines a number of helper functions."""

    #  constants taken from pygame
    MOUSEBUTTON_LEFT: int = 1
    MOUSEBUTTON_RIGHT: int = 3
    MOUSEBUTTON_WHEEL_DOWN: int = 4
    MOUSEBUTTON_WHEEL_UP: int = 5

    RE_RGB: re.Pattern[str] = re.compile(
        r'\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*'
    )

    @classmethod
    def in_range(
            cls,
            value: int,
            bounds: types.pos_t
    ) -> int:
        """Return value if it is in bounds, or the bound it is closer to.

        >>> Util.in_range(0, (0, 10))
        0
        >>> Util.in_range(0, (4, 10))
        4
        >>> Util.in_range(12, (4, 10))
        10

        """
        min_val, max_val = bounds
        result = value
        if min_val is not None:
            result = max(result, min_val)
        if max_val is not None:
            result = min(result, max_val)
        return result

    @classmethod
    def split_lines(
            cls,
            text: str,
            font: pg.font.Font,
            color: types.color_t,
            width: int = 0
    ) -> Iterator[pg.surface.Surface]:
        """Explode a text in several lines that do not exceed width pixels.

        Given a text string, split in several lines such that each
        line, when rendered with font, does not exceed the given
        width.  Yields the list of pygame surfaces containing these
        lines.  The text string may contain the following tags: <color
        rgb="XX,YY, ZZ">.

        """
        def traverse(
                elem: ET.Element,
                style: Dict[str, Any]
        ) -> Iterator[Tuple[str, Dict[str, Any]]]:
            yield from split(elem.text, style)
            for child in elem:
                child_style = dict(style)
                if child.tag == 'color':
                    try:
                        match = Util.RE_RGB.search(child.attrib['rgb'])
                    except KeyError as e:
                        raise ValueError(
                            'rgb attribute is expected for color tag'
                        ) from e
                    if match:
                        child_style['color'] = tuple(map(int, match.groups()))
                    else:
                        rgb = child.attrib['rgb']
                        raise ValueError(f'cannot parse rgb color {rgb}')
                else:
                    raise ValueError(f'undefined tag: {child.tag}')
                yield from traverse(child, child_style)
                yield from split(child.tail, style)

        def split(
                text: Optional[str],
                style: Dict[str, Any]
        ) -> Iterator[Tuple[str, Dict[str, Any]]]:
            if text is not None:
                yield text, style

        def style_color(style: Dict[str, Any]) -> Any:
            return style.get('color', color)

        def yield_surface() -> Iterator[pg.surface.Surface]:
            size = (
                sum(map(lambda s: s.get_width(), surfaces)),
                max(map(lambda s: s.get_height(), surfaces), default=0)
            )
            if size[0] <= 0:
                surface = pg.Surface((0, 0)).convert_alpha()
            else:
                surface = pg.Surface(size).convert_alpha()
                surface.fill((0, 0, 0, 0))
                w = 0
                for surf in surfaces:
                    surface.blit(surf, (w, 0))
                    w += surf.get_width()
            yield surface
        text = str(text).replace('\n', ' ')
        line = ''
        surfaces: List[pg.surface.Surface] = list()
        for block, style in traverse(
                ET.fromstring('<root>' + text + '</root>'), {}
        ):
            first = True
            for word in block.split(' '):
                if not first:
                    word = ' ' + word
                if font.size(line)[0] + font.size(word)[0] > width > 0:
                    yield from yield_surface()
                    line = ''
                    if not first:
                        word = word[1:]
                    surfaces = list()
                surfaces.append(font.render(word, True, style_color(style)))
                line += word
                first = False
        yield from yield_surface()

    @classmethod
    def save_json_file(cls, json_file: str, data: Any) -> None:
        """Json-dump data in json_file."""
        try:
            with open(json_file, 'w', encoding="utf8") as fd:
                try:
                    fd.write(json.dumps(data, separators=(',', ':')))
                except TypeError:
                    logging.warning('cannot encode data: %s', data)
        except (PermissionError, FileNotFoundError):
            logging.warning('cannot open file: %s', json_file)

    @classmethod
    def load_json_file(cls, json_file: str) -> Optional[Any]:
        """Open a json file, and load and return its content.

        Return None if the json is invalid or the file does not
        exist.

        """
        try:
            with open(json_file, 'r', encoding="utf8") as fd:
                try:
                    result = json.loads(fd.read())
                    logging.info(
                        'successfully loaded json file: %s', json_file
                    )
                    return result
                except json.decoder.JSONDecodeError:
                    logging.warning('invalid json file: %s', json_file)
                    return None
        except (PermissionError, FileNotFoundError):
            logging.warning('cannot open file: %s', json_file)
            return None
