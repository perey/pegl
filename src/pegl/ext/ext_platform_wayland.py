#!/usr/bin/env python3

'''Cross-vendor Wayland platform support extension for EGL.

This extension adds the Wayland display server as an explicitly
supportable native platform.

http://www.khronos.org/registry/egl/extensions/EXT/EGL_EXT_platform_wayland.txt

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

# Local imports.
from .ext_platform import PlatformDisplay

# New PlatformDisplay subclass.
class WaylandDisplay(PlatformDisplay):
    '''An EGL display mapped to a Wayland display.

    Class attributes:
        platform -- The numeric identifier for the X11 platform.

    Instance attributes:
        dhandle, client_apis, extensions, swap_interval, vendor,
        version, attribs -- Inherited from PlatformDisplay.

    '''
    platform = 0x31D8 # EGL_PLATFORM_WAYLAND_EXT

    def __init__(self, wl_display=None, delay_init=False):
        '''Get a display for a Wayland display.

        Keyword arguments:
            wl_display -- The native identifier for the Wayland display.
                If omitted, the Wayland default is requested.
            delay_init -- As the superclass constructor.

        '''
        super().__init__(native_id=wl_display, delay_init=delay_init)
