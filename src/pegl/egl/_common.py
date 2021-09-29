#!/usr/bin/env python3

"""Common EGL library loading objects for Pegl."""

# Copyright © 2012, 2013, 2020 Tim Pederick.
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
#
# This file is based on the header file egl.h, which carries the following
# copyright statement and licensing information:
#
#     Copyright (c) 2013-2017 The Khronos Group Inc.
#
#     Permission is hereby granted, free of charge, to any person obtaining a
#     copy of this software and/or associated documentation files (the
#     "Materials"), to deal in the Materials without restriction, including
#     without limitation the rights to use, copy, modify, merge, publish,
#     distribute, sublicense, and/or sell copies of the Materials, and to
#     permit persons to whom the Materials are furnished to do so, subject to
#     the following conditions:
#
#     The above copyright notice and this permission notice shall be included
#     in all copies or substantial portions of the Materials.
#
#     THE MATERIALS ARE PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#     EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#     MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#     IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
#     CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#     TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#     MATERIALS OR THE USE OR OTHER DEALINGS IN THE MATERIALS.

__all__ = ['_load_function', 'Arg', 'EGLBoolean', 'EGLConfig', 'EGLConfig_p',
           'EGLContext', 'EGLDisplay', 'EGLNativeDisplayType',
           'EGLNativePixmapType', 'EGLNativeWindowType', 'EGLSurface',
           'EGLint', 'EGLint_p', 'EGLClientBuffer', 'EGLenum', 'EGLAttrib',
           'EGLAttrib_p', 'EGLImage', 'EGLSync', 'EGLTime', 'eglGetError',
           'eglGetProcAddress']

# Standard library imports.
import ctypes
import ctypes.util
from enum import IntFlag
import logging
from pathlib import Path
import sys

# Local imports.
from ..errors import KNOWN_ERRORS, EGLError, EGL_SUCCESS

# Set up logging with the module name.
logger = logging.getLogger(__name__)

# Dynamic library loading.
known_names = [
    'libEGL',     # ANGLE, Mesa, ARM Mali, probably others...
    'libOpenVG',  # Khronos reference OpenVG implementation
    'libbrcmEGL', # Broadcom (older Raspberry Pi)
]
if sys.platform == 'win32':
    # MS Windows DLLs should be placed in the lib directory.
    libdir = Path(__file__).parent / 'lib'
    for name in known_names:
        egl_path = Path(__file__).parent / 'lib' / (name + '.dll')
        if egl_path.exists():
            break
    else:
        raise ImportError('could not find EGL library')

    _lib = ctypes.CDLL(str(egl_path))

    # Some implementations (like ANGLE's) need other DLLs to be loaded, and
    # will try loading them from the current working directory, not the lib
    # directory, if we don't load them ourselves.
    for other_dll in libdir.glob('*.dll'):
        if other_dll != egl_path:
            _ = ctypes.CDLL(str(other_dll))

else:
    # Shared libraries on other systems can use the system loader.
    for name in known_names:
        # Strip a "lib-" prefix.
        # TODO: Would it make more sense to leave this off to begin with?
        if name.startswith('lib'):
            name = name[3:]
        found_lib = ctypes.util.find_library(name)
        if found_lib is not None:
            break
    else:
        raise ImportError('could not find EGL library')

    _lib = ctypes.CDLL(found_lib)

    # TODO: Looks like some implementations (like Broadcom's) need the same
    # load-other-libraries behaviour as noted above for Windows. How do I
    # implement that?


# Type definitions. These are available regardless of what EGL version is
# supported by the library.
# EGL 1.0
EGLBoolean           = ctypes.c_bool
EGLConfig            = ctypes.c_void_p
EGLConfig_p          = ctypes.POINTER(EGLConfig)
EGLContext           = ctypes.c_void_p
EGLDisplay           = ctypes.c_void_p
EGLNativeDisplayType = ctypes.c_void_p
EGLNativePixmapType  = ctypes.c_void_p
EGLNativeWindowType  = ctypes.c_void_p
EGLSurface           = ctypes.c_void_p
EGLint               = ctypes.c_int32
EGLint_p             = ctypes.POINTER(EGLint)
# EGL 1.2
EGLClientBuffer      = ctypes.c_void_p
EGLenum              = ctypes.c_uint
# EGL 1.5
EGLAttrib            = ctypes.c_ssize_t # Substitute for intptr_t
EGLAttrib_p          = ctypes.POINTER(EGLAttrib)
EGLImage             = ctypes.c_void_p
EGLSync              = ctypes.c_void_p
EGLTime              = ctypes.c_uint64  # § 2.1.1: "a 64-bit unsigned integer"

# Set up error handling.
eglGetError = _lib.eglGetError
eglGetError.argtypes = []
eglGetError.restype = EGLint

# Set up function loading.
eglGetProcAddress = _lib.eglGetProcAddress
eglGetProcAddress.argtypes = [ctypes.c_char_p]
eglGetProcAddress.restype = ctypes.c_void_p

class Arg(IntFlag):
    """Direction flags for ctypes 'paramflags'"""
    IN = 1
    OUT = 2
    INOUT = IN | OUT
    IN_DEFAULT0 = 4

def _load_function(func_name, restype, *args, **kwargs):
    """Load an EGL function.

    Arguments to the function may be specified as sequences comprising
    at least the first of the following items. If multiple items are
    given, all of them up to that point must be given.

    * The type of the argument
    * The direction of the argument (a value from the Arg enumeration)
    * The name of the argument (a string)
    * The default value of the argument

    Keyword arguments:
        func_name -- The name of the function to load.
        restype -- The return type of the function.
        args -- The arguments to the function, specified as described
            above.
        error_on -- A return value that signals (or may signal) that the
            function encountered an error.

    """
    # Construct the function prototype.
    argtypes = []
    paramflags = []
    for arg in args:
        argtype, *paramflag = arg
        argtypes.append(argtype)
        paramflags.append(tuple(paramflag))
    prototype = ctypes.CFUNCTYPE(restype, *argtypes)

    # Try loading the function by name.
    try:
        fn = prototype((func_name.encode(), _lib), tuple(paramflags))
    except AttributeError:
        # Failure! Try loading it by address instead.
        logger.debug('Failed to load %r by name, trying by address instead',
                     func_name)
        address = eglGetProcAddress(func_name.encode())
        fn = None if address is None else prototype(address)

    if fn is None:
        raise ImportError(f"EGL function '{func_name}' not found")

    try:
        error_on = kwargs['error_on']
    except KeyError:
        # No error checking defined.
        pass
    else:
        def error_check(result, func, args): # pylint: disable=unused-argument
            logger.debug('Called %r with args %r and got result %r',
                         func_name, args, result)
            if (result == error_on or (result is None and
                                       isinstance(error_on, ctypes.c_void_p) and
                                       error_on.value is None)):
                error_code = eglGetError()
                if error_code != EGL_SUCCESS:
                    raise KNOWN_ERRORS.get(error_code, EGLError)
            return args
        setattr(fn, 'errcheck', error_check)

    # Store the function name, for debugging.
    fn.name = func_name

    return fn
