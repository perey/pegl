#!/usr/bin/env python3

'''EGL surface management.'''

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
from collections import namedtuple
from ctypes import c_int

# Local imports.
from . import make_int_p, native
from .attribs import attr_convert, Attribs, AttribList
from .attribs.surface import SurfaceAttribs, RenderBufferTypes, VGAlphaFormats

# Symbolic constants--okay, just one constant. This is the sole buffer type
# accepted by EGL when creating a PbufferSurface from a client buffer.
OPENVG_IMAGE = 0x3096

class Surface:
    '''Abstract base class for the available surface types.

    Although this class is not intended for instantiation, all
    subclasses share these instance attributes in common.

    Instance attributes:
        shandle -- The foreign object handle for this surface.
        display -- The EGL display to which this surface belongs. An
            instance of Display.
        config -- The configuration with which this surface was created.
            An instance of Config.
        attribs -- The attributes with which this surface was created.
            An instance of AttribList.

    '''
    def __init__(self, display, config, attribs):
        '''Set common surface parameters.

        Subclasses will need to call the foreign function that actually
        creates their particular surface type, and then set shandle to
        the returned result.

        Keyword arguments:
            display, config, attribs -- As the instance attributes.

        '''
        self.shandle = None
        self.display = display
        self.config = config
        self.attribs = (attribs if isinstance(attribs, AttribList) else
                        AttribList(SurfaceAttribs, attribs))

    def __del__(self):
        '''Delete this surface.'''
        native.eglDestroySurface(self.display, self)

    def __eq__(self, other):
        '''Compare two surfaces for equivalence.

        Two surfaces are considered equal if they have the same foreign
        function reference (i.e. the shandle attribute).

        '''
        try:
            return self.shandle == other.shandle
        except AttributeError:
            # The other object doesn't have a shandle.
            return False

    @property
    def _as_parameter_(self):
        '''Get the surface handle for use by foreign functions.'''
        return self.shandle

    def _attr(self, attr):
        '''Get the value of a surface attribute.

        Keyword arguments:
            attr -- The identifier of the attribute requested.

        '''
        # Query the attribute, storing the result in a pointer.
        result = make_int_p()
        native.eglQuerySurface(self.display, self, attr, result)

        # Dereference the pointer and convert to an appropriate type.
        return attr_convert(attr, result.contents.value, SurfaceAttribs)

    def _setattr(self, attr, value):
        '''Set the value of a surface attribute.

        Keyword arguments:
            attr -- The identifier of the attribute requested.
            value -- The value to set for this attribute.

        '''
        native.eglSurfaceAttrib(self.display, self, attr, value)

    @property
    def multisample_resolve(self):
        '''Get the filter used when resolving the multisample buffer.

        Returns:
            Either MultisampleResolve.default or MultisampleResolve.box.

        '''
        return self._attr(SurfaceAttribs.MULTISAMPLE_RESOLVE)
    @multisample_resolve.setter
    def multisample_resolve(self, val):
        '''Set the filter used when resolving the multisample buffer.

        Keyword arguments:
            val -- Either MultisampleResolve.default or
                MultisampleResolve.box.

        '''
        self._setattr(SurfaceAttribs.MULTISAMPLE_RESOLVE, val)

    @property
    def openvg_alpha_premultiplied(self):
        '''Determine whether OpenVG alpha values are premultiplied.'''
        alpha_format = self._attr(SurfaceAttribs.VG_ALPHA_FORMAT)
        # Will be None if the format is neither "pre" nor "nonpre".
        return {VGAlphaFormats.pre: True,
                VGAlphaFormats.nonpre: False}.get(alpha_format)

    @property
    def openvg_colorspace(self):
        '''Get the OpenVG colorspace in use on this surface.'''
        return self._attr(SurfaceAttribs.VG_COLORSPACE)

    @property
    def render_buffer(self):
        '''Get the type of render buffer which client APIs should use.

        Returns:
            RenderBufferTypes.BACK or RenderBufferTypes.SINGLE.

        '''
        return self._attr(SurfaceAttribs.RENDER_BUFFER)

    @property
    def size(self):
        '''Get the size of this surface.

        Returns:
            A 2-tuple giving the width and height, in pixels.

        '''
        return tuple(self._attr(attr) for attr in (SurfaceAttribs.WIDTH,
                                                   SurfaceAttribs.HEIGHT))

    @property
    def swap_behavior(self):
        '''Get the effect of a buffer swap on the color buffer.

        Returns:
            Either SwapBehaviors.preserved or SwapBehaviors.destroyed.

        '''
        return self._attr(SurfaceAttribs.SWAP_BEHAVIOR)
    @swap_behavior.setter
    def swap_behavior(self, val):
        '''Set the effect a buffer swap will have on the color buffer.

        Keyword arguments:
            val -- Either SwapBehaviors.preserved or
                SwapBehaviors.destroyed.

        '''
        return self._setattr(SurfaceAttribs.SWAP_BEHAVIOR, val)

    def copy_buffers(self, pixmap):
        '''Copy the contents of the rendering buffer to a native pixmap.

        Keyword arguments:
            pixmap -- The handle of the native pixmap to which the
                buffer will be copied.

        '''
        native.eglCopyBuffers(self.display, self, pixmap)

    def swap_buffers(self):
        '''Perform a buffer swap.

        The state of the color buffer after the swap is defined by the
        swap_behavior attribute.

        '''
        native.eglSwapBuffers(self.display, self)


class PbufferSurface(Surface):
    '''Represents an off-screen surface in a pbuffer (pixel buffer).

    Instance attributes:
        shandle, display, config, attribs -- Inherited from Surface.

    '''
    def __init__(self, display, config, attribs, buffer=None,
                 buffer_type=OPENVG_IMAGE):
        '''Create the pbuffer surface.

        The following attributes from SurfaceAttribs are accepted when
        creating a pbuffer surface:
            * WIDTH and HEIGHT
            * LARGEST_PBUFFER
            * TEXTURE_FORMAT and TEXTURE_TARGET (only used by OpenGL ES)
            * MIPMAP_TEXTURE (only used by OpenGL ES)
            * VG_COLORSPACE and VG_ALPHA_FORMAT (only used by OpenVG)

        When creating a surface bound to a client buffer (i.e. buffer is
        not None), only the TEXTURE_FORMAT, TEXTURE_TARGET and
        MIPMAP_TEXTURE attributes are accepted.

        Keyword arguments:
            display, config, attribs -- As the instance attributes.
            buffer -- An optional client buffer to bind this surface to.
            buffer_type -- The type of the client buffer, if provided.
                The default type (and the only one allowed by the EGL
                specification) is OPENVG_IMAGE.

        '''
        super().__init__(display, config, attribs)
        if buffer is None:
            self.shandle = native.eglCreatePbufferSurface(self.display,
                                                          self.config,
                                                          self.attribs)
        else:
            self.shandle =\
                native.eglCreatePbufferFromClientBuffer(self.display,
                                                        buffer_type, buffer,
                                                        self.config,
                                                        self.attribs)

    @property
    def mipmap_level(self):
        '''Get the mipmap level in use.

        This attribute is only available when the surface supports
        OpenGL ES.

        '''
        return self._attr(SurfaceAttribs.MIPMAP_LEVEL)
    @mipmap_level.setter
    def mipmap_level(self, val):
        '''Set the mipmap level to be used.

        This attribute is only available when the surface supports
        OpenGL ES.

        Keyword arguments:
            level -- The integer level number to use. If this is outside
                the available range, the closest valid level is used.

        '''
        return self._setattr(SurfaceAttribs.MIPMAP_LEVEL, val)

    @property
    def has_mipmap_textures(self):
        '''Query whether or not this surface has mipmap textures.'''
        return self._attr(SurfaceAttribs.MIPMAP_TEXTURE)

    @property
    def texture(self):
        '''Get the type of OpenGL ES texture that this surface maps to.

        Returns:
            A 2-tuple containing the texture format (None,
            TextureFormats.rgb, or TextureFormats.rgba) and target (None
            or TextureTargets.two_d).

        '''
        return tuple(self._attr(attr)
                     for attr in (SurfaceAttribs.TEXTURE_FORMAT,
                                  SurfaceAttribs.TEXTURE_TARGET))

    @property
    def texture(self):
        '''Get the type of OpenGL ES texture that this surface maps to.

        Returns:
            A 2-tuple containing the texture format (None,
            TextureFormats.rgb, or TextureFormats.rgba) and target (None
            or TextureTargets.two_d).

        '''
        return tuple(self._attr(attr)
                     for attr in (SurfaceAttribs.TEXTURE_FORMAT,
                                  SurfaceAttribs.TEXTURE_TARGET))

    @property
    def use_largest_pbuffer(self):
        '''Query whether the largest possible pbuffer was requested.'''
        return self._attr(SurfaceAttribs.LARGEST_PBUFFER)

    def bind_texture(self, buffer=RenderBufferTypes.BACK):
        '''Bind this surface to an OpenGL ES texture.

        Keyword arguments:
            buffer -- Which rendering buffer to bind. The EGL standard
                currently only supports the back buffer in this role
                and hence the argument may be omitted.

        '''
        native.eglBindTexImage(self.display, self, buffer)

    def release_texture(self, buffer=RenderBufferTypes.BACK):
        '''Release the surface from a binding to an OpenGL ES texture.

        Keyword arguments:
            buffer -- Which rendering buffer to release. The EGL
                standard currently only supports the back buffer in this
                role and hence the argument may be omitted.

        '''
        native.eglReleaseTexImage(self.display, self, buffer)


class PixmapSurface(Surface):
    '''Represents a surface that renders to a native pixmap.

    Instance attributes:
        shandle, display, config, attribs -- Inherited from Surface.

    '''
    def __init__(self, display, config, attribs, pixmap):
        '''Create the pixmap surface.

        Only the following attributes from SurfaceAttribs are accepted
        when creating a pixmap surface:
            * VG_COLORSPACE and VG_ALPHA_FORMAT (only used by OpenVG)

        Keyword arguments:
            display, config, attribs -- As the instance attributes.
            pixmap -- The native pixmap to render to.

        '''
        super().__init__(display, config, attribs)
        self.shandle = native.eglCreatePixmapSurface(self.display, self.config,
                                                     pixmap, self.attribs)


class WindowSurface(Surface):
    '''Represents an on-screen surface bound to a native window.

    Instance attributes:
        shandle, display, config, attribs -- Inherited from Surface.

    '''
    def __init__(self, display, config, attribs, window):
        '''Create the window surface.

        The following attributes from SurfaceAttribs are accepted when
        creating a window surface:
            * RENDER_BUFFER
            * VG_COLORSPACE and VG_ALPHA_FORMAT (only used by OpenVG)

        Keyword arguments:
            display, config, attribs -- As the instance attributes.
            window -- The native window to which this surface belongs.

        '''
        super().__init__(display, config, attribs)
        self.shandle = native.eglCreateWindowSurface(self.display, self.config,
                                                     window, self.attribs)

    @property
    def physical_resolution(self):
        '''Get the resolution of the physical display.

        Returns:
            A 3-tuple giving the horizontal and vertical resolution, in
            pixels per metre, and the width:height aspect ratio of each
            physical pixel. If any of these values is unknown, None is
            returned in its place.

        '''
        # Scaling and mapping the "unknown" symbol to None is handled by
        # attr_convert in the attribs module, which self._attr() calls.
        return tuple(self._attr(attr)
                     for attr in (SurfaceAttribs.HORIZONTAL_RESOLUTION,
                                  SurfaceAttribs.VERTICAL_RESOLUTION,
                                  SurfaceAttribs.PIXEL_ASPECT_RATIO))
