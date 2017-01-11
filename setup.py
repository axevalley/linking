#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='linking',
    version='1.0',
    description='Manages Linnworks linking',
    author='Luke Shiner',
    install_requires=['requests'],
    packages=find_packages(),
    )
