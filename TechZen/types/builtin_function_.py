import os

from TechZen.runtime_ import RTResult
from TechZen.errors_ import RTError
from TechZen.types.number_ import Number
from TechZen.types.string_ import String
from TechZen.types.list_ import List
from TechZen.types.base_function_ import BaseFunction
from TechZen.runner import Runner

Number.null = Number(0)
Number.false = Number(0)
Number.true = Number(1)


class BuiltInFunction(BaseFunction):
    def __init__(self, name):
        """
        Built-in functions. The other functions are inherited from the base function.
        :param name: Function name
        """
        super().__init__(name)

    def execute(self, args):
        """
        Execute the function.
        :param args: User inputted arguments
        :return: Runtime result
        """
        res = RTResult()
        exec_ctx = self.generate_new_context()

        method_name = f"execute_{self.name}"
        method = getattr(self, method_name, self.no_visit_method)

        res.register(self.check_and_populate_args(method.arg_names, args, exec_ctx))
        if res.should_return():
            return res

        return_value = res.register(method(exec_ctx))
        if res.should_return():
            return res

        return res.success(return_value)

    def no_visit_method(self, node, context):
        """
        This is the method that runs when the user typed in an invalid built-in function (doesn't exist).
        :param node: Node
        :param context: Context
        :return: Error
        """
        raise Exception(f"No execute_{self.name} method defined")

    def copy(self):
        """
        Make a copy of the built-in function.
        :return: Copy
        """
        copy = BuiltInFunction(self.name)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return f"<built-in function {self.name}>"

    def execute_print(self, exec_ctx):
        """
        Built-in print function.
        :param exec_ctx: Context for symbol table
        :return: Runtime result
        """
        print(exec_ctx.symbol_table.get("value"))
        return RTResult().success(Number.null)

    execute_print.arg_names = ["value"]

    def execute_print_ret(self, exec_ctx):
        """
        Built-in print return function.
        :param exec_ctx: Context for symbol table
        :return: Runtime result
        """
        return RTResult().success(String(str(exec_ctx.symbol_table.get("value"))))

    execute_print_ret.arg_names = ["value"]

    def execute_input(self, exec_ctx):
        """
        Built-in input function.
        :param exec_ctx: Context for symbol table
        :return: Runtime result
        """
        question = exec_ctx.symbol_table.get("value") or None
        text = input(question)
        return RTResult().success(String(text))

    execute_input.arg_names = ["value"]

    def execute_input_int(self, exec_ctx):
        """
        Built-in integer input function.
        :param exec_ctx: Context for symbol table
        :return: Runtime result
        """
        question = exec_ctx.symbol_table.get("value") or None
        while True:
            text = input(question)
            try:
                number = int(text)
                break
            except ValueError:
                print(f"'{text}' must be an integer. Try again!")
        return RTResult().success(Number(number))

    execute_input_int.arg_names = ["value"]

    def execute_clear(self, exec_ctx):
        """
        Built-in clear function. (works only on Windows, if you want to use it on another OS change 'cls' to 'clear')
        :param exec_ctx: Context for symbol table
        :return: Runtime result
        """
        os.system("cls" if os.name == "nt" else "cls")
        return RTResult().success(Number.null)

    execute_clear.arg_names = []

    def execute_is_number(self, exec_ctx):
        """
        Built-in is a number function.
        :param exec_ctx: Context for symbol table
        :return: Runtime result
        """
        is_number = isinstance(exec_ctx.symbol_table.get("value"), Number)
        return RTResult().success(Number.true if is_number else Number.false)

    execute_is_number.arg_names = ["value"]

    def execute_is_string(self, exec_ctx):
        """
        Built-in is a string function.
        :param exec_ctx: Context for symbol table
        :return: Runtime result
        """
        is_string = isinstance(exec_ctx.symbol_table.get("value"), String)
        return RTResult().success(Number.true if is_string else Number.false)

    execute_is_string.arg_names = ["value"]

    def execute_is_list(self, exec_ctx):
        """
        Built-in is a list function.
        :param exec_ctx: Context for symbol table
        :return: Runtime result
        """
        is_list = isinstance(exec_ctx.symbol_table.get("value"), List)
        return RTResult().success(Number.true if is_list else Number.false)

    execute_is_list.arg_names = ["value"]

    def execute_is_function(self, exec_ctx):
        """
        Built-in 'is a function' function.
        :param exec_ctx: Context for symbol table
        :return: Runtime result
        """
        is_function = isinstance(exec_ctx.symbol_table.get("value"), BaseFunction)
        return RTResult().success(Number.true if is_function else Number.false)

    execute_is_function.arg_names = ["value"]

    def execute_append(self, exec_ctx):
        """
        Built-in append to list function.
        :param exec_ctx: Context for symbol table
        :return: Runtime result
        """
        list_ = exec_ctx.symbol_table.get("list")
        value = exec_ctx.symbol_table.get("value")

        if not isinstance(list_, List):
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    "First argument must be list",
                    exec_ctx,
                )
            )

        list_.elements.append(value)
        return RTResult().success(Number.null)

    execute_append.arg_names = ["list", "value"]

    def execute_pop(self, exec_ctx):
        """
        Built-in pop from list function.
        :param exec_ctx: Context for symbol table
        :return: Runtime result
        """
        list_ = exec_ctx.symbol_table.get("list")
        index = exec_ctx.symbol_table.get("index")

        if not isinstance(list_, List):
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    "First argument must be list",
                    exec_ctx,
                )
            )

        if not isinstance(index, Number):
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument must be number",
                    exec_ctx,
                )
            )

        try:
            element = list_.elements.pop(index.value)
        except IndexError:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    "Element at this index could not be removed from list because index is out of bounds",
                    exec_ctx,
                )
            )
        return RTResult().success(element)

    execute_pop.arg_names = ["list", "index"]

    def execute_extend(self, exec_ctx):
        """
        Built-in extend list function.
        :param exec_ctx: Context for symbol table
        :return: Runtime result
        """
        list_a = exec_ctx.symbol_table.get("listA")
        list_b = exec_ctx.symbol_table.get("listB")

        if not isinstance(list_a, List):
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    "First argument must be list",
                    exec_ctx,
                )
            )

        if not isinstance(list_b, List):
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument must be list",
                    exec_ctx,
                )
            )

        list_a.elements.extend(list_b.elements)
        return RTResult().success(Number.null)

    execute_extend.arg_names = ["listA", "listB"]

    def execute_update_list(self, exec_ctx):
        """
        Built-in update list function.
        :param exec_ctx: Context for symbol table
        :return: Runtime result
        """
        list_ = exec_ctx.symbol_table.get("list")
        idx = exec_ctx.symbol_table.get("index")
        replacement = exec_ctx.symbol_table.get("replacement")

        if not isinstance(list_, List):
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    "First argument must be list",
                    exec_ctx,
                )
            )

        if not isinstance(idx, Number):
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument must be number",
                    exec_ctx,
                )
            )

        try:
            list_.elements[idx.value] = replacement
        except IndexError:
            return RTResult().failure(
                RTError(
                    self.pos_start, self.pos_end, "Index is out of bounds", exec_ctx
                )
            )
        return RTResult().success(List(list_.elements))

    execute_update_list.arg_names = ["list", "index", "replacement"]

    def execute_len(self, exec_ctx):
        """
        Built-in list length function.
        :param exec_ctx: Context for symbol table
        :return: Runtime result
        """
        list_ = exec_ctx.symbol_table.get("list")

        if not isinstance(list_, List):
            return RTResult().failure(
                RTError(self.pos_start, self.pos_end, "Argument must be list", exec_ctx)
            )
        return RTResult().success(Number(len(list_.elements)))

    execute_len.arg_names = ["list"]

    def execute_lower(self, exec_ctx):
        """
        Built-in lower string function.
        :param exec_ctx: Context for symbol table
        :return: Runtime result
        """
        string_ = exec_ctx.symbol_table.get("value")

        if not isinstance(string_, String):
            return RTResult().failure(
                RTError(
                    self.pos_start, self.pos_end, "Argument must be string", exec_ctx
                )
            )
        return RTResult().success(String(string_.value.lower()))

    execute_lower.arg_names = ["value"]

    def execute_upper(self, exec_ctx):
        """
        Built-in upper string function.
        :param exec_ctx: Context for symbol table
        :return: Runtime result
        """
        string_ = exec_ctx.symbol_table.get("value")

        if not isinstance(string_, String):
            return RTResult().failure(
                RTError(
                    self.pos_start, self.pos_end, "Argument must be string", exec_ctx
                )
            )
        return RTResult().success(String(string_.value.upper()))

    execute_upper.arg_names = ["value"]

    def execute_string(self, exec_ctx):
        """
        Built-in make string function.
        :param exec_ctx: Context for symbol table
        :return: Runtime result
        """
        integer_ = exec_ctx.symbol_table.get("value")

        if not isinstance(integer_, Number):
            return RTResult().failure(
                RTError(
                    self.pos_start, self.pos_end, "Argument must be string", exec_ctx
                )
            )
        return RTResult().success(String(str(integer_.value)))

    execute_string.arg_names = ["value"]

    def execute_run(self, exec_ctx):
        """
        Built-in run file function.
        :param exec_ctx: Context for symbol table
        :return: Runtime result
        """
        fn = exec_ctx.symbol_table.get("fn")

        if not isinstance(fn, String):
            return RTResult().failure(
                RTError(
                    self.pos_start, self.pos_end, "Argument must be string", exec_ctx
                )
            )

        fn = fn.value

        try:
            with open(fn, "r") as f:
                script = f.read()
        except Exception as e:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f'Failed to load script "{fn}"\n{e}',
                    exec_ctx,
                )
            )

        _, error, should_exit = Runner.run(fn, script)

        if error:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f'Failed to finish executing script "{fn}"\n{error.as_string()}',
                    exec_ctx,
                )
            )

        if should_exit:
            return RTResult().success_exit(Number.null)
        return RTResult().success(Number.null)

    execute_run.arg_names = ["fn"]

    def execute_exit(self, exec_ctx):
        """
        Built-in exit function.
        :param exec_ctx: Context for symbol table
        :return: Runtime result
        """
        return RTResult().success_exit(Number.null)

    execute_exit.arg_names = []


BuiltInFunction.print = BuiltInFunction("print")
BuiltInFunction.print_ret = BuiltInFunction("print_ret")
BuiltInFunction.input = BuiltInFunction("input")
BuiltInFunction.input_int = BuiltInFunction("input_int")
BuiltInFunction.clear = BuiltInFunction("clear")
BuiltInFunction.is_number = BuiltInFunction("is_number")
BuiltInFunction.is_string = BuiltInFunction("is_string")
BuiltInFunction.is_list = BuiltInFunction("is_list")
BuiltInFunction.is_function = BuiltInFunction("is_function")
BuiltInFunction.append = BuiltInFunction("append")
BuiltInFunction.pop = BuiltInFunction("pop")
BuiltInFunction.extend = BuiltInFunction("extend")
BuiltInFunction.len = BuiltInFunction("len")
BuiltInFunction.run = BuiltInFunction("run")
BuiltInFunction.update_list = BuiltInFunction("update_list")
BuiltInFunction.lower_string = BuiltInFunction("lower")
BuiltInFunction.upper_string = BuiltInFunction("upper")
BuiltInFunction.string = BuiltInFunction("string")
BuiltInFunction.exit = BuiltInFunction("exit")
