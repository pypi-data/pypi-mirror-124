
import keyboard as k
from time import sleep

# import functions
from .functions.cls import *
from .functions.print_header import *
from .functions.clear_buffer import *

# import classes
from .classes.theme import *
from .classes.exceptions import *
from .classes.menu_options import *

try:
    import msvcrt
except:
    raise menuException(f'failed to import "msvcrt" module in {__file__}')

version = '0.2.22'

__all__=[
    'menu',
    'version',
    'selection_delay',
    'refresh_rate'
]

re_iterations = 0
choice = 1
last_page = ''
last_teme = ''
last_theme = ''


selection_delay = 0.001 # 0.22 seems best
refresh_rate = 0.01 # 0.01 seems appropriate

# menu master class
class menu(object):

    def __init__(self, program_name):
        self.name = program_name

    def generate_selection(self, page_name, menu_items:list, menu_text:list = None, theme:str = None):

        '''
        generates an in-terminal user-selection menu that works both in windows command-prompt and powershell.

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
        global re_iterations

        if re_iterations > 10:
            clear_buffer()
            re_iterations = 0

        # this ensures that when changing pages, the selection returns to the top of the page
        if last_page != '':
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

        # get the total amount of menu_options loaded into the menu, minus any "_skip_" options.
        # if the choice goes above or below the number of loaded menu items, return to 1 or total.
        # this ensures that the options scroll in the desired way.
        total_options = 0
        total_options = len(menu_items) - menu_items.count('_skip_')
        if choice > total_options:
            choice = 1
        if choice < 1:
            choice = total_options


        # clear terminal screen and print menu header
        cls()
        print_header(self.name, page_name)

        # prints optional menu_text, if there is any.
        if menu_text != None:
            if isinstance(menu_text, str) == True:
                print(f' {color_theme.text}{menu_text}{color_theme.end}')
            elif isinstance(menu_text, list) == True:
                for item in menu_text:
                    if item == '_skip_':
                        print('')
                        continue
                    print(f' {color_theme.text}{item}{color_theme.end}')
            else:
                raise menuException('menu_text must either be a string or a list')
            print('')

        # if no menu options are present, raise exception (can't have a menu with no options, can you?).
        if len(menu_items) <= 0:
            raise Exception('menu must contain at least one menu item')

        # print menu items
        i = 1
        if isinstance(menu_items, str) == True:
            menu_option(i, item, True).print()
        elif isinstance(menu_items, list) == True:
            for item in menu_items:
                if item == '_skip_':
                    print('')
                    continue
                if i == choice:
                    menu_option(i, item, True).print()
                else:
                    menu_option(i, item).print()
                i += 1
        else:
            menuException('menu_items must either be a string or a list')

        # l00p until user selects an item in the menu
        sleep(selection_delay)
        while not k.is_pressed('enter'):
            if k.is_pressed('s'):
                try:
                    choice += 1
                    return self.generate_selection(page_name, menu_items, menu_text, theme)
                except:
                    clear_buffer()
            elif k.is_pressed('w'):
                try:
                    choice -= 1
                    return self.generate_selection(page_name, menu_items, menu_text, theme)
                except:
                    clear_buffer()
            sleep(refresh_rate)
        
        return menu_option(choice, menu_items[choice-1], menu_items[choice-1]).select()

    def terminate(self):
        while msvcrt.kbhit():
            msvcrt.getch()
        del self
        return