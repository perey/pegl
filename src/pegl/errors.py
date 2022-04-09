#!/usr/bin/env python3

"""EGL error definitions for Pegl."""

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

__all__ = ['EGLError', 'NotInitializedError', 'BadAccessError',
           'BadAllocError', 'BadAttributeError', 'BadConfigError',
           'BadContextError', 'BadCurrentSurfaceError', 'BadDisplayError',
           'BadMatchError', 'BadNativePixmapError', 'BadNativeWindowError',
           'BadParameterError', 'BadSurfaceError', 'ContextLostError']

# Error types.
# EGL 1.0
EGL_SUCCESS             = 0x3000
EGL_NOT_INITIALIZED     = 0x3001
EGL_BAD_ACCESS          = 0x3002
EGL_BAD_ALLOC           = 0x3003
EGL_BAD_ATTRIBUTE       = 0x3004
EGL_BAD_CONFIG          = 0x3005
EGL_BAD_CONTEXT         = 0x3006
EGL_BAD_CURRENT_SURFACE = 0x3007
EGL_BAD_DISPLAY         = 0x3008
EGL_BAD_MATCH           = 0x3009
EGL_BAD_NATIVE_PIXMAP   = 0x300A
EGL_BAD_NATIVE_WINDOW   = 0x300B
EGL_BAD_PARAMETER       = 0x300C
EGL_BAD_SURFACE         = 0x300D
# EGL 1.1
EGL_CONTEXT_LOST        = 0x300E

# pylint: disable=unnecessary-pass

class EGLError(Exception):
    """The base class for all EGL library errors."""
    pass

class NotInitializedError(EGLError):
    """The EGL display was not, or could not be initialized."""
    pass

class BadAccessError(EGLError):
    """An EGL resource could not be accessed."""
    pass

class BadAllocError(EGLError):
    """EGL could not allocated resources for an operation."""
    pass

class BadAttributeError(EGLError):
    """An unrecognized attribute or value was passed."""
    pass

class BadConfigError(EGLError):
    """The given EGL config is not valid."""
    pass

class BadContextError(EGLError):
    """The given EGL context is not valid."""
    pass

class BadCurrentSurfaceError(EGLError):
    """The current EGL in this thread is no longer valid."""
    pass

class BadDisplayError(EGLError):
    """The given EGL display is not valid."""
    pass

class BadMatchError(EGLError):
    """One or more inconsistent arguments were supplied."""
    pass

class BadNativePixmapError(EGLError):
    """The given native pixmap is not valid."""
    pass

class BadNativeWindowError(EGLError):
    """The given native window is not valid."""
    pass

class BadParameterError(EGLError):
    """One or more invalid parameter values were supplied."""
    pass

class BadSurfaceError(EGLError):
    """The given EGL surface is not valid for rendering."""
    pass

class ContextLostError(EGLError):
    """Contexts have been invalidated by a power management event."""
    pass

KNOWN_ERRORS = {EGL_NOT_INITIALIZED: NotInitializedError,
                EGL_BAD_ACCESS: BadAccessError,
                EGL_BAD_ALLOC: BadAllocError,
                EGL_BAD_ATTRIBUTE: BadAttributeError,
                EGL_BAD_CONFIG: BadConfigError,
                EGL_BAD_CONTEXT: BadContextError,
                EGL_BAD_CURRENT_SURFACE: BadCurrentSurfaceError,
                EGL_BAD_DISPLAY: BadDisplayError,
                EGL_BAD_MATCH: BadMatchError,
                EGL_BAD_NATIVE_PIXMAP: BadNativePixmapError,
                EGL_BAD_NATIVE_WINDOW: BadNativeWindowError,
                EGL_BAD_PARAMETER: BadParameterError,
                EGL_BAD_SURFACE: BadSurfaceError,
                EGL_CONTEXT_LOST: ContextLostError}
