#!/usr/bin/env python3

'''EGL extension support.'''

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

__all__ = (# Registered vendor extensions.
           'angle', 'hi', 'img', 'khr', 'mesa', 'nv',
           # Registered cross-vendor (EXT) extensions.
           'robustness',
           # Unregistered extensions.
           'nok', 'wl',
           # Stuff defined here.
           'load_ext')

# Standard library imports.
from ctypes import CFUNCTYPE

# Local imports.
from .. import native

# TODO: Have a way of checking for extension availability before importing an
# extension module. This function is part of it, but it needs to have the name
# string of the extension -- which I can't just put in the matching module,
# because I don't want to import it!
def is_available(display, extname):
    '''Check the availability of an extension.

    Keyword arguments:
        display -- A Display instance running the EGL implementation for
            which extension availability is being queried.
        extname -- The name string of the extension.

    '''
    return (extname in display.extensions)

def load_ext(fname, return_type, arg_types, check_errors=True, **kwargs):
    '''Load an extension function at runtime.

    Keyword arguments:
        fname -- The name of the extension function, given as a byte
            string.
        return_type -- The ctypes type that the extension function
            returns.
        arg_types -- A sequence listing the ctypes types of the
            arguments to the extension function.
        check_errors -- Whether to wrap the loaded function with EGL
            error checking. The default is True.
        Further keyword arguments are passed to the error_check function
        if check_errors was True; otherwise they are ignored.

    '''
    void_func = native.eglGetProcAddress(fname)
    if void_func is None:
        # Extension not available.
        raise ImportError('extension {} not available'.format(fname.decode()))
    typed_func = CFUNCTYPE(return_type, *arg_types)(void_func)
    if check_errors:
        return native.error_check(typed_func, **kwargs)
    else:
        return typed_func
