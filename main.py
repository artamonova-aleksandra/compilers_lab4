from srparser import SRParser
from lexer import Lexer

if __name__ == '__main__':
    infix_str = '(1 + 2) * (3 + 4) * 5 + (6 > (7 + 8))'
    lexer = Lexer()
    parser = SRParser(lexer=lexer)
    result = parser.parse(infix_str=infix_str)
    print(result)
