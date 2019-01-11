#!/usr/bin/env python
from __future__ import absolute_import

from setuptools import setup


setup(
    name='blurhash-python',
    version='0.3.1',
    packages=['blurhash'],
    package_dir={'': 'src'},
    install_requires=[
        'cffi>=1.9.1,<2.0.0',
        'Pillow>=4.1.1,<6.0.0',
        'six>=1.11.0,<2.0.0'
    ],
    setup_requires=[
        'pytest-runner==4.*',
        'cffi>=1.9.1,<2.0.0'
    ],
    cffi_modules=['src/build_blurhash.py:ffibuilder'],
    tests_require=['pytest==4.*']
)
