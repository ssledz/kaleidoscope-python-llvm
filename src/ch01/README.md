## example

```bash
echo 'def add(a b) a + b' | python src/ch01/lexer.py
```

```bash
str: def add(a b) a + b
token: Token.tok_def
identifier: add
token: (
identifier: a
identifier: b
token: )
identifier: a
token: +
identifier: b
```

## resources:
* [Kaleidoscope Introduction and the Lexer](http://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl01.html)