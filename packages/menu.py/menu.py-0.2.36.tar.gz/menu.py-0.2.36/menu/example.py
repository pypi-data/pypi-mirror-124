from menu import *
from time import sleep

my_menu = menu('example_menu')
my_theme = "White"

def primary_menu():

    page_name = 'main menu'
    text = 'the default keybinds for navigation are "s" for DOWN, "w" for UP and "ENTER" for SELECT'
    menu_items = [
        'module information',                    #CASE 1
        'change theme via selection',            #CASE 2
        'change theme via input (unavailable)',  #CASE 3   *** CURRENTLY UNAVAILABLE ***
        '_skip_',                                # "_skip_" IS IGNORED BY MENU
        '[X] exit'                               #CASE 4
    ]

    selection = my_menu.generate(page_name, menu_items, text, my_theme)

    match selection:
        case 1:
            return module_menu()
        case 2:
            return theme_selection_menu()
        case 3:
            return menuprint_error('this option is currently unavailable'), sleep(2)
        case 4:
            my_menu.terminate()
            return exit()

        #this should, in theory, never happen but we'll plan for it anyways
        case _: #wildcard
            menuprint_error('a critical error has occured'), sleep(5)
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
            return exit()

        #this should, in theory, never happen but we'll plan for it anyways
        case _:
            menuprint_error('a critical error has occured'), sleep(5)
            my_menu.terminate()
            return exit()

def theme_selection_menu():

    global my_theme

    '''
        *** please note that the color themes will be undergoing a rewrite and may not be working properly ***
    '''

    page_name = 'theme selection'
    text = 'please select one of the themes below:'

    menu_items = [
        'Red Theme',                 #CASE 1   
        'Green Theme',               #CASE 2  
        'Blue Theme',                #CASE 3
        'Light Blue Theme',          #CASE 4  
        'Yellow Theme',              #CASE 5  
        'White Theme',               #CASE 6
        '_skip_',                    # "_skip_" IS IGNORED BY MENU
        '[<] back',                  # CASE 7
        '[X] exit'                   #CASE 8
    ]

    selection = my_menu.generate(page_name, menu_items, text, my_theme)

    match selection:
            case 1:
                my_theme = 'Red'
            case 2:
                my_theme = 'Green'
            case 3:
                my_theme = 'Blue'
            case 4:
                my_theme = 'Light Blue'
            case 5:
                my_theme = 'Yellow'
            case 6:
                my_theme = 'White'
            case 7:
                return primary_menu()
            case 8:
                my_menu.terminate()
                return exit()

            #this should, in theory, never happen but we'll plan for it anyways
            case _:
                menuprint_error('a critical error has occured'), sleep(5)
                my_menu.terminate()
                return exit()

    return theme_selection_menu()

while True:
    primary_menu()
