from TechZen.types.value_ import Value
from TechZen.errors_ import RTError
from TechZen.runtime_ import RTResult
from TechZen.context_ import Context
from TechZen.symbol_table_ import SymbolTable


class BaseFunction(Value):
    def __init__(self, name):
        """
        Base class for functions.
        :param name: Function name
        """
        super().__init__()
        self.name = name or "<anonymous>"

    def generate_new_context(self):
        """
        Generate a new context for the function.
        :return: New context
        """
        new_context = Context(self.name, self.context, self.pos_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
        return new_context

    def check_args(self, arg_names, args):
        """
        Check all function arguments when you call the function.
        :param arg_names: Function arguments
        :param args: User inputted arguments
        :return: Either runtime result success or failure
        """
        res = RTResult()

        if len(args) > len(arg_names):
            return res.failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f"{len(args) - len(arg_names)} too many args passed into '{self.name}'",
                    self.context,
                )
            )

        if len(args) < len(arg_names):
            return res.failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f"{len(arg_names) - len(args)} too few args passed into '{self.name}'",
                    self.context,
                )
            )
        return res.success(None)

    @staticmethod
    def populate_args(arg_names, args, exec_ctx):
        """
        Populate function with the arguments.
        :param arg_names: Function arguments
        :param args: User inputted arguments
        :param exec_ctx: Context for symbol table
        :return: nothing
        """
        for i, _ in enumerate(args):
            arg_name = arg_names[i]
            arg_value = args[i]
            arg_value.set_context(exec_ctx)
            exec_ctx.symbol_table.set(arg_name, arg_value)

    def check_and_populate_args(self, arg_names, args, exec_ctx):
        """
        Check how if the number of arguments passed are valid and then populate the function with those arguments.
        :param arg_names: Function arguments
        :param args: User inputted arguments
        :param exec_ctx: Context for symbol table
        :return: Runtime result success
        """
        res = RTResult()
        res.register(self.check_args(arg_names, args))
        if res.should_return():
            return res
        self.populate_args(arg_names, args, exec_ctx)
        return res.success(None)
