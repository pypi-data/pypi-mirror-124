from menu import *
from time import sleep

my_menu = menu('example_menu')
my_theme = "White"

def primary_menu():

    global my_theme

    page_name = 'main menu'
    text = 'the default keybinds for navigation are "s" for DOWN, "w" for UP and "ENTER" for SELECT'
    menu_items = [
        'module information',               #CASE 1
        'change theme via selection',       #CASE 2
        'change theme via input',           #CASE 3
        '_skip_',                           # "_skip_" IS IGNORED BY MENU
        '[X] exit'                          #CASE 4
    ]

    selection = my_menu.generate(page_name, menu_items, text, my_theme)

    match selection:
        case 1:
            return module_menu()
        case 2:
            return theme_selection_menu()
        case 3:
            return print('bar'), sleep(2)
        case 4:
            return my_menu.terminate()

        #this should, in theory, never happen but we'll plan for it anyways
        case _: #wildcard
            print('error'), sleep(5)
            my_menu.terminate()
            return exit()

def module_menu():

    page_name = 'module information'
    text = [
        'name: menu.py',
        'author: deadyeti (deadyeti@deadyeti.ca)',
        'created: 2021-OCT-12',
        'last updated: 2021-OCT-20',
        '_skip_',
        '--- description ---',
        '"a simple python package to quickly and easily generate in-terminal menus"'
    ]
    menu_items = [
        '[<] back',                #CASE 1
        '[X] exit'                 #CASE 2
    ]

    selection = my_menu.generate(page_name, menu_items, text, my_theme)

    match selection:
        case 1:
            return primary_menu()
        case 2:
            my_menu.terminate()

        #this should, in theory, never happen but we'll plan for it anyways
        case _:
            print('error'), sleep(5)
            my_menu.terminate()
            return exit()

def theme_selection_menu():

    global my_theme

    '''
        *** please note that the themes are undergoing a rewrite at this time, only the blue and white themes are available ***
    '''

    page_name = 'theme selection'
    text = 'please select one of the themes below:'

    menu_items = [
        'Red Theme',                 #CASE 1   *** currently not working, will display as white
        'Green Theme',               #CASE 2   *** currently not working, will display as white
        'Blue Theme',                #CASE 3
        'Light Blue Theme',          #CASE 4   *** currently not working, will display as white
        'Yellow Theme',              #CASE 5   *** currently not working, will display as white
        'White Theme',               #CASE 6
        '_skip_',                    # "_skip_" IS IGNORED BY MENU
        '[<] back',                  # CASE 7
        '[X] exit'                   #CASE 8
    ]

    selection = my_menu.generate(page_name, menu_items, text, my_theme)

    match selection:
            case 1:
                my_theme = 'Red'
                return theme_selection_menu()
            case 2:
                my_theme = 'Green'
                return theme_selection_menu()
            case 3:
                my_theme = 'Blue'
                return theme_selection_menu()
            case 4:
                my_theme = 'Light Blue'
                return theme_selection_menu()
            case 5:
                my_theme = 'Yellow'
                return theme_selection_menu()
            case 6:
                my_theme = 'White'
                return theme_selection_menu()
            case 7:
                return
            case 8:
                my_menu.terminate()
                return exit()

            #this should, in theory, never happen but we'll plan for it anyways
            case _:
                print('error'), sleep(5)
                my_menu.terminate()
                return exit()

while True:
    primary_menu()
