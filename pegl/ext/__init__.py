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
           'extensions', 'load_ext')

# Standard library imports.
from ctypes import CFUNCTYPE

# Local imports.
from .. import native

# Extensions in the EXT namespace.
extensions = {'EGL_EXT_create_context_robustness': 'robustness'}

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
        raise ImportError("extension function '{}' not "
                          "available".format(fname.decode()))
    # Cast the pointer to a function pointer with the correct types.
    typed_func = CFUNCTYPE(return_type, *arg_types)(void_func)
    if check_errors:
        return native.error_check(typed_func, **kwargs)
    else:
        return typed_func
