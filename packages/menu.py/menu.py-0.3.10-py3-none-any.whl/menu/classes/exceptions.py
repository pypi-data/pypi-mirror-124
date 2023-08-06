# exception masterclass

__all__=[
    'menu_exception',
    'menu_type_exception',
    'menu_import_exception'
]

# general exception
class menu_exception(Exception):
    def __init__ (self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

# type exception
class menu_type_exception(TypeError):

    def __init__ (self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

# import exception
class menu_import_exception(ImportError):

    def __init__ (self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

