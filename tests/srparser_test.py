import unittest
from lexer import Lexer
from srparser import SRParser, SRParserException


def get_result(data):
    lexer = Lexer()
    parser = SRParser(lexer=lexer)
    return parser.parse(infix_str=data)


class TestSRParser(unittest.TestCase):
    def test_correct(self):
        data = '(1 + 2) * (3 + 4)'
        result = get_result(data)
        expected = '12+34+*'
        self.assertEqual(result, expected)

    def test_nested_correct(self):
        data = '(1 + (2 + 3 * 4)) <> ((3 + (4 + 6) + 4))'
        result = get_result(data)
        expected = '1234*++346++4+<>'
        self.assertEqual(result, expected)

    def test_miss_sign_close_error(self):
        data = '(1 + 4) 5'
        with self.assertRaises(SRParserException):
            get_result(data)

    def test_miss_sign_paren_error(self):
        data = '(1 + 1) (2 + 2)'
        with self.assertRaises(SRParserException):
            get_result(data)

    def test_digits_in_a_row_error(self):
        data = '1 + 1 2'
        with self.assertRaises(SRParserException):
            get_result(data)

    def test_miss_sign_open_error(self):
        data = '5 (1 + 4)'
        with self.assertRaises(SRParserException):
            get_result(data)

    def test_miss_closing_error(self):
        data = '((1+2)'
        with self.assertRaises(SRParserException):
            get_result(data)

    def test_miss_opening_error(self):
        data = '(1+2))'
        with self.assertRaises(SRParserException):
            get_result(data)

    def test_empty_error(self):
        data = ''
        with self.assertRaises(SRParserException):
            get_result(data)
