def foo():
    return 1

def bar():
    return 2

def xd(case):
    return {
        'a': foo,
        'b': bar
    }[case]()


print(xd('a'))
print(xd('b'))