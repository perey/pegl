#!/usr/bin/env python3

'''Nokia swap buffer region extension for EGL.

I can't find any official specification for this extension; it appears
to have gone offline when http://developer.symbian.org/ was closed.
However, support is widely available through the Mesa library, which
gives just one function signature:

    EGLBoolean eglSwapBuffersRegionNOK(EGLDisplay dpy,
                                       EGLSurface surface,
                                       EGLint numRects,
                                       const EGLint* rects);

The Mesa commit message that added support also has this to say:
    This extension adds a new function which provides an alternative to
    eglSwapBuffers. eglSwapBuffersRegionNOK accepts two new parameters
    in addition to those in eglSwapBuffers. The new parameters consist
    of a pointer to a list of 4-integer blocks defining rectangles (x,
    y, width, height) and an integer specifying the number of rectangles
    in the list.

http://cgit.freedesktop.org/mesa/mesa/commit/src/egl?id=52c554a79d3ed3104a9f7d112faa9129073b5a25

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
from ctypes import c_int

# Local imports.
from .. import load_ext
from ... import int_p
from ...surface import Surface

# Get the handle for the extension function.
native_swapregion = load_ext(b'eglSwapBuffersRegionNOK', ebool,
                       (display, surface, c_int, int_p), fail_on=False)

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
    rects_array = int_p(arr_type(*rect_points))

    # Perform the swap.
    native_swapregion(self.display, self, num_rects, rects_array)
Surface.swap_regions = swap_regions
