from collections import deque
from typing import Generator, Generic, Optional, TypeVar

T = TypeVar("T")


class Peekable(Generic[T]):
    __peekq: deque[T]
    __generator: Generator[T, None, None]

    def __init__(self, generator: Generator[T, None, None]) -> None:
        self.__generator = generator
        self.__peekq = deque()

    def __iter__(self):
        return self

    def __next__(self):
        if self.__peekq:
            return self.__peekq.popleft()
        nxtitem = next(self.__generator)
        return nxtitem

    def peekn(self, n: int) -> Optional[T]:
        if len(self.__peekq) > n:
            return self.__peekq[n - 1]
        rest = n - len(self.__peekq)

        for _ in range(rest):
            nxtitem = next(self.__generator)
            self.__peekq.append(nxtitem)
            item = nxtitem
        return item
