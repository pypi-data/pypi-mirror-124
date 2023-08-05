from .theme import *

__all__=[
    'menu_option'
]

# menu_option subclass
class menu_option(object):

    def __init__(self, number:int, name:str, bHighlight:bool = False):
        self.number = number
        self.name = name
        self.bHighlight = bHighlight

    def print(self):
        if self.bHighlight == False:
            print(f' {color_theme.text} {self.name} {color_theme.end}')
        else:
            print(f' {color_theme.highlight} {self.name} {color_theme.end}')
        return

    def select(self):
        return self.number