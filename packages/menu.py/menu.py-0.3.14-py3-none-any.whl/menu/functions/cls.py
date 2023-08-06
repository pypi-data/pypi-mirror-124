from menu.classes.exceptions import *

try:
    from os import system, name
except:
    raise menu_import_exception(f'failed to import "os" module in {__name__}')

__all__=[
    'cls'
]

# function that clears the terminal screen when called
def cls():

    try:
        system('cls||clear')
    except:
        raise menu_exception(f'critical error in cls() function in {__name__}.py')

    return