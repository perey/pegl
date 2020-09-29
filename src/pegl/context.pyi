"""Typing stubs for pegl.context"""

# Standard library imports.
from typing import Any, Optional

# Local imports.
from ._caching import Cached
from .config import Config
from .enums import ClientAPI, ReadOrDraw, RenderBuffer
from .image import Image
from .surface import Surface


class ContextMeta(type(Cached)):
    @property
    def current_draw_surface(cls) -> Optional[Surface]: ...

    @property
    def current_read_surface(cls) -> Optional[Surface]: ...


class Context(Cached, metaclass=ContextMeta):
    def __init__(self, display: Display, handle: Any) -> None: ...

    def __del__(self) -> None: ...

    @classmethod
    def get_current_context(cls) -> Optional[Context]:

    @classmethod
    def get_current_surface(cls,
                            readdraw: ReadOrDraw) -> Optional[Surface]: ...

    @classmethod
    def release_current(cls) -> None: ...

    def create_image(
        self, target: ImageTarget, buffer: int,
        attribs: Optional[dict[ImageAttrib, Any]]=None) -> Image: ...

    def make_current(self, draw: Optional[Surface]=None,
                     read: Optional[Surface]=None) -> None: ...

    @property
    def client_type(self) -> ClientAPI: ...

    @property
    def client_version(self) -> int: ...

    @property
    def config(self) -> Config: ...

    @property
    def config_id(self) -> int: ...

    @property
    def render_buffer(self) -> Optional[RenderBuffer]: ...


def bind_api(api: ClientAPI) -> None: ...

def query_api() -> Optional[ClientAPI]: ...
