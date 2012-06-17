#!/usr/bin/env python3

'''NVIDIA sub-buffer post extension for EGL.

This extension provides a mechanism for posting a region of a window
surface while preserving the back buffer.

http://www.khronos.org/registry/egl/extensions/NV/EGL_NV_post_sub_buffer.txt

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
from ...attribs.surface import SurfaceAttribs
from ...native import ebool
from ...surface import Surface

# Get the handle for the extension function.
native_postsubbuffer = load_ext(b'eglPostSubBufferNV', ebool,
                                (display, surface, c_int, c_int, c_int, c_int),
                                fail_on=False)

# Wrap the extension function and place it on the Surface class. (While the
# extension is targeted specifically at window surfaces, its open-ended
# language, plus the new attribute defined below, suggest that other surfaces
# may support it also.)
def post_subbuffer(self, rect):
    '''Post a region of the back buffer to the surface.

    Keyword arguments:
        rect -- A 4-tuple containing the integer x- and y-coordinates,
            width and height of the buffer region to post. The origin of
            the coordinate pair is the lower left corner of the surface.

    '''
    x, y, width, height = rect
    native_postsubbuffer(self.display, self, x, y, width, height)
Surface.post_subbuffer = post_subbuffer

# New surface attributes.
SurfaceAttribs.extend('POST_SUB_BUFFER_SUPPORTED', 0x30BE, ebool, False)

# Provide a property to query the new attribute.
def can_post_subbuffer(self):
    '''Query whether or not posting of a sub-buffer region is supported.

    Returns:
        True if the post_subbuffer() method is supported and False
        otherwise.

    '''
    return self._attr(SurfaceAttribs.POST_SUB_BUFFER_SUPPORTED)
