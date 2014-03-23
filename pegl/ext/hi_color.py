#!/usr/bin/env python3

'''HI Corp. color format extension for EGL.

This extension adds ARGB color formats to EGL configuration options.

http://www.khronos.org/registry/egl/extensions/HI/EGL_HI_colorformats.txt

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
from collections import namedtuple

# Local imports.
from ..attribs import DONT_CARE
from ..attribs.config import ConfigAttribs

# New configuration attribute.
ColorFormats = namedtuple('ColorFormats_tuple',
                          ('RGB', 'RGBA', 'ARGB')
                          )(0x8F71, 0x8F72, 0x8F73))
ConfigAttribs.extend('COLOR_FORMAT', 0x8F70, ColorFormats, DONT_CARE)
