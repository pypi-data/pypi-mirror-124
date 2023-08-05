from _typeshed import StrPath
from threading import Thread
from typing import IO, Any, Dict, Optional, Union

_Path = StrPath

def dictConfig(config: Dict[str, Any]) -> None: ...
def fileConfig(
    fname: Union[str, IO[str]], defaults: Optional[Dict[str, str]] = ..., disable_existing_loggers: bool = ...
) -> None: ...
def listen(port: int = ...) -> Thread: ...
def stopListening() -> None: ...
