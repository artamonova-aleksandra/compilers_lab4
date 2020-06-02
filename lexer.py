from settings import Settings
from token import *
import re

token_regex = {Settings.NUMBER: r'[-]?\d+',
               Settings.PLUS_OP: r'\+|\-',
               Settings.MUL_OP: r'\*|\%|/',
               Settings.REL_OP: r'<>|<=|>=|=|<|>',
               Settings.LPAREN: '\(',
               Settings.RPAREN: '\)'}


class Lexer:
    def __init__(self):
        self._tokens = []
        self._index = 0

    def _reset(self):
        self._tokens = []
        self._index = 0

    def tokenize(self, infix_str):
        """Получить набор токенов для поданной на вход строки"""
        self._reset()

        pos = 0
        while pos < len(infix_str):
            match = None
            for key in token_regex:
                regex = re.compile(token_regex[key])
                match = regex.match(infix_str, pos)
                if match:
                    text = match.group(0)
                    self._tokens.append(Token(key, text))
                    pos = match.end(0)
                    break
            if not match:
                if infix_str[pos] == ' ' or '\n' or '\r' or '\t':
                    pos += 1
                else:
                    raise BaseException('Illegal character: %s\n' % infix_str[pos])

        self._tokens.append(token_end())

    def next_exists(self):
        """Проверить, есть ли следующий токен"""
        if self._index == len(self._tokens):
            return False
        return True

    def next(self):
        """Получить следующий токен"""
        if self.next_exists():
            token = self._tokens[self._index]
            self._index += 1
            return token
        return None


if __name__ == '__main__':
    lexer = Lexer()
    lexer.tokenize('(1+2)*3')
    while lexer.next_exists():
        next_token = lexer.next()
        print(next_token.type, next_token.value)
