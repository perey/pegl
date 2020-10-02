"""Typing stubs for pegl.attribs"""

# Standard library imports.
from typing import Any, Iterable, Optional

CTypeArray = Iterable[int]

def attrib_list(attribs: Optional[dict[int, int]],
                new_type:bool=False) -> CTypeArray: ...

DONT_CARE: Any = ...
