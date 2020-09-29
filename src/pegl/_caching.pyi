"""Typing stubs for pegl._caching"""

# Standard library imports.
from abc import ABC
from typing import ClassVar, Generic, Mapping, Protocol, TypeVar

CType = TypeVar('CType')

class CtypesPassable(Generic[CType]):
    _as_parameter_: CType

class Cached(ABC):
    _cache: ClassVar[Mapping[CType, CtypesPassable[CType]]]

    @classmethod
    def _add_to_cache(cls, instance: CtypesPassable[CType]) -> None: ...

    @classmethod
    def _remove_from_cache(cls, instance: CtypesPassable[CType]) -> None: ...

    @classmethod
    def _new_or_existing(cls, key: CType, *args: Any,
                         **kwargs: Any) -> CtypesPassable[CType]: ...
