#!/usr/bin/env python3

'''Cross-vendor X11 platform support extension for EGL.

This extension adds X11 as an explicitly supportable native platform.

http://www.khronos.org/registry/egl/extensions/EXT/EGL_EXT_platform_x11.txt

'''
# Copyright © 2014 Tim Pederick.
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
from ctypes import c_int

# Local imports.
from .ext_platform import PlatformDisplay, DisplayAttribs
from ..attribs import AttribList

# New display attribute.
DisplayAttribs.extend('PLATFORM_X11_SCREEN', 0x31D6, c_int, None)

# New PlatformDisplay subclass.
class X11Display(PlatformDisplay):
    '''An EGL display mapped to an X11 screen.

    Class attributes:
        platform -- The numeric identifier for the X11 platform.

    Instance attributes:
        dhandle, client_apis, extensions, swap_interval, vendor,
        version, attribs -- Inherited from PlatformDisplay.

    '''
    platform = 0x31D5 # EGL_PLATFORM_X11_EXT

    def __init__(self, x11_display=None, x11_screen=None, delay_init=False):
        '''Get a display for an X11 display connection and screen.

        Keyword arguments:
            x11_display, x11_screen -- The identifiers for the X11
                display and screen, respectively. If omitted, the
                X11 defaults are requested.
            delay_init -- As the superclass constructor.

        '''
        super().__init__(native_id=x11_display,
                         attribs=AttribList(DisplayAttribs,
                                            {'PLATFORM_X11_SCREEN': x11_screen
                                             },
                         delay_init=delay_init)
