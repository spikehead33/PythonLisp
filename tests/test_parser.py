import pytest

from pythonlisp.parser_ import Boolean, List, Number, Parser, ParserError, Symbol
from pythonlisp.tokenizer import Offset


@pytest.mark.parametrize(
    "input,expexted",
    [
        ("", []),
        ("x", [Symbol("x", Offset(1, 1))]),
        ("()", [[]]),
        (
            "(define x 100)",
            [
                [
                    Symbol("define", Offset(1, 2)),
                    Symbol("x", Offset(1, 9)),
                    Number(100, Offset(1, 11)),
                ]
            ],
        ),
        (
            "(define f (lambda (x y) (+ x y)))",
            [
                [
                    Symbol("define", Offset(1, 2)),
                    Symbol("f", Offset(1, 9)),
                    [
                        Symbol("lambda", Offset(1, 12)),
                        [Symbol("x", Offset(1, 20)), Symbol("y", Offset(1, 22))],
                        [
                            Symbol("+", Offset(1, 26)),
                            Symbol("x", Offset(1, 28)),
                            Symbol("y", Offset(1, 30)),
                        ],
                    ],
                ]
            ],
        ),
        (
            """
(define x 10)
(define y 10)
(define b #t)""",
            [
                [
                    Symbol("define", Offset(2, 2)),
                    Symbol("x", Offset(2, 9)),
                    Number(10, Offset(2, 11)),
                ],
                [
                    Symbol("define", Offset(3, 2)),
                    Symbol("y", Offset(3, 9)),
                    Number(10, Offset(3, 11)),
                ],
                [
                    Symbol("define", Offset(4, 2)),
                    Symbol("b", Offset(4, 9)),
                    Boolean(True, Offset(4, 11)),
                ],
            ],
        ),
    ],
)
def test_parser_success(input, expexted):
    parser = Parser()
    assert parser.parse(input) == expexted


def test_parser_unexpected_rightpar():
    with pytest.raises(ParserError):
        parser = Parser()
        parser.parse(")")


def test_parser_unclosed_list():
    with pytest.raises(ParserError):
        parser = Parser()
        parser.parse("(define x 100")
