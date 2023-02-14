from pythonlisp.tokenizer import Offset
from pythonlisp.parser_ import (
    Parser, ParserError, Lisp, SExp,
    List, Atom, Number, Symbol, Boolean
)
import pytest


@pytest.mark.parametrize("input,expexted", [
    ("", Lisp([])), ("x", Lisp([SExp(Atom(Symbol('x', Offset(1, 1))))])),
    ("()", Lisp([SExp(List([]))])),
    ("(define x 100)", Lisp([SExp(List([
        SExp(Atom(Symbol(val='define', pos=Offset(lineno=1, column=2)))),
        SExp(Atom(Symbol(val='x', pos=Offset(lineno=1, column=9)))),
        SExp(Atom(Number(val=100, pos=Offset(lineno=1, column=11))))]))])),
    ("(define f (lambda (x y) (+ x y)))", Lisp([
        SExp(
            List([
                SExp(Atom(Symbol(val='define', pos=Offset(lineno=1, column=2)))),
                SExp(Atom(Symbol(val='f', pos=Offset(lineno=1, column=9)))),
                SExp(
                    List([
                        SExp(Atom(value=Symbol(val='lambda', pos=Offset(lineno=1, column=12)))),
                        SExp(List([
                            SExp(Atom(Symbol(val='x', pos=Offset(lineno=1, column=20)))),
                            SExp(Atom(Symbol(val='y', pos=Offset(lineno=1, column=22))))
                        ])),
                        SExp(List([
                            SExp(Atom(Symbol(val='+', pos=Offset(lineno=1, column=26)))),
                            SExp(Atom(Symbol(val='x', pos=Offset(lineno=1, column=28)))),
                            SExp(Atom(Symbol(val='y', pos=Offset(lineno=1, column=30))))])
                        )
                    ])
                )
            ])
        )
    ])),
    ("""
(define x 10)
(define y 10)
(define b #t)""", Lisp([
        SExp(List([
            SExp(Atom(Symbol(val='define', pos=Offset(lineno=2, column=2)))),
            SExp(Atom(Symbol(val='x', pos=Offset(lineno=2, column=9)))),
            SExp(Atom(Number(val=10, pos=Offset(lineno=2, column=11))))
        ])),
        SExp(List([
            SExp(Atom(Symbol(val='define', pos=Offset(lineno=3, column=2)))),
            SExp(Atom(Symbol(val='y', pos=Offset(lineno=3, column=9)))),
            SExp(Atom(Number(val=10, pos=Offset(lineno=3, column=11))))
        ])),
        SExp(List([
            SExp(Atom(Symbol(val='define', pos=Offset(lineno=4, column=2)))),
            SExp(Atom(Symbol(val='b', pos=Offset(lineno=4, column=9)))),
            SExp(Atom(Boolean(val=True, pos=Offset(lineno=4, column=11))))
        ]))
    ]))
])
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
