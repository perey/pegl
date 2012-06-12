#!/usr/bin/env python3

'''EGL attributes for configuration objects.'''

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
from collections import namedtuple
from ctypes import c_int

# Local imports.
from . import Attribs, Details, NONE, NO_TEXTURE, scaled, UNKNOWN_VALUE
from .config import ConfigAttribs
from .context import ContextAttribs, RenderBufferTypes

# Objects for surface attributes.
VGColorSpaces = namedtuple('VGColorSpaces_tuple',
                           ('SRGB', 'LINEAR')
                           )(0x3089, 0x308A)
VGAlphaFormats = namedtuple('VGAlphaFormats_tuple',
                            ('NONPRE', 'PRE')
                            )(0x308B, 0x308C)
TextureFormats = namedtuple('TextureFormats_tuple',
                            ('NONE', 'RGB', 'RGBA')
                            )(NO_TEXTURE, 0x305D, 0x305E)
TextureTargets = namedtuple('TextureTargets_tuple',
                            ('NONE', 'TWO_D')
                            )(NO_TEXTURE, 0x305F)
MultisampleResolve = namedtuple('MultisampleResolve_tuple',
                                ('DEFAULT', 'BOX')
                                )(0x309A, 0x309B)
SwapBehaviors = namedtuple('SwapBehaviours_tuple',
                           ('PRESERVED', 'DESTROYED')
                           )(0x3094, 0x3095)

class SurfaceAttribs(Attribs):
    # For creating window surfaces.
    RENDER_BUFFER = ContextAttribs.RENDER_BUFFER
    # For creating Pbuffer surfaces.
    WIDTH, HEIGHT, LARGEST_PBUFFER = 0x3057, 0x3056, 0x3058
    TEXTURE_FORMAT, TEXTURE_TARGET, MIPMAP_TEXTURE = 0x3080, 0x3081, 0x3082
    # For creating all surfaces.
    VG_COLORSPACE, VG_ALPHA_FORMAT = 0x3087, 0x3088
    # For setting attributes of a surface.
    MIPMAP_LEVEL, MULTISAMPLE_RESOLVE, SWAP_BEHAVIOR = 0x3083, 0x3099, 0x3093
    # For querying attributes of a surface.
    CONFIG_ID = ConfigAttribs.CONFIG_ID
    HORIZONTAL_RESOLUTION, VERTICAL_RESOLUTION, PIXEL_ASPECT_RATIO = (0x3090,
                                                                      0x3091,
                                                                      0x3092)
    details = {RENDER_BUFFER: Details('Which buffer type this surface renders '
                                      'into', RenderBufferTypes,
                                      RenderBufferTypes.BACK),
               WIDTH: Details('Width in pixels of the pbuffer', c_int, 0),
               HEIGHT: Details('Height in pixels of the pbuffer', c_int, 0),
               LARGEST_PBUFFER: Details('Whether or not to get the largest '
                                        'available pbuffer if the requested '
                                        'size is unavailable', bool, False),
               TEXTURE_FORMAT: Details('Format of the texture that the pbuffer '
                                       'is bound to', TextureFormats,
                                       TextureFormats.NONE),
               TEXTURE_TARGET: Details('Target of the texture that the pbuffer '
                                       'is bound to', TextureTargets,
                                       TextureTargets.NONE),
               MIPMAP_TEXTURE: Details('Whether or not mipmap space is '
                                       'allocated', bool, False),
               VG_COLORSPACE: Details('The color space to be used by OpenVG',
                                      VGColorSpaces, VGColorSpaces.SRGB),
               VG_ALPHA_FORMAT: Details('Whether or not alpha values are '
                                        'premultiplied by OpenVG',
                                        VGAlphaFormats, VGAlphaFormats.NONPRE),
               MIPMAP_LEVEL: Details('The level of the mipmap texture to '
                                     'render', c_int, 0),
               MULTISAMPLE_RESOLVE: Details('The filter to use when resolving '
                                            'the multisample buffer',
                                            MultisampleResolve,
                                            MultisampleResolve.DEFAULT),
               SWAP_BEHAVIOR: Details('Effect on color buffer upon a buffer '
                                      'swap', SwapBehaviors,
                                      # The actual default is implementation-
                                      # defined, but since "preserved" behavior
                                      # needs its own bit flag in the config to
                                      # indicate support, "destroyed" seems
                                      # like a reasonable default to put here.
                                      SwapBehaviors.DESTROYED),
               CONFIG_ID: Details('The unique identifier of the configuration '
                                  'used to create this surface', c_int, 0),
               HORIZONTAL_RESOLUTION: Details('Horizontal resolution of the '
                                              'display, in pixels per metre',
                                              scaled, UNKNOWN_VALUE),
               VERTICAL_RESOLUTION: Details('Vertical resolution of the '
                                            'display, in pixels per metre',
                                            scaled, UNKNOWN_VALUE),
               PIXEL_ASPECT_RATIO: Details('Ratio of physical pixel width to '
                                           'height', scaled,
                                           UNKNOWN_VALUE)}
