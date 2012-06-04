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

# TODO: Obsolete this file by writing real unit tests!

# 0. Utility functions.
def and_list(seq, serial_comma=True, comma_between_two=False, sort=True):
    '''List elements of the sequence in natural-looking English.'''
    if sort:
        seq = sorted(seq)

    try:
        length = len(seq)
    except TypeError:
        seq = list(seq)
        length = len(seq)

    if length == 0:
        return ''
    elif length == 1:
        return str(seq[0])
    elif length == 2:
        pre_and = str(seq[0]) + (',' if comma_between_two else '')
    else:
        pre_and = (', '.join(str(i) for i in seq[:-1]) +
                   (',' if serial_comma else ''))
    return (pre_and + ' and ' + str(seq[-1]))

def clientAPIs(seq):
    apis = {'opengl_es': 'OpenGL ES 1.x', 'opengl_es2': 'OpenGL ES 2.x',
            'opengl': 'OpenGL', 'openvg': 'OpenVG'}
    for api in seq:
        yield apis.get(api, 'an unknown API')

# 1. Initialising the EGL display.
d = Display(delay_init=True)
print('Initialised EGL version {0[0]}.{0[1]} ({1} {2}).'.format(d.initialize(),
                                                                d.vendor,
                                                                d.version))
print('This implementation supports these APIs:')
print('  *', '\n  * '.join(d.client_apis.split()))
print('...and these extensions:')
print('  *', '\n  * '.join(d.extensions.split()))
print()

# 2. Getting available configurations.
c = get_configs(d)
print('There are', len(c), 'configurations available.')

# 2a. Paring down the configurations by selecting desired attributes.
reqs = {Attribs.RENDERABLE_TYPE: ClientAPIs(opengl=1)}
print('**', str(reqs[Attribs.RENDERABLE_TYPE]))
c_gl = get_configs(d, reqs)
print(len(c_gl), 'configurations support OpenGL.')

reqs[Attribs.RENDERABLE_TYPE].opengl = 0
reqs[Attribs.RENDERABLE_TYPE].opengl_es = 1
print('**', str(reqs[Attribs.RENDERABLE_TYPE]))
c_es = get_configs(d, reqs)
print(len(c_es), 'configurations support OpenGL ES 1.x.')

reqs[Attribs.RENDERABLE_TYPE].opengl_es = 0
reqs[Attribs.RENDERABLE_TYPE].opengl_es2 = 1
print('**', str(reqs[Attribs.RENDERABLE_TYPE]))
c_es2 = get_configs(d, reqs)
print(len(c_es2), 'configurations support OpenGL ES 2.x.')

reqs[Attribs.RENDERABLE_TYPE].opengl_es2 = 0
reqs[Attribs.RENDERABLE_TYPE].openvg = 1
print('**', str(reqs[Attribs.RENDERABLE_TYPE]))
c_vg = get_configs(d, reqs)
print(len(c_vg), 'configurations support OpenVG.')

reqs[Attribs.RENDERABLE_TYPE].opengl = 1
reqs[Attribs.RENDERABLE_TYPE].opengl_es = 1
reqs[Attribs.RENDERABLE_TYPE].opengl_es2 = 1
print('**', str(reqs[Attribs.RENDERABLE_TYPE]))
c_all = get_configs(d, reqs)
print(len(c_all), 'configurations support all four APIs.')

reqs[Attribs.BUFFER_SIZE] = 32
c_all_32 = get_configs(d, reqs)
print(len(c_all_32),
      'configurations support all four APIs and 32-bit colour.')

c_lum = get_configs(d, {Attribs.COLOR_BUFFER_TYPE: CBufferTypes.luminance})
print(len(c_lum), 'configurations support a luminance colour buffer.')

print()

# 3. Attribute access on a configuration.
conf = c_vg[0]
cbuf = conf.color_buffer
print('The first OpenVG configuration (ID #{0}) has a {1[size]}-bit '
      '{1[type]} colour buffer.'.format(conf.config_id, cbuf))
bit_alloc = {'RGB': 'Red/green/blue/alpha bits are allocated '
                    '{r}/{g}/{b}/{alpha_size}.',
             'luminance': 'The buffer has {luminance} luminance and '
                          '{alpha_size} alpha bits.'}
print(bit_alloc[cbuf['type']].format(**cbuf))
print('The transparency type is {0!s}, with RGB values '
      '({1[r]},{1[g]},{1[b]}).'.format(*conf.transparent_pixels))
print('The configuration comes with',
      'no caveats.' if conf.caveat is None else
      'the caveat that it is {}{}'.format(conf.caveat,
                                          '.' if type(conf.caveat) is str else
                                          ', whatever that means!'))
print('It supports {}, and can render to {} '
      'contexts.'.format(*(and_list(clientAPIs(apis))
                           for apis in (conf.conformant_apis,
                                        conf.renderable_contexts))))
print('It can render to surfaces with {} '
      'properties.'.format(and_list(conf.surface_types)))
print()
