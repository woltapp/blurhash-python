#!/usr/bin/env python
# Minimal setup.py required for CFFI extension building
# All metadata is in pyproject.toml
from setuptools import setup

setup(
    cffi_modules=["src/build_blurhash.py:ffibuilder"],
)
