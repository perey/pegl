#!/usr/bin/env python3

'''EGL 1.2 functions and constants for Pegl.'''

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

__all__ = ['eglBindAPI', 'eglQueryAPI', 'eglCreatePbufferFromClientBuffer',
           'eglReleaseThread', 'eglWaitClient', 'EGL_ALPHA_FORMAT',
           'EGL_ALPHA_FORMAT_NONPRE', 'EGL_ALPHA_FORMAT_PRE',
           'EGL_ALPHA_MASK_SIZE', 'EGL_BUFFER_PRESERVED',
           'EGL_BUFFER_DESTROYED', 'EGL_CLIENT_APIS', 'EGL_COLORSPACE',
           'EGL_COLORSPACE_sRGB', 'EGL_COLORSPACE_LINEAR',
           'EGL_COLOR_BUFFER_TYPE', 'EGL_CONTEXT_CLIENT_TYPE',
           'EGL_DISPLAY_SCALING', 'EGL_HORIZONTAL_RESOLUTION',
           'EGL_LUMINANCE_BUFFER', 'EGL_LUMINANCE_SIZE', 'EGL_OPENGL_ES_BIT',
           'EGL_OPENVG_BIT', 'EGL_OPENGL_ES_API', 'EGL_OPENVG_API',
           'EGL_OPENVG_IMAGE', 'EGL_PIXEL_ASPECT_RATIO', 'EGL_RENDERABLE_TYPE',
           'EGL_RENDER_BUFFER', 'EGL_RGB_BUFFER', 'EGL_SINGLE_BUFFER',
           'EGL_SWAP_BEHAVIOR', 'EGL_UNKNOWN', 'EGL_VERTICAL_RESOLUTION']

# Local imports.
from ._common import *
from .egl1_0 import EGL_NO_SURFACE

# Define EGL 1.2 constants.
EGL_ALPHA_FORMAT                = 0x3088
EGL_ALPHA_FORMAT_NONPRE         = 0x308B
EGL_ALPHA_FORMAT_PRE            = 0x308C
EGL_ALPHA_MASK_SIZE             = 0x303E
EGL_BUFFER_PRESERVED            = 0x3094
EGL_BUFFER_DESTROYED            = 0x3095
EGL_CLIENT_APIS                 = 0x308D
EGL_COLORSPACE                  = 0x3087
EGL_COLORSPACE_sRGB             = 0x3089
EGL_COLORSPACE_LINEAR           = 0x308A
EGL_COLOR_BUFFER_TYPE           = 0x303F
EGL_CONTEXT_CLIENT_TYPE         = 0x3097
EGL_DISPLAY_SCALING             = 10000
EGL_HORIZONTAL_RESOLUTION       = 0x3090
EGL_LUMINANCE_BUFFER            = 0x308F
EGL_LUMINANCE_SIZE              = 0x303D
EGL_OPENGL_ES_BIT               = 0x0001
EGL_OPENVG_BIT                  = 0x0002
EGL_OPENGL_ES_API               = 0x30A0
EGL_OPENVG_API                  = 0x30A1
EGL_OPENVG_IMAGE                = 0x3096
EGL_PIXEL_ASPECT_RATIO          = 0x3092
EGL_RENDERABLE_TYPE             = 0x3040
EGL_RENDER_BUFFER               = 0x3086
EGL_RGB_BUFFER                  = 0x308E
EGL_SINGLE_BUFFER               = 0x3085
EGL_SWAP_BEHAVIOR               = 0x3093
EGL_UNKNOWN                     = EGLint(-1)
EGL_VERTICAL_RESOLUTION         = 0x3091

# Prototype EGL 1.2 functions.
eglBindAPI = _load_function('eglBindAPI', EGLBoolean,
                            (EGLenum, Arg.IN, 'api'),
                            error_on=False)

eglQueryAPI = _load_function('eglQueryAPI', EGLenum)

eglCreatePbufferFromClientBuffer = \
    _load_function('eglCreatePbufferFromClientBuffer', EGLSurface,
                   (EGLDisplay, Arg.IN, 'dpy'),
                   (EGLenum, Arg.IN, 'buftype'),
                   (EGLClientBuffer, Arg.IN, 'buffer'),
                   (EGLConfig, Arg.IN, 'config'),
                   (EGLint_p, Arg.IN, 'attrib_list'),
                   error_on=EGL_NO_SURFACE)

eglReleaseThread = _load_function('eglReleaseThread', EGLBoolean,
                                  error_on=False)

eglWaitClient = _load_function('eglWaitClient', EGLBoolean, error_on=False)
