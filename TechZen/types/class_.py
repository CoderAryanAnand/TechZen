from TechZen.types.value_ import Value
from TechZen.types.string_ import String
from TechZen.types.instance_ import Instance
from TechZen.symbol_table_ import SymbolTable
from TechZen.context_ import Context
from TechZen.errors_ import RTError
from TechZen.runtime_ import RTResult


class Class(Value):
    def __init__(self, name, symbol_table):
        super().__init__()
        self.name = name
        self.symbol_table = symbol_table

    def dived_by(self, other):
        if not isinstance(other, String):
            return None, self.illegal_operation(other)

        value = self.symbol_table.get(other.value)
        if not value:
            return None, RTError(
                self.pos_start, self.pos_end,
                f"'{other.value}' is not defined",
                self.context
            )

        return value, None

    def execute(self, args):
        from TechZen.types.function_ import Function
        res = RTResult()

        exec_ctx = Context(self.name, self.context, self.pos_start)

        inst = Instance(self)
        inst.symbol_table = SymbolTable(self.symbol_table)

        exec_ctx.symbol_table = inst.symbol_table
        for name in self.symbol_table.symbols:
            inst.symbol_table.set(name, self.symbol_table.symbols[name].copy())

        for name in inst.symbol_table.symbols:
            inst.symbol_table.symbols[name].set_context(exec_ctx)

        inst.symbol_table.set('this', inst)
        inst.symbol_table.set('self', inst)

        method = inst.symbol_table.symbols[self.name] if self.name in inst.symbol_table.symbols else None

        if method is None or not isinstance(method, Function):
            return res.failure(RTError(
                self.pos_start, self.pos_end,
                f"Function '{self.name}' not defined",
                self.context
            ))

        res.register(method.execute(args))
        if res.should_return():
            return res

        return res.success(inst.set_context(self.context).set_pos(self.pos_start, self.pos_end))

    def copy(self):
        return self

    def __repr__(self):
        return f"<class {self.name}>"
