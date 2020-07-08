import sys
from enum import Enum
from typing import Optional, Union

from ch01.readchar import CharReader, BufferedCharReader


class Token(Enum):
    tok_eof = -1
    # commands
    tok_def = -2
    tok_extern = -3

    # primary
    tok_identifier = -4
    tok_number = -5


class Lexer:
    def __init__(self, char_reader=None):
        self._char_reader = char_reader or CharReader.new()
        self.__identifier_str = ''
        self.__num_val = 0
        self.__last_char = None

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
        return self._char_reader.getchar()

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

        if not self.__last_char:
            self.__last_char = self.getchar()

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
        self.__last_char = None
        return this_char


if __name__ == '__main__':

    lexer = Lexer()

    if len(sys.argv) == 2:
        lexer = Lexer(BufferedCharReader(sys.argv[1]))

    t = lexer.gettok()

    while t != Token.tok_eof:
        if t == Token.tok_identifier:
            print(f'identifier: {lexer.identifier_str}')
        elif t == Token.tok_number:
            print(f'number: {lexer.num_val}')
        else:
            print(f'token: {t}')
        t = lexer.gettok()
