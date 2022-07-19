#######################################
# CONTEXT
#######################################


class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        """
        This provides context (the parent file, the current function, etc...) for error messages.
        :param display_name: File, input or function name
        :param parent: Name of the parent input, e.g. file
        :param parent_entry_pos: Position where the child function or file is called
        """
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None
