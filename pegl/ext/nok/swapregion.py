#!/usr/bin/env python3

'''Khronos lock-surface extension for EGL.

I can't find any official specification for this extension; it appears
to have gone offline when http://developer.symbian.org/ was closed.
However, support is widely available through the Mesa library, which
specifies the following signature in eglmesaext.h:

    EGLBoolean eglSwapBuffersRegionNOK(EGLDisplay dpy, EGLSurface surface,
                                       EGLint numRects,
                                       const EGLint* rects);

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
from collections import namedtuple
from ctypes import c_int

# Local imports.
from .. import load_ext
from ... import int_p
from ...surface import Surface

# Get the handle for the extension function.
native_swapregion = load_ext(b'eglSwapBuffersRegionNOK', ebool,
                       (display, surface, c_int, int_p), fail_on=False)

# Wrap the extension function and place it on the Surface class.
def swap_region(self, rects):
    '''Perform a buffer swap for only the specified region(s).

    Keyword arguments:
        rects -- A sequence of integers defining the rectangular regions
            to swap.

    '''
    # Construct the array of integers.
    num_rects = len(rects) # I'm going to be annoyed, but not surprised, if it
                           # turns out that the array has four integers for
                           # each rect and so num_rects should be only a
                           # quarter of the array length (len(rects) // 4).
    arr_type = c_int * num_rects
    # Get the array as a pointer to int, to keep ctypes happy.
    rects_array = int_p(arr_type(*rects))

    # Perform the swap.
    native_swapregion(self.display, self, num_rects, rects_array)
Surface.swap_region = swap_region
