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

# Standard library imports.
import ctypes
from typing import Any, Dict, Optional, Tuple
from weakref import WeakValueDictionary

# Local imports.
from . import egl
from .errors import BadDisplayError
##from .config import Config
class Config: # TODO!
    def __init__(self, handle):
        self._as_parameter_ = handle

__all__ = ['Display', 'NoDisplay']

_display_cache = WeakValueDictionary()
class Display:
    """An EGL display.

    In EGL, a display is both a representation of a (physical or virtual)
    display device, and an environment for other objects.

    """
    def __init__(self, display_id: Optional[int]=None, init: bool=True,
                 *, handle=None):
        # Specifying a display by its EGLDisplay handle overrides everything
        # else.
        if handle is not None:
            _display_cache[handle.value] = self
            self._as_parameter_ = handle
            return

        if display_id is None:
            if egl.egl_version < (1, 4):
                raise ValueError('default display not available before EGL '
                                 '1.4')
            else:
                display_id = egl.EGL_DEFAULT_DISPLAY

        self._as_parameter_ = egl.eglGetDisplay(display_id)
        _display_cache[self._as_parameter_.value] = self

        if init:
            egl.eglInitialize(self)

    def __del__(self):
        # Remove this display from the cache.
        try:
            del _display_cache[self._as_parameter_]
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

    def __eq__(self, other):
        try:
            return (other._as_parameter_ == self._as_parameter_)
        except AttributeError:
            return False

    @classmethod
    def get_current_display(cls) -> 'Display':
        """Get the display for the current context on the calling thread."""
        handle = egl.eglGetCurrentDisplay()
        try:
            dpy = _display_cache[handle.value]
        except KeyError:
            dpy = cls(handle=handle)
        return dpy

    def choose_config(self, attribs: Dict['ConfigAttrib', Any],
                      num_configs: Optional[int]=None) -> Tuple[Config, ...]:
        ...

    def get_config_count(self) -> int:
        """Get the number of configurations available on this display."""
        _, count = egl.eglGetConfigs(self, None, 0)

    def get_configs(self,
                    max_configs: Optional[int]=None) -> Tuple[Config, ...]:
        """Get a list of available configurations."""
        if max_configs is None:
            max_configs = self.get_config_count()
        configs = (egl.EGLConfig * max_configs)()
        actual_count = egl.eglGetConfigs(self, configs, max_configs)
        return tuple(Config(configs[n]) for n in range(actual_count))

    def initialize(self) -> Tuple[int, int]:
        """Initialise this display."""
        return egl.eglInitialize(self)

    def terminate(self) -> None:
        """Terminate all resources associated with this display."""
        egl.eglTerminate(self)

    @property
    def extensions(self) -> str:
        return egl.eglQueryString(self, egl.EGL_EXTENSIONS).decode()

    @property
    def vendor(self) -> str:
        return egl.eglQueryString(self, egl.EGL_VENDOR).decode()

    @property
    def version(self) -> Tuple[int, int, str]:
        vnum, vendor_info = self.version_string.split(maxsplit=1)
        major, minor = vnum.split('.', maxsplit=1)
        return int(major), int(minor), vendor_info

    @property
    def version_string(self) -> str:
        return egl.eglQueryString(self, egl.EGL_VERSION).decode()


NoDisplay = Display(handle=egl.EGL_NO_DISPLAY)


if egl.egl_version >= (1, 2):
    def client_apis(self) -> str:
        return egl.eglQueryString(self, egl.EGL_CLIENT_APIS).decode()
    Display.client_apis = property(client_apis)

    def release_thread():
        """Release EGL resources used in this thread.

        This cleanup is performed automatically for the current thread when
        a display is deleted. Multithreaded applications that share one
        display across several threads must call this function in each
        thread to ensure all resources are deallocated.

        """
        egl.eglReleaseThread()

    __all__.extend(['release_thread'])
