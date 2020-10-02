#!/usr/bin/env python3

"""Definitions and utilities for pegl.attribs unit tests."""

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
from itertools import zip_longest
from typing import Sequence

def compare_array(got: Sequence[int], expected: Sequence[int]) -> bool:
    """Compare a ctypes array to another sequence.

    A ctypes array does not compare equal to another sequence of the same
    values, even if it is of the same type. I also don't (yet?) know any
    way to unpack the array except by iterating over its items.

    """
    return all(got_item == expected_item
               for (got_item, expected_item) in zip_longest(got, expected))
