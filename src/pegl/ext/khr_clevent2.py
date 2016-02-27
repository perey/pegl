#!/usr/bin/env python3

'''Khronos OpenCL event sync extension for EGL.

This extension obsoletes the one in the khr_clevent module. The decision
to use one module or the other, however, depends on which extension the
EGL implementation supports.

http://www.khronos.org/registry/egl/extensions/KHR/EGL_KHR_cl_event2.txt

'''
# Copyright © 2014 Tim Pederick.
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
from ctypes import c_int, c_int64, POINTER

# Local imports.
from .khr_sync import FenceSync, SyncAttribs

# New native type. Note that the type EGLAttribKHR is actually defined to be an
# intptr_t, but as that's not supported in ctypes, a 64-bit integer will have
# to suffice. This might break on 128-bit systems(!).
c_wideattr = c_int64
c_wideattr_list = POINTER(c_int64)

# Get handle for the new extension function.
native_createsync = load_ext(b'eglCreateSync64KHR', c_sync,
                             (c_display, c_enum, c_wideattr_list),
                             fail_on=NO_SYNC)

# Subclass SyncAttribs to generate wider native values, and add the new sync
# attribute.
class WideSyncAttribs(SyncAttribs):
    '''The set of attributes relevant to sync objects.

    Unlike the superclass, SyncAttribs, this class uses a native type
    that can fit any pointer, avoiding size issues on systems wider than
    32 bits that fail to define their EGLint types as an appropriate
    width.

    Class attributes:
        details -- As per the superclass, Attribs.
        Additionally, symbolic constants for all the known attributes
        are available as class attributes. Their names are the same as
        in the extension specification, except without the EGL_ prefix
        and _KHR suffix.

    '''
    _native_item = c_wideattr
    _native_list = c_wideattr_list

WideSyncAttribs.extend('CL_EVENT_HANDLE', 0x309C, c_wideattr, None)

# New values for SyncTypes and SyncConditions.
# TODO: Replace the namedtuple instances with extensible enumerations.
SYNC_CL_EVENT = 0x30FE
SYNC_CL_EVENT_COMPLETE = 0x30FF

# New Sync subclass.
class OpenCLSync(FenceSync):
    '''A sync object for waiting on an OpenCL event.

    Class attributes:
        extension -- The name string of the OpenCL event sync extension.
        sync_type -- The value 0x30FE, represented by the symbolic name
            SYNC_CL_EVENT.

    Instance attributes:
        synchandle, display, status, signaled, sync_type -- As per the
            superclass, FenceSync.
        attribs -- Contains one attribute, namely the OpenCL event
            handle (attribute WideSyncAttribs.CL_EVENT_HANDLE).
        sync_condition -- The condition under which this sync object
            will be automatically set to signaled. Should always be the
            value SYNC_CL_EVENT_COMPLETE.

    '''
    extension = 'EGL_KHR_cl_event'
    sync_type = SYNC_CL_EVENT

    def __init__(self, display, cl_event):
        '''Create the fence sync object.

        Keyword arguments:
            display -- As the instance attribute.
            cl_event -- The native handle for an OpenCL event.

        '''
        # OpenCL event sync objects have one attribute, an OpenCL event handle.
        super().__init__(display, {WideSyncAttribs.CL_EVENT_HANDLE: cl_event})

    def _create_handle(self):
        '''Call the native function that generates the sync handle.'''
        return native_createsync(self.display, self.__class__.sync_type,
                                 self.attribs)
