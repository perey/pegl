"""Typing stubs for pegl.attribs"""

# Standard library imports.
from typing import Any, Optional

# Seems ctypes arrays aren't Iterable, or anything else I can put as a type.
CTypeArray = Any

def attrib_list(attribs: Optional[dict[Any, Any]],
                new_type:bool=False) -> CTypeArray: ...

DONT_CARE: Any = ...
