"""
menu.py
=============================================
A simple python package for in-terminal menu creation on Windows

copyright (c) 2021-present deadyeti

MIT License, see LICENSE for more details.
"""

# import modules
from .menu import *
from menu.functions.menuinput import *
from menu.functions.menuprint import *
from menu.classes.theme import formatting

__all__ = [
    'menu',
    'menuprint',
    'menuinput',
    'formatting'
]

__title__ = 'menu'
__author__ = 'deadyeti'
__license__ = 'MIT'
__copyright__ = 'Copyright 2021-present deadyeti'
__version__ = version