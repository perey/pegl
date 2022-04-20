#!/usr/bin/env python3

'''Definitions and utilities for pegl.display unit tests.'''

# Copyright © 2020, 2021 Tim Pederick.
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
import os
import sys
from warnings import warn
from typing import Any, Callable

def get_native_display() -> tuple[int, Any, Callable[[], None]]:
    if sys.platform.startswith('win'):
        from ctypes import windll
        return (windll.user32.GetDC(None), None, lambda: None)
    else:
        # TODO: Non-Wayland systems!
        import pywayland.client
        wldpy = pywayland.client.Display()
        wldpy.connect()
        # Work around ctypes (Pegl)/cffi (PyWayland) incompatibility.
        from cffi import FFI
        return int(FFI().cast('intptr_t', wldpy._ptr)), wldpy, wldpy.disconnect

def warn_on_version_mismatch(pegl_version: tuple[int, int],
                             impl_version: tuple[int, int]) -> None:
    """Emit a warning if version numbers don't match.

    Specifically, a warning is emitted if:

    - The Pegl-detected version is higher than the implementation-reported
      version, or
    - The Pegl-detected version is lower than the implementation-reported
      version, and this is not because of an environment variable setting

    """
    if (impl_version < pegl_version or
        (impl_version < pegl_version and
         os.environ.get('PEGLEGLVERSION') != '{0}.{1}'.format(*pegl_version))):
        warn('Version mismatch: Pegl detected {0[0]}.{0[1]} but '
             'implementation reported {1[0]}.{1[1]}'.format(pegl_version,
                                                            impl_version))
