from TechZen.types.value_ import Value


class Instance(Value):
    def __init__(self, parent_class):
        super().__init__()
        self.parent_class = parent_class
        self.symbol_table = None

    def copy(self):
        return self

    def __repr__(self):
        return f"<instance of class {self.parent_class.name}>"
