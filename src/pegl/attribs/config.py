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
from . import Attribs, BitMask, Details, DONT_CARE, NONE

# Objects for config attribute values.
class SurfaceTypes(BitMask):
    '''A bit mask representing types of EGL surfaces.'''
    bit_names = ['PBUFFER', 'PIXMAP', 'WINDOW', None, None,
                 'VG_COLORSPACE_LINEAR', 'VG_ALPHA_FORMAT_PRE', None, None,
                 'MULTISAMPLE_RESOLVE_BOX', 'SWAP_BEHAVIOR_PRESERVED']


class ClientAPIs(BitMask):
    '''A bit mask representing client APIs supported by EGL.'''
    bit_names = ['OPENGL_ES', 'OPENVG', 'OPENGL_ES2', 'OPENGL']


CBufferTypes = namedtuple('CBufferTypes_tuple',
                          ('RGB', 'LUMINANCE')
                          )(0x308E, 0x308F)
Caveats = namedtuple('Caveats_tuple',
                     ('NONE', 'SLOW', 'NONCONFORMANT')
                     )(NONE, 0x3050, 0x3051)
TransparentTypes = namedtuple('TransparentTypes_tuple',
                              ('NONE', 'RGB')
                              )(NONE, 0x3052)


class ConfigAttribs(Attribs):
    '''The set of EGL attributes relevant to configuration objects.

    Class attributes:
        details -- As per the superclass, Attribs.
        must_care -- A sequence giving all values for which DONT_CARE is
            not allowed to be supplied.
        Additionally, symbolic constants for all the known attributes
        are available as class attributes. Their names are the same as
        in the EGL standard, except without the EGL_ prefix.
        

    '''
    (BUFFER_SIZE, ALPHA_SIZE, BLUE_SIZE, GREEN_SIZE, RED_SIZE, DEPTH_SIZE,
     STENCIL_SIZE, CONFIG_CAVEAT, CONFIG_ID, LEVEL, MAX_PBUFFER_HEIGHT,
     MAX_PBUFFER_PIXELS, MAX_PBUFFER_WIDTH, NATIVE_RENDERABLE,
     NATIVE_VISUAL_ID, NATIVE_VISUAL_TYPE) = range(0x3020, 0x3030)
    # There is no 0x3030.
    (SAMPLES, SAMPLE_BUFFERS, SURFACE_TYPE, TRANSPARENT_TYPE,
     TRANSPARENT_BLUE_VALUE, TRANSPARENT_GREEN_VALUE, TRANSPARENT_RED_VALUE,
     NONE, BIND_TO_TEXTURE_RGB, BIND_TO_TEXTURE_RGBA, MIN_SWAP_INTERVAL,
     MAX_SWAP_INTERVAL, LUMINANCE_SIZE, ALPHA_MASK_SIZE, COLOR_BUFFER_TYPE,
     RENDERABLE_TYPE, MATCH_NATIVE_PIXMAP, CONFORMANT) = range(0x3031, 0x3043)
    details = {BUFFER_SIZE: Details('Total number of component bits in the '
                                    'color buffer', c_int, 0),
               COLOR_BUFFER_TYPE: Details('Type of the color buffer',
                                          CBufferTypes, CBufferTypes.RGB),
               RED_SIZE: Details('Number of red bits in the color buffer',
                                 c_int, 0),
               GREEN_SIZE: Details('Number of green bits in the color buffer',
                                   c_int, 0),
               BLUE_SIZE: Details('Number of blue bits in the color buffer',
                                  c_int, 0),
               ALPHA_SIZE: Details('Number of alpha bits in the color buffer',
                                   c_int, 0),
               LUMINANCE_SIZE: Details('Number of luminance bits in the color '
                                 'buffer', c_int, 0),

               LEVEL: Details('Frame buffer level', c_int, 0),
               MAX_PBUFFER_HEIGHT: Details('Maximum height of the pbuffer',
                                           c_int, 0),
               MAX_PBUFFER_PIXELS: Details('Maximum pixel size of the pbuffer',
                                           c_int, 0),
               MAX_PBUFFER_WIDTH: Details('Maximum width of the pbuffer',
                                          c_int, 0),
               SAMPLES: Details('Number of samples per pixel', c_int, 0),
               SAMPLE_BUFFERS: Details('Number of multisample buffers', c_int,
                                       0),
               ALPHA_MASK_SIZE: Details('Number of alpha mask bits in the '
                                        'mask buffer', c_int, 0),

               DEPTH_SIZE: Details('Number of Z bits in the depth buffer',
                                   c_int, 0),
               STENCIL_SIZE: Details('Number of stencil bits in the stencil '
                                     'buffer', c_int, 0),

               MIN_SWAP_INTERVAL: Details('Minimum swap intervals before a '
                                          'buffer swap occurs', c_int,
                                          DONT_CARE),
               MAX_SWAP_INTERVAL: Details('Maximum swap intervals before a '
                                          'buffer swap occurs', c_int,
                                          DONT_CARE),

               TRANSPARENT_TYPE: Details('Support for transparency or lack '
                                         'thereof', TransparentTypes,
                                         TransparentTypes.NONE),
               TRANSPARENT_RED_VALUE: Details('Red value of transparent '
                                              'pixels', c_int,
                                              DONT_CARE),
               TRANSPARENT_GREEN_VALUE: Details('Green value of transparent '
                                                'pixels', c_int,
                                                DONT_CARE),
               TRANSPARENT_BLUE_VALUE: Details('Blue value of transparent '
                                               'pixels', c_int,
                                               DONT_CARE),

               SURFACE_TYPE: Details('Bitmask of EGL surface types supported',
                                     SurfaceTypes, SurfaceTypes(WINDOW=1)),
               BIND_TO_TEXTURE_RGB: Details('Whether or not this is bindable '
                                            'to RGB textures', bool,
                                            DONT_CARE),
               BIND_TO_TEXTURE_RGBA: Details('Whether or not this is bindable '
                                             'to RGBA textures', bool,
                                             DONT_CARE),

               CONFIG_CAVEAT: Details('Caveat for performance or conformance '
                                      'of this config', Caveats, DONT_CARE),
               CONFIG_ID: Details('Unique identifier for this config', c_int,
                                  DONT_CARE),
               RENDERABLE_TYPE: Details('Bitmask of available client '
                                        'rendering APIs', ClientAPIs,
                                        ClientAPIs(OPENGL_ES=1)),
               CONFORMANT: Details('Bitmask of specs to which contexts '
                                   'conform', ClientAPIs, ClientAPIs()),

               NATIVE_RENDERABLE: Details('Whether or not native APIs can '
                                          'render to the surface', bool,
                                          DONT_CARE),
               NATIVE_VISUAL_ID: Details('Identifier for the native visual',
                                         c_int, 0),
               NATIVE_VISUAL_TYPE: Details('Type of the native visual', c_int,
                                           DONT_CARE),
               MATCH_NATIVE_PIXMAP: Details('Handle of a valid native pixmap',
                                            c_int, NONE)}

    must_care = (LEVEL,)
