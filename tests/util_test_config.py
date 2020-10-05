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

from __future__ import annotations

# Standard library imports.
from functools import reduce
from operator import or_
from typing import Sequence
from unittest import TestCase

# Import from library being tested.
from pegl.enums import ClientAPIFlag

all_known_flags = reduce(or_, ClientAPIFlag, 0)

def has_unknown_flags(val: ClientAPIFlag) -> bool:
    return bool(val & ~all_known_flags)
