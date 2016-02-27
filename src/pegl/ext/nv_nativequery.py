#!/usr/bin/env python3

'''NVIDIA native query extension for EGL.

This extension provides a means of getting the native display, window,
or pixmap corresponding to an EGL display, window surface, or pixmap
surface, respectively.

http://www.khronos.org/registry/egl/extensions/NV/EGL_NV_native_query.txt

'''
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

# Standard library imports.
from ctypes import POINTER

# Local imports.
from . import load_ext
from ..native import (c_ibool, c_display, c_surface, c_native_display,
                      c_native_pixmap, c_native_window)
from ..display import Display
from ..surface import PixmapSurface, WindowSurface

# Extension type definitions.
c_display_p = POINTER(c_native_display)
c_pixmap_p = POINTER(c_native_pixmap)
c_window_p = POINTER(c_native_window)

# Get handles for extension functions.
native_query_display = load_ext(b'eglQueryNativeDisplayNV', c_ibool,
                                (c_display, c_display_p), fail_on=False)
native_query_pixmap = load_ext(b'eglQueryNativePixmapNV', c_ibool,
                               (c_display, c_surface, c_pixmap_p),
                               fail_on=False)
native_query_window = load_ext(b'eglQueryNativeWindowNV', c_ibool,
                               (c_display, c_surface, c_window_p),
                               fail_on=False)

# Add properties for querying these to the relevant classes.
def native_display(self):
    '''Get the native display associated with this EGL display.'''
    # Create the pointer.
    dhandle = c_display_p(None)

    # Call the native function.
    native_query_display(self, dhandle)

    # Dereference the pointer.
    return dhandle.contents
Display.native_display = property(native_display)

def native_pixmap(self):
    '''Get the native pixmap associated with this surface.'''
    # Create the pointer.
    phandle = c_pixmap_p(None)

    # Call the native function.
    native_query_pixmap(self, phandle)

    # Dereference the pointer.
    return phandle.contents
PixmapSurface.native_pixmap = property(native_pixmap)

def native_window(self):
    '''Get the native window associated with this surface.'''
    # Create the pointer.
    whandle = c_window_p(None)

    # Call the native function.
    native_query_window(self, whandle)

    # Dereference the pointer.
    return whandle.contents
WindowSurface.native_window = property(native_window)
