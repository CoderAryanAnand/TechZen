import unittest
from TechZen.lexer_ import Lexer
from TechZen.token_ import TokenType, Token


class TestLexer(unittest.TestCase):

    def test_empty(self):
        tokens = str(list(Lexer("<stdin>", "").make_tokens()))
        print([[Token(TokenType.TT_EOF)], None])
        self.assertEqual(tokens, "[[EOF], None]")

    def test_whitespace(self):
        tokens = str(list(Lexer("<stdin>", " \t\n  \t\t\n\n").make_tokens()))
        self.assertEqual(tokens, "[[NEWLINE, NEWLINE, NEWLINE, EOF], None]")

    def test_INTs(self):
        tokens = str(list(Lexer("<stdin>", "123 123.456 123. .456 .").make_tokens()))
        self.assertEqual(tokens, "[[INT:123, FLOAT:123.456, FLOAT:123.0, DOT, INT:456, DOT, EOF], None]")

    def test_operators(self):
        tokens = str(list(Lexer("<stdin>", "+-*/%//").make_tokens()))
        self.assertEqual(tokens, "[[PLUS, MINUS, DIV, MOD, DFL, EOF], None]")

    def test_parens(self):
        tokens = str(list(Lexer("<stdin>", "()").make_tokens()))
        self.assertEqual(tokens, "[[LPAREN, RPAREN, EOF], None]")

    def test_all(self):
        tokens = str(list(Lexer("<stdin>", "27 + (43 / 36 - 48) * 51").make_tokens()))
        self.assertEqual(tokens, "[[INT:27, PLUS, LPAREN, INT:43, DIV, INT:36, MINUS, INT:48, RPAREN, MUL, INT:51, "
                                 "EOF], None]")
