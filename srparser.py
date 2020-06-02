from settings import Settings
from tokens import *

matrix_keys = [Settings.RPAREN, Settings.NUMBER, Settings.MUL_OP,
               Settings.PLUS_OP, Settings.REL_OP, Settings.LPAREN,
               Settings.END]

matrix = [['>', '0', '>', '>', '>', '1', '>'],  # RPAREN
          ['>', '2', '>', '>', '>', '3', '>'],  # NUMBER
          ['>', '<', '>', '>', '>', '<', '>'],  # MUL_OP
          ['>', '<', '<', '>', '>', '<', '>'],  # PLUS_OP
          ['>', '<', '<', '<', '>', '<', '>'],  # REL_OP
          ['=', '<', '<', '<', '<', '<', '4'],  # LPAREN
          ['5', '<', '<', '<', '<', '<', '6']]  # END


def get_precedence(curr_token, next_token):
    if not isinstance(curr_token, Token) or not isinstance(next_token, Token):
        raise TypeError('Values must belong to the Token class')

    curr_index = matrix_keys.index(curr_token.type)
    next_index = matrix_keys.index(next_token.type)

    result = matrix[curr_index][next_index]
    return result


class SRParserException(Exception):
    def __init__(self, error_code=None):
        self.error_code = error_code

    def __str__(self):
        if self.error_code == '0':
            return 'Missing sign between closing parenthesis and number'
        elif self.error_code == '1':
            return 'Missing sign between parentheses'
        elif self.error_code == '2':
            return 'Two digits cannot go in a row'
        elif self.error_code == '3':
            return 'Missing sign between number and opening parenthesis'
        elif self.error_code == '4':
            return 'Missing closing parenthesis'
        elif self.error_code == '5':
            return 'Missing opening parenthesis'
        elif self.error_code == '6':
            return 'The string is empty'
        else:
            return 'Syntax error'


class SRParser:
    def __init__(self, lexer):
        self._lexer = lexer
        self._stack = []
        self._rpn = []

    def _reset(self):
        self._stack = []
        self._rpn = []

    def _check_end(self):
        """True, если stack == [$ N $]"""
        if len(self._stack) == 3:
            if [t.type for t in self._stack] == [Settings.END,
                                                 Settings.NON_TERM,
                                                 Settings.END]:
                return True
        return False

    def _debug_print_stack(self):
        print('stack = [', ' '.join([x.value for x in self._stack]) + ' ]')

    def parse(self, infix_str):
        self._reset()
        self._lexer.tokenize(infix_str)
        self._stack = [token_end()]

        while not self._check_end():
            if len(self._stack) == 0 or not self._lexer.next_exists():
                raise SRParserException()

            stack_token = [x for x in self._stack if x.type != 'NON_TERM'][-1]
            lex_token = self._lexer.next()
            precedence = get_precedence(stack_token, lex_token)

            # Перенос
            if precedence in ['<', '=']:
                self._stack.append(lex_token)

            # Свертка
            elif precedence == '>':
                while precedence not in ['<', '=']:
                    if stack_token.type == 'END' and lex_token.type == 'END':
                        break

                    if precedence not in Settings.PRECEDENCE:
                        raise SRParserException(error_code=precedence)

                    if self._stack[-1].type == Settings.NUMBER:
                        # Свертка N -> 0|..|9
                        self._rpn.append(self._stack.pop().value)
                        self._stack.append(token_non_term())

                    elif self._stack[-1].type == Settings.NON_TERM and len(self._stack) >= 4:
                        # Свертка N -> N op N
                        expr = self._stack[-3:]
                        operator = expr[1]
                        self._stack = self._stack[:-2]
                        self._rpn.append(operator.value)

                    elif self._stack[-1].type == Settings.RPAREN and len(self._stack) >= 4:
                        # Свертка N -> ( N )
                        self._stack = self._stack[:-3]
                        self._stack.append(token_non_term())

                    stack_token = [x for x in self._stack if x.type != Settings.NON_TERM][-1]
                    precedence = get_precedence(stack_token, lex_token)

                self._stack.append(lex_token)

            # Ошибка
            else:
                raise SRParserException(error_code=precedence)

        return ''.join(self._rpn)
