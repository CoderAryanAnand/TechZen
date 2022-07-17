import unittest

import sys
import os

current_file = os.path.realpath(__file__)
current_dir_tests = os.path.dirname(current_file)
parent_dir_parent_directory = os.path.dirname(current_dir_tests)
sys.path.insert(0, parent_dir_parent_directory)

from TechZen.lexer_ import Lexer
from TechZen.parser_ import Parser


class TestParser(unittest.TestCase):

    def test_empty(self):
        node = Parser(Lexer("<stdin>", "").make_tokens()[0]).parse().node
        self.assertEqual(node, None)

    def test_numbers(self):
        node = Parser(Lexer("<stdin>", "51.2").make_tokens()[0]).parse().node
        self.assertEqual(str(node.element_nodes), "[FLOAT:51.2]")

    def test_single_operations(self):

        # ADDITION
        node = Parser(Lexer("<stdin>", "27 + 14").make_tokens()[0]).parse().node
        self.assertEqual(str(node.element_nodes), "[(INT:27, PLUS, INT:14)]")

        # SUBTRACTION
        node = Parser(Lexer("<stdin>", "27 - 14").make_tokens()[0]).parse().node
        self.assertEqual(str(node.element_nodes), "[(INT:27, MINUS, INT:14)]")

        # MULTIPLICATION
        node = Parser(Lexer("<stdin>", "27 * 14").make_tokens()[0]).parse().node
        self.assertEqual(str(node.element_nodes), "[(INT:27, MUL, INT:14)]")

        # DIVISION
        node = Parser(Lexer("<stdin>", "27 / 14").make_tokens()[0]).parse().node
        self.assertEqual(str(node.element_nodes), "[(INT:27, DIV, INT:14)]")

        # FLOOR
        node = Parser(Lexer("<stdin>", "27 // 14").make_tokens()[0]).parse().node
        self.assertEqual(str(node.element_nodes), "[(INT:27, DFL, INT:14)]")

        # MODULO
        node = Parser(Lexer("<stdin>", "27 % 14").make_tokens()[0]).parse().node
        self.assertEqual(str(node.element_nodes), "[(INT:27, MOD, INT:14)]")

    def test_full_expression(self):
        node = Parser(Lexer("<stdin>", "27 + (43 / 36 - 38) * 51").make_tokens()[0]).parse().node
        self.assertEqual(str(node.element_nodes),
                         "[(INT:27, PLUS, (((INT:43, DIV, INT:36), MINUS, INT:38), MUL, INT:51))]")

    def test_if_statement(self):
        node = Parser(Lexer("<stdin>", "if TRUE then\nprint('hi')\nelse\nprint('bye')\nend").make_tokens()[0]).parse().node
        self.assertEqual(str(node.element_nodes[0])[:33],
                         "<TechZen.nodes_.IfNode object at ")

    def test_for_loop(self):
        node = Parser(Lexer("<stdin>", "for i = 0 to 5 then\nprint(i)\nend").make_tokens()[0]).parse().node
        self.assertEqual(str(node.element_nodes[0])[:34],
                         "<TechZen.nodes_.ForNode object at ")

    def test_while_loop(self):
        node = Parser(Lexer("<stdin>", "while TRUE then\nprint('hi'); break\nend").make_tokens()[0]).parse().node
        self.assertEqual(str(node.element_nodes[0])[:36],
                         "<TechZen.nodes_.WhileNode object at ")

    def test_func_def(self):
        node = Parser(Lexer("<stdin>", "fun add(a,b) -> a + b").make_tokens()[0]).parse().node
        self.assertEqual(str(node.element_nodes[0])[:38],
                         "<TechZen.nodes_.FuncDefNode object at ")

    def test_try_expr(self):
        node = Parser(Lexer("<stdin>", "try; print('a'); except; print('b'); end").make_tokens()[0]).parse().node
        self.assertEqual(str(node.element_nodes[0])[:34],
                         "<TechZen.nodes_.TryNode object at ")

    def test_class_def(self):
        node = Parser(Lexer("<stdin>", "class a; fun a(b); print(b); end; end;").make_tokens()[0]).parse().node
        self.assertEqual(str(node.element_nodes[0])[:36],
                         "<TechZen.nodes_.ClassNode object at ")

    def test_list_expr(self):
        node = Parser(Lexer("<stdin>", "[]").make_tokens()[0]).parse().node
        self.assertEqual(str(node.element_nodes[0])[:35],
                         "<TechZen.nodes_.ListNode object at ")

    def test_dict_expr(self):
        node = Parser(Lexer("<stdin>", "{}").make_tokens()[0]).parse().node
        self.assertEqual(str(node.element_nodes[0])[:35],
                         "<TechZen.nodes_.DictNode object at ")

    def test_continue(self):
        node = Parser(Lexer("<stdin>", "continue").make_tokens()[0]).parse().node
        self.assertEqual(str(node.element_nodes[0])[:39],
                         "<TechZen.nodes_.ContinueNode object at ")

    def test_break(self):
        node = Parser(Lexer("<stdin>", "break").make_tokens()[0]).parse().node
        self.assertEqual(str(node.element_nodes[0])[:36],
                         "<TechZen.nodes_.BreakNode object at ")

    def test_return(self):
        node = Parser(Lexer("<stdin>", "return").make_tokens()[0]).parse().node
        self.assertEqual(str(node.element_nodes[0])[:37],
                         "<TechZen.nodes_.ReturnNode object at ")

    def test_call(self):
        node = Parser(Lexer("<stdin>", "print()").make_tokens()[0]).parse().node
        self.assertEqual(str(node.element_nodes[0])[:35],
                         "<TechZen.nodes_.CallNode object at ")
