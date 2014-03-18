#!/usr/bin/env python3

'''Khronos OpenGL colorspace extension for EGL.

This extension allows OpenGL and OpenGL ES surfaces to use the sRGB
and linear colorspaces that are already available to OpenVG.

http://www.khronos.org/registry/egl/extensions/KHR/EGL_KHR_gl_colorspace.txt

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
from collections import namedtuple

# Local imports.
from ..surface import Surface
from ..attribs.surface import SurfaceAttribs

# New surface attributes.
GLColorSpaces = namedtuple('GLColorSpaces_tuple',
                           ('SRGB', 'LINEAR')
                           )(0x3089, 0x308A)
SurfaceAttribs.extend('GL_COLORSPACE', 0x309D, GLColorSpaces,
                      GLColorSpaces.LINEAR)

# New Surface property for querying the new attribute.
def opengl_colorspace(self):
    '''Get the OpenGL/OpenGL ES colorspace in use on this surface.'''
    return self._attr(SurfaceAttribs.GL_COLORSPACE)
Surface.opengl_colorspace = property(opengl_colorspace)
