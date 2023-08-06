
import keyboard as k
from time import sleep
from platform import python_version, system, python_version_tuple
from sys import setrecursionlimit

# import functions
from .functions.cls import *
from .functions.print_header import *
from .functions.clear_buffer import *
from .functions.debugprint import *
from .functions.check_types import *

# import classes
from .classes.theme import *
from .classes.exceptions import *
from .classes.menu_options import *

version = '0.3.8'

__all__=[
    'menu',
    'version'
]

choice = 1
_previous_pages = []
last_page = None
last_teme = ''
last_theme = ''

#selection_delay = 0.22  # 0.22 seems best
#refresh_rate = 0.01     # 0.01 seems appropriate

# menu master class
class menu(object):

    tick_rate:float = 0.01          # variable refresh rate
    selection_delay:float = 0.30    # variable selection delay

    keybind_next:str = 's'          # keybind
    keybind_prev:str = 'w'          # keybind
    keybind_sel:str = 'enter'       # keybind

    def __init__(self, program_name:str):
        self.name = program_name

    def generate(self, page_name:str, menu_items:list, menu_text:list|str = None, theme:str = None):

        '''
        generates an in-terminal selection menu that works both in windows command-prompt and powershell.

        '''

        # self setup
        #theme = theme
        #program_name = program_name
        #page_name = page_name
        #menu_items = menu_items
        #if menu_text != None:
        #    menu_text = menu_text

        global choice     
        global last_page
        global last_theme

        menu_text_list = []
        bList = False

        if page_name not in _previous_pages:
            global _previous_pages
            check_types(page_name, menu_items, menu_text, theme)
            _previous_pages.append(page_name)


        # this ensures that when changing pages, the selection returns to the top of the page
        if last_page != None:
            if last_page != page_name:
                choice = 1
        else:
            choice = 1
        last_page = page_name

        # only set the theme when applicable
        if last_theme != theme:
            if theme != None:
                color_theme.set_theme(theme)             
        last_theme = theme

        # get the total amount of menu_options loaded into the menu, minus any "_skip_" or empty string options.
        # if the choice goes above or below the number of loaded menu items, return to 1 or total.
        # this ensures that the options scroll in the desired way.
        total_options = 0
        invalid_options = 0
        valid_options = len(menu_items)
        for item in menu_items:
            if item in ['', ' ', '_skip_']:
                invalid_options += 1
        total_options = valid_options - invalid_options

        # allows menu to loop through the options
        if choice > total_options:
            choice = 1
        if choice < 1:
            choice = total_options

        # format menu_text input
        if menu_text != None:
            if isinstance(menu_text, str) == True: # if menu_text is string
                formatted_menu_text = f'{color_theme.text}{menu_text}{color_theme.end}'
            elif isinstance(menu_text, list) == True: # if menu_text is list
                bList = True
                for item in menu_text:
                    if item in ['_skip_', '', ' ']:
                        menu_text_list.append('')
                        continue
                    menu_text_list.append(f'{color_theme.text}{item}{color_theme.end}')
            else:
                raise menuException('menu_text *must* either be a string or a list')

        # if no menu options are present, raise exception (can't have a menu with no options, can you?).
        if len(menu_items) <= 0:
            raise Exception('menu_items *must* contain at least one menu item')
        

        clear_buffer()
        cls()                                   # clear terminal screen FIXME: this is causing flickering, there must be another way
        print_header(self.name, page_name)      # print the menu header
        if bList == False:
            print(f' {formatted_menu_text}')
        else:
            for item in menu_text_list:
                print(f' {item}')
        print('')

        # print menu items
        i = 1
        if isinstance(menu_items, list) == True:
            for item in menu_items:
                if item in ['', ' ', '_skip_']:
                    print('')
                    continue
                elif i == choice:
                    menu_option(i, item, True).print()
                else:
                    menu_option(i, item).print()
                i += 1
        else:
            raise menuException('menu_items *must* be a list')

        # l00p until user selects an item in the menu
        sleep(menu.selection_delay)
        while not k.is_pressed(menu.keybind_sel):
            if k.is_pressed(menu.keybind_next):
                try:
                    choice += 1
                    return self.generate(page_name, menu_items, menu_text, theme)
                except:
                    return
            elif k.is_pressed(menu.keybind_prev):
                try:
                    choice -= 1
                    return self.generate(page_name, menu_items, menu_text, theme)
                except:
                    return
            sleep(menu.tick_rate)
        
        clear_buffer()
        return menu_option(choice, menu_items[choice-1], menu_items[choice-1]).select()

    def terminate(self):
        clear_buffer()
        cls()
        return

#check that user is using the correct OS and version of python
if system().lower() != 'windows':
    raise menuException(f'invalid operating system: "{system()}"\nmenu.py currently only works on windows machines.')
if int(python_version_tuple()[0]) < 3 or int(python_version_tuple()[1]) < 6:
    raise menuException(f'invalid python version: "{python_version()}"\nmenu.py makes use of features, such as f-strings, that require python 3.6 or newer.')

try:
    setrecursionlimit(10**6)
except:
    pass
