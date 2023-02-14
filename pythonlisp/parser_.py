"""EBNF for the language

Lisp        := SExp { SExp }
SExp        := Atom | Pair | List
Pair        := LeftParen SExp "." SExp RightParen
List        := LeftParen { SExp } RightParen
Atom        := Number | String | Symbol
"""

from dataclasses import dataclass
from typing import Generator, Optional, Union

from pythonlisp.peekable import Peekable
from pythonlisp.tokenizer import (Lexeme, Offset, Token, TokenKind, Value,
                                  tokenize)


def is_tok_kind(token: Token, kind: TokenKind) -> bool:
    return token[0] == kind


def tok_lexeme(token: Token) -> Lexeme:
    return token[1]


def tok_val(token: Token) -> Value:
    return token[2]


def tok_offset(token: Token) -> Offset:
    return token[3]


class AstNode:
    pass


@dataclass(frozen=True)
class Number(AstNode):
    val: Union[float, int]
    pos: Optional[Offset]


@dataclass(frozen=True)
class String(AstNode):
    val: str
    pos: Optional[Offset]


@dataclass(frozen=True)
class Symbol(AstNode):
    val: str
    pos: Optional[Offset]


@dataclass(frozen=True)
class Boolean(AstNode):
    val: bool
    pos: Optional[Offset]


@dataclass
class Lisp(AstNode):
    sexps: list["SExp"]


@dataclass
class SExp(AstNode):
    exp: Union["Atom", "Pair", "List"]


@dataclass
class Atom(AstNode):
    value: Number | String | Symbol | Boolean


@dataclass
class Pair(AstNode):
    fst: SExp
    snd: SExp


@dataclass
class List(AstNode):
    lst: list[SExp]


class ParserError(Exception):
    pass


class Parser:
    tokens: Generator[Token, None, None] | None = None

    def parse(self, source: str) -> Lisp:
        self.tokens = tokenize(source)
        res = []
        nxt = next(self.tokens)
        while not is_tok_kind(nxt, TokenKind.EOF):
            s_exp = self.parse_sexp(nxt)
            res.append(s_exp)
            nxt = next(self.tokens)
        return Lisp(res)

    def parse_sexp(self, token: Token) -> SExp:
        if (
            is_tok_kind(token, TokenKind.NUMBER)
            or is_tok_kind(token, TokenKind.STRING)
            or is_tok_kind(token, TokenKind.SYMBOL)
        ):
            return SExp(self.parse_atom(token))
        elif is_tok_kind(token, TokenKind.RIGHTPAR):
            raise ParserError
        elif is_tok_kind(token, TokenKind.EOF):
            raise ParserError
        elif is_tok_kind(token, TokenKind.LEFTPAR):
            nxt = next(self.tokens)
            return SExp(self.parse_list(nxt))
        else:
            raise ParserError

    def parse_atom(self, token: Token) -> Atom:
        val = tok_val(token)
        offset = tok_offset(token)
        if is_tok_kind(token, TokenKind.NUMBER):
            return Atom(Number(val, offset))
        elif is_tok_kind(token, TokenKind.STRING):
            return Atom(String(val, offset))
        elif is_tok_kind(token, TokenKind.SYMBOL):
            if val == "#t" or val == "#f":
                b = True if val == "#t" else False
                return Atom(Boolean(b, offset))
            return Atom(Symbol(val, offset))
        raise ParserError

    def parse_list(self, token: Token) -> List:
        res = []
        nxt = token
        while not is_tok_kind(nxt, TokenKind.EOF) and not is_tok_kind(
            nxt, TokenKind.RIGHTPAR
        ):
            res.append(self.parse_sexp(nxt))
            nxt = next(self.tokens)
        if is_tok_kind(nxt, TokenKind.EOF):
            raise ParserError
        if not is_tok_kind(nxt, TokenKind.RIGHTPAR):
            raise ParserError
        return List(res)
