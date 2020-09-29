#!/usr/bin/env python3

'''EGL 1.0 functions and constants for Pegl.'''

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

__all__ = ['eglChooseConfig', 'eglCopyBuffers', 'eglCreateContext',
           'eglCreatePbufferSurface', 'eglCreatePixmapSurface',
           'eglCreateWindowSurface', 'eglDestroyContext', 'eglDestroySurface',
           'eglGetConfigAttrib', 'eglGetConfigs', 'eglGetCurrentDisplay',
           'eglGetCurrentSurface', 'eglGetDisplay', 'eglGetError',
           'eglGetProcAddress', 'eglInitialize', 'eglMakeCurrent',
           'eglQueryContext', 'eglQueryString', 'eglQuerySurface',
           'eglSwapBuffers', 'eglTerminate', 'eglWaitGL', 'eglWaitNative',
           'EGL_ALPHA_SIZE', 'EGL_BAD_ACCESS', 'EGL_BAD_ALLOC',
           'EGL_BAD_ATTRIBUTE', 'EGL_BAD_CONFIG', 'EGL_BAD_CONTEXT',
           'EGL_BAD_CURRENT_SURFACE', 'EGL_BAD_DISPLAY', 'EGL_BAD_MATCH',
           'EGL_BAD_NATIVE_PIXMAP', 'EGL_BAD_NATIVE_WINDOW',
           'EGL_BAD_PARAMETER', 'EGL_BAD_SURFACE', 'EGL_BLUE_SIZE',
           'EGL_BUFFER_SIZE', 'EGL_CONFIG_CAVEAT', 'EGL_CONFIG_ID',
           'EGL_CORE_NATIVE_ENGINE', 'EGL_DEPTH_SIZE', 'EGL_DONT_CARE',
           'EGL_DRAW', 'EGL_EXTENSIONS', 'EGL_FALSE', 'EGL_GREEN_SIZE',
           'EGL_HEIGHT', 'EGL_LARGEST_PBUFFER', 'EGL_LEVEL',
           'EGL_MAX_PBUFFER_HEIGHT', 'EGL_MAX_PBUFFER_PIXELS',
           'EGL_MAX_PBUFFER_WIDTH', 'EGL_NATIVE_RENDERABLE',
           'EGL_NATIVE_VISUAL_ID', 'EGL_NATIVE_VISUAL_TYPE', 'EGL_NONE',
           'EGL_NON_CONFORMANT_CONFIG', 'EGL_NOT_INITIALIZED',
           'EGL_NO_CONTEXT', 'EGL_NO_DISPLAY', 'EGL_NO_SURFACE',
           'EGL_PBUFFER_BIT', 'EGL_PIXMAP_BIT', 'EGL_READ', 'EGL_RED_SIZE',
           'EGL_SAMPLES', 'EGL_SAMPLE_BUFFERS', 'EGL_SLOW_CONFIG',
           'EGL_STENCIL_SIZE', 'EGL_SUCCESS', 'EGL_SURFACE_TYPE',
           'EGL_TRANSPARENT_BLUE_VALUE', 'EGL_TRANSPARENT_GREEN_VALUE',
           'EGL_TRANSPARENT_RED_VALUE', 'EGL_TRANSPARENT_RGB',
           'EGL_TRANSPARENT_TYPE', 'EGL_TRUE', 'EGL_VENDOR', 'EGL_VERSION',
           'EGL_WIDTH', 'EGL_WINDOW_BIT']

# Standard library imports.
import ctypes

# Local imports.
from ._common import *

# Define EGL 1.0 constants.
EGL_ALPHA_SIZE                  = 0x3021
EGL_BAD_ACCESS                  = 0x3002
EGL_BAD_ALLOC                   = 0x3003
EGL_BAD_ATTRIBUTE               = 0x3004
EGL_BAD_CONFIG                  = 0x3005
EGL_BAD_CONTEXT                 = 0x3006
EGL_BAD_CURRENT_SURFACE         = 0x3007
EGL_BAD_DISPLAY                 = 0x3008
EGL_BAD_MATCH                   = 0x3009
EGL_BAD_NATIVE_PIXMAP           = 0x300A
EGL_BAD_NATIVE_WINDOW           = 0x300B
EGL_BAD_PARAMETER               = 0x300C
EGL_BAD_SURFACE                 = 0x300D
EGL_BLUE_SIZE                   = 0x3022
EGL_BUFFER_SIZE                 = 0x3020
EGL_CONFIG_CAVEAT               = 0x3027
EGL_CONFIG_ID                   = 0x3028
EGL_CORE_NATIVE_ENGINE          = 0x305B
EGL_DEPTH_SIZE                  = 0x3025
EGL_DONT_CARE                   = EGLint(-1)
EGL_DRAW                        = 0x3059
EGL_EXTENSIONS                  = 0x3055
EGL_FALSE                       = 0
EGL_GREEN_SIZE                  = 0x3023
EGL_HEIGHT                      = 0x3056
EGL_LARGEST_PBUFFER             = 0x3058
EGL_LEVEL                       = 0x3029
EGL_MAX_PBUFFER_HEIGHT          = 0x302A
EGL_MAX_PBUFFER_PIXELS          = 0x302B
EGL_MAX_PBUFFER_WIDTH           = 0x302C
EGL_NATIVE_RENDERABLE           = 0x302D
EGL_NATIVE_VISUAL_ID            = 0x302E
EGL_NATIVE_VISUAL_TYPE          = 0x302F
EGL_NONE                        = 0x3038
EGL_NON_CONFORMANT_CONFIG       = 0x3051
EGL_NOT_INITIALIZED             = 0x3001
EGL_NO_CONTEXT                  = EGLContext(0)
EGL_NO_DISPLAY                  = EGLDisplay(0)
EGL_NO_SURFACE                  = EGLSurface(0)
EGL_PBUFFER_BIT                 = 0x0001
EGL_PIXMAP_BIT                  = 0x0002
EGL_READ                        = 0x305A
EGL_RED_SIZE                    = 0x3024
EGL_SAMPLES                     = 0x3031
EGL_SAMPLE_BUFFERS              = 0x3032
EGL_SLOW_CONFIG                 = 0x3050
EGL_STENCIL_SIZE                = 0x3026
EGL_SUCCESS                     = 0x3000
EGL_SURFACE_TYPE                = 0x3033
EGL_TRANSPARENT_BLUE_VALUE      = 0x3035
EGL_TRANSPARENT_GREEN_VALUE     = 0x3036
EGL_TRANSPARENT_RED_VALUE       = 0x3037
EGL_TRANSPARENT_RGB             = 0x3052
EGL_TRANSPARENT_TYPE            = 0x3034
EGL_TRUE                        = 1
EGL_VENDOR                      = 0x3053
EGL_VERSION                     = 0x3054
EGL_WIDTH                       = 0x3057
EGL_WINDOW_BIT                  = 0x0004

# Prototype EGL 1.0 functions (except for eglGetError and eglGetProcAddress,
# which are loaded and used in the _common module).
eglChooseConfig = _load_function('eglChooseConfig', EGLBoolean,
                                 (EGLDisplay, Arg.IN, 'dpy'),
                                 (EGLint_p, Arg.IN, 'attrib_list'),
                                 # Technically, configs is the output, but it's
                                 # easier to pass it in and just take the
                                 # number written to it as the only output.
                                 (EGLConfig_p, Arg.IN, 'configs'),
                                 (EGLint, Arg.IN, 'config_size'),
                                 (EGLint_p, Arg.OUT, 'num_config'),
                                 error_on=False)

eglCopyBuffers = _load_function('eglCopyBuffers', EGLBoolean,
                                (EGLDisplay, Arg.IN, 'dpy'),
                                (EGLSurface, Arg.IN, 'surface'),
                                (EGLNativePixmapType, Arg.IN, 'target'),
                                error_on=False)

eglCreateContext = _load_function('eglCreateContext', EGLContext,
                                  (EGLDisplay, Arg.IN, 'dpy'),
                                  (EGLConfig, Arg.IN, 'config'),
                                  (EGLContext, Arg.IN, 'share_context',
                                   EGL_NO_CONTEXT),
                                  (EGLint_p, Arg.IN, 'attrib_list'),
                                  error_on=EGL_NO_CONTEXT)

eglCreatePbufferSurface = _load_function('eglCreatePbufferSurface', EGLSurface,
                                         (EGLDisplay, Arg.IN, 'dpy'),
                                         (EGLConfig, Arg.IN, 'config'),
                                         (EGLint_p, Arg.IN, 'attrib_list'))

eglCreatePixmapSurface = _load_function('eglCreatePixmapSurface', EGLSurface,
                                        (EGLDisplay, Arg.IN, 'dpy'),
                                        (EGLConfig, Arg.IN, 'config'),
                                        (EGLNativePixmapType, Arg.IN, 'pixmap'),
                                        (EGLint_p, Arg.IN, 'attrib_list'),
                                        error_on=EGL_NO_SURFACE)

eglCreateWindowSurface = _load_function('eglCreateWindowSurface', EGLSurface,
                                        (EGLDisplay, Arg.IN, 'dpy'),
                                        (EGLConfig, Arg.IN, 'config'),
                                        (EGLNativeWindowType, Arg.IN, 'win'),
                                        (EGLint_p, Arg.IN, 'attrib_list'),
                                        error_on=EGL_NO_SURFACE)

eglDestroyContext = _load_function('eglDestroyContext', EGLBoolean,
                                   (EGLDisplay, Arg.IN, 'dpy'),
                                   (EGLContext, Arg.IN, 'ctx'),
                                   error_on=False)

eglDestroySurface = _load_function('eglDestroySurface', EGLBoolean,
                                   (EGLDisplay, Arg.IN, 'dpy'),
                                   (EGLSurface, Arg.IN, 'surface'),
                                   error_on=False)

eglGetConfigAttrib = _load_function('eglGetConfigAttrib', EGLBoolean,
                                    (EGLDisplay, Arg.IN, 'dpy'),
                                    (EGLConfig, Arg.IN, 'config'),
                                    (EGLint, Arg.IN, 'attribute'),
                                    (EGLint_p, Arg.OUT, 'value'),
                                    error_on=False)

eglGetConfigs = _load_function('eglGetConfigs', EGLBoolean,
                               (EGLDisplay, Arg.IN, 'dpy'),
                               # Technically, configs is the output, but it's
                               # easier to pass it in and just take the number
                               # written to it as the only output.
                               (EGLConfig_p, Arg.IN, 'configs'),
                               (EGLint, Arg.IN, 'config_size'),
                               (EGLint_p, Arg.OUT, 'num_config'),
                               error_on=False)

eglGetCurrentDisplay = _load_function('eglGetCurrentDisplay', EGLDisplay)

eglGetCurrentSurface = _load_function('eglGetCurrentSurface', EGLSurface,
                                      (EGLint, Arg.IN, 'readdraw'),
                                      error_on=EGL_NO_SURFACE)

eglGetDisplay = _load_function('eglGetDisplay', EGLDisplay,
                               (EGLNativeDisplayType, Arg.IN, 'display_id'),
                               error_on=EGL_NO_DISPLAY)

eglInitialize = _load_function('eglInitialize', EGLBoolean,
                               (EGLDisplay, Arg.IN, 'dpy'),
                               (EGLint_p, Arg.OUT, 'major'),
                               (EGLint_p, Arg.OUT, 'minor'),
                               error_on=False)

eglMakeCurrent = _load_function('eglMakeCurrent', EGLBoolean,
                                (EGLDisplay, Arg.IN, 'dpy'),
                                (EGLSurface, Arg.IN, 'draw', EGL_NO_SURFACE),
                                (EGLSurface, Arg.IN, 'read', EGL_NO_SURFACE),
                                (EGLContext, Arg.IN, 'ctx', EGL_NO_CONTEXT),
                                error_on=False)

eglQueryContext = _load_function('eglQueryContext', EGLBoolean,
                                 (EGLDisplay, Arg.IN, 'dpy'),
                                 (EGLContext, Arg.IN, 'ctx'),
                                 (EGLint, Arg.IN, 'attribute'),
                                 (EGLint_p, Arg.OUT, 'value'),
                                 error_on=False)

eglQueryString = _load_function('eglQueryString', ctypes.c_char_p,
                                (EGLDisplay, Arg.IN, 'dpy', EGL_NO_DISPLAY),
                                (EGLint, Arg.IN, 'name'),
                                error_on=None)

eglQuerySurface = _load_function('eglQuerySurface', EGLBoolean,
                                 (EGLDisplay, Arg.IN, 'dpy'),
                                 (EGLSurface, Arg.IN, 'surface'),
                                 (EGLint, Arg.IN, 'attribute'),
                                 (EGLint_p, Arg.OUT, 'value'),
                                 error_on=False)

eglSwapBuffers = _load_function('eglSwapBuffers', EGLBoolean,
                                (EGLDisplay, Arg.IN, 'dpy'),
                                (EGLSurface, Arg.IN, 'surface'),
                                error_on=False)

eglTerminate = _load_function('eglTerminate', EGLBoolean,
                              (EGLDisplay, Arg.IN, 'dpy'),
                              error_on=False)

eglWaitGL = _load_function('eglWaitGL', EGLBoolean, error_on=False)

eglWaitNative = _load_function('eglWaitNative', EGLBoolean,
                               (EGLint, Arg.IN, 'engine'),
                               error_on=False)
