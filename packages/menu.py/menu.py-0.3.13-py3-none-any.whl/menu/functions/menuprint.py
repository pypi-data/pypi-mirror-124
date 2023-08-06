from menu.classes.theme import *

__all__= [
    'menuprint'
]

# prints in color, using whichever color is set in the theme object
def menuprint(msg:str, newline:bool = True, error:bool = False):

    '''
    A print() function that prints in whichever **text** color your menu is set to
    '''

    if newline == True:
        if error == True:
            print(f'\n {color_theme.error}*{msg}{color_theme.end}')
        else:
            print(f'\n {color_theme.text}{msg}{color_theme.end}')
    else:
        if error == True:
            print(f' {color_theme.error}*{msg}{color_theme.end}')
        else:
            print(f' {color_theme.text}{msg}{color_theme.end}')
