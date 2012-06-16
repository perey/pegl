#!/usr/bin/env python3

'''Khronos OpenGL image binding for EGL.

The one specification defines four extensions with their own name
strings and parameters.

http://www.khronos.org/registry/egl/extensions/KHR/EGL_KHR_gl_image.txt

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
from .image import Image, ImageAttribs

# 2D image attributes.
Image.extend('EGL_KHR_gl_texture_2D_image', {'GL_TEXTURE_2D': 0x30B1})
ImageAttribs.extend('GL_TEXTURE_LEVEL', 0x30BC, c_int, 0,
                    'The mipmap level to use as the image source')

# Cube map image attributes.
Image.extend('EGL_KHR_gl_texture_cubemap_image',
             dict(zip((sign + axis for axis in ('X', 'Y', 'Z')
                       for sign in ('POSITIVE_', 'NEGATIVE_')),
                      range(0x30B3, 0x30B9))))

# 3D image attributes.
Image.extend('EGL_KHR_gl_texture_3D_image', {'GL_TEXTURE_3D': 0x30B2})
ImageAttribs.extend('GL_TEXTURE_ZOFFSET', 0x30BD, c_int, 0,
                    'The depth offset of the image to use as the source')

# Render buffer attributes.
Image.extend('EGL_KHR_gl_renderbuffer_image', {'GL_RENDERBUFFER': 0x30B9})
