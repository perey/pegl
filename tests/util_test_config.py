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
all_known_flags = 0x1 | 0x2 | 0x4 | 0x8 | 0x40

def has_unknown_flags(val: int) -> bool:
    return bool(val & ~all_known_flags)
