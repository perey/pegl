#!/usr/bin/env python3

'''EGL 1.1 functions and constants for Pegl.'''

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

__all__ = ['eglBindTexImage', 'eglReleaseTexImage', 'eglSurfaceAttrib',
           'eglSwapInterval', 'EGL_BACK_BUFFER', 'EGL_BIND_TO_TEXTURE_RGB',
           'EGL_BIND_TO_TEXTURE_RGBA', 'EGL_CONTEXT_LOST',
           'EGL_MIN_SWAP_INTERVAL', 'EGL_MAX_SWAP_INTERVAL',
           'EGL_MIPMAP_TEXTURE', 'EGL_MIPMAP_LEVEL', 'EGL_NO_TEXTURE',
           'EGL_TEXTURE_2D', 'EGL_TEXTURE_FORMAT', 'EGL_TEXTURE_RGB',
           'EGL_TEXTURE_RGBA', 'EGL_TEXTURE_TARGET']

# Local imports.
from ._common import (_load_function, Arg, EGLBoolean, EGLDisplay, EGLSurface,
                      EGLint)

# Define EGL 1.1 constants.
EGL_BACK_BUFFER                 = 0x3084
EGL_BIND_TO_TEXTURE_RGB         = 0x3039
EGL_BIND_TO_TEXTURE_RGBA        = 0x303A
EGL_CONTEXT_LOST                = 0x300E
EGL_MIN_SWAP_INTERVAL           = 0x303B
EGL_MAX_SWAP_INTERVAL           = 0x303C
EGL_MIPMAP_TEXTURE              = 0x3082
EGL_MIPMAP_LEVEL                = 0x3083
EGL_NO_TEXTURE                  = 0x305C
EGL_TEXTURE_2D                  = 0x305F
EGL_TEXTURE_FORMAT              = 0x3080
EGL_TEXTURE_RGB                 = 0x305D
EGL_TEXTURE_RGBA                = 0x305E
EGL_TEXTURE_TARGET              = 0x3081

# Prototype EGL 1.1 functions.
eglBindTexImage = _load_function('eglBindTexImage', EGLBoolean,
                                 (EGLDisplay, Arg.IN, 'dpy'),
                                 (EGLSurface, Arg.IN, 'surface'),
                                 (EGLint, Arg.IN, 'buffer'),
                                 error_on=False)

eglReleaseTexImage = _load_function('eglReleaseTexImage', EGLBoolean,
                                    (EGLDisplay, Arg.IN, 'dpy'),
                                    (EGLSurface, Arg.IN, 'surface'),
                                    (EGLint, Arg.IN, 'buffer'),
                                    error_on=False)

eglSurfaceAttrib = _load_function('eglSurfaceAttrib', EGLBoolean,
                                  (EGLDisplay, Arg.IN, 'dpy'),
                                  (EGLSurface, Arg.IN, 'surface'),
                                  (EGLint, Arg.IN, 'attribute'),
                                  (EGLint, Arg.IN, 'value'),
                                  error_on=False)

eglSwapInterval = _load_function('eglSwapInterval', EGLBoolean,
                                 (EGLDisplay, Arg.IN, 'dpy'),
                                 (EGLint, Arg.IN, 'interval'),
                                 error_on=False)
