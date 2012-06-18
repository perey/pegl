#!/usr/bin/env python3

'''Support for EGL extensions from ANGLE.

ANGLE is the Almost Native Graphics Layer Engine, a layer implementing
OpenGL ES over DirectX to allow Microsoft Windows users to run WebGL
applications.

http://code.google.com/p/angleproject/

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

__all__ = ('extensions', 'd3dtexture', 'surfacepointer')

extensions = {'EGL_ANGLE_query_surface_pointer': 'surfacepointer',
              'EGL_ANGLE_d3d_share_handle_client_buffer': 'd3dtexture',
              'EGL_ANGLE_surface_d3d_texture_2d_share_handle': 'd3dtexture'}
