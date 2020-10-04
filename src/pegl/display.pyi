"""Typing stubs for pegl.display"""

# Standard library imports.
from typing import Any, Optional, Tuple

# Local imports.
from .config import Config
from .context import Context
from .enums import (ConfigAttrib, DisplayAttrib, ImageAttrib, ImageTarget,
                    Platform, SyncAttrib, SyncType)
from .image import Image
from .surface import Surface
from .sync import Sync


class Display:
    def __init__(self, display_id: Optional[int]=..., init: bool=...,
                 *, handle: Any=...) -> None: ...

    def __del__(self): ...

    def __bool__(self) -> bool: ...

    def __eq__(self, other: Any) -> bool: ...

    @classmethod
    def get_current_display(cls) -> Display: ...

    @classmethod
    def get_platform_display(cls, platform: Platform, native_display: int,
                             attribs: Optional[dict[DisplayAttrib, Any]]=None,
                             init: bool=True) -> Display: ...

    def choose_config(
        self, attribs: dict[ConfigAttrib, Any],
        num_config: Optional[int]=None) -> tuple[Config, ...]: ...

    def create_image(
        self, target: ImageTarget, buffer: int,
        attribs: Optional[dict[ImageAttrib, Any]]=None) -> Image: ...

    def create_sync(self, synctype: SyncType,
                    attribs: Optional[dict[SyncAttrib, Any]]=None) -> Sync: ...

    def get_config_count(self) -> int: ...

    def get_configs(self,
                    num_config: Optional[int]=None) -> tuple[Config, ...]: ...

    def initialize(self) -> tuple[int, int]: ...

    def terminate(self) -> None: ...

    @property
    def attribs(self) -> dict[DisplayAttrib, Any]: ...

    @property
    def client_apis(self) -> str: ...

    @property
    def extensions(self) -> str: ...

    @property
    def swap_interval(self) -> int: ...
    @swap_interval.setter
    def swap_interval(self, interval: int) -> None: ...

    @property
    def vendor(self) -> str: ...

    @property
    def version(self) -> tuple[int, int, str]: ...

    @property
    def version_string(self) -> str: ...


NoDisplay: Display = ...

def release_thread() -> None: ...
