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

__all__ = ['Display', 'NoDisplay']

# Standard library imports.
from ctypes import ArgumentError
from types import MappingProxyType

# Local imports.
from . import egl
from .attribs import attrib_list
from ._caching import cached
from .errors import BadDisplayError
from .config import Config
from .context import Context
from .surface import Surface


@cached
class Display:
    """An EGL display.

    In EGL, a display is both a representation of a (physical or virtual)
    display device, and an environment for other objects.

    """
    def __init__(self, display_id=None, init=True, *, handle=None):
        # Specifying a display by its EGLDisplay handle overrides everything
        # else.
        if handle is not None:
            self._as_parameter_ = handle
            self._cache_key = None

            self.__class__._add_to_cache(self)
            return

        if display_id is None:
            if egl.egl_version < (1, 4):
                raise ValueError('default display not available before EGL '
                                 '1.4')
            display_id = egl.EGL_DEFAULT_DISPLAY

        self._as_parameter_ = egl.eglGetDisplay(display_id)
        self._cache_key = display_id

        self.__class__._add_to_cache(self)

        # Forwards compatibility.
        self._swap_interval = 1 # Default per § 3.10.3
        self._attribs = MappingProxyType({})

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
        except ArgumentError:
            # This instance never had its handle assigned (probably because it
            # was created on EGL 1.3 or earlier without a display_id), so
            # ctypes wouldn't even pass it to eglTerminate.
            pass
        else:
            # If termination was successful, also release EGL resources in this
            # thread.
            if egl.egl_version >= (1, 2):
                egl.eglReleaseThread()

    def __bool__(self):
        return self._as_parameter_ != egl.EGL_NO_DISPLAY

    def __eq__(self, other):
        try:
            return other._as_parameter_ == self._as_parameter_
        except AttributeError:
            return False

    @classmethod
    def get_current_display(cls):
        """Get the display for the current context on the calling thread."""
        handle = egl.eglGetCurrentDisplay()
        return cls._new_or_existing((handle, None), handle)

    def choose_config(self, attribs, num_config=None):
        """Get available configurations that match given attributes."""
        if num_config is None:
            num_config = self.get_config_count()
        configs = (egl._common.EGLConfig * num_config)()
        actual_count = egl.eglChooseConfig(self, attrib_list(attribs),
                                           configs, num_config)
        return tuple(Config._new_or_existing((configs[n], None),
                                             self, configs[n])
                     for n in range(actual_count))

    def get_config_count(self) -> int:
        """Get the number of configurations available on this display."""
        return egl.eglGetConfigs(self, None, 0)

    def get_configs(self, num_config=None):
        """Get a list of available configurations."""
        if num_config is None:
            num_config = self.get_config_count()
        configs = (egl._common.EGLConfig * num_config)()
        actual_count = egl.eglGetConfigs(self, configs, num_config)
        return tuple(Config._new_or_existing((configs[n], None),
                                             self, configs[n])
                     for n in range(actual_count))

    def initialize(self):
        """Initialise this display."""
        return egl.eglInitialize(self)

    def terminate(self):
        """Terminate all resources associated with this display."""
        egl.eglTerminate(self)

    @property
    def attribs(self):
        """The attributes used to create this display, if any."""
        return self._attribs

    @property
    def extensions(self):
        """The EGL extensions supported by this display."""
        return egl.eglQueryString(self, egl.EGL_EXTENSIONS).decode()

    @property
    def vendor(self):
        """The vendor information for the EGL implementation."""
        return egl.eglQueryString(self, egl.EGL_VENDOR).decode()

    @property
    def version(self):
        """The version information for the EGL implementation."""
        vnum, *vendor_info = self.version_string.split(maxsplit=1)
        vendor_info = '' if not vendor_info else vendor_info[0]
        major, minor = vnum.split('.', maxsplit=1)
        return int(major), int(minor), vendor_info

    @property
    def version_string(self):
        """The version information string for the EGL implementation."""
        return egl.eglQueryString(self, egl.EGL_VERSION).decode()


NoDisplay = Display(handle=egl.EGL_NO_DISPLAY)


# These are defined here to avoid a circular dependency issue, where the
# display module depends on the config module, config depends on context, and
# context depends on display.
def get_current_surface(cls, readdraw): # pylint: disable=unused-argument
    """Get a surface bound to the current context.

    Note that this class method gets a surface bound to the current
    context, not to any particular context instance. The same goes for
    the class properties current_draw_surface and current_read_surface,
    which are syntactic sugar for this method.

    """
    handle = egl.eglGetCurrentSurface(readdraw)
    return (None if handle == egl.EGL_NO_SURFACE else
            Surface._new_or_existing((handle, None),
                                     Display.get_current_display(),
                                     handle))
setattr(Context, 'get_current_surface', classmethod(get_current_surface))

def release_current(cls): # pylint: disable=unused-argument
    """Release the current context for the calling thread."""
    egl.eglMakeCurrent(Display.get_current_display(), egl.EGL_NO_SURFACE,
                       egl.EGL_NO_SURFACE, egl.EGL_NO_CONTEXT)
setattr(Context, 'release_current', classmethod(release_current))


if egl.egl_version >= (1, 1):
    def get_swap_interval(self):
        """The number of video frames to wait between buffer swaps."""
        return self._swap_interval
    def set_swap_interval(self, interval):
        # pylint: disable=missing-function-docstring
        egl.eglSwapInterval(self, interval)
        self._swap_interval = interval
    setattr(Display, 'swap_interval', property(get_swap_interval,
                                               set_swap_interval))


if egl.egl_version >= (1, 2):
    def client_apis(self):
        """The client APIs supported on this display."""
        return egl.eglQueryString(self, egl.EGL_CLIENT_APIS).decode()
    setattr(Display, 'client_apis', property(client_apis))

    def release_thread():
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
    def get_current_context(cls):
        """Get the current context for the calling thread."""
        handle = egl.eglGetCurrentContext()
        return (None if handle == egl.EGL_NO_CONTEXT else
                cls._new_or_existing((handle, None),
                                     Display.get_current_display(),
                                     handle))
    setattr(Context, 'get_current_context', classmethod(get_current_context))


if egl.egl_version >= (1, 5):
    from .image import Image
    from .sync import Sync

    def get_platform_display(cls, platform, native_display, attribs=None,
                             init=True):
        """Get a display associated with a given platform."""
        handle = egl.eglGetPlatformDisplay(platform, native_display,
                                           attrib_list(attribs, new_type=True))
        dpy = cls(handle=handle)
        # Save an immutable view of the attributes used.
        dpy._attribs = MappingProxyType({} if attribs is None else attribs)

        if init:
            dpy.initialize()

        return dpy
    setattr(Display, 'get_platform_display', classmethod(get_platform_display))

    def create_image(self, target, buffer, attribs=None):
        """Create an image from the given buffer.

        This method creates an image without reference to a context. None
        of the targets in the core specification allow this; this method
        is only valid for extension use.

        """
        return Image(self,
                     egl.eglCreateImage(self, egl.EGL_NO_CONTEXT, target,
                                        buffer,
                                        attrib_list(attribs, new_type=True)))
    setattr(Display, 'create_image', create_image)

    def create_sync(self, synctype, attribs=None):
        """Create a sync object."""
        return Sync(self,
                    egl.eglCreateSync(self, synctype,
                                      attrib_list(attribs, new_type=True)))
    setattr(Display, 'create_sync', create_sync)
