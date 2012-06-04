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
from pegl.display import Display
from pegl.config import get_configs
from pegl.attribs import Attribs, ClientAPIs, CBufferTypes

d = Display(delay_init=True)
print('Initialised EGL version {0[0]}.{0[1]} ({1} {2}).'.format(d.initialize(),
                                                                d.vendor,
                                                                d.version))

c = get_configs(d)
print('There are', len(c), 'configurations available.')
reqs = {Attribs.RENDERABLE_TYPE: ClientAPIs(vg=1)}
c_vg = get_configs(d, reqs)
print(len(c_vg), 'configurations support OpenVG.')

reqs[Attribs.RENDERABLE_TYPE].gl_es2 = 1
c_vg_es = get_configs(d, reqs)
print(len(c_vg_es), 'configurations support OpenVG and OpenGL ES 2.x.')

c_lum = get_configs(d, {Attribs.COLOR_BUFFER_TYPE: CBufferTypes.luminance})
print(len(c_lum), 'configurations support a luminance colour buffer.')

conf = c_vg_es[0]
print('The first OpenVG/OpenGL ES 2.x config (ID #{}) has this colour '
      'buffer:'.format(conf.config_id))
print(conf.color_buffer)

reqs[Attribs.BUFFER_SIZE] = 32
c_vg_es_32 = get_configs(d, reqs)
print(len(c_vg_es),
      'configurations support OpenVG, OpenGL ES 2.x, and 32-bit colour.')
