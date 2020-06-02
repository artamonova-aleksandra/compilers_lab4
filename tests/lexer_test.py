import unittest
from lexer import Lexer


def get_types(data):
    lexer = Lexer()
    lexer.tokenize(data)
    tokens = []
    while lexer.next_exists():
        next_token = lexer.next()
        tokens.append(next_token.type)
    return tokens


class TestLexer(unittest.TestCase):
    def test_parentheses(self):
        data = '((()))'
        types = get_types(data)
        expected = ['LPAREN', 'LPAREN', 'LPAREN', 'RPAREN',
                    'RPAREN', 'RPAREN', 'END']
        self.assertEqual(types, expected)

    def test_mul_operations(self):
        data = '* / %'
        types = get_types(data)
        expected = ['MUL_OP', 'MUL_OP', 'MUL_OP', 'END']
        self.assertEqual(types, expected)

    def test_plus_operations(self):
        data = '+ -'
        types = get_types(data)
        expected = ['PLUS_OP', 'PLUS_OP', 'END']
        self.assertEqual(types, expected)

    def test_rel_operations(self):
        data = '<> <= >= = < >'
        types = get_types(data)
        expected = ['REL_OP', 'REL_OP', 'REL_OP', 'REL_OP',
                    'REL_OP', 'REL_OP', 'END']
        self.assertEqual(types, expected)

    def test_numbers(self):
        data = '1 23 123 -1 -23 -123'
        types = get_types(data)
        expected = ['NUMBER', 'NUMBER', 'NUMBER', 'NUMBER',
                    'NUMBER', 'NUMBER', 'END']
        self.assertEqual(types, expected)
