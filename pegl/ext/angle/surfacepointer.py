#!/usr/bin/env python3

'''ANGLE surface-pointer querying extension for EGL.

This extension allows querying pointer attributes of surfaces, while
avoiding 32- versus 64-bit problems.

http://www.khronos.org/registry/egl/extensions/ANGLE/EGL_ANGLE_query_surface_pointer.txt

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
from ctypes import c_int, c_void_p, POINTER

# Local imports.
from .. import load_ext
from ...native import ebool, display, surface
from ...surface import Surface

# ctypes type necessary for querying pointer values.
c_void_pp = POINTER(c_void_p)

# Get handle of the extension function.
native_query = load_ext(b'eglQuerySurfacePointerANGLE', ebool,
                        (display, surface, c_int, c_void_pp), fail_on=False)

# Add function to the Surface class.
def _attr_ptr(self, attr):
    '''Get the value of a surface attribute.

    Keyword arguments:
        attr -- The identifier of the attribute requested.

    '''
    # Query the attribute, storing the result in a pointer.
    result = c_void_pp(None)
    native_query(self.display, self, attr, result)

    # Dereference the pointer.
    return result.contents
Surface._attr_ptr = _attr_ptr
