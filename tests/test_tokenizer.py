from pythonlisp.tokenizer import tokenize, TokenKind, Offset


def test_tokenize():
    test1 = """
(define x 10)
(define y 1.1)
(define s "This is the String")
x
s
(define f (lambda (x y) (+ x y)))
"""
    expect1 = [
        (TokenKind.LEFTPAR, "(", None, Offset(2, 1)),
        (TokenKind.SYMBOL, 'define', 'define', Offset(2, 2)),
        (TokenKind.SYMBOL, 'x', 'x', Offset(2, 9)),
        (TokenKind.NUMBER, '10', 10, Offset(2, 11)),
        (TokenKind.RIGHTPAR, ")", None, Offset(2, 13)),
        (TokenKind.LEFTPAR, "(", None, Offset(3, 1)),
        (TokenKind.SYMBOL, 'define', 'define', Offset(3, 2)),
        (TokenKind.SYMBOL, 'y', 'y', Offset(3, 9)),
        (TokenKind.NUMBER, '1.1', 1.1, Offset(3, 11)),
        (TokenKind.RIGHTPAR, ")", None, Offset(3, 14)),
        (TokenKind.LEFTPAR, "(", None, Offset(4, 1)),
        (TokenKind.SYMBOL, 'define', 'define', Offset(4, 2)),
        (TokenKind.SYMBOL, 's', 's', Offset(4, 9)),
        (TokenKind.STRING, '\"This is the String\"', "This is the String", Offset(4, 11)),
        (TokenKind.RIGHTPAR, ")", None, Offset(4, 31)),
        (TokenKind.SYMBOL, "x", "x", Offset(5, 1)),
        (TokenKind.SYMBOL, "s", "s", Offset(6, 1)),
        (TokenKind.LEFTPAR, "(", None, Offset(7, 1)),
        (TokenKind.SYMBOL, 'define', 'define', Offset(7, 2)),
        (TokenKind.SYMBOL, 'f', 'f', Offset(7, 9)),
        (TokenKind.LEFTPAR, '(', None, Offset(7, 11)),
        (TokenKind.SYMBOL, "lambda", 'lambda', Offset(7, 12)),
        (TokenKind.LEFTPAR, '(', None, Offset(7, 19)),
        (TokenKind.SYMBOL, 'x', 'x', Offset(7, 20)),
        (TokenKind.SYMBOL, 'y', 'y', Offset(7, 22)),
        (TokenKind.RIGHTPAR, ')', None, Offset(7, 23)),
        (TokenKind.LEFTPAR, '(', None, Offset(7, 25)),
        (TokenKind.SYMBOL, '+', '+', Offset(7, 26)),
        (TokenKind.SYMBOL, 'x', 'x', Offset(7, 28)),
        (TokenKind.SYMBOL, 'y', 'y', Offset(7, 30)),
        (TokenKind.RIGHTPAR, ')', None, Offset(7, 31)),
        (TokenKind.RIGHTPAR, ')', None, Offset(7, 32)),
        (TokenKind.RIGHTPAR, ')', None, Offset(7, 33)),
        (TokenKind.EOF, '', None, Offset(lineno=8, column=1))
        
    ]
    assert list(tokenize(test1)) == expect1
