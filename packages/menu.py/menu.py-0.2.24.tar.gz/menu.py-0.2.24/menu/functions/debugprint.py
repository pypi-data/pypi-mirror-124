from menu.classes.theme import *
from menu.menu import bDebugging

__all__=[
    'debugprint'
]

def debugprint(msg:str, sleeptime:int, log = False):

    if bDebugging == True:

        from time import sleep

        if log == False:
            print(f'\n {color_theme.error}debug: {msg}{color_theme.end}'), sleep(sleeptime)
        else:
            pass

    else:
        pass

    return