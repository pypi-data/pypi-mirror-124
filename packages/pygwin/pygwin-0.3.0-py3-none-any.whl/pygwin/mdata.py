#!/usr/bin/env python3

"""Defines some meta data for pygwin."""

import os

__all__ = [
    'CLASSIFIERS',
    'DESCRIPTION',
    'INSTALL_REQUIRES',
    'NAME',
    'PACKAGE_DATA',
    'PYTHON_REQUIRES',
    'URL',
    'VERSION'
]

NAME = 'pygwin'

DESCRIPTION = 'pygame window system'

VERSION = '0.3.0'

URL = 'https://gitlab.com/qouify/pygwin/'

CLASSIFIERS = [
    'Programming Language :: Python',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
]

INSTALL_REQUIRES = [
    'pygame >= 2.0.0'
]

PYTHON_REQUIRES = '>=3.9'

PACKAGE_DATA = {
    'pygwin.test': [
        os.path.join('data', '*'),
        os.path.join('data', 'media', '*')
    ],
    'pygwin': [
        os.path.join('data', '*'),
        os.path.join('data', 'media', '*')
    ]
}
