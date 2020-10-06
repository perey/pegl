#!/usr/bin/env python3

"""Definitions and utilities for pegl.config unit tests."""

# Copyright © 2020 Tim Pederick.
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
from unittest import TestCase

# Hard-coded, as flags might be reported by an implementation that are not
# recognized by Pegl because it loaded a lower EGL version.
FLAG_OPENGL_ES = 0x1
FLAG_OPENVG = 0x2
FLAG_OPENGL_ES2 = 0x4
FLAG_OPENGL = 0x8
FLAG_OPENGL_ES3 = 0x40
all_known_apis = (FLAG_OPENGL_ES | FLAG_OPENVG | FLAG_OPENGL_ES2 |
                  FLAG_OPENGL | FLAG_OPENGL_ES3)

FLAG_PBUFFER = 0x1
FLAG_PIXMAP = 0x2
FLAG_WINDOW = 0x4
FLAG_VG_COLORSPACE_LINEAR = 0x20
FLAG_VG_ALPHA_FORMAT_PRE = 0x40
FLAG_MULTISAMPLE_RESOLVE_BOX = 0x200
FLAG_SWAP_BEHAVIOR_PRESERVED = 0x400
all_known_surfaces = (FLAG_PBUFFER | FLAG_PIXMAP | FLAG_WINDOW |
                      FLAG_VG_COLORSPACE_LINEAR | FLAG_VG_ALPHA_FORMAT_PRE |
                      FLAG_SWAP_BEHAVIOR_PRESERVED)

def has_unknown_apis(val: int) -> bool:
    return bool(val & ~all_known_apis)

def has_unknown_surfaces(val: int) -> bool:
    return bool(val & ~all_known_surfaces)
