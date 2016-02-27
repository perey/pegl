#!/usr/bin/env python3

'''Android sync extensions for EGL.

This module defines a "fence sync object" (from the pegl.ext.khr_sync
module) that is associated with an operating-system native sync object
having a file descriptor.

http://www.khronos.org/registry/egl/extensions/ANDROID/EGL_ANDROID_native_fence_sync.txt

'''
# Copyright © 2012 Tim Pederick.
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
from ctypes import c_int

# Local imports.
from .khr_sync import c_sync, Sync, SyncAttribs
from ..native import c_display

# New symbolic constants.
NATIVE_FENCE = 0x3144
NATIVE_FENCE_SIGNALED = 0x3146
NO_NATIVE_FENCE_FD = -1
# TODO: Use a custom, extensible alternative to the namedtuple class, so that
# NATIVE_FENCE can be added to khr_sync.SyncTypes, and NATIVE_FENCE_SIGNALED
# to khr_sync.SyncConditions. Of course, I'm really only using those namedtuple
# instances as enumerations, and there's now a proper one of those in the
# standard library as of Python 3.3...

# Get handles of extension functions.
native_dupnativefence = load_ext(b'eglDupNativeFenceFDANDROID', c_int,
                             (c_display, c_sync), fail_on=NO_NATIVE_FENCE_FD)

# New sync attribute.
SyncAttribs.extend('NATIVE_FENCE_FD', 0x3145, c_int, NO_NATIVE_FENCE_FD)

# New Sync subclass.
class NativeFenceSync(Sync):
    '''Represents the "native fence" type of sync object.

    Class attributes:
        extension -- The name string of the native fence sync extension.
        sync_type -- SyncTypes.FENCE.

    Instance attributes:
        synchandle, display, status, signaled, sync_type -- As per the
            superclass, Sync.
        attribs -- Always an empty AttribList.
        fd -- The file descriptor associated with this sync object.
        sync_condition -- The condition under which this sync object
            will be automatically set to signaled. Should always be the
            value 0x3146 (decimal 12614), indicating "native fence
            signaled".

    '''
    extension = 'EGL_ANDROID_native_fence_sync'
    sync_type = NATIVE_FENCE

    def __init__(self, display, fd=NO_NATIVE_FENCE_FD):
        '''Create the fence sync object.

        Keyword arguments:
            display -- As the instance attribute.

        '''
        # Native fence sync objects have only one attribute.
        super().__init__(display, {SyncAttribs.NATIVE_FENCE_FD: fd})

    @property
    def sync_condition(self):
        '''Get the condition under which this sync object gets signaled.'''
        return self._attr(SyncAttribs.SYNC_CONDITION)

    def duplicate_fd(self):
        '''Get a duplicate of this sync object's file descriptor.'''
        return native_dupnativefence(self.display, self)
