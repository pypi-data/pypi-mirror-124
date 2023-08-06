from menu.classes.theme import *

__all__=[
    'menuprint',
    'menuprint_error'
]

# prints in color, using whichever color is set in the theme object
def menuprint(msg:str, newline:bool = True):

    '''
    A print() function that prints in whichever **text** color your menu is set to\n
    for **error** color printing, use menuprint_error()
    '''

    if newline == True:
        print(f'\n {color_theme.text}{msg}{color_theme.end}')
    else:
        print(f' {color_theme.text}{msg}{color_theme.end}')


# prints in error_color, using whichever color is set in the theme object
def menuprint_error(msg, newline:bool = False):

    '''
    a print() function that prints in whichever **error** color your menu is set to.\n
    for **text** color printing, user menuprint()
    '''

    if newline == False:
        print(f' {color_theme.error}*{msg}{color_theme.end}')
    else:
        print(f'\n {color_theme.error}*{msg}{color_theme.end}')