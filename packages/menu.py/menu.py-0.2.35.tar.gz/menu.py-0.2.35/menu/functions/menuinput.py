from menu.classes.theme import *
from menu.classes.exceptions import *
from .clear_buffer import *


__all__=[
    'menuinput'
]

def menuinput(msg:str, newline:bool = False):

    '''
    Exactly like input() except it uses the same color as the menu color theme.
    '''

    # clear input buffer, important before any input
    clear_buffer()
    
    if newline == False:
        user_input = input(f' {color_theme.text}{msg}') + f'{color_theme.end}'
    else:
        user_input = input(f' {color_theme.text}{msg}') + f'{color_theme.end}'
    return user_input

