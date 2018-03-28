#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Setup script for food2fork
'''
# import os
# _USERNAME = os.getenv("SUDO_USER") or os.getenv("USER")
# _HOME = os.path.expanduser("~"+_USERNAME)
# _CONFIGDIR = os.path.join(_HOME, ".config")

from setuptools import setup

setup(
    name="food2fork",
    version="1.0",
    description="",
    long_description="""
    Simple module to ...
    """,
    author="Julien Spronck",
    author_email="github@frenetic.be",
    url="https://frenetic.be",
    packages=["food2fork"],
    #       entry_points = {"console_scripts":["food2fork = "
    #                                          "food2fork:main"]},
    #       data_files=[(_CONFIGDIR,
    #                   ["food2fork/food2fork_config.py"])],
    license="Free for non-commercial use"
)