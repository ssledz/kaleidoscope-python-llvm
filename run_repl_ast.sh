#!/usr/bin/env bash
export PYTHONPATH="$PYTHONPATH:$(pwd)/src"
pipenv run python src/ch02/repl.py
