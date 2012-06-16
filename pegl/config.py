#!/usr/bin/env python3

'''EGL configuration management.'''

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
from ctypes import c_void_p

# Local imports.
from . import make_int_p, native
from .attribs import attr_convert, AttribList, DONT_CARE
from .attribs.config import Caveats, CBufferTypes, ConfigAttribs

MAX_CONFIGS = 256 # Arbitrary! "256 configs should be enough for anybody..."

# TODO: Consider making these two functions methods of Display instead.
def count_configs(display):
    '''Get the number of configurations supported for a given display.

    Keyword arguments:
        display -- The EGL display for which to check configurations.

    '''
    count = make_int_p()
    # Calling eglGetConfigs with a null pointer (i.e. None) gets the
    # total number of available configurations, without retrieving any.
    native.eglGetConfigs(display, None, 0, count)

    # Dereference the pointer holding the result.
    return count.contents.value

def get_configs(display, attribs=None, max_configs=MAX_CONFIGS):
    '''Get supported configurations for a given display.

    Keyword arguments:
        display -- The EGL display for which to check configurations.
        attribs -- An optional mapping (a dict or AttribList) that lists
            attributes required of any configurations. The EGL standard
            specifies which attributes must match exactly, which must be
            the given value or greater, and which match at least the
            given flags in a bit mask.
        max_configs -- The maximum number of configurations to return.
            If omitted, the default is {}. If None, count_configs() will
            be called first to ensure that all available configurations
            are retrieved.
            

    '''.format(MAX_CONFIGS)
    if max_configs is None:
        max_configs = count_configs(display)

    configs = (c_void_p * max_configs)()
    actual_count = make_int_p()

    if attribs is None:
        # Get all configurations.
        native.eglGetConfigs(display, configs, max_configs, actual_count)
    else:
        # Get configurations that match the required attributes.
        if type(attribs) is not AttribList:
            attribs = AttribList(ConfigAttribs, attribs)

        native.eglChooseConfig(display, attribs, configs, max_configs,
                               actual_count)

    return tuple(Config(cfg, display)
                 for cfg in configs[:actual_count.contents.value])


class Config:
    '''A set of EGL configuration options.

    Instance attributes:
        config_id -- The unique identifier for this configuration.
        chandle -- The foreign object handle for this configuration.
        display -- The EGL display to which this configuration belongs.
        alpha_mask_size -- The size in bits of the alpha mask buffer.
        bind_textures -- Texture types that this configuration allows
            binding to.
        caveat -- A caveat regarding speed or conformance when using
            this configuration.
        conformant_apis -- A bit mask specifying the APIs to which this
            configuration claims conformance.
        color_buffer -- A dict of the color buffer type and bit sizes
            in this configuration.
        depth_buffer_size -- The size in bits of the depth buffer.
        frame_buffer_level -- The level at which surfaces are created
            in the frame buffer.
        multisample -- A dict giving the number of multisample buffers
            available and the number of samples per pixel. Note that the
            EGL specification limits the former value to 0 or 1.
        native_renderable -- Whether or not this configuration allows
            rendering to its surfaces from the native system.
        native_visual -- A 2-tuple of the ID and type of the native
            visual associated with this configuration, if any.
        pbuffer_limits -- The maximum width, height, and total number of
            pixels accepted by the pbuffer (pixel buffer).
        renderable_contexts -- A bit mask specifying which client APIs
            can render to contexts in this configuration.
        stencil_buffer_size -- The size in bits of the stencil buffer.
        surface_types -- A bit mask specifying which EGL surface type
            attributes are supported by this configuration.
        swap_intervals -- The range of values accepted for the number of
            swap intervals between buffer swaps. A 2-tuple in the form
            (min, max + 1).
        transparent_pixels -- A dict specifying which type of
            transparency this configuration supports, if any, and what
            the relevant transparency values are if it does.

    '''
    def __init__(self, chandle, display):
        '''Initialise the configuration.

        Keyword arguments:
            chandle -- As the instance attribute. This is treated as an
                opaque value and should be passed unchanged from the
                foreign function that provided this configuration.
            display -- As the instance attribute.

        '''
        self.chandle = chandle
        self.display = display

    @property
    def _as_parameter_(self):
        '''Get the config reference for use by foreign functions.'''
        return self.chandle

    def _attr(self, attr):
        '''Get the value of a configuration attribute.

        Keyword arguments:
            attr -- The value identifying the desired attribute. Best
                supplied as a symbolic constant from ConfigAttribs.

        Returns:
            An integer, boolean, or bit mask value, as appropriate to
            the attribute in question, or None if the value indicates
            the symbolic constant NONE, or DONT_CARE if that value is
            allowed and indicated.

        '''
        # Call the foreign function, which stores its result in a pointer.
        result = make_int_p()
        native.eglGetConfigAttrib(self.display, self, attr, result)

        # Dereference the pointer and convert to an appropriate type.
        return attr_convert(attr, result.contents.value, ConfigAttribs)

    @property
    def alpha_mask_size(self):
        '''Get the size in bits of the alpha mask buffer.'''
        return self._attr(ConfigAttribs.ALPHA_MASK_SIZE)

    @property
    def bind_textures(self):
        '''Get texture types that this configuration allows binding to.'''
        texs = []
        if self._attr(ConfigAttribs.BIND_TO_TEXTURE_RGB):
            texs.append('RGB')
        if self._attr(ConfigAttribs.BIND_TO_TEXTURE_RGBA):
            texs.append('RGBA')
        return tuple(texs)

    @property
    def caveat(self):
        '''Get the rendering caveat for this configuration, if any.

        Note that the caveat of non-conformance refers only to OpenGL ES
        and is superseded by the conformant_apis attribute, which should
        be relied upon instead.

        '''
        cav = self._attr(ConfigAttribs.CONFIG_CAVEAT)

        if cav == Caveats.SLOW:
            return 'slow'
        elif cav == Caveats.NONCONFORMANT:
            return 'non-conformant'
        else:
            # Could be None, DONT_CARE, or unrecognised.
            return cav

    @property
    def conformant_apis(self):
        '''List client APIs to which this configuration is conformant.

        The claim of conformance is made by the EGL implementation
        itself, and should be trusted or not trusted accordingly.

        '''
        return self._attr(ConfigAttribs.CONFORMANT)._flags_set

    @property
    def config_id(self):
        '''Get the unique identifier for this configuration.'''
        return self._attr(ConfigAttribs.CONFIG_ID)

    @property
    def color_buffer(self):
        '''Get the color buffer attributes of this configuration.'''
        btype = self._attr(ConfigAttribs.COLOR_BUFFER_TYPE)
        buffer_info = {'size': self._attr(ConfigAttribs.BUFFER_SIZE),
                       'alpha_size': self._attr(ConfigAttribs.ALPHA_SIZE)}
        if btype == CBufferTypes.RGB:
            buffer_info['type'] = 'RGB'
            for key, attr in (('r', ConfigAttribs.RED_SIZE),
                              ('g', ConfigAttribs.GREEN_SIZE),
                              ('b', ConfigAttribs.BLUE_SIZE)):
                buffer_info[key] = self._attr(attr)
        elif btype == CBufferTypes.LUMINANCE:
            buffer_info['type'] = 'luminance'
            buffer_info['luminance'] = self._attr(ConfigAttribs.LUMINANCE_SIZE)
        else:
            buffer_info['type'] = 'unknown'

        return buffer_info

    @property
    def depth_buffer_size(self):
        '''Get the size in bits of the depth buffer.'''
        return self._attr(ConfigAttribs.DEPTH_SIZE)

    @property
    def frame_buffer_level(self):
        '''Get the frame buffer level at which new surfaces are created.

        The default level is 0. Other levels represent overlays and
        underlays, the exact behaviour of which depends on the native
        windowing system.

        '''
        return self._attr(ConfigAttribs.LEVEL)

    @property
    def multisample(self):
        '''Get details of the multisample buffer in this configuration.'''
        return {'buffers': self._attr(ConfigAttribs.SAMPLE_BUFFERS),
                'samples': self._attr(ConfigAttribs.SAMPLES)}

    @property
    def native_renderable(self):
        '''Determine whether native calls can render to EGL surfaces.'''
        return self._attr(ConfigAttribs.NATIVE_RENDERABLE)

    @property
    def native_visual(self):
        '''Get the native visual associated with this configuration.'''
        nvid, nvtype = (self._attr(attr)
                        for attr in (ConfigAttribs.NATIVE_VISUAL_ID,
                                     ConfigAttribs.NATIVE_VISUAL_TYPE))
        return {'id': nvid,
                'type': (None if (nvid == 0 and
                                  nvtype == ConfigAttribs.NONE)
                                  # Which it should, if nvid == 0.
                         else nvtype)}

    @property
    def pbuffer_limits(self):
        '''Get the maximum dimensions of the pbuffer (pixel buffer).'''
        return {'width': self._attr(ConfigAttribs.MAX_PBUFFER_WIDTH),
                'height': self._attr(ConfigAttribs.MAX_PBUFFER_HEIGHT),
                'pixels': self._attr(ConfigAttribs.MAX_PBUFFER_PIXELS)}

    @property
    def renderable_contexts(self):
        '''List client APIs to which this configuration can render.'''
        return self._attr(ConfigAttribs.RENDERABLE_TYPE)._flags_set

    @property
    def stencil_buffer_size(self):
        '''Get the size in bits of the stencil buffer.'''
        return self._attr(ConfigAttribs.STENCIL_SIZE)

    @property
    def surface_types(self):
        '''List surface types to which this configuration can render.'''
        # TODO: Separate properties to query some or all of these flags?
        # (Including the new flags in ext.khr.locksurface)
        return self._attr(ConfigAttribs.SURFACE_TYPE)._flags_set

    @property
    def swap_intervals(self):
        '''Get the limits on swap intervals between buffer swaps.'''
        return (self._attr(ConfigAttribs.MIN_SWAP_INTERVAL),
                # Upper limit given as max + 1, as normal for ranges in Python.
                self._attr(ConfigAttribs.MAX_SWAP_INTERVAL) + 1)

    @property
    def transparent_pixels(self):
        '''Get the transparent pixel support of this configuration.'''
        ttype = self._attr(ConfigAttribs.TRANSPARENT_TYPE)
        return (None if (ttype is None or ttype == TransparentTypes.NONE) else
                'RGB' if ttype == TransparentTypes.RGB else
                'unknown',
                {'r': self._attr(ConfigAttribs.TRANSPARENT_RED_VALUE),
                 'g': self._attr(ConfigAttribs.TRANSPARENT_GREEN_VALUE),
                 'b': self._attr(ConfigAttribs.TRANSPARENT_BLUE_VALUE)})
