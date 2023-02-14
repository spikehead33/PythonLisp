from collections import deque, namedtuple
from enum import Enum
from typing import Generator, Tuple, Union

Offset = namedtuple("Offset", ["lineno", "column"])
TokenKind = Enum(
    "TokenKind", ["LEFTPAR", "RIGHTPAR", "NUMBER", "STRING", "SYMBOL", "EOF"]
)
Symbol = str
String = str
Number = Union[int, float]
Value = Symbol | String | Number | None
Lexeme = str
Token = Tuple[TokenKind, Lexeme, Value, Offset]

LINE_BREAKS = " \t\n"


def tokenize(source: str) -> Generator[Token, None, None]:
    skip = 0
    lineno, column = 1, 1
    for i, ch in enumerate(source):
        if skip > 0:
            skip -= 1
            continue
        kind = TokenKind.EOF
        value: Value = None
        lexeme = ""
        offset = Offset(lineno, column)
        if ch == "\n":
            lineno += 1
            column = 1
            continue
        elif ch in [" ", "\t"]:
            column += 1
            continue
        elif ch == "(":
            kind = TokenKind.LEFTPAR
            column += 1
            lexeme = ch
        elif ch == ")":
            kind = TokenKind.RIGHTPAR
            column += 1
            lexeme = ch
        elif ch == '"':
            kind = TokenKind.STRING
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
                raise RuntimeError(f"unterminated string found in {lineno}:{column}")
            lexeme = "".join(strbuffer)
            skip = len(lexeme) - 1
            strbuffer.popleft()  # remove the \" in both ends
            strbuffer.pop()
            value = "".join(strbuffer).replace('\\"', '"')
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
            lexeme = "".join(buffer)
            skip = len(lexeme) - 1

            try:
                value = float(lexeme)
            except ValueError:
                pass

            try:
                value = int(lexeme)
            except ValueError:
                pass

            if type(value) == int or type(value) == float:
                kind = TokenKind.NUMBER
            else:
                value = lexeme
                kind = TokenKind.SYMBOL
        yield (kind, lexeme, value, offset)
    kind = TokenKind.EOF
    yield (kind, "", None, Offset(lineno, column))
