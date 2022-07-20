from TechZen.errors_ import InvalidSyntaxError
from TechZen.nodes_ import *
from TechZen.token_ import TokenType, Keywords

#######################################
# PARSE RESULT
#######################################


class ParseResult:
    def __init__(self):
        """
        This is the parse result. This class checks if there are any errors, or successes.
        """
        self.error = None
        self.node = None
        self.last_registered_advance_count = 0
        self.advance_count = 0
        self.to_reverse_count = 0

    def register_advancement(self):
        """
        Register the advancement
        :return: nothing
        """
        self.last_registered_advance_count = 1
        self.advance_count += 1

    def register(self, res):
        """
        Register the result
        :param res: Result
        :return: Result node
        """
        self.last_registered_advance_count = res.advance_count
        self.advance_count += res.advance_count
        if res.error:
            self.error = res.error
        return res.node

    def try_register(self, res):
        """
        Try to register the result, else reverse the advances
        :param res: Result
        :return: self.register if it works, else None
        """
        if res.error:
            self.to_reverse_count = res.advance_count
            return None
        return self.register(res)

    def success(self, node):
        """
        This doesn't do much, just registers self.node = node.
        :param node: node
        :return: Parse result
        """
        self.node = node
        return self

    def failure(self, error):
        """
        Registers the failure, and saves the error.
        :param error: Error
        :return: Parse result
        """
        if not self.error or self.last_registered_advance_count == 0:
            self.error = error
        return self


#######################################
# PARSER
#######################################


class Parser:
    def __init__(self, tokens):
        """
        This is the parser. It looks if there is an illegal character error, or expected character error. It also
        finds out if the syntax for each expression / statement is correct. It also prioritizes things, for example,
        multiplication before addition.
        :param tokens: All the tokens found from the lexer
        """
        self.tokens = tokens
        self.token_idx = -1
        self.current_token = None
        self.advance()

    def advance(self):
        """
        Advances to the next token
        :return: Current token (after advancing)
        """
        self.token_idx += 1
        self.update_current_token()
        return self.current_token

    def reverse(self, amount=1):
        """
        Goes back to the previous token
        :param amount: How many tokens to go back, default 1
        :return: Current token
        """
        self.token_idx -= amount
        self.update_current_token()
        return self.current_token

    def update_current_token(self):
        """
        Update the current token
        :return: nothing
        """
        if 0 <= self.token_idx < len(self.tokens):
            self.current_token = self.tokens[self.token_idx]

    def parse(self):
        """
        This parses all the code. SEE GRAMMAR.TXT FOR MORE EXPLANATION.
        :return: Parse result
        """
        res = self.statements()
        if not res.error and self.current_token.type != TokenType.TT_EOF:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Expected '+', '-', '*', or '/'",
                )
            )
        return res

    ###################################

    def statements(self):
        """
        Parses all statements.
        :return: Parse result
        """
        res = ParseResult()
        statements = []
        pos_start = self.current_token.pos_start.copy()

        while self.current_token.type == TokenType.TT_NEWLINE:
            res.register_advancement()
            self.advance()

        statement = res.register(self.statement())
        if res.error:
            return res
        statements.append(statement)

        more_statements = True

        while True:
            newline_count = 0
            while self.current_token.type == TokenType.TT_NEWLINE:
                res.register_advancement()
                self.advance()
                newline_count += 1
            if newline_count == 0:
                more_statements = False
            if not more_statements:
                break
            statement = res.try_register(self.statement())
            if not statement:
                self.reverse(res.to_reverse_count)
                more_statements = False
                continue
            statements.append(statement)

        return res.success(
            ListNode(statements, pos_start, self.current_token.pos_end.copy())
        )

    def statement(self):
        """
        Parses all statements in statements.
        :return: Parse result
        """
        res = ParseResult()
        pos_start = self.current_token.pos_start.copy()

        if self.current_token.matches(TokenType.TT_KEYWORD, Keywords.KW_RETURN.value):
            res.register_advancement()
            self.advance()

            expr = res.try_register(self.expr())
            if not expr:
                self.reverse(res.to_reverse_count)
            return res.success(
                ReturnNode(expr, pos_start, self.current_token.pos_start.copy())
            )

        if self.current_token.matches(TokenType.TT_KEYWORD, Keywords.KW_CONTINUE.value):
            res.register_advancement()
            self.advance()
            return res.success(
                ContinueNode(pos_start, self.current_token.pos_start.copy())
            )

        if self.current_token.matches(TokenType.TT_KEYWORD, Keywords.KW_BREAK.value):
            res.register_advancement()
            self.advance()
            return res.success(
                BreakNode(pos_start, self.current_token.pos_start.copy())
            )

        expr = res.register(self.expr())
        if res.error:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Expected 'RETURN', 'CONTINUE', 'BREAK', 'VAR', 'IF', 'FOR', 'WHILE', 'CLASS', 'FUN', int, float, "
                    "identifier, "
                    "'+', '-', '(', '[' or 'NOT' ",
                )
            )
        return res.success(expr)

    def expr(self):
        """
        Parses all expressions.
        :return: Parse result
        """
        res = ParseResult()

        if self.current_token.matches(TokenType.TT_KEYWORD, Keywords.KW_VAR.value):
            res.register_advancement()
            self.advance()

            if self.current_token.type != TokenType.TT_IDENTIFIER:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        "Expected identifier",
                    )
                )

            var_name = self.current_token
            res.register_advancement()
            self.advance()

            extra_names = []

            while self.current_token.type == TokenType.TT_DOT:
                res.register_advancement()
                self.advance()

                if self.current_token.type != TokenType.TT_IDENTIFIER:
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_token.pos_start,
                            self.current_token.pos_end,
                            "Expected identifier",
                        )
                    )

                extra_names.append(self.current_token)

                res.register_advancement()
                self.advance()

            if self.current_token.type != TokenType.TT_EQ:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        "Expected '='",
                    )
                )

            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error:
                return res
            return res.success(VarAssignNode(var_name, expr, extra_names))

        node = res.register(
            self.bin_op(
                self.comp_expr,
                (
                    (TokenType.TT_KEYWORD, Keywords.KW_AND.value),
                    (TokenType.TT_KEYWORD, Keywords.KW_OR.value),
                ),
            )
        )

        if res.error:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Expected 'VAR', 'IF', 'FOR', 'WHILE', 'CLASS' 'FUN', int, float, identifier, '+', '-', '(', "
                    "'[' or 'NOT' ",
                )
            )

        return res.success(node)

    def comp_expr(self):
        """
        Parses all comparison expressions.
        :return: Parse result
        """
        res = ParseResult()
        if self.current_token.matches(TokenType.TT_KEYWORD, Keywords.KW_NOT.value):
            op_token = self.current_token
            res.register_advancement()
            self.advance()

            node = res.register(self.comp_expr())
            if res.error:
                return res

            return res.success(UnaryOpNode(op_token, node))

        node = res.register(
            self.bin_op(
                self.arith_expr,
                (
                    TokenType.TT_EE,
                    TokenType.TT_NE,
                    TokenType.TT_LT,
                    TokenType.TT_GT,
                    TokenType.TT_LTE,
                    TokenType.TT_GTE,
                ),
            )
        )
        if res.error:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Expected int, float, identifier, '+', '-', '[', '(', or 'NOT'",
                )
            )

        return res.success(node)

    def arith_expr(self):
        """
        Parses all arithmetic expressions.
        :return: Parse result
        """
        return self.bin_op(self.term, (TokenType.TT_PLUS, TokenType.TT_MINUS))

    def term(self):
        """
        Parses all terms.
        :return: Parse result
        """
        return self.bin_op(
            self.factor,
            (TokenType.TT_MUL, TokenType.TT_DIV, TokenType.TT_MOD, TokenType.TT_DFL),
        )

    def factor(self):
        """
        Parses all factors.
        :return: Parse result
        """
        res = ParseResult()
        token = self.current_token

        if token.type in (TokenType.TT_PLUS, TokenType.TT_MINUS):
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOpNode(token, factor))

        return self.power()

    def power(self):
        """
        Parses all powers.
        :return: Parse result
        """
        return self.bin_op(self.call, (TokenType.TT_POW,), self.factor)

    def call(self):
        """
        Parses all function calls.
        :return: Parse result
        """
        res = ParseResult()
        atom = res.register(self.atom())
        if res.error:
            return res

        while self.current_token.type == TokenType.TT_DOT:
            child = atom
            res.register_advancement()
            self.advance()

            child_ = res.register(self.call())
            if res.error:
                return res

            child.child = child_
            child = child_

        if self.current_token.type == TokenType.TT_LPAREN:
            res.register_advancement()
            self.advance()
            arg_nodes = []

            if self.current_token.type == TokenType.TT_RPAREN:
                res.register_advancement()
                self.advance()
            else:
                arg_nodes.append(res.register(self.expr()))
                if res.error:
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_token.pos_start,
                            self.current_token.pos_end,
                            "Expected ')', 'VAR', 'IF', 'FOR', 'WHILE', 'FUN', int, float, identifier, '+', '-', '(', "
                            "'[' or 'NOT' ",
                        )
                    )

                while self.current_token.type == TokenType.TT_COMMA:
                    res.register_advancement()
                    self.advance()

                    arg_nodes.append(res.register(self.expr()))
                    if res.error:
                        return res

                if self.current_token.type != TokenType.TT_RPAREN:
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_token.pos_start,
                            self.current_token.pos_end,
                            f"Expected ',' or ')'",
                        )
                    )

                res.register_advancement()
                self.advance()
            return res.success(CallNode(atom, arg_nodes))
        return res.success(atom)

    def atom(self):
        """
        Parses all atoms. (see grammar.txt for more explanation)
        :return: Parse result
        """
        # sourcery no-metrics skip: remove-unnecessary-else, swap-if-else-branches
        res = ParseResult()
        token = self.current_token

        if token.type in (TokenType.TT_INT, TokenType.TT_FLOAT):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(token))

        if token.type == TokenType.TT_STRING:
            res.register_advancement()
            self.advance()
            return res.success(StringNode(token))

        elif token.type == TokenType.TT_IDENTIFIER:
            res.register_advancement()
            self.advance()
            return res.success(VarAccessNode(token))

        elif token.type == TokenType.TT_LPAREN:
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error:
                return res
            if self.current_token.type == TokenType.TT_RPAREN:
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        "Expected ')'",
                    )
                )

        elif token.type == TokenType.TT_LSQUARE:
            list_expr = res.register(self.list_expr())
            if res.error:
                return res
            return res.success(list_expr)

        elif token.type == TokenType.TT_LCURLY:
            dict_expr = res.register(self.dict_expr())
            if res.error:
                return res
            return res.success(dict_expr)

        elif token.matches(TokenType.TT_KEYWORD, Keywords.KW_IF.value):
            if_expr = res.register(self.if_expr())
            if res.error:
                return res
            return res.success(if_expr)

        elif token.matches(TokenType.TT_KEYWORD, Keywords.KW_FOR.value):
            for_expr = res.register(self.for_expr())
            if res.error:
                return res
            return res.success(for_expr)

        elif token.matches(TokenType.TT_KEYWORD, Keywords.KW_WHILE.value):
            while_expr = res.register(self.while_expr())
            if res.error:
                return res
            return res.success(while_expr)

        elif token.matches(TokenType.TT_KEYWORD, Keywords.KW_FUN.value):
            func_def = res.register(self.func_def())
            if res.error:
                return res
            return res.success(func_def)

        elif token.matches(TokenType.TT_KEYWORD, Keywords.KW_CLASS.value):
            class_node = res.register(self.class_node())
            if res.error:
                return res
            return res.success(class_node)

        elif token.matches(TokenType.TT_KEYWORD, Keywords.KW_TRY.value):
            try_expr = res.register(self.try_expr())
            if res.error:
                return res
            return res.success(try_expr)

        return res.failure(
            InvalidSyntaxError(
                self.current_token.pos_start,
                self.current_token.pos_end,
                "Expected int, float, identifier, '+', '-', "
                "'(', '[', 'IF', 'FOR', 'WHILE', 'CLASS' or 'FUN'",
            )
        )

    def list_expr(self):
        """
        Parses all list expressions.
        :return: Parse result
        """
        res = ParseResult()
        element_nodes = []
        pos_start = self.current_token.pos_start.copy()

        if self.current_token.type != TokenType.TT_LSQUARE:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Expected '['",
                )
            )
        res.register_advancement()
        self.advance()

        if self.current_token.type == TokenType.TT_RSQUARE:
            res.register_advancement()
            self.advance()
        else:
            element_nodes.append(res.register(self.expr()))
            if res.error:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        "Expected ']', 'VAR', int, float, identifier, '+', '-', '[', or '('",
                    )
                )
            while self.current_token.type == TokenType.TT_COMMA:
                res.register_advancement()
                self.advance()

                element_nodes.append(res.register(self.expr()))
                if res.error:
                    return res
            if self.current_token.type != TokenType.TT_RSQUARE:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        "Expected ',' or ']'",
                    )
                )

            res.register_advancement()
            self.advance()
        return res.success(
            ListNode(element_nodes, pos_start, self.current_token.pos_end.copy())
        )

    def dict_expr(self):
        """
        Parses all dictionary expressions.
        :return: Parse result
        """
        res = ParseResult()
        element_nodes = {}
        pos_start = self.current_token.pos_start.copy()

        if self.current_token.type != TokenType.TT_LCURLY:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Expected '{'",
                )
            )
        res.register_advancement()
        self.advance()

        if self.current_token.type == TokenType.TT_RCURLY:
            res.register_advancement()
            self.advance()
        else:
            key = res.register(self.expr())
            if res.error:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        "Expected '}', 'VAR', int, float, identifier, '+', '-', '[', or '('",
                    )
                )

            if self.current_token.type != TokenType.TT_COLON:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        "Expected ':'",
                    )
                )
            res.register_advancement()
            self.advance()
            value = res.register(self.expr())
            if res.error:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        "Expected 'VAR', int, float, identifier, '+', '-', '[', or '('",
                    )
                )
            element_nodes[key] = value
            while self.current_token.type == TokenType.TT_COMMA:
                res.register_advancement()
                self.advance()

                key = res.register(self.expr())
                if res.error:
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_token.pos_start,
                            self.current_token.pos_end,
                            "Expected '}', 'VAR', int, float, identifier, '+', '-', '[', or '('",
                        )
                    )
                if self.current_token.type != TokenType.TT_COLON:
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_token.pos_start,
                            self.current_token.pos_end,
                            "Expected ':'",
                        )
                    )
                res.register_advancement()
                self.advance()
                value = res.register(self.expr())
                if res.error:
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_token.pos_start,
                            self.current_token.pos_end,
                            "Expected 'VAR', int, float, identifier, '+', '-', '[', or '('",
                        )
                    )
                element_nodes[key] = value
            if self.current_token.type != TokenType.TT_RCURLY:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        "Expected ',' or '}'",
                    )
                )

            res.register_advancement()
            self.advance()
        return res.success(
            DictNode(element_nodes, pos_start, self.current_token.pos_end.copy())
        )

    def if_expr(self):
        """
        Parses all if expressions (only if).
        :return: Parse result
        """
        res = ParseResult()
        all_cases = res.register(self.if_expr_cases(Keywords.KW_IF.value))
        if res.error:
            return res
        cases, else_case = all_cases
        return res.success(IfNode(cases, else_case))

    def if_expr_b(self):
        """
        Parses all if expressions (only elif).
        :return: Parse result
        """
        return self.if_expr_cases(Keywords.KW_ELIF.value)

    def if_expr_c(self):
        """
        Parses all if expressions (only else).
        :return: Parse result
        """
        res = ParseResult()
        else_case = None

        if self.current_token.matches(TokenType.TT_KEYWORD, Keywords.KW_ELSE.value):
            res.register_advancement()
            self.advance()

            if self.current_token.type == TokenType.TT_NEWLINE:
                res.register_advancement()
                self.advance()

                statements = res.register(self.statements())
                if res.error:
                    return res
                else_case = (statements, True)

                if not self.current_token.matches(
                    TokenType.TT_KEYWORD, Keywords.KW_END.value
                ):
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_token.pos_start,
                            self.current_token.pos_end,
                            "Expected 'END'",
                        )
                    )
                res.register_advancement()
                self.advance()
            else:
                expr = res.register(self.statement())
                if res.error:
                    return res
                else_case = (expr, False)

        return res.success(else_case)

    def if_expr_b_or_c(self):
        """
        Decides whether if expression is elif or else.
        :return: Parse result
        """
        res = ParseResult()
        cases, else_case = [], None

        if self.current_token.matches(TokenType.TT_KEYWORD, Keywords.KW_ELIF.value):
            all_cases = res.register(self.if_expr_b())
            if res.error:
                return res
            cases, else_case = all_cases
        else:
            else_case = res.register(self.if_expr_c())
            if res.error:
                return res

        return res.success((cases, else_case))

    def if_expr_cases(self, case_keyword):
        """
        Parses all if expressions.
        :return: Parse result
        """
        res = ParseResult()
        cases = []
        else_case = None

        if not self.current_token.matches(TokenType.TT_KEYWORD, case_keyword):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    f"Expected '{case_keyword}'",
                )
            )

        res.register_advancement()
        self.advance()

        condition = res.register(self.expr())
        if res.error:
            return res

        if not self.current_token.matches(TokenType.TT_KEYWORD, Keywords.KW_THEN.value):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Expected 'THEN'",
                )
            )

        res.register_advancement()
        self.advance()

        if self.current_token.type == TokenType.TT_NEWLINE:
            res.register_advancement()
            self.advance()

            statements = res.register(self.statements())
            if res.error:
                return res
            cases.append((condition, statements, True))

            if self.current_token.matches(TokenType.TT_KEYWORD, Keywords.KW_END.value):
                res.register_advancement()
                self.advance()
            else:
                all_cases = res.register(self.if_expr_b_or_c())
                if res.error:
                    return res
                new_cases, else_case = all_cases
                cases.extend(new_cases)
        else:
            expr = res.register(self.statement())
            if res.error:
                return res
            cases.append((condition, expr, False))

            all_cases = res.register(self.if_expr_b_or_c())
            if res.error:
                return res
            new_cases, else_case = all_cases
            cases.extend(new_cases)

        return res.success((cases, else_case))

    def for_expr(self):
        """
        Parses all for loops.
        :return: Parse result
        """
        res = ParseResult()

        if not self.current_token.matches(TokenType.TT_KEYWORD, Keywords.KW_FOR.value):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Expected 'FOR'",
                )
            )

        res.register_advancement()
        self.advance()

        if self.current_token.type != TokenType.TT_IDENTIFIER:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Expected identifier",
                )
            )

        var_name = self.current_token
        res.register_advancement()
        self.advance()

        if self.current_token.type != TokenType.TT_EQ:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Expected '='",
                )
            )

        res.register_advancement()
        self.advance()

        start_value = res.register(self.expr())
        if res.error:
            return res

        if not self.current_token.matches(TokenType.TT_KEYWORD, Keywords.KW_TO.value):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Expected 'TO'",
                )
            )

        res.register_advancement()
        self.advance()

        end_value = res.register(self.expr())
        if res.error:
            return res

        if self.current_token.matches(TokenType.TT_KEYWORD, Keywords.KW_STEP.value):
            res.register_advancement()
            self.advance()

            step_value = res.register(self.expr())
            if res.error:
                return res
        else:
            step_value = None

        if not self.current_token.matches(TokenType.TT_KEYWORD, Keywords.KW_THEN.value):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Expected 'THEN'",
                )
            )

        res.register_advancement()
        self.advance()

        if self.current_token.type == TokenType.TT_NEWLINE:
            res.register_advancement()
            self.advance()

            body = res.register(self.statements())
            if res.error:
                return res

            if not self.current_token.matches(
                TokenType.TT_KEYWORD, Keywords.KW_END.value
            ):
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        "Expected 'END'",
                    )
                )

            res.register_advancement()
            self.advance()

            return res.success(
                ForNode(var_name, start_value, end_value, step_value, body, True)
            )

        body = res.register(self.statement())
        if res.error:
            return res

        return res.success(
            ForNode(var_name, start_value, end_value, step_value, body, False)
        )

    def while_expr(self):
        """
        Parses all while loops.
        :return: Parse result
        """
        res = ParseResult()

        if not self.current_token.matches(
            TokenType.TT_KEYWORD, Keywords.KW_WHILE.value
        ):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Expected 'WHILE'",
                )
            )

        res.register_advancement()
        self.advance()

        condition = res.register(self.expr())
        if res.error:
            return res

        if not self.current_token.matches(TokenType.TT_KEYWORD, Keywords.KW_THEN.value):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Expected 'THEN'",
                )
            )

        res.register_advancement()
        self.advance()

        if self.current_token.type == TokenType.TT_NEWLINE:
            res.register_advancement()
            self.advance()

            body = res.register(self.statements())
            if res.error:
                return res

            if not self.current_token.matches(
                TokenType.TT_KEYWORD, Keywords.KW_END.value
            ):
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        "Expected 'END'",
                    )
                )

            res.register_advancement()
            self.advance()

            return res.success(WhileNode(condition, body, True))

        body = res.register(self.statement())
        if res.error:
            return res

        return res.success(WhileNode(condition, body, False))

    def class_node(self):
        """
        Parses all class nodes.
        :return: Parse result
        """
        res = ParseResult()

        pos_start = self.current_token.pos_start

        if not self.current_token.matches(
            TokenType.TT_KEYWORD, Keywords.KW_CLASS.value
        ):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Expected 'CLASS'",
                )
            )

        res.register_advancement()
        self.advance()

        if self.current_token.type != TokenType.TT_IDENTIFIER:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Expected identifier",
                )
            )

        class_name_token = self.current_token

        res.register_advancement()
        self.advance()

        if self.current_token.type != TokenType.TT_NEWLINE:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Expected NEWLINE",
                )
            )

        res.register_advancement()
        self.advance()

        body = res.register(self.statements())
        if res.error:
            return res

        if not self.current_token.matches(TokenType.TT_KEYWORD, Keywords.KW_END.value):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Expected 'END'",
                )
            )

        res.register_advancement()
        self.advance()

        return res.success(
            ClassNode(class_name_token, body, pos_start, self.current_token.pos_end)
        )

    def func_def(self):
        """
        Parses all function definitions.
        :return: Parse result
        """
        res = ParseResult()

        if not self.current_token.matches(TokenType.TT_KEYWORD, Keywords.KW_FUN.value):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Expected 'FUN'",
                )
            )

        res.register_advancement()
        self.advance()

        if self.current_token.type == TokenType.TT_IDENTIFIER:
            var_name_token = self.current_token
            res.register_advancement()
            self.advance()
            if self.current_token.type != TokenType.TT_LPAREN:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        "Expected '('",
                    )
                )
        else:
            var_name_token = None
            res.register_advancement()
            self.advance()
            if self.current_token.type != TokenType.TT_LPAREN:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        "Expected identifier or '('",
                    )
                )

        res.register_advancement()
        self.advance()
        arg_name_tokens = []

        if self.current_token.type == TokenType.TT_IDENTIFIER:
            arg_name_tokens.append(self.current_token)
            res.register_advancement()
            self.advance()

            while self.current_token.type == TokenType.TT_COMMA:
                res.register_advancement()
                self.advance()

                if self.current_token.type != TokenType.TT_IDENTIFIER:
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_token.pos_start,
                            self.current_token.pos_end,
                            "Expected identifier",
                        )
                    )

                arg_name_tokens.append(self.current_token)
                res.register_advancement()
                self.advance()

            if self.current_token.type != TokenType.TT_RPAREN:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        "Expected ',' or ')'",
                    )
                )
        elif self.current_token.type != TokenType.TT_RPAREN:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Expected identifier or ')'",
                )
            )

        res.register_advancement()
        self.advance()

        if self.current_token.type == TokenType.TT_ARROW:
            res.register_advancement()
            self.advance()
            body = res.register(self.expr())
            if res.error:
                return res
            return res.success(FuncDefNode(var_name_token, arg_name_tokens, body, True))

        if self.current_token.type != TokenType.TT_NEWLINE:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Expected '->', or NEWLINE",
                )
            )

        res.register_advancement()
        self.advance()

        body = res.register(self.statements())
        if res.error:
            return res

        if not self.current_token.matches(TokenType.TT_KEYWORD, Keywords.KW_END.value):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Expected 'END'",
                )
            )

        res.register_advancement()
        self.advance()

        return res.success(FuncDefNode(var_name_token, arg_name_tokens, body, False))

    def try_expr(self):
        """
        Parses all try expressions.
        :return: Parse result
        """
        res = ParseResult()
        pos_start = self.current_token.pos_start

        if not self.current_token.matches(TokenType.TT_KEYWORD, Keywords.KW_TRY.value):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Expected 'TRY'",
                )
            )

        res.register_advancement()
        self.advance()

        if self.current_token.type != TokenType.TT_NEWLINE:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Expected NEWLINE",
                )
            )

        res.register_advancement()
        self.advance()

        try_statements = res.register(self.statements())
        if res.error:
            return res

        while not self.current_token.matches(
            TokenType.TT_KEYWORD, Keywords.KW_EXCEPT.value
        ):
            res.register_advancement()
            self.advance()
            if self.current_token.matches(TokenType.TT_KEYWORD, Keywords.KW_END.value):
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        "Expected 'EXCEPT'",
                    )
                )

        res.register_advancement()
        self.advance()

        if self.current_token.type != TokenType.TT_NEWLINE:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Expected NEWLINE",
                )
            )

        res.register_advancement()
        self.advance()

        except_statements = res.register(self.statements())
        if res.error:
            print(res)

        if not self.current_token.matches(TokenType.TT_KEYWORD, Keywords.KW_END.value):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Expected 'END'",
                )
            )

        res.register_advancement()
        self.advance()

        return res.success(
            TryNode(
                try_statements, except_statements, pos_start, self.current_token.pos_end
            )
        )

    ###################################

    def bin_op(self, func_a, ops, func_b=None):
        if func_b is None:
            func_b = func_a
        res = ParseResult()
        left = res.register(func_a())
        if res.error:
            return res

        while (
            self.current_token.type in ops
            or (self.current_token.type, self.current_token.value) in ops
        ):
            op_token = self.current_token
            res.register_advancement()
            self.advance()
            right = res.register(func_b())
            if res.error:
                return res
            left = BinOpNode(left, op_token, right)

        return res.success(left)
