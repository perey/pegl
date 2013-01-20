#!/usr/bin/env python3

'''NVIDIA system time extension for EGL.

This extension provides a means of querying the system time from the EGL
system rather than any external API.

http://www.khronos.org/registry/egl/extensions/NV/EGL_NV_system_time.txt

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
from ctypes import c_ulonglong

# Local imports.
from .. import load_ext

# Get handles for extension functions.
native_freq = load_ext(b'eglGetSystemTimeFrequencyNV', c_ulonglong, ())
native_time = load_ext(b'eglGetSystemTimeNV', c_ulonglong, ())

# Wrap the extension functions.
def _freq():
    '''Get the frequency of the system timer, in ticks per second.

    This value is guaranteed not to change while the system is running,
    and so the module attribute frequency may be used instead of
    querying the system timer repeatedly with this function.

    '''
    return native_freq()

# Look up the frequency once and save it for future use.
frequency = _freq()

def systime():
    '''Get the current value of the system timer.

    The value returned is a number of implementation-defined "ticks";
    the conversion from ticks to seconds can be found with the freq()
    function, or else the time() function can be called to do this
    conversion automatically.

    '''
    return native_time()

def time():
    '''Get the current system time, in seconds.'''
    return native_time() / frequency
