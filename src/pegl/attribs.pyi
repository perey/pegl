"""Typing stubs for pegl.attribs"""

# Standard library imports.
from typing import Any, Dict, Iterable, List, Optional

__all__: List[str] = ...

CTypeArray = Iterable[int]

def attrib_list(attribs: Optional[Dict[int, int]],
                new_type:bool=False) -> CTypeArray: ...

DONT_CARE: Any = ...
