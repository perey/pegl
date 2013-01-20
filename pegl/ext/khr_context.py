#!/usr/bin/env python3

'''Khronos context attribute extension for EGL.

This extension provides several new attributes that may be supplied at
context creation to specify OpenGL and OpenGL ES version support.

http://www.khronos.org/registry/egl/extensions/KHR/EGL_KHR_create_context.txt

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

# Standard library imports.
from collections import namedtuple
from ctypes import c_int

# Local imports.
from ...attribs import BitMask
from ...attribs.context import ContextAttribs

# New context attributes.
class ContextFlags(BitMask):
    '''A bit mask representing extension flags for context creation.'''
    bit_names = ['OPENGL_DEBUG', 'OPENGL_FORWARD_COMPATIBLE',
                 'OPENGL_ROBUST_ACCESS']

class ContextProfiles(BitMask):
    '''A bit mask representing extension profiles for context creation.'''
    bit_names = ['OPENGL_CORE_PROFILE', 'OPENGL_COMPATIBILITY_PROFILE']

ResetNotifications = namedtuple('ResetNotifications_tuple',
                                ('NO_RESET_NOTIFICATION',
                                 'LOSE_CONTEXT_ON_RESET')
                                )(0x31BE, 0x31BF)

# Alias defined by this extension.
ContextAttribs.CONTEXT_MAJOR_VERSION = ContextAttribs.CONTEXT_CLIENT_VERSION
ContextAttribs.extend('CONTEXT_MINOR_VERSION', 0x30FB, c_int, 0)
ContextAttribs.extend('CONTEXT_FLAGS', 0x30FC, ContextFlags, ContextFlags())
ContextAttribs.extend('CONTEXT_OPENGL_PROFILE_MASK', 0x30FD, ContextProfiles,
                      ContextProfiles(OPENGL_CORE_PROFILE=1))
ContextAttribs.extend('CONTEXT_OPENGL_RESET_NOTIFICATION_STRATEGY', 0x31BD,
                      ResetNotifications,
                      ResetNotifications.NO_RESET_NOTIFICATION)

# No new methods or properties are defined to query these attributes, as they
# are only available in EGL at context creation. The client API may provide
# the means to query them from an existing context, however.
