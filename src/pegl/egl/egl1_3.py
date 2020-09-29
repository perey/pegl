#!/usr/bin/env python3

'''EGL 1.3 constants for Pegl.'''

# Copyright © 2012, 2013, 2020 Tim Pederick.
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
#
# This file is based on the header file egl.h, which carries the following
# copyright statement and licensing information:
#
#     Copyright (c) 2013-2017 The Khronos Group Inc.
#
#     Permission is hereby granted, free of charge, to any person obtaining a
#     copy of this software and/or associated documentation files (the
#     "Materials"), to deal in the Materials without restriction, including
#     without limitation the rights to use, copy, modify, merge, publish,
#     distribute, sublicense, and/or sell copies of the Materials, and to
#     permit persons to whom the Materials are furnished to do so, subject to
#     the following conditions:
#
#     The above copyright notice and this permission notice shall be included
#     in all copies or substantial portions of the Materials.
#
#     THE MATERIALS ARE PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#     EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#     MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#     IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
#     CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#     TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#     MATERIALS OR THE USE OR OTHER DEALINGS IN THE MATERIALS.

__all__ = ['EGL_CONFORMANT', 'EGL_CONTEXT_CLIENT_VERSION',
           'EGL_MATCH_NATIVE_PIXMAP', 'EGL_OPENGL_ES2_BIT',
           'EGL_VG_ALPHA_FORMAT', 'EGL_VG_ALPHA_FORMAT_NONPRE',
           'EGL_VG_ALPHA_FORMAT_PRE', 'EGL_VG_ALPHA_FORMAT_PRE_BIT',
           'EGL_VG_COLORSPACE', 'EGL_VG_COLORSPACE_sRGB',
           'EGL_VG_COLORSPACE_LINEAR', 'EGL_VG_COLORSPACE_LINEAR_BIT']

# TODO: There are no new EGL 1.3 functions, so a lack of support will not be
# detected when failing to load this module. Should I detect support in some
# other way?

# Define EGL 1.3 constants.
EGL_CONFORMANT                  = 0x3042
EGL_CONTEXT_CLIENT_VERSION      = 0x3098
EGL_MATCH_NATIVE_PIXMAP         = 0x3041
EGL_OPENGL_ES2_BIT              = 0x0004
EGL_VG_ALPHA_FORMAT             = 0x3088
EGL_VG_ALPHA_FORMAT_NONPRE      = 0x308B
EGL_VG_ALPHA_FORMAT_PRE         = 0x308C
EGL_VG_ALPHA_FORMAT_PRE_BIT     = 0x0040
EGL_VG_COLORSPACE               = 0x3087
EGL_VG_COLORSPACE_sRGB          = 0x3089 # pylint: disable=invalid-name
EGL_VG_COLORSPACE_LINEAR        = 0x308A
EGL_VG_COLORSPACE_LINEAR_BIT    = 0x0020
