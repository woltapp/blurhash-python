#!/usr/bin/env python
from __future__ import absolute_import

from setuptools import setup


with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()


setup(
    name='blurhash-python',
    description='BlurHash encoder implementation for Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://blurha.sh',
    version='1.0.0',
    author='Atte Lautanala',
    author_email='atte.lautanala@wolt.com',
    packages=['blurhash'],
    package_dir={'': 'src'},
    install_requires=[
        'cffi>=1.9.1',
        'Pillow>=4.1.1',
        'six>=1.11.0',
    ],
    setup_requires=[
        'cffi>=1.9.1',
    ],
    cffi_modules=['src/build_blurhash.py:ffibuilder'],
    tests_require=[
        'pytest',
    ],
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Progarmming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ),
)
