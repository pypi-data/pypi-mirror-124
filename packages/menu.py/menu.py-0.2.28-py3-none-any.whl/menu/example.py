import menu as m
from time import sleep

app_name = 'yetimenu: example menu'
my_theme = ''

def primary_menu():

    global my_theme

    if my_theme == '':
        my_theme = 'Purple'
    menu_type = 'selection'
    page_name = 'main menu'
    menu_items = [
        'module information',               #CASE 1
        'change theme via selection',       #CASE 2
        'change theme via input',           #CASE 3
        '_skip_',                           # _skip_ IS IGNORED BY MENU
        '[X] exit'                          #CASE 4
    ]

    selection = m.generate(menu_type, my_theme, app_name, page_name, menu_items)

    match selection:
        case 1:
            return module_menu()
        case 2:
            return theme_selection_menu()
        case 3:
            return print('bar'), sleep(2)
        case 4:
            m._exit_()

        case _: #wildcard
            return print('error'), exit()

def module_menu():

    page_name = 'module information'
    menu_type = 'selection'
    text = [
        'name: yetimenu',
        'author: deadyeti (deadyeti@deadyeti.ca)',
        'created: 2021-OCT-12',
        'last updated: 2021-OCT-13',
        '_skip_',
        '--- description ---',
        '"a simple python module to quickly and easily generate in-terminal menus"'
    ]
    menu_items = [
        '[<] back',                #CASE 1
        '[X] exit'                 #CASE 2
    ]

    selection = m.generate(menu_type, my_theme, app_name, page_name, menu_items, text)

    match selection:
        case 1:
            return primary_menu()
        case 2:
            m._exit_()

        case _: #wildcard
            return print('wut?'), exit()

def theme_selection_menu():

    global my_theme

    page_name = 'theme selection'
    menu_type = 'selection'
    text = [
        'please select from the available built-in themes below:'
    ]

    menu_items = [
        'Red Theme',                 #CASE 1
        'Green Theme',               #CASE 2
        'Blue Theme',                #CASE 3
        'Light Blue Theme',          #CASE 4
        'Yellow Theme',              #CASE 5
        'White Theme',               #CASE 6
        '_skip_',                    # _skip_ IS IGNORED BY MENU
        '[<] back',                  # CASE 7
        '[X] exit'                   #CASE 8
    ]

    selection = m.generate(menu_type, my_theme, app_name, page_name, menu_items, text)

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
                m._exit_()

            case _: #wildcard
                return print('error'), exit()

while True:
    primary_menu()
