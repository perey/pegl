#!/usr/bin/env python3

'''EGL Khronos (KHR) extension support.'''

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

__all__ = ('extensions', 'glimage', 'locksurface', 'sync', 'vgimage')

extensions = {'EGL_KHR_create_context': 'context',
              'EGL_KHR_gl_texture_2D_image': 'glimage',
              'EGL_KHR_gl_texture_cubemap_image': 'glimage',
              'EGL_KHR_gl_texture_3D_image': 'glimage',
              'EGL_KHR_gl_renderbuffer_image': 'glimage',
              'EGL_KHR_fence_sync': 'sync',
              'EGL_KHR_image': 'image',
              'EGL_KHR_image_base': 'image',
              'EGL_KHR_image_pixmap': 'image',
              'EGL_KHR_lock_surface': 'locksurface',
              'EGL_KHR_lock_surface2': 'locksurface',
              'EGL_KHR_reusable_sync': 'sync',
              'EGL_KHR_stream': 'stream',
              'EGL_KHR_stream_consumer_gltexture': 'stream',
              # This extension requires absolutely no new code on the EGL side.
              'EGL_KHR_stream_producer_aldatalocator': 'stream',
              'EGL_KHR_stream_producer_eglsurface': 'streamsurface',
              'EGL_KHR_stream_fifo': 'fifostream',
              'EGL_KHR_vg_parent_image': 'vgimage'}
