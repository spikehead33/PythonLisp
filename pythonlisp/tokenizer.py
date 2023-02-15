from collections import deque, namedtuple
from dataclasses import dataclass
from enum import Enum, auto
from typing import Generator, Tuple, Union


@dataclass
class Offset:
    lineno: int
    column: int

    # def __repr__(self) -> str:
    #     return f"line: {self.lineno}, column: {self.column}"


class TokenKind(Enum):
    LEFTPAREN = auto()
    RIGHTPAREN = auto()
    NUMBER = auto()
    STRING = auto()
    SYMBOL = auto()
    EOF = auto()


@dataclass
class Token:
    kind: TokenKind
    lexeme: str
    value: str | int | float | None
    offset: Offset


LINE_BREAKS = " \t\n"


class Tokenizer:
    def tokenize(self, source: str) -> Generator[Token, None, None]:
        skip = 0
        lineno, column = 1, 1
        for i, ch in enumerate(source):
            if skip > 0:
                skip -= 1
                continue
            # a new token
            token = Token(TokenKind.EOF, "", None, Offset(lineno, column))
            if ch == "\n":
                lineno += 1
                column = 1
                continue
            elif ch in [" ", "\t"]:
                column += 1
                continue
            elif ch == "(":
                token.kind = TokenKind.LEFTPAREN
                token.lexeme = ch
                column += 1
            elif ch == ")":
                token.kind = TokenKind.RIGHTPAREN
                token.lexeme = ch
                column += 1
            elif ch == '"':
                token.kind = TokenKind.STRING
                strbuffer: deque[str] = deque()
                for cursor in range(i, len(source)):
                    column += 1
                    strbuffer.append(source[cursor])
                    if (
                        len(strbuffer) > 1
                        and strbuffer[-2] != "\\"
                        and strbuffer[-1] == '"'
                    ):
                        break
                    if source[cursor] == "\n":
                        lineno += 1
                        column = 1
                if strbuffer[-1] != '"':
                    raise RuntimeError(
                        f"unterminated string found in {lineno}:{column}"
                    )
                token.lexeme = "".join(strbuffer)
                skip = len(token.lexeme) - 1
                strbuffer.popleft()  # remove the \" in both ends
                strbuffer.pop()
                token.value = "".join(strbuffer).replace('\\"', '"')
            else:  # Determine if the Token belongs to NUMBER/SYMBOL/UNKNOWN
                buffer: list[str] = []
                for cursor in range(i, len(source)):
                    if (
                        source[cursor] == "("
                        or source[cursor] == ")"
                        or source[cursor] in LINE_BREAKS
                    ):
                        break
                    column += 1
                    buffer.append(source[cursor])
                token.lexeme = "".join(buffer)
                skip = len(token.lexeme) - 1

                try:
                    token.value = float(token.lexeme)
                except ValueError:
                    pass

                try:
                    token.value = int(token.lexeme)
                except ValueError:
                    pass

                if type(token.value) == int or type(token.value) == float:
                    token.kind = TokenKind.NUMBER
                else:
                    token.kind = TokenKind.SYMBOL
            yield token
        yield Token(TokenKind.EOF, "", None, Offset(lineno, column))
