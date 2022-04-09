#!/usr/bin/env python3

'''EGL 1.5 functions and constants for Pegl.'''

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

__all__ = ['eglCreateSync', 'eglDestroySync', 'eglClientWaitSync',
           'eglGetSyncAttrib', 'eglCreateImage', 'eglDestroyImage',
           'eglGetPlatformDisplay', 'eglCreatePlatformWindowSurface',
           'eglCreatePlatformPixmapSurface', 'eglWaitSync',
           'EGL_CONTEXT_MAJOR_VERSION', 'EGL_CONTEXT_MINOR_VERSION',
           'EGL_CONTEXT_OPENGL_PROFILE_MASK',
           'EGL_CONTEXT_OPENGL_RESET_NOTIFICATION_STRATEGY',
           'EGL_NO_RESET_NOTIFICATION', 'EGL_LOSE_CONTEXT_ON_RESET',
           'EGL_CONTEXT_OPENGL_CORE_PROFILE_BIT',
           'EGL_CONTEXT_OPENGL_COMPATIBILITY_PROFILE_BIT',
           'EGL_CONTEXT_OPENGL_DEBUG', 'EGL_CONTEXT_OPENGL_FORWARD_COMPATIBLE',
           'EGL_CONTEXT_OPENGL_ROBUST_ACCESS', 'EGL_OPENGL_ES3_BIT',
           'EGL_CL_EVENT_HANDLE', 'EGL_SYNC_CL_EVENT',
           'EGL_SYNC_CL_EVENT_COMPLETE', 'EGL_SYNC_PRIOR_COMMANDS_COMPLETE',
           'EGL_SYNC_TYPE', 'EGL_SYNC_STATUS', 'EGL_SYNC_CONDITION',
           'EGL_SIGNALED', 'EGL_UNSIGNALED', 'EGL_SYNC_FLUSH_COMMANDS_BIT',
           'EGL_FOREVER', 'EGL_TIMEOUT_EXPIRED', 'EGL_CONDITION_SATISFIED',
           'EGL_NO_SYNC', 'EGL_SYNC_FENCE', 'EGL_GL_COLORSPACE',
           'EGL_GL_COLORSPACE_SRGB', 'EGL_GL_COLORSPACE_LINEAR',
           'EGL_GL_RENDERBUFFER', 'EGL_GL_TEXTURE_2D', 'EGL_GL_TEXTURE_LEVEL',
           'EGL_GL_TEXTURE_3D', 'EGL_GL_TEXTURE_ZOFFSET',
           'EGL_GL_TEXTURE_CUBE_MAP_POSITIVE_X',
           'EGL_GL_TEXTURE_CUBE_MAP_NEGATIVE_X',
           'EGL_GL_TEXTURE_CUBE_MAP_POSITIVE_Y',
           'EGL_GL_TEXTURE_CUBE_MAP_NEGATIVE_Y',
           'EGL_GL_TEXTURE_CUBE_MAP_POSITIVE_Z',
           'EGL_GL_TEXTURE_CUBE_MAP_NEGATIVE_Z', 'EGL_IMAGE_PRESERVED',
           'EGL_NO_IMAGE']

# Standard library imports.
import ctypes

# Local imports.
from ._common import (_load_function, Arg, EGLBoolean, EGLConfig, EGLContext,
                      EGLDisplay, EGLSurface, EGLint, EGLClientBuffer, EGLenum,
                      EGLAttrib_p, EGLImage, EGLSync, EGLTime)
from .egl1_0 import EGL_FALSE, EGL_NO_DISPLAY, EGL_NO_CONTEXT, EGL_NO_SURFACE

# Define EGL 1.5 constants.
EGL_CONTEXT_MAJOR_VERSION                      = 0x3098
EGL_CONTEXT_MINOR_VERSION                      = 0x30FB
EGL_CONTEXT_OPENGL_PROFILE_MASK                = 0x30FD
EGL_CONTEXT_OPENGL_RESET_NOTIFICATION_STRATEGY = 0x31BD
EGL_NO_RESET_NOTIFICATION                      = 0x31BE
EGL_LOSE_CONTEXT_ON_RESET                      = 0x31BF
EGL_CONTEXT_OPENGL_CORE_PROFILE_BIT            = 0x00000001
EGL_CONTEXT_OPENGL_COMPATIBILITY_PROFILE_BIT   = 0x00000002
EGL_CONTEXT_OPENGL_DEBUG                       = 0x31B0
EGL_CONTEXT_OPENGL_FORWARD_COMPATIBLE          = 0x31B1
EGL_CONTEXT_OPENGL_ROBUST_ACCESS               = 0x31B2
EGL_OPENGL_ES3_BIT                             = 0x00000040
EGL_CL_EVENT_HANDLE                            = 0x309C
EGL_SYNC_CL_EVENT                              = 0x30FE
EGL_SYNC_CL_EVENT_COMPLETE                     = 0x30FF
EGL_SYNC_PRIOR_COMMANDS_COMPLETE               = 0x30F0
EGL_SYNC_TYPE                                  = 0x30F7
EGL_SYNC_STATUS                                = 0x30F1
EGL_SYNC_CONDITION                             = 0x30F8
EGL_SIGNALED                                   = 0x30F2
EGL_UNSIGNALED                                 = 0x30F3
EGL_SYNC_FLUSH_COMMANDS_BIT                    = 0x0001
EGL_FOREVER                                    = 0xFFFFFFFFFFFFFFFF
EGL_TIMEOUT_EXPIRED                            = 0x30F5
EGL_CONDITION_SATISFIED                        = 0x30F6
EGL_NO_SYNC                                    = EGLSync(0)
EGL_SYNC_FENCE                                 = 0x30F9
EGL_GL_COLORSPACE                              = 0x309D
EGL_GL_COLORSPACE_SRGB                         = 0x3089
EGL_GL_COLORSPACE_LINEAR                       = 0x308A
EGL_GL_RENDERBUFFER                            = 0x30B9
EGL_GL_TEXTURE_2D                              = 0x30B1
EGL_GL_TEXTURE_LEVEL                           = 0x30BC
EGL_GL_TEXTURE_3D                              = 0x30B2
EGL_GL_TEXTURE_ZOFFSET                         = 0x30BD
EGL_GL_TEXTURE_CUBE_MAP_POSITIVE_X             = 0x30B3
EGL_GL_TEXTURE_CUBE_MAP_NEGATIVE_X             = 0x30B4
EGL_GL_TEXTURE_CUBE_MAP_POSITIVE_Y             = 0x30B5
EGL_GL_TEXTURE_CUBE_MAP_NEGATIVE_Y             = 0x30B6
EGL_GL_TEXTURE_CUBE_MAP_POSITIVE_Z             = 0x30B7
EGL_GL_TEXTURE_CUBE_MAP_NEGATIVE_Z             = 0x30B8
EGL_IMAGE_PRESERVED                            = 0x30D2
EGL_NO_IMAGE                                   = EGLImage(0)

# Prototype EGL 1.5 functions.
eglCreateSync = _load_function('eglCreateSync', EGLSync,
                               (EGLDisplay, Arg.IN, 'dpy'),
                               (EGLenum, Arg.IN, 'type'),
                               (EGLAttrib_p, Arg.IN, 'attrib_list'),
                               error_on=EGL_NO_SYNC)

eglDestroySync = _load_function('eglDestroySync', EGLBoolean,
                                (EGLDisplay, Arg.IN, 'dpy'),
                                (EGLSync, Arg.IN, 'sync'),
                                error_on=False)

eglClientWaitSync = _load_function('eglClientWaitSync', EGLint,
                                   (EGLDisplay, Arg.IN, 'dpy'),
                                   (EGLSync, Arg.IN, 'sync'),
                                   (EGLint, Arg.IN, 'flags'),
                                   (EGLTime, Arg.IN, 'timeout'),
                                   error_on=EGL_FALSE)

eglGetSyncAttrib = _load_function('eglGetSyncAttrib', EGLBoolean,
                                  (EGLDisplay, Arg.IN, 'dpy'),
                                  (EGLSync, Arg.IN, 'sync'),
                                  (EGLint, Arg.IN, 'attribute'),
                                  (EGLAttrib_p, Arg.OUT, 'value'),
                                  error_on=False)

eglCreateImage = _load_function('eglCreateImage', EGLImage,
                                (EGLDisplay, Arg.IN, 'dpy'),
                                (EGLContext, Arg.IN, 'ctx', EGL_NO_CONTEXT),
                                (EGLenum, Arg.IN, 'target'),
                                (EGLClientBuffer, Arg.IN, 'buffer'),
                                (EGLAttrib_p, Arg.IN, 'attrib_list'),
                                error_on=EGL_NO_IMAGE)

eglDestroyImage = _load_function('eglDestroyImage', EGLBoolean,
                                 (EGLDisplay, Arg.IN, 'dpy'),
                                 (EGLImage, Arg.IN, 'image'),
                                 error_on=False)

eglGetPlatformDisplay = _load_function('eglGetPlatformDisplay', EGLDisplay,
                                       (EGLenum, Arg.IN, 'platform'),
                                       (ctypes.c_void_p, Arg.IN,
                                        'native_display'),
                                       (EGLAttrib_p, Arg.IN, 'attrib_list'),
                                       error_on=EGL_NO_DISPLAY)

eglCreatePlatformWindowSurface =\
    _load_function('eglCreatePlatformWindowSurface', EGLSurface,
                   (EGLDisplay, Arg.IN, 'dpy'),
                   (EGLConfig, Arg.IN, 'config'),
                   (ctypes.c_void_p, Arg.IN, 'native_window'),
                   (EGLAttrib_p, Arg.IN, 'attrib_list'),
                   error_on=EGL_NO_SURFACE)

eglCreatePlatformPixmapSurface = \
    _load_function('eglCreatePlatformPixmapSurface', EGLSurface,
                   (EGLDisplay, Arg.IN, 'dpy'),
                   (EGLConfig, Arg.IN, 'config'),
                   (ctypes.c_void_p, Arg.IN, 'native_pixmap'),
                   (EGLAttrib_p, Arg.IN, 'attrib_list'),
                   error_on=EGL_NO_SURFACE)

eglWaitSync = _load_function('eglWaitSync', EGLBoolean,
                             (EGLDisplay, Arg.IN, 'dpy'),
                             (EGLSync, Arg.IN, 'sync'),
                             (EGLint, Arg.IN, 'flags'),
                             error_on=False)
