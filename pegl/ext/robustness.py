#!/usr/bin/env python3

'''Cross-vendor context robustness extension for EGL.

This wrapper has been designed for version 3 of the extension.

http://www.khronos.org/registry/egl/extensions/EXT/EGL_EXT_create_context_robustness.txt

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

# Local imports.
from ..attribs.context import ContextAttribs

# New context attributes.
ResetStrategies = namedtuple('ResetStrategies_tuple',
                             ('NO_RESET_NOTIFICATION',
                              'LOSE_CONTEXT_ON_RESET'),
                             )(0x31BE, 0x31BF)

ContextAttribs.extend('OPENGL_ROBUST_ACCESS', 0x30BF, bool, False)
ContextAttribs.extend('OPENGL_RESET_NOTIFICATION_STRATEGY', 0x3138,
                      ResetStrategies, ResetStrategies.NO_RESET_NOTIFICATION)
