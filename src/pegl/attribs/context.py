#!/usr/bin/env python3

'''EGL attributes for configuration objects.'''

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
from . import Attribs, Details, NONE
from .config import ConfigAttribs

# Objects for context attributes.
RenderBufferTypes = namedtuple('RenderBufferTypes_tuple',
                               ('NONE', 'BACK', 'SINGLE')
                               )(NONE, 0x3084, 0x3085)
ContextAPIs = namedtuple('ContextAPIs_tuple',
                         ('OPENGL', 'OPENGL_ES', 'OPENVG')
                         )(0x30A2, 0x30A0, 0x30A1)

class ContextAttribs(Attribs):
    '''The set of EGL attributes relevant to context objects.'''
    CONFIG_ID = ConfigAttribs.CONFIG_ID
    RENDER_BUFFER = 0x3086
    CONTEXT_CLIENT_TYPE, CONTEXT_CLIENT_VERSION = 0x3097, 0x3098
    details = {CONFIG_ID: Details('The unique identifier of the configuration '
                                  'used to create this context', c_int, 0),
               RENDER_BUFFER: Details('Which buffer type this context renders '
                                      'into', RenderBufferTypes,
                                      RenderBufferTypes.BACK),
               CONTEXT_CLIENT_TYPE: Details('The client API for which this '
                                            'context was created', ContextAPIs,
                                            NONE),
               CONTEXT_CLIENT_VERSION: Details('The client API version for '
                                               'which this context was '
                                               'created', c_int, 1)}
