import sys

from ch01.lexer import Token
from ch02.parser import Parser

p = Parser()


def ready(nl=False):
    prefix = '\n' if nl else ''
    print(f'{prefix}ready> ', file=sys.stderr, end='', flush=True)


def info(msg):
    print(msg, file=sys.stderr, flush=True, end='')


def handle_top_level_expression():
    exp = p.parse_top_level_expr()
    if exp:
        info(f'\nEvaluate a top-level expression into an anonymous function: {exp}')
        ready(True)
    else:
        ready()
        p.next_token()  # Skip token for error recovery


def handle_extern():
    ext = p.parse_extern()
    if ext:
        info(f'\nParsed an extern: {ext}')
        ready(True)
    else:
        ready()
        p.next_token()  # Skip token for error recovery


def handle_definition():
    fn = p.parse_definition()
    if fn:
        info(f'\nParsed a function definition: {fn}')
        ready(True)
    else:
        ready()
        p.next_token()  # Skip token for error recovery


def main_loop():
    while True:
        curr = p.current_token
        if curr == Token.tok_eof:
            return
        elif curr == ';':
            p.next_token()
        elif curr == Token.tok_def:
            handle_definition()
        elif curr == Token.tok_extern:
            handle_extern()
        else:
            handle_top_level_expression()


if __name__ == '__main__':
    ready()
    p.next_token()
    main_loop()
