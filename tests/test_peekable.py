from pythonlisp.peekable import Peekable


def test_peekable():
    items = (i for i in range(100))
    p = Peekable(items)
    assert p.peekn(1) == 0
    assert p.peekn(2) == 1
    assert next(p) == 0
    assert next(p) == 1
    assert next(p) == 2
    assert p.peekn(3) == 5
