#!/usr/bin/env python3

'''EGL attribute list handling for Pegl.'''

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

__all__ = ['attrib_list', 'DONT_CARE']

# Standard library imports.
from itertools import chain
from typing import Any, Optional

# Local imports.
from .egl import EGL_NONE
from .egl._common import EGLAttrib, EGLint

def attrib_list(attribs: Optional[dict[Any, Any]], new_type=False):
    """Convert a Python dict into an EGL attribute list.

    Keyword arguments:
        attribs -- The dict to convert. If this is None, then so is the
            return value (representing a NULL in C).
        new_type -- Whether or not the attribute list should be
            represented by the EGL 1.5 ``EGLAttrib`` type. If False or
            omitted, the older (and possibly narrower) ``EGLint`` type
            will be used instead.

    """
    if attribs is None:
        return None
    else:
        # Construct a sequence of keys followed by values, terminated with
        # the special value EGL_NONE.
        ctype = (EGLAttrib if new_type else EGLint)
        length = 2 * len(attribs) + 1
        seq = [*chain.from_iterable(attribs.items()), EGL_NONE]

        return (ctype * length)(seq)

DONT_CARE = egl.EGL_DONT_CARE
