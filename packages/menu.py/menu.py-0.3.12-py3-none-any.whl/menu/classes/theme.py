
from time import sleep
from configparser import ConfigParser
from .exceptions import *

__all__=[
    'color_theme',
    'formatting'
]

class color_theme:

    # default color theme (white)
    text = '\33[37m'
    highlight = '\33[7m'
    error = '\033[91m'
    title = '\33[7m'
    page = '\33[37m'
    end = '\033[0m'

    def set_theme(color:str):
        if color.lower() in ['blue', 'bleu']:
            color_theme.text = '\33[34m'
            color_theme.highlight = '\33[44m\033[30m'
            color_theme.error = '\033[91m'
            color_theme.title = '\33[44m\033[30m'
            color_theme.page = '\33[34m'
        elif color.lower() in ['light blue', 'bleu pâle', 'bleu pale']:
            color_theme.text = '\033[36m'
            color_theme.highlight = '\033[46m\033[30m'
            color_theme.error = '\033[91m'
            color_theme.title = '\033[46m\033[30m'
            color_theme.page = '\033[36m'
        elif color.lower() in ['red', 'rouge']:
            color_theme.text = '\033[31m'
            color_theme.highlight = '\033[41m\033[30m'
            color_theme.error = '\33[33m'
            color_theme.title = '\033[41m\033[30m'
            color_theme.page = '\033[31m'
        elif color.lower() in ['green', 'vert']:
            color_theme.text = '\033[32m'
            color_theme.highlight = '\033[42m\033[30m'
            color_theme.error = '\033[91m'
            color_theme.title = '\033[102m\033[30m'
            color_theme.page = '\33[92m'
        elif color.lower() in ['purple', 'violet', 'mauve']:
            color_theme.text = '\33[95m'
            color_theme.highlight = '\33[45m\033[30m'
            color_theme.error = '\033[91m'
            color_theme.title = '\33[45m\033[30m'
            color_theme.page = '\33[95m'
        elif color.lower() in ['yellow', 'jaune']:
            color_theme.text = '\33[33m'
            color_theme.highlight = '\33[43m\033[30m'
            color_theme.error = '\033[91m'
            color_theme.title = '\33[43m\033[30m'
            color_theme.page = '\33[33m'
        else: # reset to default "white" theme
            color_theme.text = '\33[37m'
            color_theme.highlight = '\33[7m'
            color_theme.error = '\033[91m'
            color_theme.title = '\33[7m'
            color_theme.page = '\33[37m'

        return

class formatting:

    title_sep = '::'
    page_brackets = ['[', ']']

    def set_formatting(title_sep:str, page_brackets:list):

        if title_sep == None:
            formatting.title_sep == ''
        elif isinstance(title_sep, str):
            formatting.title_sep = title_sep
        else:
            raise menuException('title_sep must be a string')
        

        if page_brackets == None:
            formatting.page_brackets = ''
        elif isinstance(page_brackets, list):
            if len(page_brackets) != 2:
                raise menuException(f'page_brackets MUST be a list containing exactly 2 items, your list contains {len(page_brackets)} item(s)')
            else:
                formatting.page_brackets = page_brackets
        else:
            raise menuException(f'page_brackets MUST be a list containing exactly 2 items. You entered a {type(page_brackets)}')
