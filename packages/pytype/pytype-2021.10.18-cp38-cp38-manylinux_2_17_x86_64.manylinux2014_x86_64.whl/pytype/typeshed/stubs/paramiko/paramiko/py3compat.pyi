import sys
from typing import Any, Iterable, Sequence, Text, Type, TypeVar, Union

_T = TypeVar("_T")

PY2: bool

string_types: Union[Type[Any], Sequence[Type[Any]]]
text_type: Union[Type[Any], Sequence[Type[Any]]]
bytes_types: Union[Type[Any], Sequence[Type[Any]]]
bytes = bytes
integer_types: Union[Type[Any], Sequence[Type[Any]]]
long = int

def input(prompt: Any) -> str: ...
def decodebytes(s: bytes) -> bytes: ...
def encodebytes(s: bytes) -> bytes: ...

if sys.version_info >= (3, 0):
    import builtins as builtins
    import io

    StringIO = io.StringIO
    BytesIO = io.BytesIO
else:
    import __builtin__ as builtins
    import cStringIO

    StringIO = cStringIO.StringIO
    BytesIO = StringIO

def byte_ord(c: Union[int, str]) -> int: ...
def byte_chr(c: int) -> bytes: ...
def byte_mask(c: int, mask: int) -> bytes: ...
def b(s: Union[bytes, str], encoding: str = ...) -> bytes: ...
def u(s: Union[bytes, str], encoding: str = ...) -> Text: ...
def b2s(s: Union[bytes, str]) -> str: ...
def is_callable(c: Any) -> bool: ...
def next(c: Iterable[_T]) -> _T: ...

MAXSIZE: int
