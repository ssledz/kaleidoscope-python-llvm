import sys
from ch01.lexer import Lexer, Token
from ch02.parser import Parser

if __name__ == '__main__':
    # from ch01.readchar import BufferedCharReader
    # p = Parser(Lexer(BufferedCharReader('def bina(a b) a + b')))

    p = Parser()
    print('ready> ', file=sys.stderr)
    p.next_token()

    while(True):
        print('ready> ', file=sys.stderr)
        {
            Token.tok_eof: lambda : sys.exit(0)
        }
