#!/usr/bin/env python3

"""EGL configuration management for Pegl."""

# Copyright © 2012, 2020, 2021 Tim Pederick.
#
# This file is part of Pegl.
#
# Pegl is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pegl is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
# License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pegl. If not, see <http://www.gnu.org/licenses/>.

__all__ = ['Config']

# Local imports.
from . import egl
from .attribs import attrib_list
from ._caching import cached
from .enums import ConfigCaveat, SurfaceTypeFlag, TransparentType
from .context import Context
from .surface import Surface

# TODO: The value of an EGLConfig is not the same as its ID, as retrieved by
# config_id (on the config or on a surface created from it). This complicates
# caching quite a bit... And it's entirely possible that it affects other
# cached types as well!

@cached('_as_parameter_', 'config_id')
class Config:
    """A set of EGL configuration options."""
    _config_info = ['_handle_hex',
                    '_color_buffer_info',
                    '_depth_info',
                    '_stencil_info',
                    '_sample_info']

    def __init__(self, display, handle):
        self._display = display
        self._as_parameter_ = handle

        self.__class__._add_to_cache(self) # pylint: disable=no-member

    def __repr__(self):
        return '<{}: {:#08x}>'.format(self.__class__.__name__,
                                      self._as_parameter_)

    def __str__(self):
        config_info = (getattr(self, info_prop)
                       for info_prop in self.__class__._config_info)
        return '<{} #{}: {}>'.format(self.__class__.__name__, self.config_id,
                                     ', '.join(item for item in config_info
                                               if item is not None))

    @property
    def _handle_hex(self):
        """Get the EGL config handle in hexadecimal."""
        return format(self._as_parameter_, '#010x')

    def _get_color_buffer_info(self):
        """Get a friendly string for the color buffer type and size."""
        color_type, bits = 'RGB', [self.red_size, self.blue_size,
                                   self.green_size]
        if self.alpha_size > 0:
            color_type += 'A'
            bits += [self.alpha_size]

        return '{}-bit {} {!r}'.format(self.buffer_size, color_type,
                                       tuple(bits))

    @property
    def _color_buffer_info(self):
        """Get a friendly string for the color buffer type and size."""
        return self._get_color_buffer_info()

    @property
    def _depth_info(self):
        """Get a string describing the depth buffer, if any."""
        return (None if self.depth_size == 0 else
                '{}-bit depth'.format(self.depth_size))

    @property
    def _stencil_info(self):
        """Get a string describing the stencil buffer, if any."""
        return (None if self.stencil_size == 0 else
                '{}-bit stencil'.format(self.stencil_size))

    @property
    def _sample_info(self):
        """Get a string describing the multisampling, if any."""
        return (None if self.sample_buffers == 0 else
                '{}× MSAA'.format(self.samples))

    def create_context(self, share_context=None, attribs=None):
        """Create a rendering context that uses this configuration."""
        return Context(self._display,
                       egl.eglCreateContext(self._display, self,
                                            egl.EGL_NO_CONTEXT if share_context
                                            is None else share_context,
                                            attrib_list(attribs)))

    def create_pbuffer_surface(self, attribs=None):
        """Create a pbuffer (off-screen) rendering surface."""
        return Surface(self._display,
                       egl.eglCreatePbufferSurface(self._display, self,
                                                   attrib_list(attribs)))

    def create_pixmap_surface(self, pixmap, attribs=None):
        """Create a pixmap (off-screen) rendering surface."""
        return Surface(self._display,
                       egl.eglCreatePixmapSurface(self._display, self, pixmap,
                                                  attrib_list(attribs)))

    def create_window_surface(self, win, attribs=None):
        """Create a window (on-screen) rendering surface."""
        return Surface(self._display,
                       egl.eglCreateWindowSurface(self._display, self, win,
                                                  attrib_list(attribs)))

    def get_config_attrib(self, attribute):
        """Get an attribute of this configuration.

        Users will generally not need this function, as the available
        attributes may be queried using properties instead.

        """
        return egl.eglGetConfigAttrib(self._display, self, attribute)

    @property
    def alpha_size(self):
        """The number of color buffer bits used for alpha."""
        return egl.eglGetConfigAttrib(self._display, self, egl.EGL_ALPHA_SIZE)

    @property
    def blue_size(self):
        """The number of color buffer bits used for blue."""
        return egl.eglGetConfigAttrib(self._display, self, egl.EGL_BLUE_SIZE)

    @property
    def buffer_size(self):
        """The number of non-padding bits in the color buffer."""
        return egl.eglGetConfigAttrib(self._display, self, egl.EGL_BUFFER_SIZE)

    @property
    def config_caveat(self):
        """Any caveat that applies when using this config."""
        caveat = ConfigCaveat(egl.eglGetConfigAttrib(self._display, self,
                                                     egl.EGL_CONFIG_CAVEAT))
        return None if caveat == ConfigCaveat.NONE else caveat

    @property
    def config_id(self):
        """The config's unique identifier."""
        return egl.eglGetConfigAttrib(self._display, self, egl.EGL_CONFIG_ID)

    @property
    def depth_size(self):
        """The number of bits in the depth buffer."""
        return egl.eglGetConfigAttrib(self._display, self, egl.EGL_DEPTH_SIZE)

    @property
    def green_size(self):
        """The number of color buffer bits used for green."""
        return egl.eglGetConfigAttrib(self._display, self, egl.EGL_GREEN_SIZE)

    @property
    def level(self):
        """The overlay or underlay level of the frame buffer."""
        return egl.eglGetConfigAttrib(self._display, self, egl.EGL_LEVEL)

    @property
    def max_pbuffer_height(self):
        """The maximum height in pixels of a pbuffer surface."""
        return egl.eglGetConfigAttrib(self._display, self,
                                      egl.EGL_MAX_PBUFFER_HEIGHT)

    @property
    def max_pbuffer_pixels(self):
        """The maximum number of pixels in a pbuffer surface."""
        return egl.eglGetConfigAttrib(self._display, self,
                                      egl.EGL_MAX_PBUFFER_PIXELS)

    @property
    def max_pbuffer_width(self):
        """The maximum width in pixels of a pbuffer surface."""
        return egl.eglGetConfigAttrib(self._display, self,
                                      egl.EGL_MAX_PBUFFER_WIDTH)

    @property
    def native_renderable(self):
        """Whether native APIs can render to a surface."""
        return bool(egl.eglGetConfigAttrib(self._display, self,
                                           egl.EGL_NATIVE_RENDERABLE))

    @property
    def native_visual_id(self):
        """A platform-specific identifier for the native visual"""
        return egl.eglGetConfigAttrib(self._display, self,
                                       egl.EGL_NATIVE_VISUAL_ID)

    @property
    def native_visual_type(self):
        """A platform-defined type for the native visual."""
        return egl.eglGetConfigAttrib(self._display, self,
                                       egl.EGL_NATIVE_VISUAL_TYPE)

    @property
    def red_size(self):
        """The number of color buffer bits used for red."""
        return egl.eglGetConfigAttrib(self._display, self, egl.EGL_RED_SIZE)

    @property
    def samples(self):
        """The number of samples per pixel."""
        return egl.eglGetConfigAttrib(self._display, self, egl.EGL_SAMPLES)

    @property
    def sample_buffers(self):
        """The number of multisample buffers."""
        return egl.eglGetConfigAttrib(self._display, self,
                                      egl.EGL_SAMPLE_BUFFERS)

    @property
    def stencil_size(self):
        """The number of bits in the stencil buffer."""
        return egl.eglGetConfigAttrib(self._display, self,
                                      egl.EGL_STENCIL_SIZE)

    @property
    def surface_type(self):
        """The type(s) of surface supported."""
        return SurfaceTypeFlag(egl.eglGetConfigAttrib(self._display, self,
                                                      egl.EGL_SURFACE_TYPE))

    @property
    def transparent_blue_value(self):
        """The blue value of the transparent color."""
        return egl.eglGetConfigAttrib(self._display, self,
                                      egl.EGL_TRANSPARENT_BLUE_VALUE)

    @property
    def transparent_green_value(self):
        """The green value of the transparent color."""
        return egl.eglGetConfigAttrib(self._display, self,
                                      egl.EGL_TRANSPARENT_GREEN_VALUE)

    @property
    def transparent_red_value(self):
        """The red value of the transparent color."""
        return egl.eglGetConfigAttrib(self._display, self,
                                      egl.EGL_TRANSPARENT_RED_VALUE)

    @property
    def transparent_type(self):
        """The type of transparency supported."""
        ttype = TransparentType(egl.eglGetConfigAttrib(
                                    self._display, self,
                                    egl.EGL_TRANSPARENT_TYPE))
        return None if ttype == TransparentType.NONE else ttype


# These are defined here to avoid a circular dependency issue, where the config
# module depends on the context or surface module, and vice versa.
def config(self): # pylint: disable=missing-function-docstring
    handle = self.config_id
    return Config._new_or_existing((None, handle), self._display, handle) # pylint: disable=no-member
setattr(Context, 'config',
        property(config, doc='The config object used to create this context.'))
setattr(Surface, 'config',
        property(config, doc='The config object used to create this surface.'))

if egl.egl_version >= (1, 1):
    def bind_to_texture_rgb(self):
        """Whether or not RGB textures can be bound."""
        return bool(egl.eglGetConfigAttrib(self._display, self,
                                           egl.EGL_BIND_TO_TEXTURE_RGB))
    setattr(Config, 'bind_to_texture_rgb', property(bind_to_texture_rgb))

    def bind_to_texture_rgba(self):
        """Whether or not RGBA textures can be bound."""
        return bool(egl.eglGetConfigAttrib(self._display, self,
                                           egl.EGL_BIND_TO_TEXTURE_RGBA))
    setattr(Config, 'bind_to_texture_rgba', property(bind_to_texture_rgba))

    def max_swap_interval(self):
        """The maximum number of video frames between buffer swaps."""
        return egl.eglGetConfigAttrib(self._display, self,
                                      egl.EGL_MAX_SWAP_INTERVAL)
    setattr(Config, 'max_swap_interval', property(max_swap_interval))

    def min_swap_interval(self):
        """The minimum number of video frames between buffer swaps."""
        return egl.eglGetConfigAttrib(self._display, self,
                                      egl.EGL_MIN_SWAP_INTERVAL)
    setattr(Config, 'min_swap_interval', property(min_swap_interval))


if egl.egl_version >= (1, 2):
    from .enums import ClientAPIFlag, ColorBufferType

    def create_pbuffer_from_client_buffer(self, buftype, buffer, attribs=None):
        """Create a pbuffer (off-screen) surface from a client buffer."""
        return Surface(self._display,
                       egl.eglCreatePbufferFromClientBuffer(
                           self._display, buftype, buffer, self,
                           attrib_list(attribs)))
    setattr(Config, 'create_pbuffer_from_client_buffer',
            create_pbuffer_from_client_buffer)

    def alpha_mask_size(self):
        """The number of bits in the alpha mask buffer."""
        return egl.eglGetConfigAttrib(self._display, self,
                                      egl.EGL_ALPHA_MASK_SIZE)
    setattr(Config, 'alpha_mask_size', property(alpha_mask_size))

    def color_buffer_type(self):
        """The type of color buffer."""
        return ColorBufferType(egl.eglGetConfigAttrib(
                                   self._display, self,
                                   egl.EGL_COLOR_BUFFER_TYPE))
    setattr(Config, 'color_buffer_type', property(color_buffer_type))

    def luminance_size(self):
        """The number of color buffer bits used for luminance."""
        return egl.eglGetConfigAttrib(self._display, self,
                                      egl.EGL_LUMINANCE_SIZE)
    setattr(Config, 'luminance_size', property(luminance_size))

    def renderable_type(self):
        """The supported client API(s)."""
        return ClientAPIFlag(egl.eglGetConfigAttrib(self._display, self,
                                                    egl.EGL_RENDERABLE_TYPE))
    setattr(Config, 'renderable_type', property(renderable_type))

    def _get_color_buffer_info(self):
        """Get a friendly string for the color buffer type and size."""
        if self.color_buffer_type == ColorBufferType.LUMINANCE:
            color_type, bits = 'L', [self.luminance_size]
        else:
            color_type, bits = 'RGB', [self.red_size, self.blue_size,
                                       self.green_size]
        if self.alpha_size > 0:
            color_type += 'A'
            bits += [self.alpha_size]
        if len(bits) == 1:
            return '{}-bit {}'.format(self.buffer_size, color_type)

        return '{}-bit {} {!r}'.format(self.buffer_size, color_type,
                                       tuple(bits))
    setattr(Config, '_get_color_buffer_info', _get_color_buffer_info)


if egl.egl_version >= (1, 3):
    # ClientAPIFlag already imported under version 1.2, above.
    def conformant(self):
        """Client APIs for which conformance requirements are met."""
        return ClientAPIFlag(egl.eglGetConfigAttrib(self._display, self,
                                                    egl.EGL_CONFORMANT))
    setattr(Config, 'conformant', property(conformant))


if egl.egl_version >= (1, 5):
    def create_platform_pixmap_surface(self, native_pixmap, attribs=None):
        """Create a pixmap (off-screen) rendering surface."""
        return Surface(self._display,
                       egl.eglCreatePlatformPixmapSurface(
                           self._display, self, native_pixmap,
                           attrib_list(attribs, new_type=True)))
    setattr(Config, 'create_platform_pixmap_surface',
            create_platform_pixmap_surface)

    def create_platform_window_surface(self, native_window, attribs=None):
        """Create a window (on-screen) rendering surface."""
        return Surface(self._display,
                       egl.eglCreatePlatformWindowSurface(
                           self._display, self, native_window,
                           attrib_list(attribs, new_type=True)))
    setattr(Config, 'create_platform_window_surface',
            create_platform_window_surface)
