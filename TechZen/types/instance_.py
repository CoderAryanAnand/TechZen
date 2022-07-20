from TechZen.types.value_ import Value


class Instance(Value):
    def __init__(self, parent_class):
        """
        Instance type. Inherits from Value class.
        :param parent_class: Parent class
        """
        super().__init__()
        self.parent_class = parent_class
        self.symbol_table = None

    def copy(self):
        """
        Make a copy of instance.
        :return: Copy
        """
        return self

    def __repr__(self):
        return f"<instance of class {self.parent_class.name}>"
