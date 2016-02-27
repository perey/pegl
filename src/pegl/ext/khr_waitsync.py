#!/usr/bin/env python3

'''Khronos server-wait sync extension for EGL.

A server-wait sync call is similar to an ordinary (client) wait on a
sync object. However, rather than the thread making the call, it is the
thread serving the request that blocks.

http://www.khronos.org/registry/egl/extensions/KHR/EGL_KHR_wait_sync.txt

'''
# Copyright © 2013 Tim Pederick.
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
from .. import load_ext
from .khr_sync import c_sync, Sync
from ..native import c_display, c_ibool

# Get the handle of the extension function.
native_waitsync = load_ext(b'eglWaitSyncKHR', c_ibool, # Technically it returns
                           (c_display, c_sync, c_int), # an int, but the only
                           fail_on=False)              # values are 0 and 1.

# Add server-wait functionality to the Sync class.
def server_wait(self):
    '''Block the server thread until this sync object is signaled.

    This function will return immediately; the calling thread is not
    blocked! Instead, the thread serving the client API blocks.

    '''
    # From the extension spec: "<flags> must be 0."
    return native_waitsync(self.display, self, 0)
    # The return value is ignorable, since it should only ever be True; if it
    # would be False, an exception should have resulted instead.
Sync.server_wait = server_wait
