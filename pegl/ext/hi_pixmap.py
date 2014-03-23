#!/usr/bin/env python3

'''HI Corp. client pixmap extension for EGL.

This extension allows pixmap surfaces to use a specifically allocated
block of memory for a color buffer.

http://www.khronos.org/registry/egl/extensions/HI/EGL_HI_clientpixmap.txt

'''
# Copyright © 2014 Tim Pederick.
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
from ctypes import POINTER, Structure, c_int, c_void_p

# Local imports.
from . import load_ext
from ..attribs.surface import SurfaceAttribs
from ..surface import Surface
from ..native import c_config, c_display, c_surface

# New extension type.
class ClientPixmap(Structure):
    _fields_ = [('pData', c_void_p),
                ('iWidth', c_int),
                ('iHeight', c_int),
                ('iStride', c_int)]
    # Pythonically named properties for the fields.
    @property
    def data(self):
        return self.pData
    @data.setter
    def data(self, ptr):
        self.pData = ptr

    @property
    def width(self):
        return self.iWidth
    @width.setter
    def width(self, w):
        self.iWidth = w

    @property
    def height(self):
        return self.iHeight
    @height.setter
    def height(self, h):
        self.iHeight = h

    @property
    def stride(self):
        return self.iStride
    @stride.setter
    def stride(self, s):
        self.iStride = s
c_pixmap_p = POINTER(ClientPixmap)

# Get the handle of the new extension function.
native_createpixmapsurface = load_ext(b'eglCreatePixmapSurfaceHI', c_surface,
                                      (c_display, c_config, c_pixmap_p))

# New Surface attribute.
SurfaceAttribs.extend('CLIENT_PIXMAP_POINTER', 0x8F74, c_void_p, None)

# New Surface subclass.
def ClientPixmapSurface(Surface):
    '''Represents a surface that renders to a pixmap in a memory buffer.

    Instance attributes:
        shandle, display, config, attribs -- Inherited from Surface.

    '''
    def __init__(self, display, config, pixmap):
        '''Create the pixmap surface.

        Only the following attributes from SurfaceAttribs are accepted
        when creating a pixmap surface:
            * VG_COLORSPACE and VG_ALPHA_FORMAT (only used by OpenVG)

        Keyword arguments:
            display, config -- As the instance attributes.
            pixmap -- The buffer to render to. An instance of
                ClientPixmap.

        '''
        super().__init__(display, config, attribs=None)
        self.shandle = native_createpixmapsurface(self.display, self.config,
                                                  pixmap)


# Write-only property for setting the pixmap pointer.
def set_pixmap_pointer(self, ptr):
    '''Set the native pointer to the memory buffer.'''
    self._setattr(SurfaceAttribs.CLIENT_PIXMAP_POINTER, ptr)
ClientPixmapSurface.pixmap_pointer = property(fset=set_pixmap_pointer)
