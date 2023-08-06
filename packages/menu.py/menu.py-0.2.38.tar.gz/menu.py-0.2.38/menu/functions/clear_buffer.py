from menu.classes.exceptions import *

try:
    from msvcrt import kbhit, getch
except:
    raise menuException(f'failed to import "msvcrt" module in {__file__}')

__all__=[
    'clear_buffer'
]

def clear_buffer():

    # clears the input buffer
    try:
        while kbhit():
            getch()
    except:
        raise menuException(f'failed to clear input buffer in file: {__file__}')
    
    return