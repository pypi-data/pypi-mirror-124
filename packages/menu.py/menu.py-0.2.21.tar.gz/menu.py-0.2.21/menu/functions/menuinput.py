from menu.classes.theme import *
from menu.classes.exceptions import *

try:
    from msvcrt import kbhit, getch
except:
    raise menuException(f'failed to import "msvcrt" module in {__file__}')


__all__=[
    'menuinput'
]

def menuinput(msg:str, newline:bool = False):

    '''
    Exactly like input() except it uses the same color as the menu color theme.
    '''

    # clear input buffer so that no earlier inputs get in the input field
    while kbhit():
            getch()
    
    if newline == False:
        user_input = input(f' {color_theme.text}{msg}') + f'{color_theme.end}'
    else:
        user_input = input(f' {color_theme.text}{msg}') + f'{color_theme.end}'
    return user_input

