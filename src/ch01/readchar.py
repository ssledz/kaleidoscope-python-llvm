import os
import sys
import termios
import tty
from abc import ABC

_EOF = 4


class CharReader(ABC):
    def getchar(self) -> str:
        pass

    @staticmethod
    def new():
        is_interactive = os.isatty(sys.stdin.fileno())
        if is_interactive:
            return InteractiveCharReader()
        else:
            return BufferedCharReader('\n'.join([l.rstrip() for l in sys.stdin]))


class BufferedCharReader(CharReader):
    def __init__(self, buffer: str):
        self._buffer = buffer
        self._current_index = 0

    def getchar(self):
        if self._current_index >= len(self._buffer):
            return None
        c = self._buffer[self._current_index]
        self._current_index += 1
        return c


class InteractiveCharReader(CharReader):
    def getchar(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            if ord(ch) == _EOF:
                return None
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        if ord(ch) != 13:
            print(ch, file=sys.stderr, end='', flush=True)
        return ch
