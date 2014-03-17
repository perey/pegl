#!/usr/bin/env python3

'''Cross-vendor swap damaged regions extension for EGL.

This extension provides hints as to which regions of a buffer have
changes ("damage") since the last swap. The whole back buffer is still
swapped, but the compositor can avoid recomposing unchanged regions.

http://www.khronos.org/registry/egl/extensions/EXT/EGL_EXT_swap_buffers_with_damage.txt

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
from . import load_ext
from ..native import c_display, c_surface, c_ibool, c_int_p
from ..surface import Surface

# Get the handle for the extension function.
native_swapdamage = load_ext(b'eglSwapBuffersWithDamageEXT', c_ibool,
                             (c_display, c_surface, c_int_p, c_int),
                             fail_on=False)

#TODO: Most of the code here was copied and minimally adapted from the older
# nok_swapregions module. Changes to one module should track in the other, and
# in fact it might be advisable to rip out common code and put it in a shared
# module somewhere.

# Wrap the extension function and place it on the Surface class.
def swap_damage(self, rects=()):
    '''Perform a buffer swap for only the regions specified as damaged.

    Keyword arguments:
        rects -- A sequence of 4-tuples, each containing the integer x-
            and y-coordinates, width and height of a region to swap. The
            origin of this coordinate system is the bottom left.

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
    native_swapdamage(self.display, self, rects_array, num_rects)
Surface.swap_damage = swap_damage
