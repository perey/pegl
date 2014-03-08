#!/usr/bin/env python3

'''Android blob caching extension for EGL.

This extension is used to provide functions for accessing a cache, in
which compiled shaders and other binary blobs can be stored.

http://www.khronos.org/registry/egl/extensions/ANDROID/EGL_ANDROID_blob_cache.txt


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
from ctypes import CFUNCTYPE, c_void_p
try:
    # New in Python 3.2!
    from ctypes import c_ssize_t as c_sizei
except ImportError:
    # Fallback for older Python versions.
    from ctypes import c_longlong as c_sizei

# Local imports.
from . import load_ext
from ..display import Display
from ..native import c_display

# New extension types. Note that c_sizei was defined by import, above.
c_setter = CFUNCTYPE(None, c_void_p, c_sizei, c_void_p, c_sizei)
c_getter = CFUNCTYPE(c_sizei, c_void_p, c_sizei, c_void_p, c_sizei)

# Get the handle of the new extension function.
native_setblobfuncs = load_ext(b'eglSetBlobCacheFuncsANDROID', None,
                               (c_display, c_setter, c_getter))

# New Display function.
def set_blob_cache_funcs(self, setter, getter):
    '''Set the blob cache set and get functions.

    Keyword arguments:
        setter, getter -- Native pointers to the callback functions.

    '''
    # Call the native function.
    native_setblobfuncs(self, setter, getter)
Display.set_blob_cache_funcs = set_blob_cache_funcs
