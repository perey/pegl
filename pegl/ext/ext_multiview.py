#!/usr/bin/env python3

'''Cross-vendor multiview window surface extension for EGL.

http://www.khronos.org/registry/egl/extensions/EXT/EGL_EXT_multiview_window.txt

'''
# Copyright © 2013 Tim Pederick.
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
from ctypes import c_int

# Local imports.
from ...attribs.surface import SurfaceAttribs

# This extension defines just one new attribute.
SurfaceAttribs.extend('MULTIVIEW_VIEW_COUNT', 0x3134, c_int, 1)

# TODO: Convenient querying of this attribute?
