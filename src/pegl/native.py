#!/usr/bin/env python3

'''EGL library interface for Pegl.'''

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

# List module exports for EGL 1.0.
__all__ = ['eglChooseConfig', 'eglCopyBuffers', 'eglCreateContext',
           'eglCreatePbufferSurface', 'eglCreatePixmapSurface',
           'eglCreateWindowSurface', 'eglDestroyContext', 'eglDestroySurface',
           'eglGetConfigAttrib', 'eglGetConfigs', 'eglGetCurrentDisplay',
           'eglGetCurrentSurface', 'eglGetDisplay', 'eglGetError',
           'eglGetProcAddress', 'eglInitialize', 'eglMakeCurrent',
           'eglQueryContext', 'eglQueryString', 'eglQuerySurface',
           'eglSwapBuffers', 'eglTerminate', 'eglWaitGL', 'eglWaitNative',
           'egl_version', 'EGL_ALPHA_SIZE', 'EGL_BAD_ACCESS', 'EGL_BAD_ALLOC',
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
import sys

# Dynamic library loading.
##libname = 'libEGL'
##if sys.platform.startswith('linux'):
##    libclass, libext = ctypes.CDLL, '.so'
##elif sys.platform == 'darwin':
##    libclass, libext = ctypes.CDLL, '.dylib'
##elif sys.platform == 'win32':
##    libclass, libext = ctypes.CDLL, '.dll'
##else:
##    raise ImportError('Pegl not supported on {}'.format(sys.platform))
##       
##_lib = libclass(libname + libext)
_lib = ctypes.CDLL('libEGL.dll') # TODO

# Type definitions. Note that these are NOT listed in __all__. They are also
# available regardless of what EGL version is supported by the library.
# EGL 1.0
EGLBoolean           = ctypes.c_bool
EGLConfig            = ctypes.c_void_p
EGLConfig_p          = ctypes.POINTER(EGLConfig)
EGLContext           = ctypes.c_void_p
EGLDisplay           = ctypes.c_void_p
EGLNativeDisplayType = ctypes.c_void_p
EGLNativePixmapType  = ctypes.c_void_p
EGLNativeWindowType  = ctypes.c_void_p
EGLSurface           = ctypes.c_void_p
EGLint               = ctypes.c_int32
EGLint_p             = ctypes.POINTER(EGLint)
# EGL 1.2
EGLClientBuffer      = ctypes.c_void_p
EGLenum              = ctypes.c_uint
# EGL 1.5
EGLAttrib            = ctypes.c_ssize_t # Substitute for intptr_t
EGLAttrib_p          = ctypes.POINTER(EGLAttrib)
EGLImage             = ctypes.c_void_p
EGLSync              = ctypes.c_void_p
EGLTime              = ctypes.c_uint64  # § 2.1.1: "a 64-bit unsigned integer"

# Set up error handling.
eglGetError = _lib.eglGetError
eglGetError.argtypes = []
eglGetError.restype = EGLint

# Prototype remaining EGL 1.0 functions (other than eglGetError).
eglChooseConfig = _lib.eglChooseConfig
eglChooseConfig.argtypes = [EGLDisplay, EGLint_p, EGLConfig_p, EGLint,
                            EGLint_p]
eglChooseConfig.restype = EGLBoolean

eglCopyBuffers = _lib.eglCopyBuffers
eglCopyBuffers.argtypes = [EGLDisplay, EGLSurface, EGLNativePixmapType]
eglCopyBuffers.restype = EGLBoolean

eglCreateContext = _lib.eglCreateContext
eglCreateContext.argtypes = [EGLDisplay, EGLConfig, EGLContext, EGLint_p]
eglCreateContext.restype = EGLContext

eglCreatePbufferSurface = _lib.eglCreatePbufferSurface
eglCreatePbufferSurface.argtypes = [EGLDisplay, EGLConfig, EGLint_p]
eglCreatePbufferSurface.restype = EGLSurface

eglCreatePixmapSurface = _lib.eglCreatePixmapSurface
eglCreatePixmapSurface.argtypes = [EGLDisplay, EGLConfig, EGLNativePixmapType, EGLint_p]
eglCreatePixmapSurface.restype = EGLSurface

eglCreateWindowSurface = _lib.eglCreateWindowSurface
eglCreateWindowSurface.argtypes = [EGLDisplay, EGLConfig, EGLNativeWindowType, EGLint_p]
eglCreateWindowSurface.restype = EGLSurface

eglDestroyContext = _lib.eglDestroyContext
eglDestroyContext.argtypes = [EGLDisplay, EGLContext]
eglDestroyContext.restype = EGLBoolean

eglDestroySurface = _lib.eglDestroySurface
eglDestroySurface.argtypes = [EGLDisplay, EGLSurface]
eglDestroySurface.restype = EGLBoolean

eglGetConfigAttrib = _lib.eglGetConfigAttrib
eglGetConfigAttrib.argtypes = [EGLDisplay, EGLConfig, EGLint, EGLint_p]
eglGetConfigAttrib.restype = EGLBoolean

eglGetConfigs = _lib.eglGetConfigs
eglGetConfigs.argtypes = [EGLDisplay, EGLConfig_p, EGLint, EGLint_p]
eglGetConfigs.restype = EGLBoolean

eglGetCurrentDisplay = _lib.eglGetCurrentDisplay
eglGetCurrentDisplay.argtypes = []
eglGetCurrentDisplay.restype = EGLDisplay

eglGetCurrentSurface = _lib.eglGetCurrentSurface
eglGetCurrentSurface.argtypes = [EGLint]
eglGetCurrentSurface.restype = EGLSurface

eglGetDisplay = _lib.eglGetDisplay
eglGetDisplay.argtypes = [EGLNativeDisplayType]
eglGetDisplay.restype = EGLDisplay

eglGetProcAddress = _lib.eglGetProcAddress
eglGetProcAddress.argtypes = [ctypes.c_char_p]
# Returns a function pointer that must be cast to the proper function type.
# (egl.h even calls it "__eglMustCastToProperFunctionPointerType"!)

eglInitialize = _lib.eglInitialize
eglInitialize.argtypes = [EGLDisplay, EGLint_p, EGLint_p]
eglInitialize.restype = EGLBoolean

eglMakeCurrent = _lib.eglMakeCurrent
eglMakeCurrent.argtypes = [EGLDisplay, EGLSurface, EGLSurface, EGLContext]
eglMakeCurrent.restype = EGLBoolean

eglQueryContext = _lib.eglQueryContext
eglQueryContext.argtypes = [EGLDisplay, EGLContext, EGLint, EGLint_p]
eglQueryContext.restype = EGLBoolean

eglQueryString = _lib.eglQueryString
eglQueryString.argtypes = [EGLDisplay, EGLint]
eglQueryString.restype = ctypes.c_char_p

eglQuerySurface = _lib.eglQuerySurface
eglQuerySurface.argtypes = [EGLDisplay, EGLSurface, EGLint, EGLint_p]
eglQuerySurface.restype = EGLBoolean

eglSwapBuffers = _lib.eglSwapBuffers
eglSwapBuffers.argtypes = [EGLDisplay, EGLSurface]
eglSwapBuffers.restype = EGLBoolean

eglTerminate = _lib.eglTerminate
eglTerminate.argtypes = [EGLDisplay]
eglTerminate.restype = EGLBoolean

eglWaitGL = _lib.eglWaitGL
eglWaitGL.argtypes = []
eglWaitGL.restype = EGLBoolean

eglWaitNative = _lib.eglWaitNative
eglWaitNative.argtypes = [EGLint]
eglWaitNative.restype = EGLBoolean

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

# Set version number.
egl_version = (1, 0)

# Try prototyping EGL 1.1 functions.
try:
    eglBindTexImage = _lib.eglBindTexImage
    eglBindTexImage.argtypes = [EGLDisplay, EGLSurface, EGLint]
    eglBindTexImage.restype = EGLBoolean

    eglReleaseTexImage = _lib.eglReleaseTexImage
    eglReleaseTexImage.argtypes = [EGLDisplay, EGLSurface, EGLint]
    eglReleaseTexImage.restype = EGLBoolean

    eglSurfaceAttrib = _lib.eglSurfaceAttrib
    eglSurfaceAttrib.argtypes = [EGLDisplay, EGLSurface, EGLint, EGLint]
    eglSurfaceAttrib.restype = EGLBoolean

    eglSwapInterval = _lib.eglSwapInterval
    eglSwapInterval.argtypes = [EGLDisplay, EGLint]
    eglSwapInterval.restype = EGLBoolean
except AttributeError:
    # Failure; EGL 1.1 not supported.
    pass
else:
    # Success! Add EGL 1.1 constants.
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

    # Update the version number and the module exports.
    egl_version = (1, 1)
    __all__.extend(['eglBindTexImage', 'eglReleaseTexImage',
                    'eglSurfaceAttrib', 'eglSwapInterval', 'EGL_BACK_BUFFER',
                    'EGL_BIND_TO_TEXTURE_RGB', 'EGL_BIND_TO_TEXTURE_RGBA',
                    'EGL_CONTEXT_LOST', 'EGL_MIN_SWAP_INTERVAL',
                    'EGL_MAX_SWAP_INTERVAL', 'EGL_MIPMAP_TEXTURE',
                    'EGL_MIPMAP_LEVEL', 'EGL_NO_TEXTURE', 'EGL_TEXTURE_2D',
                    'EGL_TEXTURE_FORMAT', 'EGL_TEXTURE_RGB',
                    'EGL_TEXTURE_RGBA', 'EGL_TEXTURE_TARGET'])

    # Try prototyping EGL 1.2 functions.
    try:
        eglBindAPI = _lib.eglBindAPI
        eglBindAPI.argtypes = [EGLenum]
        eglBindAPI.restype = EGLBoolean

        eglQueryAPI = _lib.eglQueryAPI
        eglQueryAPI.argtypes = []
        eglQueryAPI.restype = EGLenum

        eglCreatePbufferFromClientBuffer = \
            _lib.eglCreatePbufferFromClientBuffer
        eglCreatePbufferFromClientBuffer.argtypes = [EGLDisplay, EGLenum,
                                                     EGLClientBuffer,
                                                     EGLConfig, EGLint_p]
        eglCreatePbufferFromClientBuffer.restype = EGLSurface

        eglReleaseThread = _lib.eglReleaseThread
        eglReleaseThread.argtypes = []
        eglReleaseThread.restype = EGLBoolean

        eglWaitClient = _lib.eglWaitClient
        eglWaitClient.argtypes = []
        eglWaitClient.restype = EGLBoolean
    except AttributeError:
        # Failure; EGL 1.2 not supported.
        pass
    else:
        # Success! Add EGL 1.2 constants.
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

        # Update the version number and the module exports.
        egl_version = (1, 2)
        __all__.extend(['eglBindAPI', 'eglQueryAPI',
                        'eglCreatePbufferFromClientBuffer', 'eglReleaseThread',
                        'eglWaitClient', 'EGL_ALPHA_FORMAT',
                        'EGL_ALPHA_FORMAT_NONPRE', 'EGL_ALPHA_FORMAT_PRE',
                        'EGL_ALPHA_MASK_SIZE', 'EGL_BUFFER_PRESERVED',
                        'EGL_BUFFER_DESTROYED', 'EGL_CLIENT_APIS',
                        'EGL_COLORSPACE', 'EGL_COLORSPACE_sRGB',
                        'EGL_COLORSPACE_LINEAR', 'EGL_COLOR_BUFFER_TYPE',
                        'EGL_CONTEXT_CLIENT_TYPE', 'EGL_DISPLAY_SCALING',
                        'EGL_HORIZONTAL_RESOLUTION', 'EGL_LUMINANCE_BUFFER',
                        'EGL_LUMINANCE_SIZE', 'EGL_OPENGL_ES_BIT',
                        'EGL_OPENVG_BIT', 'EGL_OPENGL_ES_API',
                        'EGL_OPENVG_API', 'EGL_OPENVG_IMAGE',
                        'EGL_PIXEL_ASPECT_RATIO', 'EGL_RENDERABLE_TYPE',
                        'EGL_RENDER_BUFFER', 'EGL_RGB_BUFFER',
                        'EGL_SINGLE_BUFFER', 'EGL_SWAP_BEHAVIOR',
                        'EGL_UNKNOWN', 'EGL_VERTICAL_RESOLUTION'])

        # TODO: There are no new EGL 1.3 functions. Should I detect support
        # some other way?
        if True:
            # Add EGL 1.3 constants.
            EGL_CONFORMANT                  = 0x3042
            EGL_CONTEXT_CLIENT_VERSION      = 0x3098
            EGL_MATCH_NATIVE_PIXMAP         = 0x3041
            EGL_OPENGL_ES2_BIT              = 0x0004
            EGL_VG_ALPHA_FORMAT             = 0x3088
            EGL_VG_ALPHA_FORMAT_NONPRE      = 0x308B
            EGL_VG_ALPHA_FORMAT_PRE         = 0x308C
            EGL_VG_ALPHA_FORMAT_PRE_BIT     = 0x0040
            EGL_VG_COLORSPACE               = 0x3087
            EGL_VG_COLORSPACE_sRGB          = 0x3089
            EGL_VG_COLORSPACE_LINEAR        = 0x308A
            EGL_VG_COLORSPACE_LINEAR_BIT    = 0x0020

            # Update the version number and the module exports.
            egl_version = (1, 3)
            __all__.extend(['EGL_CONFORMANT', 'EGL_CONTEXT_CLIENT_VERSION',
                            'EGL_MATCH_NATIVE_PIXMAP', 'EGL_OPENGL_ES2_BIT',
                            'EGL_VG_ALPHA_FORMAT',
                            'EGL_VG_ALPHA_FORMAT_NONPRE',
                            'EGL_VG_ALPHA_FORMAT_PRE',
                            'EGL_VG_ALPHA_FORMAT_PRE_BIT',
                            'EGL_VG_COLORSPACE', 'EGL_VG_COLORSPACE_sRGB',
                            'EGL_VG_COLORSPACE_LINEAR',
                            'EGL_VG_COLORSPACE_LINEAR_BIT'])

            # Try prototyping EGL 1.4 functions.
            try:
                eglGetCurrentContext = _lib.eglGetCurrentContext
                eglGetCurrentContext.argtypes = []
                eglGetCurrentContext.restype = EGLContext
            except AttributeError:
                # Failure; EGL 1.4 not supported.
                pass
            else:
                # Success! Add EGL 1.4 constants.
                EGL_DEFAULT_DISPLAY             = EGLNativeDisplayType(0)
                EGL_MULTISAMPLE_RESOLVE_BOX_BIT = 0x0200
                EGL_MULTISAMPLE_RESOLVE         = 0x3099
                EGL_MULTISAMPLE_RESOLVE_DEFAULT = 0x309A
                EGL_MULTISAMPLE_RESOLVE_BOX     = 0x309B
                EGL_OPENGL_API                  = 0x30A2
                EGL_OPENGL_BIT                  = 0x0008
                EGL_SWAP_BEHAVIOR_PRESERVED_BIT = 0x0400

                # Update the version number and the module exports.
                egl_version = (1, 4)
                __all__.extend(['EGL_DEFAULT_DISPLAY',
                                'EGL_MULTISAMPLE_RESOLVE_BOX_BIT',
                                'EGL_MULTISAMPLE_RESOLVE',
                                'EGL_MULTISAMPLE_RESOLVE_DEFAULT',
                                'EGL_MULTISAMPLE_RESOLVE_BOX',
                                'EGL_OPENGL_API', 'EGL_OPENGL_BIT',
                                'EGL_SWAP_BEHAVIOR_PRESERVED_BIT'])

                # Try prototyping EGL 1.5 functions.
                try:
                    eglCreateSync = _lib.eglCreateSync
                    eglCreateSync.argtypes = [EGLDisplay, EGLenum, EGLAttrib_p]
                    eglCreateSync.restype = EGLSync

                    eglDestroySync = _lib.eglDestroySync
                    eglDestroySync.argtypes = [EGLDisplay, EGLSync]
                    eglDestroySync.restype = EGLBoolean

                    eglClientWaitSync = _lib.eglClientWaitSync
                    eglClientWaitSync.argtypes = [EGLDisplay, EGLSync, EGLint,
                                                  EGLTime]
                    eglClientWaitSync.restype = EGLint

                    eglGetSyncAttrib = _lib.eglGetSyncAttrib
                    eglGetSyncAttrib.argtypes = [EGLDisplay, EGLSync, EGLint,
                                                 EGLAttrib_p]
                    eglGetSyncAttrib.restype = EGLBoolean

                    eglCreateImage = _lib.eglCreateImage
                    eglCreateImage.argtypes = [EGLDisplay, EGLContext, EGLenum,
                                               EGLClientBuffer, EGLAttrib_p]
                    eglCreateImage.restype = EGLImage

                    eglDestroyImage = _lib.eglDestroyImage
                    eglDestroyImage.argtypes = [EGLDisplay, EGLImage]
                    eglDestroyImage.restype = EGLBoolean

                    eglGetPlatformDisplay = _lib.eglGetPlatformDisplay
                    eglGetPlatformDisplay.argtypes = [EGLenum, ctypes.c_void_p,
                                                      EGLAttrib_p]
                    eglGetPlatformDisplay.restype = EGLDisplay

                    eglCreatePlatformWindowSurface = \
                        _lib.eglCreatePlatformWindowSurface
                    eglCreatePlatformWindowSurface.argtypes = [EGLDisplay,
                                                               EGLConfig,
                                                               ctypes.c_void_p,
                                                               EGLAttrib_p]
                    eglCreatePlatformWindowSurface.restype = EGLSurface

                    eglCreatePlatformPixmapSurface = \
                        _lib.eglCreatePlatformPixmapSurface
                    eglCreatePlatformPixmapSurface.argtypes = [EGLDisplay,
                                                               EGLConfig,
                                                               ctypes.c_void_p,
                                                               EGLAttrib_p]
                    eglCreatePlatformPixmapSurface.restype = EGLSurface

                    eglWaitSync = _lib.eglWaitSync
                    eglWaitSync.argtypes = [EGLDisplay, EGLSync, EGLint]
                    eglWaitSync.restype = EGLBoolean
                except AttributeError:
                    # Failure; EGL 1.5 not supported.
                    pass
                else:
                    # Success! Add EGL 1.5 constants.
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
                    EGL_FOREVER                            = 0xFFFFFFFFFFFFFFFF
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

                    # Update the version number and the module exports.
                    egl_version = (1, 5)
                    __all__.extend(['eglCreateSync', 'eglDestroySync',
                                    'eglClientWaitSync', 'eglGetSyncAttrib',
                                    'eglCreateImage', 'eglDestroyImage',
                                    'eglGetPlatformDisplay',
                                    'eglCreatePlatformWindowSurface',
                                    'eglCreatePlatformPixmapSurface',
                                    'eglWaitSync', 'EGL_CONTEXT_MAJOR_VERSION',
                                    'EGL_CONTEXT_MINOR_VERSION',
                                    'EGL_CONTEXT_OPENGL_PROFILE_MASK',
                                    'EGL_CONTEXT_OPENGL_RESET_NOTIFICATION_'
                                    'STRATEGY',
                                    'EGL_NO_RESET_NOTIFICATION',
                                    'EGL_LOSE_CONTEXT_ON_RESET',
                                    'EGL_CONTEXT_OPENGL_CORE_PROFILE_BIT',
                                    'EGL_CONTEXT_OPENGL_COMPATIBILITY_PROFILE_'
                                    'BIT',
                                    'EGL_CONTEXT_OPENGL_DEBUG',
                                    'EGL_CONTEXT_OPENGL_FORWARD_COMPATIBLE',
                                    'EGL_CONTEXT_OPENGL_ROBUST_ACCESS',
                                    'EGL_OPENGL_ES3_BIT',
                                    'EGL_CL_EVENT_HANDLE',
                                    'EGL_SYNC_CL_EVENT',
                                    'EGL_SYNC_CL_EVENT_COMPLETE',
                                    'EGL_SYNC_PRIOR_COMMANDS_COMPLETE',
                                    'EGL_SYNC_TYPE', 'EGL_SYNC_STATUS',
                                    'EGL_SYNC_CONDITION', 'EGL_SIGNALED',
                                    'EGL_UNSIGNALED',
                                    'EGL_SYNC_FLUSH_COMMANDS_BIT',
                                    'EGL_FOREVER', 'EGL_TIMEOUT_EXPIRED',
                                    'EGL_CONDITION_SATISFIED', 'EGL_NO_SYNC',
                                    'EGL_SYNC_FENCE', 'EGL_GL_COLORSPACE',
                                    'EGL_GL_COLORSPACE_SRGB',
                                    'EGL_GL_COLORSPACE_LINEAR',
                                    'EGL_GL_RENDERBUFFER', 'EGL_GL_TEXTURE_2D',
                                    'EGL_GL_TEXTURE_LEVEL',
                                    'EGL_GL_TEXTURE_3D',
                                    'EGL_GL_TEXTURE_ZOFFSET',
                                    'EGL_GL_TEXTURE_CUBE_MAP_POSITIVE_X',
                                    'EGL_GL_TEXTURE_CUBE_MAP_NEGATIVE_X',
                                    'EGL_GL_TEXTURE_CUBE_MAP_POSITIVE_Y',
                                    'EGL_GL_TEXTURE_CUBE_MAP_NEGATIVE_Y',
                                    'EGL_GL_TEXTURE_CUBE_MAP_POSITIVE_Z',
                                    'EGL_GL_TEXTURE_CUBE_MAP_NEGATIVE_Z',
                                    'EGL_IMAGE_PRESERVED', 'EGL_NO_IMAGE'])
