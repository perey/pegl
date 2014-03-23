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
from ..attribs.context import ContextAttribs
from ..attribs.surface import SurfaceAttribs
from ..context import Context
from ..surface import Surface

# This extension defines just one new attribute, but it applies to both
# surfaces and contexts.
MULTIVIEW_VIEW_COUNT = 0x3134
ContextAttribs.extend('MULTIVIEW_VIEW_COUNT', MULTIVIEW_VIEW_COUNT, c_int, 1)
SurfaceAttribs.extend('MULTIVIEW_VIEW_COUNT', MULTIVIEW_VIEW_COUNT, c_int, 1)

# New Context property, for querying the new attribute in ContextAttribs.
# This attribute cannot be set except by creating a surface with the
# corresponding attribute.
def ctx_multiview_view_count(self):
    '''Get the number of multiview buffers created by this context.'''
    return self._attr(ContextAttribs.MULTIVIEW_VIEW_COUNT)
Context.multiview_view_count = property(ctx_multiview_view_count)

# New Surface property, for querying the new attribute in SurfaceAttribs.
# This attribute cannot be set except at surface creation.
def surf_multiview_view_count(self):
    '''Get the number of multiview buffers requested for this surface.'''
    return self._attr(SurfaceAttribs.MULTIVIEW_VIEW_COUNT)
Surface.multiview_view_count = property(surf_multiview_view_count)
