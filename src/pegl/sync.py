#!/usr/bin/env python3

"""EGL synchronisation control for Pegl."""

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

__all__ = ['wait_gl', 'wait_native']

# Local imports.
from . import egl
from .enums import NativeEngine

def wait_gl():
    """Instruct native rendering to wait on any OpenGL ES rendering.

    EGL provides this function for backwards compatibility; it is
    defined to be equivalent to saving the bound API, binding the
    OpenGL ES API, calling wait_client(), and then rebinding the
    original API. New code should just use wait_client() instead.

    """
    egl.eglWaitGL()

def wait_native(engine=NativeEngine.CORE):
    """Instruct client API rendering to wait on any native rendering.

    Keyword arguments:
        engine -- An implementation-defined reference to a native
            rendering engine. If omitted, the reference points to the
            EGL core native engine.

    """
    egl.eglWaitNative(engine)

if egl.egl_version >= (1, 2):
    def wait_client():
        """Instruct native rendering to wait on any client API rendering.

        This is an EGL-level instruction equivalent to API-specific calls
        such as glFinish().

        """
        egl.eglWaitClient()

    __all__.extend(['wait_client'])

if egl.egl_version >= (1, 5):
    from .enums import SyncCondition, SyncFlag, SyncResult, SyncType

    class Sync:
        """An object that is 'signalled' when a condition is met."""
        def __init__(self, display, handle):
            self._as_parameter_ = handle
            self._display = display

        def client_wait_sync(self, flags=SyncFlag.NONE, timeout=None):
            """Block the calling thread, waiting on this sync.

            Keyword arguments:
                flags -- An optional set of flags to control the waiting
                    behaviour. If omitted, no flags are set.
                timeout -- A number of nanoseconds to wait before
                    unblocking if the sync is not signalled. If this is
                    None or omitted, then the sync will wait indefinitely.

            """
            if timeout is None:
                timeout = egl.EGL_FOREVER
            result = egl.eglClientWaitSync(self._display, self, flags, timeout)
            return SyncResult(result)

        def wait_sync(self, flags=SyncFlag.NONE):
            """Instruct the client API server to wait on this sync."""
            egl.eglWaitSync(self._display, self, flags)

        @property
        def sync_condition(self):
            """When will this sync object be signaled?"""
            return SyncCondition(egl.eglGetSyncAttrib(self._display, self,
                                                      egl.EGL_SYNC_CONDITION))

        @property
        def sync_status(self):
            """Is this sync object signaled?"""
            return bool(egl.eglGetSyncAttrib(self._display, self,
                                             egl.EGL_SYNC_STATUS))

        @property
        def sync_type(self):
            """The type of this sync object."""
            return SyncType(egl.eglGetSyncAttrib(self._display, self,
                                                 egl.EGL_SYNC_TYPE))

    __all__.extend(['Sync'])
