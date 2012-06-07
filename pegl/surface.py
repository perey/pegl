#!/usr/bin/env python3

'''EGL surface management.'''

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
from ctypes import c_int

# Local imports.
from . import egl, error_check, make_int_p, NONE
from .attribs import (Attribs, AttribList, SurfaceAttribs)

class Surface:
    '''Abstract base class for the available surface types.

    Although this class is not intended for instantiation, all
    subclasses share these instance attributes in common.

    Instance attributes:
        shandle -- The foreign object handle for this surface.
        display -- The EGL display to which this surface belongs, an
            instance of Display.
        config -- The configuration with which this surface was created,
            an instance of Config.
        attribs -- The attributes with which this surface was created,
            an instance of Attribs.

    '''
    def __init__(self, display, config, attribs):
        '''Set common surface parameters.

        Subclasses will need to call the foreign function that actually
        creates their particular surface type, and then set shandle to
        the returned result.

        Keyword arguments:
            display, config, attribs -- As the instance attributes.

        '''
        self.shandle = None
        self.display = display
        self.config = config
        self.attribs = attribs

    def __del__(self):
        '''Delete this surface.'''
        error_check(egl.eglDestroySurface)(self.display, self)

    @property
    def _as_parameter(self):
        '''Get the surface handle for use by foreign functions.'''
        return self.shandle


class PbufferSurface:
    pass


class PixmapSurface:
    pass


class WindowSurface:
    pass
