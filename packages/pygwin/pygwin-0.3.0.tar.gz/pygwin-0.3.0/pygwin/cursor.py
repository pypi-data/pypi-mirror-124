#!/usr/bin/env python3

"""Definition of class Cursor."""

from typing import Optional, Union, Dict, Literal
import logging
import pygame as pg

from . import Media


class Cursor:
    """Class Cursor contains various functions for cursor management."""

    status_t = Literal['base', 'clicked']

    __ON: bool = False
    __DEFAULT: Dict[status_t, pg.surface.Surface] = dict()

    @classmethod
    def set_default(
            cls,
            img: Union[str, pg.surface.Surface],
            status: status_t = 'base'
    ) -> None:
        """Set the default image file of status.

        img can be either the file path of the image or either a
        pygame Surface.

        """
        media = Media.get_image(img)
        if media is not None:
            Cursor.__DEFAULT[status] = media

    @classmethod
    def get_default(
            cls, status: status_t = 'base'
    ) -> Optional[pg.surface.Surface]:
        """Get the default image of status."""
        return Cursor.__DEFAULT.get(status)

    @classmethod
    def activate(cls) -> None:
        """Activate pygwin's cursor system.

        The cursor image of the base context must have been set before
        this to work. If successful, the system cursor becomes
        invisible.

        """
        if 'base' not in Cursor.__DEFAULT:
            logging.error('default cursor image is not set')
        else:
            Cursor.__ON = True
            pg.mouse.set_visible(False)

    @classmethod
    def deactivate(cls) -> None:
        """Deactivate pygwin's cursor system.

        The system cursor becomes visible again.

        """
        Cursor.__ON = False
        pg.mouse.set_visible(True)

    @classmethod
    def activated(cls) -> bool:
        """Check if the cursor system has been activated."""
        return Cursor.__ON
