import sys
from enum import Enum
from typing import Optional, Union


class Token(Enum):
    tok_eof = -1
    # commands
    tok_def = -2
    tok_extern = -3

    # primary
    tok_identifier = -4
    tok_number = -5


class Lexer:
    def __init__(self, buff: str):
        self.__buffer = buff
        self.__buffer_cursor = 0
        self.__identifier_str = ''
        self.__num_val = 0
        self.__last_char = ' '

    @property
    def identifier_str(self) -> str:
        """
        If the current token is an identifier, identifier_str holds the name of the identifier
        """
        return self.__identifier_str

    @property
    def num_val(self) -> float:
        """
        If the current token is a numeric literal (like 1.0), NumVal holds its value.
        """
        return self.__num_val

    def getchar(self) -> Optional[str]:
        if self.__buffer_cursor >= len(self.__buffer):
            return None
        c = self.__buffer[self.__buffer_cursor]
        self.__buffer_cursor += 1
        return c

    def __isnum(self) -> bool:
        return self.__last_char and (self.__last_char.isdigit() or self.__last_char == '.')

    def __isalpha(self) -> bool:
        return self.__last_char and self.__last_char.isalpha()

    def __isalnum(self) -> bool:
        return self.__last_char and self.__last_char.isalnum()

    def __isspace(self) -> bool:
        return self.__last_char and self.__last_char.isspace()

    def gettok(self) -> Union[Token, str]:
        """
        :return: the next token from buffer.
        """
        # skip white spaces
        while self.__isspace():
            self.__last_char = self.getchar()

        if self.__isalpha():
            self.__identifier_str = self.__last_char
            self.__last_char = self.getchar()
            while self.__isalnum():
                self.__identifier_str += self.__last_char
                self.__last_char = self.getchar()
            if self.identifier_str == 'def':
                return Token.tok_def
            if self.identifier_str == 'extern':
                return Token.tok_extern
            return Token.tok_identifier

        if self.__isnum():
            num_str = ''
            while self.__isnum():
                num_str += self.__last_char
                self.__last_char = self.getchar()
            self.__num_val = float(num_str)
            return Token.tok_number

        if self.__last_char and self.__last_char == '#':
            while self.__last_char and self.__last_char != '\n' and self.__last_char != '\r':
                self.__last_char = self.getchar()
            if self.__last_char:
                return self.gettok()

        if not self.__last_char:
            return Token.tok_eof

        this_char = self.__last_char
        self.__last_char = self.getchar()
        return this_char


if __name__ == '__main__':
    buffer = '\n'.join([l.rstrip() for l in sys.stdin])
    print(f'str: {buffer}')

    lexer = Lexer(buffer)

    t = lexer.gettok()

    while t != Token.tok_eof:
        if t == Token.tok_identifier:
            print(f'identifier: {lexer.identifier_str}')
        elif t == Token.tok_number:
            print(f'number: {lexer.num_val}')
        else:
            print(f'token: {t}')
        t = lexer.gettok()
