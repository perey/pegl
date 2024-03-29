#!/usr/bin/env python3

'''Pegl: A Python wrapper for the EGL API.'''

# Copyright © 2012, 2013, 2020 Tim Pederick.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

__author__ = 'Tim Pederick'
__version__ = '0.2a1'
__all__ = ['egl', 'egl_version']

# Import module objects to the package namespace.
# pylint: disable=wrong-import-position
from .egl import egl_version

from .attribs import *
from .attribs import __all__ as attribs_all
__all__.extend(attribs_all)

from .config import *
from .config import __all__ as config_all
__all__.extend(config_all)

from .context import *
from .context import __all__ as context_all
__all__.extend(context_all)

from .display import *
from .display import __all__ as display_all
__all__.extend(display_all)

from .enums import *
from .enums import __all__ as enums_all
__all__.extend(enums_all)

from .errors import *
from .errors import __all__ as errors_all
__all__.extend(errors_all)

from .image import *
from .image import __all__ as image_all
__all__.extend(image_all)

from .surface import *
from .surface import __all__ as surface_all
__all__.extend(surface_all)

from .sync import *
from .sync import __all__ as sync_all
__all__.extend(sync_all)
