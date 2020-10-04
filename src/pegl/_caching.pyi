"""Typing stubs for pegl._caching"""

# Standard library imports.
from abc import ABC
from typing import (Any, Callable, ClassVar, Generic, Hashable, List, Mapping,
                    Protocol, Tuple, Union)

__all__: List[str] = ...

class HasHashableValue(Protocol):
    value: Hashable

CacheKey = Union[Hashable, HasHashableValue]

class CtypesPassable(Protocol):
    _as_parameter_: CacheKey

def extract_key(key: CacheKey) -> Hashable: ...

class CachedClass(Protocol):
    _cache_keys: ClassVar[Tuple[str, ...]]
    _caches: ClassVar[List[Mapping[Hashable, CtypesPassable]]]

    @classmethod
    def _add_to_cache(cls, instance: CtypesPassable) -> None: ...

    @classmethod
    def _remove_from_cache(cls, instance: CtypesPassable) -> None: ...

    @classmethod
    def _get_existing(cls, keys: Tuple[CacheKey, ...]) -> CtypesPassable: ...

    @classmethod
    def _new_or_existing(cls, keys: Tuple[CacheKey, ...],
                         *args: Any, **kwargs: Any) -> CtypesPassable: ...

caching_decorator = Callable[[type], CachedClass]

def cached(*args: str) -> caching_decorator: ...
