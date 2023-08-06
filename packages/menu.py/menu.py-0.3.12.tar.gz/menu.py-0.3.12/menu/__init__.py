"""
menu.py
=============================================
A simple python package for in-terminal menu creation on Windows

copyright (c) 2021-present deadyeti

MIT License, see LICENSE for more details.
"""

# import functions
#from .menu import generate
#from .menu import terminate

# import classes
#from .menu import cprint
#from .menu import eprint

# import modules
from .menu import *
from .functions.menuinput import *
from .functions.menuprint import *
from .classes.theme import formatting

__all__ = [
    'menu',
    'menuprint',
    'menuprint_error',
    'menuinput',
    'formatting'
]

__title__ = 'menu'
__author__ = 'deadyeti'
__license__ = 'MIT'
__copyright__ = 'Copyright 2021-present deadyeti'
__version__ = version