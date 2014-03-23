#!/usr/bin/env python3

'''Khronos OpenCL event sync extension for EGL.

Note that, because it puts an OpenCL event handle into an attribute list
where (especially on 64-bit systems) it is not guaranteed to fit, this
extension is deprecated and replaced by khr_clevent2.

http://www.khronos.org/registry/egl/extensions/KHR/EGL_KHR_cl_event.txt

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
from ctypes import c_int

# Local imports.
from .khr_sync import FenceSync, SyncAttribs

# New sync attribute.
SyncAttribs.extend('CL_EVENT_HANDLE', 0x309C, c_int, None)

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
            handle (attribute SyncAttribs.CL_EVENT_HANDLE).
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
        super().__init__(display, {SyncAttribs.CL_EVENT_HANDLE: cl_event})
