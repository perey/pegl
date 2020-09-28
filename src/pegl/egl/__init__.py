#!/usr/bin/env python3

'''EGL library interface for Pegl.'''

# Copyright © 2012, 2013, 2020 Tim Pederick.
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

__all__ = ['egl_version']

# Standard library imports.
import logging

# Load constants and functions from each successive version of EGL out of the
# version-specific module and into the subpackage namespace.
# TODO: Configurable version loading!!
from .egl1_0 import *
from .egl1_0 import __all__ as egl1_0_all
__all__.extend(egl1_0_all)
egl_version = (1, 0)

try:
    from .egl1_1 import *
    from .egl1_1 import __all__ as egl1_1_all
except ImportError as e:
    logging.debug(e)
else:
    __all__.extend(egl1_1_all)
    egl_version = (1, 1)

    try:
        from .egl1_2 import *
        from .egl1_2 import __all__ as egl1_2_all
    except ImportError as e:
        logging.debug(e)
    else:
        __all__.extend(egl1_2_all)
        egl_version = (1, 2)

        try:
            from .egl1_3 import *
            from .egl1_3 import __all__ as egl1_3_all
        except ImportError as e:
            logging.debug(e)
        else:
            __all__.extend(egl1_3_all)
            egl_version = (1, 3)

            try:
                from .egl1_4 import *
                from .egl1_4 import __all__ as egl1_4_all
            except ImportError as e:
                logging.debug(e)
            else:
                __all__.extend(egl1_4_all)
                egl_version = (1, 4)

                try:
                    from .egl1_5 import *
                    from .egl1_5 import __all__ as egl1_5_all
                except ImportError as e:
                    logging.debug(e)
                else:
                    __all__.extend(egl1_5_all)
                    egl_version = (1, 5)
logging.debug('Loaded EGL version {}.{}'.format(*egl_version))