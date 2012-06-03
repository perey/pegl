#!/usr/bin/env python3

'''EGL 1.4 display management.'''
# Standard library imports.
from ctypes import POINTER, c_int, c_void_p

# Local imports.
from . import egl, error_check

int_p = POINTER(c_int)

# EGL constants.
CLIENT_APIS, EXTENSIONS, VENDOR, VERSION = 0x308D, 0x3055, 0x3053, 0x3054
DEFAULT_DISPLAY, NO_DISPLAY = c_void_p(0), c_void_p(0)

@error_check
def current_display():
    '''Get the current display.'''
    return Display(dhandle=egl.eglGetCurrentDisplay())

class Display:
    '''An EGL display.'''
    def __init__(self, dhandle=None, native_id=None):
        '''Get a display, either a specified one or the default one.'''
        self.dhandle = (dhandle if dhandle is not None else
                        egl.eglGetDisplay(DEFAULT_DISPLAY
                                          if native_id is None else
                                          native_id))

    def __eq__(self, other):
        '''Compare two displays for equivalence.'''
        try:
            return self.dhandle == other.dhandle
        except AttributeError:
            # The other object doesn't have a dhandle.
            return False

    @property
    def _as_parameter_(self):
        '''Get the display as a foreign function parameter.'''
        return self.dhandle

    @error_check
    def _query(self, target):
        '''Query the string value of an EGL instance parameter.'''
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
def init(display=None, native_id=None):
    '''Initialise EGL for a given display.'''
    if display is None:
        display = Display(native_id)
    major, minor = int_p(), int_p()
    major.contents, minor.contents = c_int(0), c_int(0)
    egl.eglInitialize(display, major, minor)
    return (major[0], minor[0])
