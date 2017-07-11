#!/usr/bin/env python
from __future__ import absolute_import

from setuptools import setup


setup(
    name='blurhash-python',
    version='0.1.0',
    packages=['blurhash'],
    install_requires=[
        'cffi>=1.9.1',
        'Pillow>=4.1.1'
    ],
    setup_requires=['cffi>=1.9.1'],
    cffi_modules=['build_blurhash.py:ffibuilder'],
    test_suite='tests'
)
