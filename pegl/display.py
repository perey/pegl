#!/usr/bin/env python3

'''EGL 1.4 display management.'''

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
from ctypes import c_void_p

# Local imports.
from . import egl, error_check, make_int_p

# EGL constants.
CLIENT_APIS, EXTENSIONS, VENDOR, VERSION = 0x308D, 0x3055, 0x3053, 0x3054
DEFAULT_DISPLAY, NO_DISPLAY = c_void_p(0), c_void_p(0)

@error_check
def current_display():
    '''Get the current EGL display.'''
    return Display(dhandle=egl.eglGetCurrentDisplay())

class Display:
    '''An EGL display.

    In EGL, a display is not only a representation of a (physical or
    virtual) display device; it is also the overall context of all EGL
    operations (although "context" also has a different meaning in EGL).
    As such, details of the EGL implementation are accessed from a
    Display instance.

    Instance attributes:
        dhandle -- The foreign object handle for this display.
        client_apis -- A string describing the client APIs supported
            (such as OpenGL, OpenGL_ES, and OpenVG). Although the value
            is implementation-defined, it will likely be a list of API
            names delimited by spaces.
        extensions -- A string describing the EGL extensions supported.
            Again, this is likely to be a space-delimited list.
        vendor -- The vendor string for this EGL implementation.
        version -- A string describing the implementation version.

    '''
    def __init__(self, dhandle=None, native_id=None, delay_init=False):
        '''Get a display, either a specified one or the default one.

        Keyword arguments:
            dhandle -- As the instance attribute. If omitted, the
                native_id is used instead.
            native_id -- An identifier for a platform-native display.
                This is ignored if dhandle is supplied. If both are
                omitted, the EGL default display is requested.
            delay_init -- If True, the display's initialize() method
                will not be called automatically. This should be done
                by the application before doing any EGL operations.

        '''
        self.dhandle = (dhandle if dhandle is not None else
                        egl.eglGetDisplay(DEFAULT_DISPLAY
                                          if native_id is None else
                                          native_id))
        if not delay_init:
            self.initialize()

    def __eq__(self, other):
        '''Compare two displays for equivalence.

        Two displays are considered equal if they have the same foreign
        function reference (i.e. the dhandle attribute).

        '''
        try:
            return self.dhandle == other.dhandle
        except AttributeError:
            # The other object doesn't have a dhandle.
            return False

    @property
    def _as_parameter_(self):
        '''Get the display reference for use by foreign functions.'''
        return self.dhandle

    @error_check
    def _query(self, target):
        '''Query an EGL instance parameter.

        Keyword arguments:
            target -- A value identifying the parameter sought. This
                should be a symbolic constant from those defined in this
                module (CLIENT_APIS, EXTENSIONS, VENDOR, or VERSION).
        Returns:
            A string value for the EGL parameter requested.

        '''
        # TODO: The codec chosen is a bit arbitrary and might be best left off.
        # Client applications can just use the bytes or decode them themselves.
        return egl.eglQueryString(self, target).decode('ISO-8859-1')

    @property
    def client_apis(self):
        '''Get the client APIs available on this EGL instance.'''
        return self._query(CLIENT_APIS)

    @property
    def extensions(self):
        '''Get the extensions available on this EGL instance.'''
        return self._query(EXTENSIONS)

    @property
    def vendor(self):
        '''Get the vendor string for this EGL instance.'''
        return self._query(VENDOR)

    @property
    def version(self):
        '''Get the EGL version of this EGL instance.'''
        return self._query(VERSION)

    @error_check
    def initialize(self):
        '''Initialize EGL for this display.

        Returns:
            An EGL version number, in (major, minor) format.

        '''
        # Create and initialize the return pointers.
        major, minor = make_int_p(), make_int_p()

        egl.eglInitialize(self, major, minor)
        return (major[0], minor[0])
