"""EBNF for the language

Lisp        := SExp { SExp }
SExp        := Atom | Pair | List
Pair        := LeftParen SExp "." SExp RightParen
List        := LeftParen { SExp } RightParen
Atom        := Number | String | Symbol
"""

from dataclasses import dataclass
from typing import Generator, NewType, Optional, Union

from pythonlisp.tokenizer import Offset, Token, Tokenizer, TokenKind


class SExp:
    pass


@dataclass(frozen=True)
class Number(SExp):
    val: int | float
    pos: Offset

    def __repr__(self) -> str:
        return f"{self.val}"


@dataclass(frozen=True)
class String(SExp):
    val: str
    pos: Offset

    def __repr__(self) -> str:
        return f"{self.val}"


@dataclass(frozen=True)
class Boolean(SExp):
    val: bool
    pos: Offset

    def __repr__(self) -> str:
        return f"{self.val})"


@dataclass(frozen=True)
class Symbol(SExp):
    val: str
    pos: Offset

    def __repr__(self) -> str:
        return f"Symbol({self.val})"


class List(list, SExp):
    def __repr__(self) -> str:
        return super().__repr__().replace("[", "(").replace("]", ")").replace(",", "")


class ParserError(Exception):
    pass


class Parser:
    tokenizer: Tokenizer
    tokens: Optional[Generator[Token, None, None]]

    def __init__(self) -> None:
        self.tokenizer = Tokenizer()
        self.tokens = None

    def parse(self, source: str) -> list[SExp]:
        self.tokens = self.tokenizer.tokenize(source)
        res = []
        nxt = next(self.tokens)
        while nxt.kind != TokenKind.EOF:
            s_exp = self.parse_sexp(nxt)
            res.append(s_exp)
            nxt = next(self.tokens)
        return res

    def parse_sexp(self, token: Token):
        offset = token.offset
        if token.kind == TokenKind.NUMBER:
            return Number(token.value, offset)
        elif token.kind == TokenKind.STRING:
            return String(token.value, offset)
        elif token.kind == TokenKind.SYMBOL:
            if token.lexeme == "#t":
                return Boolean(True, offset)
            elif token.lexeme == "#f":
                return Boolean(False, offset)
            return Symbol(token.lexeme, offset)
        elif token.kind == TokenKind.RIGHTPAREN:
            raise ParserError(f"Error: unexpected ')' found in {offset}")
        elif token.kind == TokenKind.LEFTPAREN:
            nxt = next(self.tokens)
            return self.parse_list(nxt)

    def parse_list(self, token: Token) -> List:
        res = []
        nxt = token
        while nxt.kind != TokenKind.EOF and nxt.kind != TokenKind.RIGHTPAREN:
            res.append(self.parse_sexp(nxt))
            nxt = next(self.tokens)
        if nxt.kind != TokenKind.RIGHTPAREN:
            raise ParserError(f"Error: unclosed parenthesis found in {token.offset}")
        return List(res)
