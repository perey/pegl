#!/usr/bin/env python3

'''EGL configuration management.'''

# Copyright © 2012 Tim Pederick.
#
# This file is part of PEGL.
#
# PEGL is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PEGL is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
# License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PEGL. If not, see <http://www.gnu.org/licenses/>.

# Standard library imports.
from ctypes import c_void_p

# Local imports.
from . import egl, error_check, make_int_p
from .attribs import (Attribs, AttribList, BitMask, Caveats, CBufferTypes,
                      DONT_CARE)

MAX_CONFIGS = 256 # Arbitrary! But it's sufficient for MY computer...

def get_configs(display, attribs=None):
    '''Get supported configurations for a given display.

    Keyword arguments:
        display -- The EGL display for which to check configurations.
        attribs -- An optional mapping (a dict or AttribList) that lists
            attributes required of any configurations. The EGL standard
            specifies which attributes must match exactly, which match
            "at least" the given value, and which match at least the
            given flags in a bit mask.

    '''
    configs = (c_void_p * MAX_CONFIGS)()
    actual_count = make_int_p()

    if attribs is None:
        # Get all configurations.
        error_check(egl.eglGetConfigs(display, configs, MAX_CONFIGS,
                                      actual_count))
    else:
        # Get configurations that match the required attributes.
        if type(attribs) is not AttribList:
            # FIXME: Why do I need to get this _as_parameter_?
            # Isn't ctypes supposed to do that for itself? But
            # when I leave it off, it complains that I gave it
            # "LP_c_int instance instead of c_int_Array_3", so
            # there's clearly a difference when I do it myself.
            attribs = AttribList(attribs)._as_parameter_
        error_check(egl.eglChooseConfig(display, attribs, configs, MAX_CONFIGS,
                                        actual_count))

    return tuple(Config(cfg, display) for cfg in configs[:actual_count[0]])


class Config:
    '''A set of EGL configuration options.

    Instance attributes:
        chandle -- The foreign object handle for this configuration.
        display -- The EGL display to which this configuration belongs.
        config_id -- The unique identifier for this configuration.
        color_buffer -- A dict of the color buffer type and bit sizes.

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
                supplied as a symbolic constant from Attribs.

        Returns:
            An integer, boolean, or bit mask value, as appropriate to
            the attribute in question, or None if value indicates the
            EGL symbolic constant NONE, or DONT_CARE if that value is
            allowed and indicated.

        '''
        result = make_int_p()
        error_check(egl.eglGetConfigAttrib(self.display, self, attr, result))

        # Dereference the pointer.
        result = result[0]

        # Convert to an appropriate type.
        details = Attribs.details[attr]
        if details.dontcare and result == DONT_CARE._as_parameter_:
            return DONT_CARE
        elif details.values is bool:
            return bool(result)
        elif (result == Attribs.NONE and
              issubclass(type(details.values), tuple) and
              Attribs.NONE in details.values):
            # The value is the EGL symbolic constant for NONE, in an
            # enumeration (named tuple) that supports it.
            return None
        else:
            try:
                if issubclass(details.values, BitMask):
                    return details.values(result)
            except TypeError:
                # details.values is not a class.
                pass

        # Finally...
        return result

    @property
    def bind_textures(self):
        '''Get texture types that this configuration allows binding to.'''
        texs = []
        if self._attr(Attribs.BIND_TO_TEXTURE_RGB):
            texs.append('RGB')
        if self._attr(Attribs.BIND_TO_TEXTURE_RGBA):
            texs.append('RGBA')
        return tuple(texs)

    @property
    def caveat(self):
        '''Get the rendering caveat for this configuration, if any.

        Note that the caveat of non-conformance refers only to OpenGL ES
        and is superseded by the conformant_apis attribute, which should
        be relied upon instead.

        '''
        cav = self._attr(Attribs.CONFIG_CAVEAT)

        if cav == Caveats.slow:
            return 'slow'
        elif cav == Caveats.nonconformant:
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
        return self._attr(Attribs.CONFORMANT)._flags_set

    @property
    def config_id(self):
        '''Get the unique identifier for this configuration.'''
        return self._attr(Attribs.CONFIG_ID)

    @property
    def color_buffer(self):
        '''Get the color buffer attributes of this configuration.'''
        btype = self._attr(Attribs.COLOR_BUFFER_TYPE)
        buffer_info = {'size': self._attr(Attribs.BUFFER_SIZE),
                       'alpha_size': self._attr(Attribs.ALPHA_SIZE),
                       'alpha_mask_size': self._attr(Attribs.ALPHA_MASK_SIZE)}
        if btype == CBufferTypes.rgb:
            buffer_info['type'] = 'RGB'
            for key, attr in (('r', Attribs.RED_SIZE),
                              ('g', Attribs.GREEN_SIZE),
                              ('b', Attribs.BLUE_SIZE)):
                buffer_info[key] = self._attr(attr)
        elif btype == CBufferTypes.luminance:
            buffer_info['type'] = 'luminance'
            buffer_info['luminance'] = self._attr(Attribs.LUMINANCE_SIZE)
        else:
            buffer_info['type'] = 'unknown'

        return buffer_info

    @property
    def renderable_contexts(self):
        '''List client APIs to which this configuration can render.'''
        return self._attr(Attribs.RENDERABLE_TYPE)._flags_set

    @property
    def surface_types(self):
        '''List surface types to which this configuration can render.'''
        return self._attr(Attribs.SURFACE_TYPE)._flags_set

    @property
    def transparent_pixels(self):
        '''Get the transparent pixel support of this configuration.'''
        ttype = self._attr(Attribs.TRANSPARENT_TYPE)
        return (None if (ttype is None or ttype == TransparentTypes.none) else
                'RGB' if ttype == TransparentTypes.rgb else
                'unknown', {'r': self._attr(Attribs.TRANSPARENT_RED_VALUE),
                            'g': self._attr(Attribs.TRANSPARENT_GREEN_VALUE),
                            'b': self._attr(Attribs.TRANSPARENT_BLUE_VALUE)})
