from TechZen.runtime_ import RTResult
from TechZen.errors_ import RTError
from TechZen.token_ import TokenType, Keywords
from TechZen.context_ import Context
from TechZen.symbol_table_ import SymbolTable
from TechZen.types.number_ import Number
from TechZen.types.list_ import List
from TechZen.types.class_ import Class
from TechZen.types.instance_ import Instance

Number.null = Number(0)
Number.false = Number(0)
Number.true = Number(1)


class Interpreter:
    @classmethod
    def visit(cls, node, context):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(cls, method_name, cls.no_visit_method)
        return method(node, context)

    @classmethod
    def no_visit_method(cls, node, context):
        raise Exception(f"No visit_{type(node).__name__} method defined")

    @classmethod
    def visit_NumberNode(cls, node, context):
        return RTResult().success(
            Number(node.token.value)
            .set_context(context)
            .set_pos(node.pos_start, node.pos_end)
        )

    @classmethod
    def visit_StringNode(cls, node, context):
        from TechZen.types.string_ import String

        return RTResult().success(
            String(node.token.value)
            .set_context(context)
            .set_pos(node.pos_start, node.pos_end)
        )

    @classmethod
    def visit_ListNode(cls, node, context):
        res = RTResult()
        elements = []

        for element_node in node.element_nodes:
            elements.append(res.register(cls.visit(element_node, context)))
            if res.should_return():
                return res

        return res.success(
            List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    @classmethod
    def visit_DictNode(cls, node, context):
        from TechZen.types.dict_ import Dict

        res = RTResult()
        elements = {}
        keys = []
        values = []
        for key in node.element_nodes.keys():
            keys.append(key)
            values.append(node.element_nodes[key])

        try:
            for key, value in zip(keys, values):
                elements[res.register(cls.visit(key, context))] = res.register(
                    cls.visit(value, context)
                )
                if res.should_return():
                    return res
        except ValueError:
            elements[res.register(cls.visit(keys[0], context))] = res.register(
                cls.visit(values[0], context)
            )

        return res.success(
            Dict(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    @classmethod
    def visit_VarAccessNode(cls, node, context):
        res = RTResult()
        var_name = node.var_name_token.value
        value = context.symbol_table.get(var_name)

        if not value:
            return res.failure(
                RTError(
                    node.pos_start,
                    node.pos_end,
                    f"'{var_name}' is not defined",
                    context,
                )
            )

        if node.child:
            if not isinstance(value, Instance) and not isinstance(value, Class):
                return res.failure(
                    RTError(
                        node.pos_start,
                        node.pos_end,
                        "Value must be instance of class or class",
                        context,
                    )
                )

            new_context = Context(value.parent_class.name, context, node.pos_start)
            new_context.symbol_table = value.symbol_table

            child = res.register(cls.visit(node.child, new_context))
            if res.error:
                return res

            value = child

        value = value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        return res.success(value)

    @classmethod
    def visit_VarAssignNode(cls, node, context):
        res = RTResult()
        var_name = node.var_name_token.value
        value = res.register(cls.visit(node.value_node, context))
        if res.should_return():
            return res

        if node.extra_names:

            nd = context.symbol_table.get(var_name)
            prev = None

            if not nd:
                return res.failure(
                    RTError(
                        node.pos_start,
                        node.pos_end,
                        f"'{var_name}' not defined",
                        context,
                    )
                )

            for index, name_token in enumerate(node.extra_names):
                name = name_token.value

                if not isinstance(nd, Class) and not isinstance(nd, Instance):
                    return res.failure(
                        RTError(
                            node.pos_start,
                            node.pos_end,
                            "Value must be instance of class or class",
                            context,
                        )
                    )

                prev = nd
                nd = (
                    nd.symbol_table.symbols[name]
                    if name in nd.symbol_table.symbols
                    else None
                )

                if not nd and index != len(node.extra_names) - 1:
                    return res.failure(
                        RTError(
                            node.pos_start,
                            node.pos_end,
                            f"'{name}' not defined",
                            context,
                        )
                    )

            prev.symbol_table.set(name, value)
            return res.success(value)

        context.symbol_table.set(var_name, value)
        return res.success(value)

    @classmethod
    def visit_BinOpNode(cls, node, context):  # sourcery no-metrics
        res = RTResult()
        left = res.register(cls.visit(node.left_node, context))
        if res.should_return():
            return res
        right = res.register(cls.visit(node.right_node, context))
        if res.should_return():
            return res

        if node.op_token.type == TokenType.TT_PLUS:
            result, error = left.added_to(right)
        elif node.op_token.type == TokenType.TT_MINUS:
            result, error = left.subbed_by(right)
        elif node.op_token.type == TokenType.TT_MUL:
            result, error = left.multed_by(right)
        elif node.op_token.type == TokenType.TT_POW:
            result, error = left.pow_of(right)
        elif node.op_token.type == TokenType.TT_MOD:
            result, error = left.mod_by(right)
        elif node.op_token.type == TokenType.TT_DIV:
            result, error = left.dived_by(right)
        elif node.op_token.type == TokenType.TT_DFL:
            result, error = left.floor_by(right)
        elif node.op_token.type == TokenType.TT_EE:
            result, error = left.get_comparison_eq(right)
        elif node.op_token.type == TokenType.TT_NE:
            result, error = left.get_comparison_ne(right)
        elif node.op_token.type == TokenType.TT_LT:
            result, error = left.get_comparison_lt(right)
        elif node.op_token.type == TokenType.TT_GT:
            result, error = left.get_comparison_gt(right)
        elif node.op_token.type == TokenType.TT_LTE:
            result, error = left.get_comparison_lte(right)
        elif node.op_token.type == TokenType.TT_GTE:
            result, error = left.get_comparison_gte(right)
        elif node.op_token.matches(TokenType.TT_KEYWORD, Keywords.KW_AND.value):
            result, error = left.anded_by(right)
        elif node.op_token.matches(TokenType.TT_KEYWORD, Keywords.KW_AND.value):
            result, error = left.ored_by(right)

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    @classmethod
    def visit_UnaryOpNode(cls, node, context):
        res = RTResult()
        number = res.register(cls.visit(node.node, context))
        if res.should_return():
            return res

        error = None

        if node.op_token.type == TokenType.TT_MINUS:
            number, error = number.multed_by(Number(-1))
        elif node.op_token.matches(TokenType.TT_KEYWORD, Keywords.KW_NOT.value):
            number, error = number.notted()

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))

    @classmethod
    def visit_IfNode(cls, node, context):
        res = RTResult()
        for condition, expr, should_return_null in node.cases:
            condition_value = res.register(cls.visit(condition, context))
            if res.should_return():
                return res

            if condition_value.is_true():
                expr_value = res.register(cls.visit(expr, context))
                if res.should_return():
                    return res
                return res.success(Number.null if should_return_null else expr_value)

        if node.else_case:
            expr, should_return_null = node.else_case
            else_value = res.register(cls.visit(expr, context))
            if res.should_return():
                return res
            return res.success(Number.null if should_return_null else else_value)

        return res.success(Number.null)

    @classmethod
    def visit_ForNode(cls, node, context):
        res = RTResult()
        elements = []

        start_value = res.register(cls.visit(node.start_value_node, context))
        if res.should_return():
            return res

        end_value = res.register(cls.visit(node.end_value_node, context))
        if res.should_return():
            return res

        if node.step_value_node:
            step_value = res.register(cls.visit(node.step_value_node, context))
            if res.should_return():
                return res
        else:
            step_value = Number(1)

        i = start_value.value

        if step_value.value >= 0:
            condition = lambda: i < end_value.value
        else:
            condition = lambda: i > end_value.value

        while condition():
            context.symbol_table.set(node.var_name_token.value, Number(i))
            i += step_value.value

            value = res.register(cls.visit(node.body_node, context))
            if (
                res.should_return()
                and res.loop_should_continue is False
                and res.loop_should_break is False
            ):
                return res

            if res.loop_should_continue:
                continue

            if res.loop_should_break:
                break

            elements.append(value)

        return res.success(
            Number.null
            if node.should_return_null
            else List(elements)
            .set_context(context)
            .set_pos(node.pos_start, node.pos_end)
        )

    @classmethod
    def visit_WhileNode(cls, node, context):
        res = RTResult()
        elements = []

        while True:
            condition = res.register(cls.visit(node.condition_node, context))
            if res.should_return():
                return res

            if not condition.is_true():
                break

            value = res.register(cls.visit(node.body_node, context))
            if (
                res.should_return()
                and res.loop_should_continue is False
                and res.loop_should_break is False
            ):
                return res

            if res.loop_should_continue:
                continue

            if res.loop_should_break:
                break

            elements.append(value)

        return res.success(
            Number.null
            if node.should_return_null
            else List(elements)
            .set_context(context)
            .set_pos(node.pos_start, node.pos_end)
        )

    @classmethod
    def visit_FuncDefNode(cls, node, context):
        from TechZen.types.function_ import Function

        res = RTResult()

        func_name = node.var_name_token.value if node.var_name_token else None
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_name_tokens]
        func_value = (
            Function(func_name, body_node, arg_names, node.should_auto_return)
            .set_context(context)
            .set_pos(node.pos_start, node.pos_end)
        )

        if node.var_name_token:
            context.symbol_table.set(func_name, func_value)

        return res.success(func_value)

    @classmethod
    def visit_CallNode(cls, node, context):
        res = RTResult()
        args = []

        value_to_call = res.register(cls.visit(node.node_to_call, context))
        if res.should_return():
            return res
        value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)

        for arg_node in node.arg_nodes:
            args.append(res.register(cls.visit(arg_node, context)))
            if res.should_return():
                return res

        return_value = res.register(value_to_call.execute(args))
        if res.should_return():
            return res
        return_value = (
            return_value.copy()
            .set_pos(node.pos_start, node.pos_end)
            .set_context(context)
        )
        return res.success(return_value)

    @classmethod
    def visit_ReturnNode(cls, node, context):
        res = RTResult()

        if node.node_to_return:
            value = res.register(cls.visit(node.node_to_return, context))
            if res.should_return():
                return res
        else:
            value = Number.null

        return res.success_return(value)

    @classmethod
    def visit_ContinueNode(cls, node, context):
        return RTResult().success_continue()

    @classmethod
    def visit_BreakNode(cls, node, context):
        return RTResult().success_break()

    @classmethod
    def visit_ClassNode(cls, node, context):
        res = RTResult()

        ctx = Context(node.class_name_token.value, node.pos_start)
        ctx.symbol_table = SymbolTable(context.symbol_table)

        res.register(cls.visit(node.body_nodes, ctx))
        if res.should_return():
            return res

        cls_ = (
            Class(node.class_name_token.value, ctx.symbol_table)
            .set_context(context)
            .set_pos(node.pos_start, node.pos_end)
        )
        context.symbol_table.set(node.class_name_token.value, cls_)
        return res.success(cls_)

    @classmethod
    def visit_TryNode(cls, node, context):
        res = RTResult()
        _ = res.register(cls.visit(node.try_statements, context))
        broken = bool(res.should_return())
        if broken:
            _ = res.register(cls.visit(node.except_statements, context))
            if res.should_return():
                return res
        return res.success(Number.null)
