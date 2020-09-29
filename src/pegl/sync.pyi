"""Typing stubs for pegl.sync"""

# Standard library imports
from typing import Any, Optional

# Local imports.
from .display import Display
from .enums import NativeEngine, SyncCondition, SyncFlag, SyncResult, SyncType


class Sync:
    def __init__(self, display: Display, handle: Any) -> None: ...

    def client_wait_sync(self, flags: SyncFlag=...,
                         timeout: Optional[int]=...) -> SyncResult: ...

    def wait_sync(self, flags: SyncFlag=...) -> None: ...

    @property
    def sync_condition(self) -> SyncCondition: ...

    @property
    def sync_status(self) -> bool: ...

    @property
    def sync_type(self) -> SyncType: ...


def wait_gl() -> None: ...

def wait_native(engine: Optional[NativeEngine]=...): ...

def wait_client() -> None: ...
