import unittest
from TechZen.nodes_ import *
from TechZen.lexer_ import Lexer
from TechZen.parser_ import Parser
from TechZen.interpreter_ import Interpreter
from TechZen.types.number_ import Number

from TechZen.global_symbol_table_ import global_symbol_table
from TechZen.context_ import Context

interpreter = Interpreter()
context = Context('<program>')
context.symbol_table = global_symbol_table


class TestInterpreter(unittest.TestCase):

    def test_numbers(self):
        value = Interpreter().visit(Parser(Lexer("<stdin>", "51.2").make_tokens()[0]).parse().node, context).value
        self.assertEqual(str(value), "51.2")

    def test_string(self):
        value = Interpreter().visit(Parser(Lexer("<stdin>", "'[51.2]'").make_tokens()[0]).parse().node, context).value
        self.assertEqual(str(value), "[51.2]")

    def test_list(self):
        value = Interpreter().visit(Parser(Lexer("<stdin>", "[51.2, 3]").make_tokens()[0]).parse().node, context).value
        self.assertEqual(str(value), "51.2, 3")

    def test_dict(self):
        value = Interpreter().visit(
            Parser(Lexer("<stdin>", "{'a': 51.2}").make_tokens()[0]).parse().node, context).value
        self.assertEqual(str(value), "{a: 51.2}")

    def test_single_operations(self):
        result = Interpreter().visit(Parser(Lexer("<stdin>", "27 + 14").make_tokens()[0]).parse().node, context).value
        self.assertEqual(str(result), "41")

        result = Interpreter().visit(Parser(Lexer("<stdin>", "27 - 14").make_tokens()[0]).parse().node, context).value
        self.assertEqual(str(result), "13")

        result = Interpreter().visit(Parser(Lexer("<stdin>", "27 * 14").make_tokens()[0]).parse().node, context).value
        self.assertEqual(str(result), "378")

        result = Interpreter().visit(Parser(Lexer("<stdin>", "28 / 14").make_tokens()[0]).parse().node, context).value
        self.assertEqual(str(result), "2.0")

        self.assertRaises(Exception,
                          Interpreter().visit(Parser(Lexer("<stdin>",
                                                           "28 / 0").make_tokens()[0]).parse().node, context).value)

    def test_variable(self):
        result = Interpreter().visit(
            Parser(
                Lexer("<stdin>",
                      "run('file_tests/variable_test.techzen')").make_tokens()[0]).parse().node, context).value

        self.assertEqual(str(result), "0")

    def test_if(self):
        result = Interpreter().visit(
            Parser(
                Lexer("<stdin>",
                      "run('file_tests/if_test.techzen')").make_tokens()[0]).parse().node, context).value

        self.assertEqual(str(result), "0")

    def test_for(self):
        result = Interpreter().visit(
            Parser(
                Lexer("<stdin>",
                      "run('file_tests/for_test.techzen')").make_tokens()[0]).parse().node, context).value

        self.assertEqual(str(result), "0")

    def test_while(self):
        result = Interpreter().visit(
            Parser(
                Lexer("<stdin>",
                      "run('file_tests/while_test.techzen')").make_tokens()[0]).parse().node, context).value

        self.assertEqual(str(result), "0")

    def test_function(self):
        result = Interpreter().visit(
            Parser(
                Lexer("<stdin>",
                      "run('file_tests/function_test.techzen')").make_tokens()[0]).parse().node, context).value

        self.assertEqual(str(result), "0")

    def test_class(self):
        result = Interpreter().visit(
            Parser(
                Lexer("<stdin>",
                      "run('file_tests/class_test.techzen')").make_tokens()[0]).parse().node, context).value

        self.assertEqual(str(result), "0")

    def test_try(self):
        result = Interpreter().visit(
            Parser(
                Lexer("<stdin>",
                      "run('file_tests/try_test.techzen')").make_tokens()[0]).parse().node, context).value

        self.assertEqual(str(result), "0")
