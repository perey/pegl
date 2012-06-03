#!/usr/bin/env python3

'''EGL 1.4 attribute lists.'''

# Copyright © 2012 Tim Pederick.
#
# This file is part of PEGL.
#
# PEGL is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PEGL is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
# License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PEGL. If not, see <http://www.gnu.org/licenses/>.

# Standard library imports.
from collections import namedtuple
from ctypes import c_bool, c_int
from itertools import cycle

Details = namedtuple('Details', ('desc', 'values', 'dontcare', 'default'))

NONE = 0x3038

def bitmask(bit_positions):
    '''Generate a bitmask with convenient Python representations.'''
    class BitMask:
        '''A bitmask with convenient Python representations.'''
        width = len(bit_positions)
        bit_names = bit_positions
        def __init__(self, *args, **kwargs):
            self.bits = [0] * self.width

            for n, posname in enumerate(self.bit_names):
                if posname is None:
                    continue
                getter = lambda self: self.bits[n]
                setter = lambda self, val: self._set_bit(n, val)
                self.__setattr__(posname, property(getter, setter))

            for mask in args:
                self._from_int(mask)

            for bit_name in kwargs:
                # Allow an AttributeError to propagate upwards
                setter = self.__getattribute__(bit_name).fset
                setter(self, kwargs[bit_name])

        @property
        def _as_parameter_(self):
            return int(self)

        def __int__(self):
            return sum(2 ** i if bit else 0 for i, bit in enumerate(self.bits))

        def _set_bit(self, bit_pos, val):
            self.bits[bit_pos] = bool(val)

        def _from_int(self, mask):
            pos = 0
            mask = int(mask)
            while mask > 0 and pos < self.width:
                mask, bit = divmod(mask, 2)
                self.bits[pos] = bool(bit)
                pos += 1

    return BitMask

SurfaceTypes = bitmask(('pbuffer', 'pixmap', 'window', None, None,
                        'vg_col_linear', 'vg_alpha_pre', None, None,
                        'multisample_box', 'swap_preserve'))
ClientAPIs = bitmask(('gl_es', 'vg', 'gl_es2', 'gl'))

class DONT_CARE:
    '''A don't-care value for an attribute.'''
    _as_parameter_ = -1

CBufferTypes = namedtuple('CBufferTypes',
                          ('rgb', 'luminance')
                          )(0x308E, 0x308F)
Caveats = namedtuple('Caveats',
                     ('none', 'slow', 'nonconform')
                     )(NONE, 0x3050, 0x3051)
TransparentTypes = namedtuple('TransparentTypes',
                              ('none', 'rgb')
                              )(NONE, 0x3052)

class Attribs:
    '''The set of available EGL attribute values.'''
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
                                    'color buffer', c_int, False, 0),
               COLOR_BUFFER_TYPE: Details('Type of the color buffer',
                                          CBufferTypes, True,
                                          CBufferTypes.rgb),
               RED_SIZE: Details('Number of red bits in the color buffer',
                                 c_int, True, 0),
               GREEN_SIZE: Details('Number of green bits in the color buffer',
                                   c_int, True, 0),
               BLUE_SIZE: Details('Number of blue bits in the color buffer',
                                  c_int, True, 0),
               ALPHA_SIZE: Details('Number of alpha bits in the color buffer',
                                   c_int, False, 0),
               ALPHA_MASK_SIZE: Details('Number of alpha mask bits in the '
                                        'color buffer', c_int, False, 0),
               LUMINANCE_SIZE: Details('Number of luminance bits in the color '
                                 'buffer', c_int, False, 0),

               LEVEL: Details('Frame buffer level', c_int, False, 0),
               MAX_PBUFFER_HEIGHT: Details('Maximum height of the pbuffer',
                                           c_int, False, 0),
               MAX_PBUFFER_PIXELS: Details('Maximum pixel size of the pbuffer',
                                           c_int, False, 0),
               MAX_PBUFFER_WIDTH: Details('Maximum width of the pbuffer',
                                          c_int, False, 0),
               SAMPLES: Details('Number of samples per pixel', c_int,
                                False, 0),
               SAMPLE_BUFFERS: Details('Number of multisample buffers', c_int,
                                       False, 0),

               DEPTH_SIZE: Details('Number of Z bits in the depth buffer',
                                   c_int, False, 0),
               STENCIL_SIZE: Details('Number of stencil bits in the stencil '
                                     'buffer', c_int, False, 0),

               MIN_SWAP_INTERVAL: Details('Minimum swap intervals before a '
                                          'buffer swap occurs', c_int, True,
                                          DONT_CARE),
               MAX_SWAP_INTERVAL: Details('Maximum swap intervals before a '
                                          'buffer swap occurs', c_int, True,
                                          DONT_CARE),

               TRANSPARENT_TYPE: Details('Support for transparency or lack '
                                         'thereof', TransparentTypes, False,
                                         TransparentTypes.none),
               TRANSPARENT_RED_VALUE: Details('Red value of transparent '
                                              'pixels', c_int, True,
                                              DONT_CARE),
               TRANSPARENT_GREEN_VALUE: Details('Green value of transparent '
                                                'pixels', c_int, True,
                                                DONT_CARE),
               TRANSPARENT_BLUE_VALUE: Details('Blue value of transparent '
                                               'pixels', c_int, True,
                                               DONT_CARE),

               SURFACE_TYPE: Details('Bitmask of EGL surface types supported',
                                     SurfaceTypes, False,
                                     SurfaceTypes(window=1)),
               BIND_TO_TEXTURE_RGB: Details('Whether or not this is bindable '
                                            'to RGB textures', c_bool, True,
                                            DONT_CARE),
               BIND_TO_TEXTURE_RGBA: Details('Whether or not this is bindable '
                                             'to RGBA textures', c_bool, True,
                                             DONT_CARE),

               CONFIG_CAVEAT: Details('Caveat for performance or conformance '
                                      'of this config', Caveats, True,
                                      DONT_CARE),
               CONFIG_ID: Details('Unique identifier for this config', c_int,
                                  True, DONT_CARE),
               RENDERABLE_TYPE: Details('Bitmask of available client '
                                        'rendering APIs', ClientAPIs, False,
                                        ClientAPIs(gl_es=1)),
               CONFORMANT: Details('Bitmask of specs to which contexts conform',
                                   ClientAPIs, False, ClientAPIs()),

               NATIVE_RENDERABLE: Details('Whether or not native APIs can '
                                          'render to the surface', c_bool,
                                          True, DONT_CARE),
               NATIVE_VISUAL_ID: Details('Identifier for the native visual',
                                         c_int, False, 0),
               NATIVE_VISUAL_TYPE: Details('Native visual type', c_int, True,
                                           DONT_CARE),
               MATCH_NATIVE_PIXMAP: Details('Handle of a valid native pixmap',
                                            c_int, False, NONE)}

    @classmethod
    def desc(cls, value):
        '''Get a textual description of a given attribute.

        This may also be used to test for the validity of a given
        attribute. If the return value is None, the value supplied does
        not map to any known attribute.

        '''
        details = cls.details.get(value)
        return (None if details is None else details.desc)


class AttribList:
    '''A list of context attributes.'''
    def __init__(self, mapping=None):
        self._items = {}

        if mapping is not None:
            for key, val in mapping.items():
                self[key] = val

    def __getitem__(self, index):
        '''Get the value of an attribute, or None if it is unset.'''
        if Attribs.desc(index) is None:
            raise ValueError('not a valid attribute type')
        return self._items.get(index)

    def __setitem__(self, index, val):
        '''Set the value of an attribute.'''
        details = Attribs.details.get(index)
        if details is None:
            raise ValueError('not a valid attribute type')
        elif val is DONT_CARE and not details.dontcare:
            raise ValueError('attribute cannot be DONT_CARE')
        elif val is None:
            val = details.default

        try:
            if val not in details.values:
                raise ValueError('not a legal attribute value')
        except TypeError:
            # "in" is not applicable to this attribute type.
            if type(val) is not type(details.values):
                val = details.values(val)

        self._items[index] = val

    def __delitem__(self, index):
        '''Remove the value set for an attribute.'''
        del(self._items[index])

    @property
    def _as_parameter_(self):
        '''Convert to an array for use as a foreign function argument.'''
        arr_len = 2 * len(self._items) + 1
        arr_type = c_int * arr_len

        arr = []
        for kv_pair in self.items():
            arr.extend(kv_pair)
        arr.append(Attribs.NONE)

        return arr_type(*arr)

    def get(self, index):
        '''Get the value of an attribute, or its default if it is unset.'''
        val = self[index]
        if val is None:
            return Attribs.details[value].default
        else:
            return val

    def items(self):
        '''Iterate over key-value pairs of attributes.'''
        return self._items.items()
