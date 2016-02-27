#!/usr/bin/env python3

'''Cross-vendor buffer age extension for EGL.

http://www.khronos.org/registry/egl/extensions/EXT/EGL_EXT_buffer_age.txt

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
from ..attribs.surface import SurfaceAttribs
from ..surface import Surface

# This extension defines just one new surface attribute.
BUFFER_AGE = 0x3134
SurfaceAttribs.extend('BUFFER_AGE', BUFFER_AGE, c_int, 0)

# New Surface property, for querying the new attribute in SurfaceAttribs.
# This attribute cannot be set.
def buffer_age(self):
    '''Get the age (in frames) of the current back buffer contents.

    Single-buffered drawing never has a "back" buffer as such, and so
    the buffer age will always be 0. An age of 1 indicates that the last
    buffer swap just copied contents; double-buffering will usually give
    an age of 2, triple-buffering a 3, and so on.

    '''
    return self._attr(SurfaceAttribs.BUFFER_AGE)
Surface.buffer_age = property(buffer_age)
