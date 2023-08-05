from menu.classes.exceptions import *

try:
    from os import system, name
except:
    raise menuException(f'failed to import "os" module in {__file__}')

__all__=[
    'cls'
]

# function that clears the terminal screen when called
def cls():
    system('cls' if name=='nt' else 'clear')
    return