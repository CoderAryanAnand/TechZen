# TODO docstring

class NumberNode:
    def __init__(self, token):
        """
        This is the number node in the AST that's parsed in the Parser.
        :param token: Number
        """
        self.token = token

        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end

        self.child = None

    def __repr__(self):
        return f"{self.token}"


class StringNode:
    def __init__(self, token):
        """
        This is the string node in the AST that's parsed in the Parser.
        :param token: String
        """
        self.token = token

        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end

        self.child = None

    def __repr__(self):
        return f"{self.token}"


class ListNode:
    def __init__(self, element_nodes, pos_start, pos_end):
        """
        This is the list node in the AST that's parsed in the Parser.
        :param element_nodes: Elements of the list
        :param pos_start: Start position
        :param pos_end: End position
        """
        self.element_nodes = element_nodes

        self.pos_start = pos_start
        self.pos_end = pos_end

        self.child = None


class DictNode:
    def __init__(self, element_nodes, pos_start, pos_end):
        """
        This is the dictionary node in the AST that's parsed in the Parser.
        :param element_nodes: Elements of the dictionary
        :param pos_start: Start position
        :param pos_end: End position
        """
        self.element_nodes = element_nodes

        self.pos_start = pos_start
        self.pos_end = pos_end

        self.child = None


class VarAccessNode:
    def __init__(self, var_name_token):
        """
        This is the variable access node in the AST that's parsed in the Parser.'
        :param var_name_token: Variable name
        """
        self.var_name_token = var_name_token

        self.pos_start = self.var_name_token.pos_start
        self.pos_end = self.var_name_token.pos_end

        self.child = None


class VarAssignNode:
    def __init__(self, var_name_token, value_node, extra_names=None):
        """
        This is the variable assign node in the AST that's parsed in the Parser.'
        :param var_name_token: Variable name
        :param value_node: Variable value
        :param extra_names: Extra names
        """
        if extra_names is None:
            extra_names = []
        self.var_name_token = var_name_token
        self.value_node = value_node
        self.extra_names = extra_names

        self.pos_start = self.var_name_token.pos_start
        self.pos_end = (
            self.extra_names[len(self.extra_names) - 1].pos_end
            if len(self.extra_names) > 0
            else self.var_name_token.pos_end
        )

        self.child = None


class BinOpNode:
    def __init__(self, left_node, op_token, right_node):
        """
        This is the binary operation node in the AST that's parsed in the Parser.'
        :param left_node: The node on the left of the operator
        :param op_token: The operator token
        :param right_node: The node on the right of the operator
        """
        self.left_node = left_node
        self.op_token = op_token
        self.right_node = right_node

        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

        self.child = None

    def __repr__(self):
        return f"({self.left_node}, {self.op_token}, {self.right_node})"


class UnaryOpNode:
    def __init__(self, op_token, node):
        """
        This is the unary operation node in the AST that's parsed in the Parser.
        :param op_token: The operator token
        :param node: The node after the operator
        """
        self.op_token = op_token
        self.node = node

        self.pos_start = self.op_token.pos_start
        self.pos_end = node.pos_end

        self.child = None

    def __repr__(self):
        return f"({self.op_token}, {self.node})"


class IfNode:
    def __init__(self, cases, else_case):
        """
        This is the if node in the AST that's parsed in the Parser.
        :param cases: All the cases in the if statement
        :param else_case: The else case of the if statement
        """
        self.cases = cases
        self.else_case = else_case

        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = (self.else_case or self.cases[len(self.cases) - 1])[0].pos_end

        self.child = None


class ForNode:
    def __init__(
        self,
        var_name_token,
        start_value_node,
        end_value_node,
        step_value_node,
        body_node,
        should_return_null,
    ):
        """
        This is the for node in the AST that's parsed in the Parser.'
        :param var_name_token: The variable name
        :param start_value_node: The start value
        :param end_value_node: The end value
        :param step_value_node: The step value
        :param body_node: The code in the for loop
        :param should_return_null: The should return null value
        """
        self.var_name_token = var_name_token
        self.start_value_node = start_value_node
        self.end_value_node = end_value_node
        self.step_value_node = step_value_node
        self.body_node = body_node
        self.should_return_null = should_return_null

        self.pos_start = self.var_name_token.pos_start
        self.pos_end = self.body_node.pos_end

        self.child = None


class WhileNode:
    def __init__(self, condition_node, body_node, should_return_null):
        """
        This is the while node in the AST that's parsed in the Parser.
        :param condition_node: The condition
        :param body_node: The code in the while loop
        :param should_return_null: The should return null value
        """
        self.condition_node = condition_node
        self.body_node = body_node
        self.should_return_null = should_return_null

        self.pos_start = self.condition_node.pos_start
        self.pos_end = self.body_node.pos_end

        self.child = None


class FuncDefNode:
    def __init__(self, var_name_token, arg_name_tokens, body_node, should_auto_return):
        """
        This is the function definition node in the AST that's parsed in the Parser.
        :param var_name_token: The function name
        :param arg_name_tokens: The arguments
        :param body_node: The function code
        :param should_auto_return: The should auto return value
        """
        self.var_name_token = var_name_token
        self.arg_name_tokens = arg_name_tokens
        self.body_node = body_node
        self.should_auto_return = should_auto_return

        if self.var_name_token:
            self.pos_start = self.var_name_token.pos_start
        elif len(self.arg_name_tokens) > 0:
            self.pos_start = self.arg_name_tokens[0].pos_start
        else:
            self.pos_start = self.body_node.pos_start

        self.pos_end = self.body_node.pos_end

        self.child = None


class CallNode:
    def __init__(self, node_to_call, arg_nodes):
        """
        This is the call node in the AST that's parsed in the Parser.
        :param node_to_call: The function / class to call
        :param arg_nodes: The arguments
        """
        self.node_to_call = node_to_call
        self.arg_nodes = arg_nodes

        self.pos_start = self.node_to_call.pos_start

        if len(self.arg_nodes) > 0:
            self.pos_end = self.arg_nodes[len(self.arg_nodes) - 1].pos_end
        else:
            self.pos_end = self.node_to_call.pos_end

        self.child = None


class ReturnNode:
    def __init__(self, node_to_return, pos_start, pos_end):
        """
        This is the return node in the AST that's parsed in the Parser.
        :param node_to_return: The node to return
        :param pos_start: Start position
        :param pos_end: End position
        """
        self.node_to_return = node_to_return

        self.pos_start = pos_start
        self.pos_end = pos_end

        self.child = None


class ContinueNode:
    def __init__(self, pos_start, pos_end):
        """
        This is the continue node in the AST that's parsed in the Parser.
        :param pos_start: Start position
        :param pos_end: End position
        """
        self.pos_start = pos_start
        self.pos_end = pos_end

        self.child = None


class BreakNode:
    def __init__(self, pos_start, pos_end):
        """
        This is the break node in the AST that's parsed in the Parser.
        :param pos_start: Start position
        :param pos_end: End position
        """
        self.pos_start = pos_start
        self.pos_end = pos_end

        self.child = None


class ClassNode:
    def __init__(self, class_name_token, body_nodes, pos_start, pos_end):
        """
        This is the class node in the AST that's parsed in the Parser.
        :param class_name_token: The class name
        :param body_nodes: The functions in the class
        :param pos_start: Start position
        :param pos_end: End position
        """
        self.class_name_token = class_name_token
        self.body_nodes = body_nodes
        self.pos_start = pos_start
        self.pos_end = pos_end

        self.child = None


class TryNode:
    def __init__(self, try_statements, except_statements, pos_start, pos_end):
        """
        This is the try node in the AST that's parsed in the Parser.
        :param try_statements: Code in the try section
        :param except_statements: Code in the except section
        :param pos_start: Start position
        :param pos_end: End position
        """
        self.try_statements = try_statements
        self.except_statements = except_statements
        self.pos_start = pos_start
        self.pos_end = pos_end

        self.child = None
