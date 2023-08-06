#!/usr/bin/env python3

"""Setup script for pygwin."""

from setuptools import setup, find_packages
from pygwin import mdata


setup(
    name=mdata.NAME,
    version=mdata.VERSION,
    description=mdata.DESCRIPTION,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url=mdata.URL,
    classifiers=mdata.CLASSIFIERS,
    packages=find_packages('.'),
    package_dir={'': '.'},
    package_data=mdata.PACKAGE_DATA,
    install_requires=mdata.INSTALL_REQUIRES,
    python_requires=mdata.PYTHON_REQUIRES
)
