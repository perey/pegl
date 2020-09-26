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

# Standard library imports.
from enum import IntEnum, IntFlag

# Local imports.
from . import egl

__all__ = ['ConfigAttrib', 'SurfaceTypeFlag']

# Enumerations available unchanged from EGL 1.0.

# Data for enumerations that expand in later versions.
config_attrib = [('ALPHA_SIZE', egl.EGL_ALPHA_SIZE),
                 ('BLUE_SIZE', egl.EGL_BLUE_SIZE),
                 ('BUFFER_SIZE', egl.EGL_BUFFER_SIZE),
                 ('CONFIG_CAVEAT', egl.EGL_CONFIG_CAVEAT),
                 ('CONFIG_ID', egl.EGL_CONFIG_ID),
                 ('DEPTH_SIZE', egl.EGL_DEPTH_SIZE),
                 ('GREEN_SIZE', egl.EGL_GREEN_SIZE),
                 ('LEVEL', egl.EGL_LEVEL),
                 ('MAX_PBUFFER_HEIGHT', egl.EGL_MAX_PBUFFER_HEIGHT),
                 ('MAX_PBUFFER_PIXELS', egl.EGL_MAX_PBUFFER_PIXELS),
                 ('MAX_PBUFFER_WIDTH', egl.EGL_MAX_PBUFFER_WIDTH),
                 ('NATIVE_RENDERABLE', egl.EGL_NATIVE_RENDERABLE),
                 ('NATIVE_VISUAL_ID', egl.EGL_NATIVE_VISUAL_ID),
                 ('NATIVE_VISUAL_TYPE', egl.EGL_NATIVE_VISUAL_TYPE),
                 ('RED_SIZE', egl.EGL_RED_SIZE),
                 ('SAMPLES', egl.EGL_SAMPLES),
                 ('SAMPLE_BUFFERS', egl.EGL_SAMPLE_BUFFERS),
                 ('STENCIL_SIZE', egl.EGL_STENCIL_SIZE),
                 ('SURFACE_TYPE', egl.EGL_SURFACE_TYPE),
                 ('TRANSPARENT_BLUE_VALUE', egl.EGL_TRANSPARENT_BLUE_VALUE),
                 ('TRANSPARENT_GREEN_VALUE', egl.EGL_TRANSPARENT_GREEN_VALUE),
                 ('TRANSPARENT_RED_VALUE', egl.EGL_TRANSPARENT_RED_VALUE),
                 ('TRANSPARENT_TYPE', egl.EGL_TRANSPARENT_TYPE)]

surface_type_flag = [('PBUFFER', egl.EGL_PBUFFER_BIT),
                     ('PBUFFER_BIT', egl.EGL_PBUFFER_BIT),
                     ('PIXMAP', egl.EGL_PIXMAP_BIT),
                     ('PIXMAP_BIT', egl.EGL_PIXMAP_BIT),
                     ('WINDOW', egl.EGL_WINDOW_BIT),
                     ('WINDOW_BIT', egl.EGL_WINDOW_BIT)]

# Additional enumerations and data by version.
if egl.egl_version >= (1, 1):
    config_attrib.extend([('BIND_TO_TEXTURE_RGB', egl.EGL_BIND_TO_TEXTURE_RGB),
                          ('BIND_TO_TEXTURE_RGBA',
                           egl.EGL_BIND_TO_TEXTURE_RGBA),
                          ('MAX_SWAP_INTERVAL', egl.EGL_MAX_SWAP_INTERVAL),
                          ('MIN_SWAP_INTERVAL', egl.EGL_MIN_SWAP_INTERVAL)])

if egl.egl_version >= (1, 2):
    config_attrib.extend([('ALPHA_MASK_SIZE', egl.EGL_ALPHA_MASK_SIZE),
                          ('COLOR_BUFFER_TYPE', egl.EGL_COLOR_BUFFER_TYPE),
                          ('LUMINANCE_SIZE', egl.EGL_LUMINANCE_SIZE),
                          ('RENDERABLE_TYPE', egl.EGL_RENDERABLE_TYPE)])

    class ColorBufferType(IntEnum):
        RGB = egl.EGL_RGB_BUFFER
        RGB_BUFFER = egl.EGL_RGB_BUFFER
        LUMINANCE = egl.EGL_LUMINANCE_BUFFER
        LUMINANCE_BUFFER = egl.EGL_LUMINANCE_BUFFER

    __all__.extend(['ColorBufferType'])

if egl.egl_version >= (1, 3):
    config_attrib.extend([('CONFORMANT', egl.EGL_CONFORMANT),
                          ('MATCH_NATIVE_PIXMAP',
                           egl.EGL_MATCH_NATIVE_PIXMAP)])

    surface_type_flag.extend([('VG_ALPHA_FORMAT_PRE',
                               egl.EGL_VG_ALPHA_FORMAT_PRE_BIT),
                              ('VG_ALPHA_FORMAT_PRE_BIT',
                               egl.EGL_VG_ALPHA_FORMAT_PRE_BIT),
                              ('VG_COLORSPACE_LINEAR',
                               egl.EGL_VG_COLORSPACE_LINEAR_BIT),
                              ('VG_COLORSPACE_LINEAR_BIT',
                               egl.EGL_VG_COLORSPACE_LINEAR_BIT)])

if egl.egl_version >= (1, 4):
    surface_type_flag.extend([('MULTISAMPLE_RESOLVE_BOX',
                               egl.EGL_MULTISAMPLE_RESOLVE_BOX_BIT),
                              ('MULTISAMPLE_RESOLVE_BOX_BIT',
                               egl.EGL_MULTISAMPLE_RESOLVE_BOX_BIT),
                              ('SWAP_BEHAVIOR_PRESERVED',
                               egl.EGL_SWAP_BEHAVIOR_PRESERVED_BIT),
                              ('SWAP_BEHAVIOR_PRESERVED_BIT',
                               egl.EGL_SWAP_BEHAVIOR_PRESERVED_BIT)])

# Construct enumerations that may have expanded.
ConfigAttrib = IntEnum('ConfigAttrib', config_attrib, module=__name__)

SurfaceTypeFlag = IntFlag('SurfaceTypeFlag', surface_type_flag,
                          module=__name__)
