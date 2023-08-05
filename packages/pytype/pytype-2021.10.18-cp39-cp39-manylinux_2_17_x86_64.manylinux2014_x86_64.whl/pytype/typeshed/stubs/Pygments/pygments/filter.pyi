from collections.abc import Iterable, Iterator
from typing import Any, Optional

from pygments.lexer import Lexer
from pygments.token import _TokenType

def apply_filters(stream, filters, lexer: Optional[Any] = ...): ...
def simplefilter(f): ...

class Filter:
    options: Any
    def __init__(self, **options) -> None: ...
    def filter(self, lexer: Lexer, stream: Iterable[tuple[_TokenType, str]]) -> Iterator[tuple[_TokenType, str]]: ...

class FunctionFilter(Filter):
    function: Any
    def __init__(self, **options) -> None: ...
    def filter(self, lexer: Lexer, stream: Iterable[tuple[_TokenType, str]]) -> Iterator[tuple[_TokenType, str]]: ...
