#!/usr/bin/env python
from __future__ import absolute_import

from setuptools import setup


setup(
    name='blurhash-python',
    version='0.3.3',
    packages=['blurhash'],
    package_dir={'': 'src'},
    install_requires=[
        'cffi',
        'Pillow',
        'six'
    ],
    setup_requires=[
        'pytest-runner',
        'cffi'
    ],
    cffi_modules=['src/build_blurhash.py:ffibuilder'],
    tests_require=['pytest']
)
