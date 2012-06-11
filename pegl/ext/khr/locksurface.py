#!/usr/bin/env python3

'''Khronos lock-surface extension for EGL.

Surface locking is defined in a pair of extension specifications. This
wrapper has been designed for version 18 of the first extension, and
version 2 of the second.

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
from ...attribs import Attribs, AttribList, BitMask, Details, DONT_CARE
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
new_defaults = (None, 0, BitmapOrigins(), 0, 0, 0, 0, 0)

for args in zip(new_attribs, new_values, new_types, new_defaults):
    SurfaceAttribs.extend(*args)

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
