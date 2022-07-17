from TechZen.lexer_ import Lexer
from TechZen.parser_ import Parser
from TechZen.interpreter_ import Interpreter
from TechZen.context_ import Context


class Runner:
    @staticmethod
    def run(fn, text):
        from TechZen.global_symbol_table_ import global_symbol_table
        from TechZen.lexer_ import Lexer
        # Generate tokens
        lexer = Lexer(fn, text)
        tokens, error = lexer.make_tokens()
        if error:
            return None, error, False

        # Generate Abstract Syntax Tree (AST)
        parser = Parser(tokens)
        ast = parser.parse()
        if ast.error:
            return None, ast.error, False

        # Run program
        interpreter = Interpreter()
        context = Context('<program>')
        context.symbol_table = global_symbol_table
        result = interpreter.visit(ast.node, context)

        return result.value, result.error, result.should_exit
