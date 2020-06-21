#!/usr/bin/env bash
export PYTHONPATH="$PYTHONPATH:$(pwd)/src"
echo 'def bina(a b) a + b' | pipenv run python src/ch01/lexer.py
#pipenv run python src/ch01/lexer.py 'def bina(a b) a + b'