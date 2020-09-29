#!/usr/bin/env python3

"""EGL rendering surfaces for Pegl."""

# Copyright © 2012, 2020 Tim Pederick.
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

__all__ = ['Surface']

# Local imports.
from . import egl
from ._caching import Cached
from .errors import BadSurfaceError

class Surface(Cached):
    """A rendering surface."""
    def __init__(self, display, handle):
        self._display = display
        self._as_parameter_ = handle

        self.__class__._add_to_cache(self)

    def __del__(self):
        # Remove this surface from the cache.
        try:
            self.__class__._remove_from_cache(self)
        except AttributeError:
            # This instance never got its handle properly assigned.
            pass
        except KeyError:
            # This instance never got cached.
            pass

        # Destroy this surface.
        try:
            egl.eglDestroySurface(self._display, self)
        except BadSurfaceError:
            # This instance has an invalid handle, so there's nothing to
            # destroy.
            pass

    def copy_buffers(self, target):
        """Copy the color buffer of this surface to a native pixmap."""
        egl.eglCopyBuffers(self._display, self, target)

    def swap_buffers(self, target):
        """Post the surface's back buffer to the window.

        This method is valid, but has no effect, on pbuffer, pixmap, and
        single-buffered window surfaces.

        """
        egl.eglSwapBuffers(self._display, self, target)

    @property
    def config(self):
        # Implemented in pegl.config to avoid dependency problems.
        raise NotImplementedError

    @property
    def config_id(self):
        return egl.eglQuerySurface(self._display, self, egl.EGL_CONFIG_ID)

    @property
    def height(self):
        return egl.eglQuerySurface(self._display, self, egl.EGL_HEIGHT)

    @property
    def largest_pbuffer(self):
        return bool(egl.eglQuerySurface(self._display, self,
                                        egl.EGL_LARGEST_PBUFFER))

    @property
    def width(self):
        return egl.eglQuerySurface(self._display, self, egl.EGL_WIDTH)


if egl.egl_version >= (1, 1):
    from .enums import RenderBuffer, TextureFormat, TextureTarget

    def bind_tex_image(self, buffer=RenderBuffer.BACK):
        """Bind a buffer of this surface as a texture.

        In the core EGL specification, this method is only valid for
        pbuffer surfaces and only for OpenGL ES rendering. Additionally,
        the back buffer must be the one specified, even if the surface
        is not double-buffered. (This is the default, and so the buffer
        argument may be omitted.) Extensions may alter these
        requirements.

        """
        egl.eglBindTexImage(self._display, self, buffer)
    setattr(Surface, 'bind_tex_image', bind_tex_image)

    def release_tex_image(self, buffer=RenderBuffer.BACK):
        """Release a buffer of this surface that was bound as a texture.

        In the core EGL specification, this method is only valid for
        pbuffer surfaces and only for OpenGL ES rendering. Additionally,
        the back buffer must be the one specified, even if the surface
        is not double-buffered. (This is the default, and so the buffer
        argument may be omitted.) Extensions may alter these
        requirements.

        """
        egl.eglReleaseTexImage(self._display, self, buffer)
    setattr(Surface, 'release_tex_image', release_tex_image)

    def get_mipmap_level(self):
        return egl.eglQuerySurface(self._display, self, egl.EGL_MIPMAP_LEVEL)
    def set_mipmap_level(self, level):
        egl.eglSurfaceAttrib(self._display, self, egl.EGL_MIPMAP_LEVEL, level)
    setattr(Surface, 'mipmap_level', property(get_mipmap_level,
                                              set_mipmap_level))

    def mipmap_texture(self):
        return bool(egl.eglQuerySurface(self._display, self,
                                        egl.EGL_MIPMAP_TEXTURE))
    setattr(Surface, 'mipmap_texture', property(mipmap_texture))

    def render_buffer(self):
        return RenderBuffer(egl.eglQuerySurface(self._display, self,
                                                egl.EGL_RENDER_BUFFER))
    setattr(Surface, 'render_buffer', property(render_buffer))

    def texture_format(self):
        fmt = egl.eglQuerySurface(self._display, self, egl.EGL_TEXTURE_FORMAT)
        return (None if fmt == egl.EGL_NO_TEXTURE else TextureFormat(fmt))
    setattr(Surface, 'texture_format', property(texture_format))

    def texture_target(self):
        tgt = egl.eglQuerySurface(self._display, self, egl.EGL_TEXTURE_TARGET)
        return (None if tgt == egl.EGL_NO_TEXTURE else TextureTarget(tgt))
    setattr(Surface, 'texture_target', property(texture_target))


if egl.egl_version >= (1, 2):
    from .enums import SwapBehavior

    def horizontal_resolution(self):
        scaled_value = egl.eglQuerySurface(self._display, self,
                                           egl.EGL_HORIZONTAL_RESOLUTION)
        return (None if scaled_value == egl.EGL_UNKNOWN else
                scaled_value / egl.EGL_DISPLAY_SCALING)
    setattr(Surface, 'horizontal_resolution', property(horizontal_resolution))

    def pixel_aspect_ratio(self):
        scaled_value = egl.eglQuerySurface(self._display, self,
                                           egl.EGL_PIXEL_ASPECT_RATIO)
        return (None if scaled_value == egl.EGL_UNKNOWN else
                scaled_value / egl.EGL_DISPLAY_SCALING)
    setattr(Surface, 'pixel_aspect_ratio', property(pixel_aspect_ratio))

    def swap_behavior(self):
        return SwapBehavior(egl.eglQuerySurface(self._display, self,
                                                egl.EGL_SWAP_BEHAVIOR))
    setattr(Surface, 'swap_behavior', property(swap_behavior))

    def vertical_resolution(self):
        scaled_value = egl.eglQuerySurface(self._display, self,
                                           egl.EGL_VERTICAL_RESOLUTION)
        return (None if scaled_value == egl.EGL_UNKNOWN else
                scaled_value / egl.EGL_DISPLAY_SCALING)
    setattr(Surface, 'vertical_resolution', property(vertical_resolution))


if egl.egl_version >= (1, 4):
    from .enums import MultisampleResolve

    def get_multisample_resolve(self):
        return MultisampleResolve(
            egl.eglQuerySurface(self._display, self,
                                egl.EGL_MULTISAMPLE_RESOLVE))
    def set_multisample_resolve(self, method):
        egl.eglSurfaceAttrib(self._display, self, egl.EGL_MULTISAMPLE_RESOLVE,
                             method)
    setattr(Surface, 'multisample_resolve',
            property(get_multisample_resolve, set_multisample_resolve))
