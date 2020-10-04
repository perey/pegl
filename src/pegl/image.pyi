"""Typing stubs for pegl.image"""

# Standard library imports.
from typing import Any, List

__all__: List[str] = ...

# Local imports.
from .display import Display
class Image:
    def __init__(self, display: Display, handle: Any) -> None: ...

    def __del__(self) -> None: ...
