#!/usr/bin/env python3

"""EGL display management for Pegl."""

# Copyright © 2012, 2013, 2020 Tim Pederick.
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

from __future__ import annotations

__all__ = ['Display', 'NoDisplay']

# Standard library imports.
import ctypes
from typing import Any, Optional

# Local imports.
from . import egl
from .attribs import attrib_list
from ._caching import Cached
from .enums import ConfigAttrib
from .errors import BadDisplayError
from .config import Config
from .context import Context
from .surface import Surface


class Display(Cached):
    """An EGL display.

    In EGL, a display is both a representation of a (physical or virtual)
    display device, and an environment for other objects.

    """
    def __init__(self, display_id: Optional[int]=None, init: bool=True,
                 *, handle: Any=None):
        # Specifying a display by its EGLDisplay handle overrides everything
        # else.
        if handle is not None:
            self._as_parameter_ = handle
            self.__class__._add_to_cache(self)
            return

        if display_id is None:
            if egl.egl_version < (1, 4):
                raise ValueError('default display not available before EGL '
                                 '1.4')
            else:
                display_id = egl.EGL_DEFAULT_DISPLAY

        self._as_parameter_ = egl.eglGetDisplay(display_id)
        self.__class__._add_to_cache(self)

        # Forwards compatibility.
        self._attribs = {}

        if init:
            egl.eglInitialize(self)

    def __del__(self):
        # Remove this display from the cache.
        try:
            self.__class__._remove_from_cache(self)
        except AttributeError:
            # This instance never got its handle properly assigned.
            pass
        except KeyError:
            # This instance never got cached.
            pass

        # Terminate this display.
        try:
            egl.eglTerminate(self)
        except BadDisplayError:
            # This instance has an invalid handle, so there's nothing to
            # terminate.
            pass

        # Release EGL resources in this thread.
        if egl.egl_version >= (1, 2):
            egl.eglReleaseThread()

    def __eq__(self, other: Any) -> bool:
        try:
            return (other._as_parameter_ == self._as_parameter_)
        except AttributeError:
            return False

    def choose_config(self, attribs: dict[ConfigAttrib, Any],
                      num_config: Optional[int]=None) -> tuple[Config, ...]:
        """Get available configurations that match given attributes."""
        if num_config is None:
            num_config = self.get_config_count()
        configs = (egl._common.EGLConfig * num_config)()
        actual_count = egl.eglChooseConfig(self, attrib_list(attribs),
                                              configs, num_config)
        return tuple(Config._new_or_existing(configs[n], self, configs[n])
                     for n in range(actual_count))

    def get_config_count(self) -> int:
        """Get the number of configurations available on this display."""
        return egl.eglGetConfigs(self, None, 0)

    def get_configs(self, num_config: Optional[int]=None
                    ) -> tuple[Config, ...]:
        """Get a list of available configurations."""
        if num_config is None:
            num_config = self.get_config_count()
        configs = (egl._common.EGLConfig * num_config)()
        actual_count = egl.eglGetConfigs(self, configs, num_config)
        return tuple(Config._new_or_existing(configs[n], self, configs[n])
                     for n in range(actual_count))

    def initialize(self) -> tuple[int, int]:
        """Initialise this display."""
        return egl.eglInitialize(self)

    def terminate(self) -> None:
        """Terminate all resources associated with this display."""
        egl.eglTerminate(self)

    @property
    def attribs(self) -> dict[DisplayAttrib, Any]:
        return self._attribs

    @property
    def extensions(self) -> str:
        return egl.eglQueryString(self, egl.EGL_EXTENSIONS).decode()

    @property
    def vendor(self) -> str:
        return egl.eglQueryString(self, egl.EGL_VENDOR).decode()

    @property
    def version(self) -> tuple[int, int, str]:
        vnum, vendor_info = self.version_string.split(maxsplit=1)
        major, minor = vnum.split('.', maxsplit=1)
        return int(major), int(minor), vendor_info

    @property
    def version_string(self) -> str:
        return egl.eglQueryString(self, egl.EGL_VERSION).decode()


NoDisplay = Display(handle=egl.EGL_NO_DISPLAY)


# These are defined here to avoid a circular dependency issue, where the
# display module depends on the config module, config depends on context, and
# context depends on display.
def get_current_display(cls) -> Display:
    """Get the display for the current context on the calling thread."""
    handle = egl.eglGetCurrentDisplay()
    return Display._new_or_existing(handle, handle)
Context.get_current_display = classmethod(get_current_display)

def get_current_surface(cls, readdraw: ReadOrDraw) -> Optional[Surface]:
    """Get a surface bound to the current context.

    Note that this class method gets a surface bound to the current
    context, not to any particular context instance. The same goes for
    the class properties current_draw_surface and current_read_surface,
    which are syntactic sugar for this method.

    """
    handle = egl.eglGetCurrentSurface(readdraw)
    return (None if handle == egl.EGL_NO_SURFACE else
            Surface._new_or_existing(handle, Display.get_current_display(),
                                     handle))
Context.get_current_surface = classmethod(get_current_surface)

def release_current(cls) -> None:
    """Release the current context for the calling thread."""
    egl.eglMakeCurrent(Display.get_current_display(), egl.EGL_NO_SURFACE,
                       egl.EGL_NO_SURFACE, egl.EGL_NO_CONTEXT)
Context.release_current = classmethod(release_current)


if egl.egl_version >= (1, 1):
    def set_swap_interval(self, interval: int) -> None:
        egl.eglSwapInterval(self, interval)
    Display.swap_interval = property(fset=set_swap_interval)

  
if egl.egl_version >= (1, 2):
    def client_apis(self) -> str:
        return egl.eglQueryString(self, egl.EGL_CLIENT_APIS).decode()
    Display.client_apis = property(client_apis)

    def release_thread() -> None:
        """Release EGL resources used in this thread.

        This cleanup is performed automatically for the current thread when
        a display is deleted. Multithreaded applications that share one
        display across several threads must call this function in each
        thread to ensure all resources are deallocated.

        """
        egl.eglReleaseThread()

    __all__.extend(['release_thread'])


if egl.egl_version >= (1, 4):
    # This is defined here for the same reason as get_current_surface, above.
    def get_current_context(cls) -> Optional[Context]:
        """Get the current context for the calling thread."""
        handle = egl.eglGetCurrentContext()
        return (None if handle == egl.EGL_NO_CONTEXT else
                cls._new_or_existing(handle, Display.get_current_display(),
                                     handle))
    Context.get_current_context = classmethod(get_current_context)


if egl.egl_version >= (1, 5):
    from .image import Image
    from .sync import Sync

    def get_platform_display(cls, platform: Platform, native_display: int,
                             attribs: Optional[dict[DisplayAttrib, Any]]=None,
                             init: bool=True) -> Display:
        """Get a display associated with a given platform."""
        handle = egl.eglGetPlatformDisplay(platform, native_display,
                                           attrib_list(attribs, new_type=True))
        dpy = cls(handle=handle)
        dpy._attribs = attribs

        if init:
            dpy.initialize()
    Display.get_platform_display = classmethod(get_platform_display)

    def create_image(self, target: ImageTarget, buffer, int,
                     attribs: Optional[dict[ImageAttrib, Any]]=None) -> Image:
        """Create an image from the given buffer.

        This method creates an image without reference to a context. None
        of the targets in the core specification allow this; this method
        is only valid for extension use.

        """
        return Image(self, egl.eglCreateImage(
                               self, EGL_NO_CONTEXT, target, buffer,
                               attrib_list(attribs, new_type=True)))
    Display.create_image = create_image

    def create_sync(self, synctype: SyncType,
                    attribs: Optional[dict[SyncAttrib, Any]]=None) -> Sync:
        """Create a sync object."""
        return Sync(self, egl.eglCreateSync(self, synctype,
                                            attrib_list(attribs, new_type=True)
                                            ))
    Display.create_sync = create_sync
