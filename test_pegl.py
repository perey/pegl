#!/usr/bin/env python3

# Copyright © 2012 Tim Pederick.
#
# This file is part of PEGL.
#
# PEGL is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PEGL is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
# License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PEGL. If not, see <http://www.gnu.org/licenses/>.

import pegl
from pegl.display import Display, init
from pegl.config import get_configs

d = Display()
print('Initialised EGL version {0[0]}.{0[1]} ({1} {2}).'.format(init(d),
                                                                 d.vendor,
                                                                 d.version))

c = get_configs(d)
print('There are', len(c), 'configurations available.')
