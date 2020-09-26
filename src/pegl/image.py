#!/usr/bin/env python3

"""EGL image objects for Pegl."""

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

__all__ = []

# Standard library imports.
from typing import Any

# Local imports.
from . import egl

if egl.egl_version >= (1, 5):
    __all__.extend(['Image'])

    class Image:
        """An EGL image.

        In EGL, an image represents state (presumably 2D image data) that
        can be shared between multiple client APIs.

        """
        def __init__(self, display: 'Display', handle: Any):
            self._display = display
            self._as_parameter_ = handle

        def __del__(self):
            egl.eglDestroyImage(self._display, self)
