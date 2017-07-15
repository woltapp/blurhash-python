#!/usr/bin/env python
from __future__ import absolute_import

from setuptools import setup


setup(
    name='blurhash-python',
    version='0.2.0',
    packages=['blurhash'],
    package_dir={'': 'src'},
    install_requires=[
        'cffi>=1.9.1,<1.11.0',
        'Pillow>=4.1.1,<4.3.0'
    ],
    setup_requires=[
        'pytest-runner==2.11.1',
        'cffi>=1.9.1,<1.11.0'
    ],
    cffi_modules=['src/build_blurhash.py:ffibuilder'],
    tests_require=['pytest==3.1.3']
)
