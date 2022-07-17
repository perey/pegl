"""Typing stubs for pegl.config"""

# Standard library imports.
from typing import Any, Dict, List, Optional

# Local imports.
from .context import Context
from .display import Display
from .enums import (ClientAPIFlag, ClientBufferType, ColorBufferType,
                    ConfigAttrib, ConfigCaveat, ContextAttrib, SurfaceAttrib,
                    SurfaceTypeFlag, TransparentType)
from .surface import Surface

__all__: List[str] = ...


class Config:
    def __init__(self, display: Display, handle: Any) -> None: ...

    def create_context(
        self, share_context: Optional[Context]=...,
        attribs: Optional[Dict[ContextAttrib, Any]]=...) -> Context: ...

    def create_pbuffer_from_client_buffer(
        self, buftype: ClientBufferType, buffer: Any,
        attribs: Optional[Dict[SurfaceAttrib, Any]]=...) -> Surface: ...

    def create_pbuffer_surface(
        self, attribs: Optional[Dict[SurfaceAttrib, Any]]=...) -> Surface: ...

    def create_pixmap_surface(
        self, pixmap: int,
        attribs: Optional[Dict[SurfaceAttrib, Any]]=...) -> Surface: ...

    def create_platform_pixmap_surface(
        self, native_pixmap: int,
        attribs: Optional[Dict[SurfaceAttrib, Any]]=...) -> Surface: ...

    def create_platform_window_surface(
        self, native_window: int,
        attribs: Optional[Dict[SurfaceAttrib, Any]]=...) -> Surface: ...

    def create_window_surface(
        self, win: int,
        attribs: Optional[Dict[SurfaceAttrib, Any]]=...) -> Surface: ...

    def get_config_attrib(self, attribute: ConfigAttrib) -> Any: ...

    @property
    def alpha_mask_size(self) -> int: ...

    @property
    def alpha_size(self) -> int: ...

    @property
    def bind_to_texture_rgb(self) -> bool: ...

    @property
    def bind_to_texture_rgba(self) -> bool: ...

    @property
    def blue_size(self) -> int: ...

    @property
    def buffer_size(self) -> int: ...

    @property
    def color_buffer_type(self) -> ColorBufferType: ...

    @property
    def config_caveat(self) -> Optional[ConfigCaveat]: ...

    @property
    def config_id(self) -> int: ...

    @property
    def conformant(self) -> ClientAPIFlag: ...

    @property
    def depth_size(self) -> int: ...

    @property
    def green_size(self) -> int: ...

    @property
    def level(self) -> int: ...

    @property
    def luminance_size(self) -> int: ...

    @property
    def max_pbuffer_height(self) -> int: ...

    @property
    def max_swap_interval(self) -> bool: ...

    @property
    def min_swap_interval(self) -> bool: ...

    @property
    def max_pbuffer_pixels(self) -> int: ...

    @property
    def max_pbuffer_width(self) -> int: ...

    @property
    def native_renderable(self) -> bool: ...

    @property
    def native_visual_id(self) -> int: ...

    @property
    def native_visual_type(self) -> Optional[Any]: ...

    @property
    def red_size(self) -> int: ...

    @property
    def renderable_type(self) -> ClientAPIFlag: ...

    @property
    def samples(self) -> int: ...

    @property
    def sample_buffers(self) -> int: ...

    @property
    def stencil_size(self) -> int: ...

    @property
    def surface_type(self) -> SurfaceTypeFlag: ...

    @property
    def transparent_blue_value(self) -> int: ...

    @property
    def transparent_green_value(self) -> int: ...

    @property
    def transparent_red_value(self) -> int: ...

    @property
    def transparent_type(self) -> Optional[TransparentType]: ...
