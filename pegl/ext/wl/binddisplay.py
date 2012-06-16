#!/usr/bin/env python3

'''Wayland display binding for EGL.

While the specification of this extension has not been submitted to
Khronos, it is widely available through the Mesa library.

http://cgit.freedesktop.org/mesa/mesa/tree/docs/WL_bind_wayland_display.spec

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
from ctypes import c_void_p

# Local imports.
from .. import load_ext
from ..khr.image import Image
from ...display import Display
from ...native import ebool, display

# Extension type.
wl_display = c_void_p

# Get handles of extension functions.
native_bind = load_ext(b'eglBindWaylandDisplayWL', ebool,
                       (display, wl_display), fail_on=False)
native_unbind = load_ext(b'eglUnbindWaylandDisplayWL', ebool,
                         (display, wl_display), fail_on=False)

# Extend the Display class with methods to bind and unbind Wayland displays.
def bind_wayland_display(self, wl_display):
    '''Bind a Wayland display handle to this EGL display.

    Keyword arguments:
        wl_display -- The foreign handle of the Wayland display to bind.

    '''
    self.wl_display = wl_display
    native_bind(self, wl_display)
Display.bind_wayland_display = bind_wayland_display

# TODO: Add a cleanup hook to Display to call unbind_... upon deletion.
def unbind_wayland_display(self, wl_display=None):
    '''Unbind a Wayland display handle from this EGL display.

    Keyword arguments:
        wl_display -- The foreign handle of the Wayland display to bind.
            This can (and generally should) be omitted, in which case
            the last display handle bound will be unbound.

    '''
    native_unbind(self, self.wl_display if wl_display is None else wl_display)
Display.unbind_wayland_display = unbind_wayland_display

# New image target.
Image.extend('EGL_WL_bind_wayland_display', {'WAYLAND_BUFFER': 0x31D5})
