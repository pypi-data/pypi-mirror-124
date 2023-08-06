from menu.classes.theme import *

__all__=[
    'debugprint'
]

bDebugging = True

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