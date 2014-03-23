#!/usr/bin/env python3

'''Mesa GBM platform support extension for EGL.

This extension adds GBM as an explicitly supportable native platform.

http://www.khronos.org/registry/egl/extensions/MESA/EGL_MESA_platform_gbm.txt

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
class GBMDisplay(PlatformDisplay):
    '''An EGL display mapped to a GBM device.

    Class attributes:
        platform -- The numeric identifier for the GBM platform.

    Instance attributes:
        dhandle, client_apis, extensions, swap_interval, vendor,
        version, attribs -- Inherited from PlatformDisplay.

    '''
    platform = 0x31D7 # EGL_PLATFORM_GBM_MESA

    def __init__(self, gbm_device, delay_init=False):
        '''Get a display for a GBM device.

        Keyword arguments:
            gbm_device -- The identifier for the GBM device.
            delay_init -- As the superclass constructor.

        '''
        super().__init__(native_id=gbm_device, delay_init=delay_init)
