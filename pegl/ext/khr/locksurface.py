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
from .. import is_available, load_ext
from ...attribs import (Attribs, AttribList, BitMask, Details, DONT_CARE,
                        UNKNOWN_VALUE)
from ...attribs.config import ConfigAttribs, SurfaceTypes
from ...attribs.surface import SurfaceAttribs
from ...native import ebool, display, surface, attr_list
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
new_defaults = (None, UNKNOWN_VALUE, BitmapOrigins(), UNKNOWN_VALUE,
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
    if type(attribs) is not AttribList:
        attribs = AttribList(LockAttribs, attribs)
    native_lock(self.display, self, attribs)
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
    if bitmap_format == MatchFormats.RGB_565_EXACT:
        return 'RGB 565'
    elif bitmap_format == MatchFormats.RGBA_8888_EXACT:
        return 'RGBA 8888'
    else:
        raise ValueError('EGL supplied an unknown format')
Config.match_format = property(match_format)

# New Surface properties, for querying the new attributes in SurfaceAttribs.
def bitmap_pixel_size(self):
    '''Get the bit size of pixels in the mapped buffer.

    The lock_surface2 extension provides a simple query attribute for
    this. Support is also provided for the more involved method from
    the original lock_surface extension, if only that is available.

    '''
    if is_available(self.display, 'EGL_KHR_lock_surface2'):
        # Easy!
        return self._attr(SurfaceAttribs.BITMAP_PIXEL_SIZE)
    else:
        # Hard! "The size of a pixel in the mapped buffer, in bytes, can
        # be determined by querying the EGL_BUFFER_SIZE attribute of the
        # EGLConfig, rounding up to the nearest multiple of 8, and
        # converting from bits to bytes."
        BITS_PER_BYTE = 8
        bufsize = self.config._attr(ConfigAttribs.BUFFER_SIZE)
        bytesize = (bufsize // BITS_PER_BYTE) + 1
        return bytesize * BITS_PER_BYTE
Surface.bitmap_pixel_size = property(bitmap_pixel_size)

# TODO: The other Surface properties.
