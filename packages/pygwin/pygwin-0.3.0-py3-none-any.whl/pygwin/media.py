#!/usr/bin/env python3

"""Definition of class Media."""

import os
import logging
import functools
from typing import Union, Optional, Any, Dict
import pkg_resources
import pygame as pg

from pygwin import Util, types
from pygwin.style import DEFAULT


class Media:
    """Media provides helper methods to handle pygame media."""

    PATH = [
        os.path.curdir,
        os.path.join(
            pkg_resources.resource_filename('pygwin', 'data'), 'media'
        )
    ]

    FONTS: Dict[str, Any] = {
    }

    @classmethod
    @functools.lru_cache(maxsize=10000)
    def get(
            cls,
            mtype: types.media_t,
            file_path: Optional[str],
            **kwargs: Any
    ) -> Optional[Union[pg.surface.Surface, pg.font.Font, pg.mixer.Sound]]:
        """Load and return a media from the given file path.

        mtype must be in ['image', 'font', 'sound'] or otherwise None
        is returned.  result of the method is cached.  if file_path is
        a relative path, get will look in all paths of the Media.PATH
        variable to find it

        (for images) kwarg scale is an optional (int, int): size of
        the resulting image.

        (for images) kwarg rotate if an optional int: rotation angle
        of the resulting image.

        (for fonts) kwarg size is an optional int: size of the
        resulting font.  default size is 24

        """
        if file_path is None:
            return None
        try:

            #  look in PATH if file_path is a relative path
            if not os.path.isabs(file_path):
                for mdir in Media.PATH:
                    abs_path = os.path.join(mdir, file_path)
                    if os.path.isfile(abs_path):
                        file_path = abs_path
                        break

            result: Optional[
                Union[pg.surface.Surface, pg.font.Font, pg.mixer.Sound]
            ] = None
            if mtype == 'image':
                result = pg.image.load(file_path).convert_alpha()
                rotate = kwargs.get('rotate')
                if rotate is not None:
                    result = pg.transform.rotate(result, rotate)
                scale = kwargs.get('scale')
                if scale is not None:
                    result = pg.transform.scale(result, scale)
            elif mtype == 'font':
                result = pg.font.Font(file_path, kwargs.get('size', 24))
            elif mtype == 'sound':
                result = pg.mixer.Sound(file_path)
        except pg.error:
            logging.error('could not load media file "%s"', file_path)
        except FileNotFoundError:
            logging.error('file "%s" does not exist', file_path)
        return result

    @classmethod
    def add_media_path(cls, path: str, pos: int = 0) -> None:
        """Add directory path to the PATH variable used by Media.get.

        The path is added at position pos.

        """
        Media.PATH.insert(pos, path)
        Media.get.cache_clear()

    @classmethod
    def rem_media_path(cls, path: str) -> None:
        """Remove directory path from the PATH variable used by Media.get."""
        if path not in Media.PATH:
            logging.info('%s is not in Media.PATH', path)
        else:
            Media.PATH.remove(path)
            Media.get.cache_clear()

    @classmethod
    def get_image(
            cls,
            img: Union[pg.surface.Surface, str],
            **kwargs: Any
    ) -> Optional[pg.surface.Surface]:
        """Load and return a pygame Surface.

        Return img if it is already a pygame Surface.  Otherwise load
        the Surface from file path img and return it.  Result of the
        method is cached.  kwargs are the same as for Media.get.

        """
        if isinstance(img, pg.Surface):
            return img
        result = Media.get('image', img, **kwargs)
        if isinstance(result, pg.surface.Surface):
            return result
        return None

    @classmethod
    def get_image_(
            cls,
            img: Union[pg.surface.Surface, str],
            **kwargs: Any
    ) -> pg.surface.Surface:
        """Load an image with Media.get_image + check result is not None."""
        result = Media.get_image(img, **kwargs)
        assert result is not None
        return result

    @classmethod
    def get_font(
            cls,
            font: str,
            **kwargs: Any
    ) -> Optional[pg.font.Font]:
        """Load and return a pygame Font.

        Parameter font can be a file path or the id of a font
        previously loaded by Media.load_fonts.  result of the method
        is cached.  kwargs are the same as for Media.get.

        """
        if font in Media.FONTS:
            path = Media.FONTS[font]['file']
        else:
            path = font
        result = Media.get('font', path, **kwargs)
        if isinstance(result, pg.font.Font):
            return result
        return None

    @classmethod
    def get_font_(
            cls,
            font: str,
            **kwargs: Any
    ) -> pg.font.Font:
        """Load a font with Media.get_fonf + check result is not None."""
        result = Media.get_font(font, **kwargs)
        assert result is not None
        return result

    @classmethod
    def get_sound(
            cls,
            file_path: str,
            **kwargs: Any
    ) -> Optional[pg.mixer.Sound]:
        """Load and return a pygame Sound.

        Load the pygame Sound from file file_path and return it.
        Result of the method is cached.  kwargs are the same as for
        Media.get.

        """
        result = Media.get('sound', file_path, **kwargs)
        if isinstance(result, pg.mixer.Sound):
            return result
        return None

    @classmethod
    def play_sound(
            cls,
            file_path: str,
            wait: bool = False
    ) -> Optional[pg.mixer.Channel]:
        """Load and play a sound.

        Sound is loaded from file file_path.  If wait is True,
        play_sound waits until sound is finished and returns None.
        Otherwise it returns the pygame Channel returned by
        pg.mixer.Sound.play.  Sounds loaded is cached.

        """
        sound = Media.get_sound(file_path)
        result = None
        if sound is not None:
            logging.info('playing sound %s', file_path)
            result = sound.play()
            if wait:
                Media.wait_sound(result)
                result = None
        return result

    @classmethod
    def wait_sound(
            cls,
            channel: Optional[pg.mixer.Channel]
    ) -> None:
        """Wait as long as the channel is busy.

        The method has bo effect if channel is None.

        """
        if channel is not None:
            while channel.get_busy():
                pg.time.wait(10)

    @classmethod
    def load_fonts(
            cls,
            json_file: str
    ) -> None:
        """Load font definitions from file path json_file."""
        data = Util.load_json_file(json_file)
        if data is None:
            return
        for font_id, font in data.items():
            Media.FONTS[font_id] = font
            if font.get('default', False):
                DEFAULT['font'] = font_id
                DEFAULT['font-size'] = font.get('size', 24)

    @classmethod
    def get_font_size(
            cls,
            font_id: str
    ) -> int:
        """Get the size of a font loaded by Media.load_fonts."""
        if font_id in Media.FONTS:
            if 'size' in Media.FONTS[font_id]:
                return int(Media.FONTS[font_id]['size'])
            logging.warning('font %s has an undefined size', font_id)
        else:
            logging.warning('undefined font: %s', font_id)
        return 24
