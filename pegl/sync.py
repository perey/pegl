#!/usr/bin/env python3

'''EGL 1.4 thread controls.'''

# Copyright © 2012 Tim Pederick.
#
# This file is part of PEGL.
#
# PEGL is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PEGL is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
# License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PEGL. If not, see <http://www.gnu.org/licenses/>.

# Local imports.
from . import egl, error_check

@error_check
def release_thread():
    return bool(egl.eglReleaseThread())

@error_check
def wait_client():
    return bool(egl.eglWaitClient())

@error_check
def wait_GL():
    return bool(egl.eglWaitGL())

@error_check
def wait_native():
    return bool(egl.eglWaitNative())
