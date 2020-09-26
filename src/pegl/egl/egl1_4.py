#!/usr/bin/env python3

'''EGL 1.4 functions and constants for Pegl.'''

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

__all__ = ['eglGetCurrentContext', 'EGL_DEFAULT_DISPLAY',
           'EGL_MULTISAMPLE_RESOLVE_BOX_BIT', 'EGL_MULTISAMPLE_RESOLVE',
           'EGL_MULTISAMPLE_RESOLVE_DEFAULT', 'EGL_MULTISAMPLE_RESOLVE_BOX',
           'EGL_OPENGL_API', 'EGL_OPENGL_BIT',
           'EGL_SWAP_BEHAVIOR_PRESERVED_BIT']

# Local imports.
from ._common import *

# Define EGL 1.4 constants.
EGL_DEFAULT_DISPLAY             = EGLNativeDisplayType(0)
EGL_MULTISAMPLE_RESOLVE_BOX_BIT = 0x0200
EGL_MULTISAMPLE_RESOLVE         = 0x3099
EGL_MULTISAMPLE_RESOLVE_DEFAULT = 0x309A
EGL_MULTISAMPLE_RESOLVE_BOX     = 0x309B
EGL_OPENGL_API                  = 0x30A2
EGL_OPENGL_BIT                  = 0x0008
EGL_SWAP_BEHAVIOR_PRESERVED_BIT = 0x0400

# Prototype EGL 1.4 functions.
eglGetCurrentContext = _load_function('eglGetCurrentContext', EGLContext)
