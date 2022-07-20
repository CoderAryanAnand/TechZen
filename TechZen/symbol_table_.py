#######################################
# SYMBOL TABLE
#######################################


class SymbolTable:
    def __init__(self, parent=None):
        """
        This is the symbol table. This is where all built-in functions and variable are stored.
        :param parent: None, otherwise a parent
        """
        self.symbols = {}
        self.parent = parent

    def get(self, name):
        """
        Get a value from the table
        :param name: key
        :return: value
        """
        value = self.symbols.get(name, None)
        if value is None and self.parent:
            return self.parent.get(name)
        return value

    def set(self, name, value):
        """
        Set a value in the symbol table
        :param name: key
        :param value: value
        :return: nothing
        """
        self.symbols[name] = value

    def remove(self, name):
        """
        Remove value from symbol table
        :param name: key
        :return: nothing
        """
        del self.symbols[name]
