from .theme import *

class menuprint(object):

    '''
    A print() function that prints in color
    
    '''

    def __init__(self, msg:str, error:bool = False, newline:bool = True):
        self.msg = msg
        if error != False:
            if newline == True:
                print(f'\n {color_theme.error}*{self.msg}{color_theme.end}')
            else:
                print(f' {color_theme.error}*{self.msg}{color_theme.end}')
        else:
            if newline == True:
                print(f'\n {color_theme.text}{self.msg}{color_theme.end}')
            else:
                print(f' {color_theme.text}{self.msg}{color_theme.end}')