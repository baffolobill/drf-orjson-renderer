#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='drf_orjson',
    version='2.0',
    description='Django Rest Framework ORJSON Renderer',
    author='Gizmag,baffolobill',
    url='https://github.com/baffolobill/drf-orjson-renderer',
    packages=find_packages(),
    install_requires=['django', 'orjson', 'djangorestframework']
)
