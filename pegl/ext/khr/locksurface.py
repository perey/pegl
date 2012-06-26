#!/usr/bin/env python3

'''Khronos lock-surface extension for EGL.

Surface locking is defined in a pair of extension specifications. This
wrapper has been designed for version 2 of the second extension, which
claims backwards compatibility with the first extension.

http://www.khronos.org/registry/egl/extensions/KHR/EGL_KHR_lock_surface.txt
http://www.khronos.org/registry/egl/extensions/KHR/EGL_KHR_lock_surface2.txt

'''
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
from ctypes import c_int, c_void_p

# Local imports.
from .. import load_ext
from ...attribs import (Attribs, AttribList, BitMask, Details, DONT_CARE,
                        UNKNOWN_VALUE)
from ...attribs.config import ConfigAttribs, SurfaceTypes
from ...attribs.surface import SurfaceAttribs
from ...native import ebool, display, surface, attr_list
from ...config import Config
from ...surface import Surface

# Get handles of extension functions.
native_lock = load_ext(b'eglLockSurfaceKHR', ebool,
                       (display, surface, attr_list), fail_on=False)
native_unlock = load_ext(b'eglUnlockSurfaceKHR', ebool,
                         (display, surface), fail_on=False)

# New config attributes.
SurfaceTypes.extend(7, 'LOCK_SURFACE')
SurfaceTypes.extend(8, 'OPTIMAL_FORMAT')

MatchFormats = namedtuple('MatchFormat_tuple',
                          ('RGB_565_EXACT', 'RGB_565',
                           'RGBA_8888_EXACT', 'RGBA_8888')
                          )(0x30C0, 0x30C1, 0x30C2, 0x30C3)
ConfigAttribs.extend('MATCH_FORMAT', 0x3043, MatchFormats, DONT_CARE)

# New surface attributes.
BitmapOrigins = namedtuple('BitmapOrigins_tuple',
                           ('LOWER_LEFT', 'UPPER_RIGHT')
                           )(0x30CE, 0x30CF)

new_attribs = ('BITMAP_POINTER', 'BITMAP_PITCH', 'BITMAP_ORIGIN',
               'BITMAP_PIXEL_RED_OFFSET', 'BITMAP_PIXEL_GREEN_OFFSET',
               'BITMAP_PIXEL_BLUE_OFFSET', 'BITMAP_PIXEL_ALPHA_OFFSET',
               'BITMAP_PIXEL_LUMINANCE_OFFSET')
new_values = range(0x30C6, 0x30CE)
new_types = (c_void_p, c_int, BitmapOrigins, c_int, c_int, c_int, c_int, c_int)
new_defaults = (None, UNKNOWN_VALUE, BitmapOrigins.LOWER_LEFT, UNKNOWN_VALUE,
                UNKNOWN_VALUE, UNKNOWN_VALUE, UNKNOWN_VALUE, UNKNOWN_VALUE)
for args in zip(new_attribs, new_values, new_types, new_defaults):
    SurfaceAttribs.extend(*args)

SurfaceAttribs.extend('BITMAP_PIXEL_SIZE', 0x3110, # From lock_surface2.
                      c_int, UNKNOWN_VALUE)

# Brand new attributes for surface locks.
class LockUsageHints(BitMask):
    '''A bit mask representing usage hints for locked surfaces.

    Making use of these hints to optimise access can increase the
    performance of operations on buffers mapped from a locked surface.

    '''
    bit_names = ['READ_SURFACE', 'WRITE_SURFACE']


class LockAttribs(Attribs):
    '''The set of EGL extension attributes applicable to surface locks.

    Class attributes:
        details -- As per the superclass, Attribs.
        Additionally, symbolic constants for all the known attributes
        are available as class attributes. Their names are the same as
        in the extension specification, except without the EGL_ prefix
        and _KHR suffix.

    '''
    MAP_PRESERVE_PIXELS, LOCK_USAGE_HINT = 0x30C4, 0x30C5

    details = {MAP_PRESERVE_PIXELS: Details('Whether or not to initially fill '
                                            'the mapped buffer from the color '
                                            'buffer of a locked surface', bool,
                                            False),
               LOCK_USAGE_HINT: Details('Hints on intended use (read and/or '
                                        'write) of the mapped buffer',
                                        LockUsageHints,
                                        LockUsageHints(READ_SURFACE=1,
                                                       WRITE_SURFACE=1))}

# Lock and unlock functions. As these will be added to the Surface class as
# instance methods, the self argument refers to the surface.
def _lock(self, attribs):
    '''Lock the surface.

    Keyword arguments:
        attribs -- The locking attributes to set.

    '''
    native_lock(self.display, self,
                attribs if isinstance(attribs, AttribList) else
                AttribList(LockAttribs, attribs))
Surface.lock = _lock

def _unlock(self):
    '''Unlock the surface.'''
    native_unlock(self.display, self)
Surface.unlock = _unlock

# New Config property, for querying the new attribute in ConfigAttribs.
def match_format(self):
    '''Get the mapped buffer format supported by this configuration.

    Returns:
        A string specifying either 'RGB 565' or 'RGBA 8888'.

    '''
    bitmap_format = self._attr(ConfigAttribs.MATCH_FORMAT)
    # The two formats that are not "_EXACT" can be supplied when requesting a
    # Config, but cannot be returned when querying its properties.
    if bitmap_format == MatchFormats.RGB_565_EXACT:
        return 'RGB 565'
    elif bitmap_format == MatchFormats.RGBA_8888_EXACT:
        return 'RGBA 8888'
    else:
        raise ValueError('EGL returned an unknown format')
Config.match_format = property(match_format)

# New Surface properties, for querying the new attributes in SurfaceAttribs.
def bitmap_pointer(self):
    '''Get the native pointer to the mapped buffer.'''
    return self._attr(SurfaceAttribs.BITMAP_POINTER)
Surface.bitmap_pointer = property(bitmap_pointer)

def bitmap_pitch(self):
    '''Get the pitch (bytes between rows) of the mapped buffer.'''
    return self._attr(SurfaceAttribs.BITMAP_PITCH)
Surface.bitmap_pitch = property(bitmap_pitch)

def bitmap_origin(self):
    '''Get the mapped buffer corner that is the coordinate origin.

    Returns:
        A value from BitmapOrigins, either BitmapOrigins.LOWER_LEFT or
        BitmapOrigins.UPPER_RIGHT.

    '''
    return self._attr(SurfaceAttribs.BITMAP_ORIGIN)
Surface.bitmap_origin = property(bitmap_origin)

def bitmap_component_offsets(self):
    '''Get the offset of each color component in the mapped buffer.

    Offsets are the first (least significant) bit position of the
    contiguous range of bits within each pixel that holds the value of
    each color component.

    A color component that does not exist (e.g. luminance in an RGBA
    buffer) has an offset of zero. If a component exists but is not in a
    contiguous range of bits, the offset is None.

    Returns:
        A mapping object with 'red', 'green', 'blue', 'alpha' and
        'luminance' as its keys, and None or an integer for the offset
        values.

    '''
    components = ('red', 'green', 'blue', 'alpha', 'luminance')

    return dict((comp.lower(),
                 self._attr(getattr(SurfaceAttribs,
                                    'BITMAP_PIXEL_{}_OFFSET'.format(comp))))
                for comp in components)
Surface.bitmap_component_offsets = property(bitmap_component_offsets)

def bitmap_pixel_size(self):
    '''Get the bit size of pixels in the mapped buffer.

    The lock_surface2 extension provides a simple query attribute for
    this. If that is not available, the size of a pixel in the color
    buffer is given (which may include some "unused" bits).

    '''
    if 'EGL_KHR_lock_surface2' in self.display.extensions:
        # Easy!
        return self._attr(SurfaceAttribs.BITMAP_PIXEL_SIZE)
    else:
        # We fall back on the buffer size.
        return self.config._attr(ConfigAttribs.BUFFER_SIZE)
Surface.bitmap_pixel_size = property(bitmap_pixel_size)
