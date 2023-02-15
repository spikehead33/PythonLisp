from pythonlisp.tokenizer import Offset, Token, Tokenizer, TokenKind


def test_tokenize():
    test1 = """
(define x 10)
(define y 1.1)
(define s "This is the String")
x
s
(define f (lambda (x y) (+ x y)))
"""
    tokenizer = Tokenizer()
    expect1 = [
        Token(TokenKind.LEFTPAREN, "(", None, Offset(2, 1)),
        Token(TokenKind.SYMBOL, "define", None, Offset(2, 2)),
        Token(TokenKind.SYMBOL, "x", None, Offset(2, 9)),
        Token(TokenKind.NUMBER, "10", 10, Offset(2, 11)),
        Token(TokenKind.RIGHTPAREN, ")", None, Offset(2, 13)),
        Token(TokenKind.LEFTPAREN, "(", None, Offset(3, 1)),
        Token(TokenKind.SYMBOL, "define", None, Offset(3, 2)),
        Token(TokenKind.SYMBOL, "y", None, Offset(3, 9)),
        Token(TokenKind.NUMBER, "1.1", 1.1, Offset(3, 11)),
        Token(TokenKind.RIGHTPAREN, ")", None, Offset(3, 14)),
        Token(TokenKind.LEFTPAREN, "(", None, Offset(4, 1)),
        Token(TokenKind.SYMBOL, "define", None, Offset(4, 2)),
        Token(TokenKind.SYMBOL, "s", None, Offset(4, 9)),
        Token(
            TokenKind.STRING,
            '"This is the String"',
            "This is the String",
            Offset(4, 11),
        ),
        Token(TokenKind.RIGHTPAREN, ")", None, Offset(4, 31)),
        Token(TokenKind.SYMBOL, "x", None, Offset(5, 1)),
        Token(TokenKind.SYMBOL, "s", None, Offset(6, 1)),
        Token(TokenKind.LEFTPAREN, "(", None, Offset(7, 1)),
        Token(TokenKind.SYMBOL, "define", None, Offset(7, 2)),
        Token(TokenKind.SYMBOL, "f", None, Offset(7, 9)),
        Token(TokenKind.LEFTPAREN, "(", None, Offset(7, 11)),
        Token(TokenKind.SYMBOL, "lambda", None, Offset(7, 12)),
        Token(TokenKind.LEFTPAREN, "(", None, Offset(7, 19)),
        Token(TokenKind.SYMBOL, "x", None, Offset(7, 20)),
        Token(TokenKind.SYMBOL, "y", None, Offset(7, 22)),
        Token(TokenKind.RIGHTPAREN, ")", None, Offset(7, 23)),
        Token(TokenKind.LEFTPAREN, "(", None, Offset(7, 25)),
        Token(TokenKind.SYMBOL, "+", None, Offset(7, 26)),
        Token(TokenKind.SYMBOL, "x", None, Offset(7, 28)),
        Token(TokenKind.SYMBOL, "y", None, Offset(7, 30)),
        Token(TokenKind.RIGHTPAREN, ")", None, Offset(7, 31)),
        Token(TokenKind.RIGHTPAREN, ")", None, Offset(7, 32)),
        Token(TokenKind.RIGHTPAREN, ")", None, Offset(7, 33)),
        Token(TokenKind.EOF, "", None, Offset(lineno=8, column=1)),
    ]
    assert list(tokenizer.tokenize(test1)) == expect1
