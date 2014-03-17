#!/usr/bin/env python3

'''Nokia swap buffer region extension for EGL.

This extension allows a buffer swap to be performed only on specified
regions of the back buffer.

http://www.khronos.org/registry/egl/extensions/NOK/EGL_NOK_swap_region2.txt

'''
# Copyright © 2012-14 Tim Pederick.
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
from . import load_ext
from ..native import c_ibool, c_display, c_surface, c_int_p
from ..surface import Surface

# Get the handle for the extension function.
native_swapregion = load_ext(b'eglSwapBuffersRegion2NOK', c_ibool,
                             (c_display, c_surface, c_int, c_int_p),
                             fail_on=False)

# TODO: This code is copied more or less exactly from the older nok_swapregion
# module; the ext_swapdamage module does the same. Any changes to one of these
# modules should be tracked in the others, and it would be nice to rip out the
# common code and put it into a shared module. Also, nok_swapregion can be
# deprecated now that this extension is supported.

# Wrap the extension function and place it on the Surface class.
def swap_regions(self, rects):
    '''Perform a buffer swap for only the specified regions.

    Keyword arguments:
        rects -- A sequence of 4-tuples, each containing the integer x-
        and y-coordinates, width and height of a region to swap.

    '''
    RECT_LEN = 4

    # Flatten the 4-tuples into one long list of points.
    num_rects = len(rects)
    rect_points = []
    for rect in rects:
        if len(rect) > RECT_LEN:
            # Trim the excess.
            rect_points.extend(rect[:RECT_LEN])
        elif len(rect) < RECT_LEN:
            # Pad with zeroes.
            rect_points.extend((rect + (0,) * RECT_LEN)[:RECT_LEN])
        else:
            # "But the third chair was just right!"
            rect_points.extend(rect)
    # Sanity check.
    assert len(rect_points) == RECT_LEN * num_rects

    # Construct the array of integers.
    arr_type = c_int * (RECT_LEN * num_rects)
    # Make it a pointer to int to keep ctypes happy.
    rects_array = c_int_p(arr_type(*rect_points))

    # Perform the swap.
    native_swapregion(self.display, self, num_rects, rects_array)
Surface.swap_regions = swap_regions
