#!/usr/bin/env python3

"""EGL enumerations for Pegl."""

# Copyright © 2020 Tim Pederick.
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
# The function hex_repr is based on the "aenum" package:
#     Copyright (c) 2015, 2016, 2017, 2018 Ethan Furman.
#     All rights reserved.
#
#     Redistribution and use in source and binary forms, with or without
#     modification, are permitted provided that the following conditions
#     are met:
#
#         Redistributions of source code must retain the above
#         copyright notice, this list of conditions and the
#         following disclaimer.
#
#         Redistributions in binary form must reproduce the above
#         copyright notice, this list of conditions and the following
#         disclaimer in the documentation and/or other materials
#         provided with the distribution.
#
#         Neither the name Ethan Furman nor the names of any
#         contributors may be used to endorse or promote products
#         derived from this software without specific prior written
#         permission.
#
#     THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#     "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#     LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
#     FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
#     COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
#     INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
#     BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#     LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#     CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
#     LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
#     ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#     POSSIBILITY OF SUCH DAMAGE.

# Standard library imports.
from aenum import IntEnum, IntFlag, extend_enum, _decompose
# I sure hope importing _decompose doesn't come back to bite me...

# Local imports.
from . import egl

__all__ = ['ConfigAttrib', 'ConfigCaveat', 'NativeEngine', 'ReadOrDraw',
           'SurfaceAttrib', 'SurfaceTypeFlag', 'TransparentType']

# Use hexadecimal in the repr to make it easier to compare to the EGL headers.
def hex_repr(self):
    cls = self.__class__
    if self._name_ is not None:
        return '<{}.{}: {:#06x}>'.format(cls.__name__, self._name_,
                                         self._value_)
    members, uncovered = _decompose(cls, self._value_)
    return '<{}.{}: {:#06x}>'.format(cls.__name__,
                                     '|'.join([str(m._name_ or m._value_)
                                               for m in members]),
                                     self._value_)
IntEnum.__repr__ = hex_repr
IntFlag.__repr__ = hex_repr

# EGL 1.0 enumerations.
class ConfigAttrib(IntEnum):
    ALPHA_SIZE = egl.EGL_ALPHA_SIZE
    BLUE_SIZE = egl.EGL_BLUE_SIZE
    BUFFER_SIZE = egl.EGL_BUFFER_SIZE
    CONFIG_CAVEAT = egl.EGL_CONFIG_CAVEAT
    CONFIG_ID = egl.EGL_CONFIG_ID
    DEPTH_SIZE = egl.EGL_DEPTH_SIZE
    GREEN_SIZE = egl.EGL_GREEN_SIZE
    LEVEL = egl.EGL_LEVEL
    MAX_PBUFFER_HEIGHT = egl.EGL_MAX_PBUFFER_HEIGHT
    MAX_PBUFFER_PIXELS = egl.EGL_MAX_PBUFFER_PIXELS
    MAX_PBUFFER_WIDTH = egl.EGL_MAX_PBUFFER_WIDTH
    NATIVE_RENDERABLE = egl.EGL_NATIVE_RENDERABLE
    NATIVE_VISUAL_ID = egl.EGL_NATIVE_VISUAL_ID
    NATIVE_VISUAL_TYPE = egl.EGL_NATIVE_VISUAL_TYPE
    RED_SIZE = egl.EGL_RED_SIZE
    SAMPLES = egl.EGL_SAMPLES
    SAMPLE_BUFFERS = egl.EGL_SAMPLE_BUFFERS
    STENCIL_SIZE = egl.EGL_STENCIL_SIZE
    SURFACE_TYPE = egl.EGL_SURFACE_TYPE
    TRANSPARENT_BLUE_VALUE = egl.EGL_TRANSPARENT_BLUE_VALUE
    TRANSPARENT_GREEN_VALUE = egl.EGL_TRANSPARENT_GREEN_VALUE
    TRANSPARENT_RED_VALUE = egl.EGL_TRANSPARENT_RED_VALUE
    TRANSPARENT_TYPE = egl.EGL_TRANSPARENT_TYPE

class ConfigCaveat(IntEnum):
    NONE = egl.EGL_NONE
    NON_CONFORMANT = egl.EGL_NON_CONFORMANT_CONFIG
    NON_CONFORMANT_CONFIG = egl.EGL_NON_CONFORMANT_CONFIG
    SLOW = egl.EGL_SLOW_CONFIG
    SLOW_CONFIG = egl.EGL_SLOW_CONFIG

class NativeEngine(IntEnum):
    CORE = egl.EGL_CORE_NATIVE_ENGINE
    CORE_NATIVE_ENGINE = egl.EGL_CORE_NATIVE_ENGINE

class ReadOrDraw(IntEnum):
    DRAW = egl.EGL_DRAW
    READ = egl.EGL_READ

class SurfaceAttrib(IntEnum):
    HEIGHT = egl.EGL_HEIGHT
    LARGEST_PBUFFER = egl.EGL_LARGEST_PBUFFER
    WIDTH = egl.EGL_WIDTH

class SurfaceTypeFlag(IntFlag):
    PBUFFER = egl.EGL_PBUFFER_BIT
    PBUFFER_BIT = egl.EGL_PBUFFER_BIT
    PIXMAP = egl.EGL_PIXMAP_BIT
    PIXMAP_BIT = egl.EGL_PIXMAP_BIT
    WINDOW = egl.EGL_WINDOW_BIT
    WINDOW_BIT = egl.EGL_WINDOW_BIT

class TransparentType(IntEnum):
    NONE = egl.EGL_NONE
    RGB = egl.EGL_TRANSPARENT_RGB
    TRANSPARENT_RGB = egl.EGL_TRANSPARENT_RGB


# Additional enumerations and data by version.
if egl.egl_version >= (1, 1):
    for name, value in [('BIND_TO_TEXTURE_RGB', egl.EGL_BIND_TO_TEXTURE_RGB),
                        ('BIND_TO_TEXTURE_RGBA', egl.EGL_BIND_TO_TEXTURE_RGBA),
                        ('MAX_SWAP_INTERVAL', egl.EGL_MAX_SWAP_INTERVAL),
                        ('MIN_SWAP_INTERVAL', egl.EGL_MIN_SWAP_INTERVAL)]:
        extend_enum(ConfigAttrib, name, value)

    for name, value in [('MIPMAP_TEXTURE', egl.EGL_MIPMAP_TEXTURE),
                        ('TEXTURE_FORMAT', egl.EGL_TEXTURE_FORMAT),
                        ('TEXTURE_TARGET', egl.EGL_TEXTURE_TARGET)]:
        extend_enum(SurfaceAttrib, name, value)

    class RenderBuffer(IntEnum):
        BACK = egl.EGL_BACK_BUFFER
        BACK_BUFFER = egl.EGL_BACK_BUFFER

    class TextureFormat(IntEnum):
        NO_TEXTURE = egl.EGL_NO_TEXTURE
        RGB = egl.EGL_TEXTURE_RGB
        TEXTURE_RGB = egl.EGL_TEXTURE_RGB
        RGBA = egl.EGL_TEXTURE_RGBA
        TEXTURE_RGBA = egl.EGL_TEXTURE_RGBA

    class TextureTarget(IntEnum):
        NO_TEXTURE = egl.EGL_NO_TEXTURE
        TEXTURE_2D = egl.EGL_TEXTURE_2D

    __all__.extend(['RenderBuffer', 'TextureFormat', 'TextureTarget'])


if egl.egl_version >= (1, 2):
    for name, value in [('ALPHA_MASK_SIZE', egl.EGL_ALPHA_MASK_SIZE),
                        ('COLOR_BUFFER_TYPE', egl.EGL_COLOR_BUFFER_TYPE),
                        ('LUMINANCE_SIZE', egl.EGL_LUMINANCE_SIZE),
                        ('RENDERABLE_TYPE', egl.EGL_RENDERABLE_TYPE)]:
        extend_enum(ConfigAttrib, name, value)

    for name, value in [('SINGLE', egl.EGL_SINGLE_BUFFER),
                        ('SINGLE_BUFFER', egl.EGL_SINGLE_BUFFER)]:
        extend_enum(RenderBuffer, name, value)

    for name, value in [('RENDER_BUFFER', egl.EGL_RENDER_BUFFER)]:
        extend_enum(SurfaceAttrib, name, value)

    class ClientAPI(IntEnum):
        OPENGL_ES = egl.EGL_OPENGL_ES_API
        OPENGL_ES_API = egl.EGL_OPENGL_ES_API
        OPENVG = egl.EGL_OPENVG_API
        OPENVG_API = egl.EGL_OPENVG_API

    class ClientAPIFlag(IntFlag):
        OPENGL_ES = egl.EGL_OPENGL_ES_BIT
        OPENGL_ES_BIT = egl.EGL_OPENGL_ES_BIT
        OPENVG = egl.EGL_OPENVG_BIT
        OPENVG_BIT = egl.EGL_OPENVG_BIT

    class ClientBufferType(IntEnum):
        OPENVG_IMAGE = egl.EGL_OPENVG_IMAGE

    class ColorBufferType(IntEnum):
        RGB = egl.EGL_RGB_BUFFER
        RGB_BUFFER = egl.EGL_RGB_BUFFER
        LUMINANCE = egl.EGL_LUMINANCE_BUFFER
        LUMINANCE_BUFFER = egl.EGL_LUMINANCE_BUFFER

    class ContextAttrib(IntEnum):
        CLIENT_TYPE = egl.EGL_CONTEXT_CLIENT_TYPE
        CONTEXT_CLIENT_TYPE = egl.EGL_CONTEXT_CLIENT_TYPE

    class SwapBehavior(IntEnum):
        BUFFER_DESTROYED = egl.EGL_BUFFER_DESTROYED
        BUFFER_PRESERVED = egl.EGL_BUFFER_PRESERVED

    __all__.extend(['ClientAPI', 'ClientAPIFlag', 'ClientBufferType',
                    'ColorBufferType', 'ContextAttrib', 'SwapBehavior'])


if egl.egl_version >= (1, 3):
    for name, value in [('OPENGL_ES2', egl.EGL_OPENGL_ES2_BIT),
                        ('OPENGL_ES2_BIT', egl.EGL_OPENGL_ES2_BIT)]:
        extend_enum(ClientAPIFlag, name, value)

    for name, value in [('CONFORMANT', egl.EGL_CONFORMANT),
                        ('MATCH_NATIVE_PIXMAP', egl.EGL_MATCH_NATIVE_PIXMAP)]:
        extend_enum(ConfigAttrib, name, value)

    for name, value in [('CLIENT_VERSION', egl.EGL_CONTEXT_CLIENT_VERSION),
                        ('CONTEXT_CLIENT_VERSION',
                         egl.EGL_CONTEXT_CLIENT_VERSION),
                        ('MAJOR_VERSION', egl.EGL_CONTEXT_MAJOR_VERSION),
                        ('CONTEXT_MAJOR_VERSION',
                         egl.EGL_CONTEXT_MAJOR_VERSION)]:
        extend_enum(ContextAttrib, name, value)

    for name, value in [('VG_ALPHA_FORMAT', egl.EGL_VG_ALPHA_FORMAT),
                        ('VG_COLORSPACE', egl.EGL_VG_COLORSPACE)]:
        extend_enum(SurfaceAttrib, name, value)

    for name, value in [('VG_ALPHA_FORMAT_PRE',
                         egl.EGL_VG_ALPHA_FORMAT_PRE_BIT),
                        ('VG_ALPHA_FORMAT_PRE_BIT',
                         egl.EGL_VG_ALPHA_FORMAT_PRE_BIT),
                        ('VG_COLORSPACE_LINEAR',
                         egl.EGL_VG_COLORSPACE_LINEAR_BIT),
                        ('VG_COLORSPACE_LINEAR_BIT',
                         egl.EGL_VG_COLORSPACE_LINEAR_BIT)]:
        extend_enum(SurfaceTypeFlag, name, value)

    class VGAlphaFormat(IntEnum):
        NONPRE = egl.EGL_VG_ALPHA_FORMAT_NONPRE
        VG_ALPHA_FORMAT_NONPRE = egl.EGL_VG_ALPHA_FORMAT_NONPRE
        PRE = egl.EGL_VG_ALPHA_FORMAT_PRE
        VG_ALPHA_FORMAT_PRE = egl.EGL_VG_ALPHA_FORMAT_PRE

    class VGColorspace(IntEnum):
        sRGB = egl.EGL_VG_COLORSPACE_sRGB
        # It's odd how OpenGL uses SRGB, but OpenVG uses sRGB (notice the
        # lower-case s). To save errors, I'm providing both as aliases.
        SRGB = egl.EGL_VG_COLORSPACE_sRGB
        VG_COLORSPACE_sRGB = egl.EGL_VG_COLORSPACE_sRGB
        VG_COLORSPACE_SRGB = egl.EGL_VG_COLORSPACE_sRGB
        LINEAR = egl.EGL_VG_COLORSPACE_LINEAR
        VG_COLORSPACE_LINEAR = egl.EGL_VG_COLORSPACE_LINEAR

    __all__.extend(['VGAlphaFormat', 'VGColorspace'])


if egl.egl_version >= (1, 4):
    for name, value in [('MULTISAMPLE_RESOLVE_BOX',
                         egl.EGL_MULTISAMPLE_RESOLVE_BOX_BIT),
                        ('MULTISAMPLE_RESOLVE_BOX_BIT',
                         egl.EGL_MULTISAMPLE_RESOLVE_BOX_BIT),
                        ('SWAP_BEHAVIOR_PRESERVED',
                         egl.EGL_SWAP_BEHAVIOR_PRESERVED_BIT),
                        ('SWAP_BEHAVIOR_PRESERVED_BIT',
                         egl.EGL_SWAP_BEHAVIOR_PRESERVED_BIT)]:
        extend_enum(SurfaceTypeFlag, name, value)

    for name, value in [('OPENGL', egl.EGL_OPENGL_API),
                        ('OPENGL_API', egl.EGL_OPENGL_API)]:
        extend_enum(ClientAPI, name, value)

    for name, value in [('OPENGL', egl.EGL_OPENGL_BIT),
                        ('OPENGL_BIT', egl.EGL_OPENGL_BIT)]:
        extend_enum(ClientAPIFlag, name, value)


    class MultisampleResolve(IntEnum):
        DEFAULT = egl.EGL_MULTISAMPLE_RESOLVE_DEFAULT
        MULTISAMPLE_RESOLVE_DEFAULT = egl.EGL_MULTISAMPLE_RESOLVE_DEFAULT
        BOX = egl.EGL_MULTISAMPLE_RESOLVE_BOX
        MULTISAMPLE_RESOLVE_BOX = egl.EGL_MULTISAMPLE_RESOLVE_BOX

    __all__.extend(['MultisampleResolve'])


if egl.egl_version >= (1, 5):
    for name, value in [('OPENGL_ES3', egl.EGL_OPENGL_ES3_BIT),
                        ('OPENGL_ES3_BIT', egl.EGL_OPENGL_ES3_BIT)]:
        extend_enum(ClientAPIFlag, name, value)

    for name, value in [('MINOR_VERSION', egl.EGL_CONTEXT_MINOR_VERSION),
                        ('CONTEXT_MINOR_VERSION',
                         egl.EGL_CONTEXT_MINOR_VERSION),
                        ('OPENGL_PROFILE',
                         egl.EGL_CONTEXT_OPENGL_PROFILE_MASK),
                        ('CONTEXT_OPENGL_PROFILE_MASK',
                         egl.EGL_CONTEXT_OPENGL_PROFILE_MASK),
                        ('OPENGL_DEBUG', egl.EGL_CONTEXT_OPENGL_DEBUG),
                        ('CONTEXT_OPENGL_DEBUG',
                         egl.EGL_CONTEXT_OPENGL_DEBUG),
                        ('OPENGL_FORWARD_COMPATIBLE',
                         egl.EGL_CONTEXT_OPENGL_FORWARD_COMPATIBLE),
                        ('CONTEXT_OPENGL_FORWARD_COMPATIBLE',
                         egl.EGL_CONTEXT_OPENGL_FORWARD_COMPATIBLE),
                        ('OPENGL_ROBUST_ACCESS',
                         egl.EGL_CONTEXT_OPENGL_ROBUST_ACCESS),
                        ('CONTEXT_OPENGL_ROBUST_ACCESS',
                         egl.EGL_CONTEXT_OPENGL_ROBUST_ACCESS),
                        ('OPENGL_RESET_NOTIFICATION_STRATEGY',
                         egl.EGL_CONTEXT_OPENGL_RESET_NOTIFICATION_STRATEGY),
                        ('CONTEXT_OPENGL_RESET_NOTIFICATION_STRATEGY',
                         egl.EGL_CONTEXT_OPENGL_RESET_NOTIFICATION_STRATEGY)]:
        extend_enum(ContextAttrib, name, value)

    for name, value in [('GL_COLORSPACE', egl.EGL_GL_COLORSPACE)]:
        extend_enum(SurfaceAttrib, name, value)


    class GLColorspace(IntEnum):
        SRGB = egl.EGL_GL_COLORSPACE_SRGB
        # It's odd how OpenGL uses SRGB, but OpenVG uses sRGB (notice the
        # lower-case s). To save errors, I'm providing both as aliases.
        sRGB = egl.EGL_GL_COLORSPACE_SRGB
        GL_COLORSPACE_SRGB = egl.EGL_GL_COLORSPACE_SRGB
        GL_COLORSPACE_sRGB = egl.EGL_GL_COLORSPACE_SRGB
        LINEAR = egl.EGL_GL_COLORSPACE_LINEAR
        GL_COLORSPACE_LINEAR = egl.EGL_GL_COLORSPACE_LINEAR

    class ImageAttrib(IntEnum):
        GL_TEXTURE_LEVEL = egl.EGL_GL_TEXTURE_LEVEL
        GL_TEXTURE_ZOFFSET = egl.EGL_GL_TEXTURE_ZOFFSET
        IMAGE_PRESERVED = egl.EGL_IMAGE_PRESERVED

    class ImageTarget(IntEnum):
        GL_TEXTURE_2D = egl.EGL_GL_TEXTURE_2D
        GL_TEXTURE_CUBE_MAP_POSITIVE_X = egl.EGL_GL_TEXTURE_CUBE_MAP_POSITIVE_X
        GL_TEXTURE_CUBE_MAP_NEGATIVE_X = egl.EGL_GL_TEXTURE_CUBE_MAP_NEGATIVE_X
        GL_TEXTURE_CUBE_MAP_POSITIVE_Y = egl.EGL_GL_TEXTURE_CUBE_MAP_POSITIVE_Y
        GL_TEXTURE_CUBE_MAP_NEGATIVE_Y = egl.EGL_GL_TEXTURE_CUBE_MAP_NEGATIVE_Y
        GL_TEXTURE_CUBE_MAP_POSITIVE_Z = egl.EGL_GL_TEXTURE_CUBE_MAP_POSITIVE_Z
        GL_TEXTURE_CUBE_MAP_NEGATIVE_Z = egl.EGL_GL_TEXTURE_CUBE_MAP_NEGATIVE_Z
        GL_TEXTURE_3D = egl.EGL_GL_TEXTURE_3D
        GL_RENDERBUFFER = egl.EGL_GL_RENDERBUFFER

    class OpenGLProfileFlag(IntFlag):
        CORE = egl.EGL_CONTEXT_OPENGL_CORE_PROFILE_BIT
        CONTEXT_OPENGL_CORE_PROFILE_BIT = \
            egl.EGL_CONTEXT_OPENGL_CORE_PROFILE_BIT
        COMPATIBILITY = egl.EGL_CONTEXT_OPENGL_COMPATIBILITY_PROFILE_BIT
        CONTEXT_OPENGL_COMPATIBILITY_PROFILE_BIT = \
            egl.EGL_CONTEXT_OPENGL_COMPATIBILITY_PROFILE_BIT

    class Platform(IntEnum):
        pass

    class DisplayAttrib(IntEnum):
        pass

    class ResetNotificationStrategy(IntEnum):
        NO_RESET_NOTIFICATION = egl.EGL_NO_RESET_NOTIFICATION
        LOSE_CONTEXT_ON_RESET = egl.EGL_LOSE_CONTEXT_ON_RESET

    class SyncAttrib(IntEnum):
        CL_EVENT_HANDLE = egl.EGL_CL_EVENT_HANDLE

    class SyncCondition(IntEnum):
        PRIOR_COMMANDS_COMPLETE = egl.EGL_SYNC_PRIOR_COMMANDS_COMPLETE
        SYNC_PRIOR_COMMANDS_COMPLETE = egl.EGL_SYNC_PRIOR_COMMANDS_COMPLETE
        CL_EVENT_COMPLETE = egl.EGL_SYNC_CL_EVENT_COMPLETE
        SYNC_CL_EVENT_COMPLETE = egl.EGL_SYNC_CL_EVENT_COMPLETE

    class SyncFlag(IntFlag):
        NONE = 0
        FLUSH_COMMANDS = egl.EGL_SYNC_FLUSH_COMMANDS_BIT
        SYNC_FLUSH_COMMANDS_BIT = egl.EGL_SYNC_FLUSH_COMMANDS_BIT

    class SyncResult(IntEnum):
        CONDITION_SATISFIED = egl.EGL_CONDITION_SATISFIED
        TIMEOUT_EXPIRED = egl.EGL_TIMEOUT_EXPIRED

    class SyncType(IntEnum):
        FENCE = egl.EGL_SYNC_FENCE
        SYNC_FENCE = egl.EGL_SYNC_FENCE
        CL_EVENT = egl.EGL_SYNC_CL_EVENT
        SYNC_CL_EVENT = egl.EGL_SYNC_CL_EVENT

    __all__.extend(['GLColorspace', 'ImageAttrib', 'ImageTarget', 'Platform',
                    'PlatformAttrib', 'SyncAttrib', 'SyncCondition',
                    'SyncFlag', 'SyncResult', 'SyncType'])
