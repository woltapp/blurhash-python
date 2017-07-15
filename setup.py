#!/usr/bin/env python
from __future__ import absolute_import

from setuptools import setup


setup(
    name='blurhash-python',
    version='0.1.1',
    packages=['blurhash'],
    package_dir={'': 'src'},
    install_requires=[
        'cffi>=1.9.1',
        'Pillow>=4.1.1'
    ],
    setup_requires=[
        'pytest-runner==2.11.1',
        'cffi>=1.9.1'
    ],
    cffi_modules=['build_blurhash.py:ffibuilder'],
    tests_require=['pytest==3.1.3']
)
