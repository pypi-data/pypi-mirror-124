from menu.classes.theme import *

__all__=[
    'print_header'
]

# function that prints the terminal header when called
def print_header(program_name, page_name):
    if page_name != None:
        print(f' {color_theme.title} {program_name} {color_theme.end} {color_theme.text}{formatting.title_sep}{color_theme.end}{color_theme.page} {formatting.page_brackets[0]} {page_name} {formatting.page_brackets[1]}{color_theme.end}\n')
    else:
        print(f' {color_theme.title}  {program_name}  {color_theme.end}\n')
