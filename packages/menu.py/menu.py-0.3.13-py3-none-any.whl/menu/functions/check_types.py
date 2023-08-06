
from menu.classes.exceptions import *

__all__ = [
    'check_types'
]

def check_types(page_name, menu_items, menu_text = None, theme = None):
    # make sure all inputs are correct type
    if type(page_name) != str:
        raise menu_type_exception(f'method parameter "page_name" must be a string, not {type(page_name)}')
    if type(menu_items) != list:
            raise menu_type_exception(f'method parameter "menu_items" must be a string, not {type(menu_items)}')
    if menu_text != None:
        if type(menu_text) != str:
            if type(menu_text) == list:
                pass
            else:
                raise menu_type_exception(f'method parameter "menu_text" must be a string or a list, not {type(menu_text)}')
    if theme != None:
        if type(theme) != str:
            raise menu_type_exception(f'method parameter "theme" must be a string, not {type(theme)}')
    
    return