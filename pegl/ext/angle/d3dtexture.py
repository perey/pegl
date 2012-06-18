#!/usr/bin/env python3

'''ANGLE Direct3D texture handle extensions for EGL.

This module implements two related ANGLE extensions. The first extension
provides a way to obtain a pointer to a Direct3D texture that underlies
an EGL surface, thus allowing shared access to the rendering surface
from other APIs.

The second extension allows using a Direct3D texture as a client buffer
when creating a pbuffer surface. The presence of two extensions in the
one module presents no compatibility problems, since this second
extension depends on the first, and in fact it introduces absolutely no
code not present in the first extension's wrapper. All the extension
does is permit the use of a value from the first extension as a client
buffer type.

http://www.khronos.org/registry/egl/extensions/ANGLE/EGL_ANGLE_surface_d3d_texture_2d_share_handle.txt
http://www.khronos.org/registry/egl/extensions/ANGLE/EGL_ANGLE_d3d_share_handle_client_buffer.txt

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

# Local imports.
from . import surfacepointer
from ...surface import Surface

# Symbolic constant for the D3D handle attribute. To construct a PbufferSurface
# from a Direct3D client buffer, pass this value as the buffer_type parameter
# to the PbufferSurface constructor.
D3D_TEXTURE_2D_SHARE_HANDLE = 0x3200

# Add a property to the Surface class for querying this attribute.
def d3d_texture_2d(self):
    '''Get a handle for the Direct3D 2D texture of this surface.'''
    return self._attr_ptr(D3D_TEXTURE_2D_SHARE_HANDLE)
Surface.d3d_texture_2d = d3d_texture_2d
