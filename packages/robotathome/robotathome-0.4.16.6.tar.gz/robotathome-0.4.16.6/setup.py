#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup for RobotAtHome API
"""

import os
import sys

from setuptools import find_packages, setup

def read(rel_path):
    """ Docstring """
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    """ Docstring """
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="robotathome",
    version=get_version("robotathome/__init__.py"),
    description="This package provides a Python Toolbox with a set of functions to assist in the management of Robot@Home 2 Dataset",
    long_description=long_description,
    long_description_content_type="text/markdown",

    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/goyoambrosio/RobotAtHome_API",
    keywords=('semantic mapping '
              'object categorization '
              'object recognition '
              'room categorization '
              'room recognition '
              'contextual information '
              'mobile robots '
              'domestic robots '
              'home environment '
              'robotic dataset benchmark '
              ),

    author="G. Ambrosio-Cestero",
    author_email="gambrosio@uma.es",

    packages=find_packages(),

    install_requires=[
        "humanize",
        "click",
        "urllib3",
        "loguru",
        "mxnet",
        "gluoncv",
        "opencv-python",
        "numpy"
    ],

    extras_require={
        'interactive': ['matplotlib>=3', 'jupyter'],
        'opencv': ['opencv-python >= 4.5.3'],
        'mxnet': ['mxnet', 'gluoncv']
    },
    python_requires='>=3.6',
)
