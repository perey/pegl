#!/usr/bin/env python3

'''Perform a functional test of the Pegl package on this system.'''

# Copyright © 2012 Tim Pederick.
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

import pegl
from pegl.attribs.config import ConfigAttribs, ClientAPIs, CBufferTypes
from pegl.attribs.context import ContextAPIs
from pegl.config import get_configs
import pegl.context as context
from pegl.display import Display
from pegl.ext import extensions as extlist
from pegl.surface import PbufferSurface

# TODO: Obsolete this file by writing unit tests and real functional tests!

# -1. Utility functions.
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
    apis = {'OPENGL_ES': 'OpenGL ES 1.x', 'OPENGL_ES2': 'OpenGL ES 2.x',
            'OPENGL': 'OpenGL', 'OPENVG': 'OpenVG'}
    for api in seq:
        yield apis.get(api, 'an unknown API')

# 0. Checking for "client extension" support.
try:
    import pegl.ext.ext_extensiontypes as xt
except ImportError:
    print('Client extensions not supported, creating display...')
else:
    print('The following client extensions are supported:')
    print('  *', '\n *'.join(xt.client_extensions))
    print()

# 1. Initialising the EGL display.
d = Display(delay_init=True)
print('Initialised EGL version {0[0]}.{0[1]} ({1} '
      '{2!s}).'.format(d.initialize(), d.vendor, d.version))
print('This implementation supports these APIs:')
print('  *', '\n  * '.join(d.client_apis))

# 1a. Checking for supported extensions.
first_supported = None
print('...and these extensions:')
for ext in d.extensions:
    if first_supported is None and ext in extlist:
        first_supported = ext
    print('  * {} ({}supported by Pegl)'.format(ext,
                                                '' if ext in extlist
                                                else 'not '))
if first_supported is not None:
    print("Trying to enable extension '{}'...".format(first_supported),
          end=' ')
    try:
        ext = d.load_extension(first_supported)
    except ImportError:
        print('Failed!')
    else:
        print('Success!')
else:
    print('No extensions supported by Pegl and by the implementation.',
          'Skipping extension-loading test.')
print()

# 2. Getting available configurations.
c = get_configs(d)
print('There are', len(c), 'configurations available.')

# 2a. Paring down the configurations by selecting desired attributes.
reqs = {'RENDERABLE_TYPE': ClientAPIs(OPENGL=1)}
c_gl = get_configs(d, reqs)
print(len(c_gl), 'configurations support OpenGL.' +
      (' (I wonder what the other ' + str(len(c) - len(c_gl)) + ' do?)'
       if len(c) - len(c_gl) else ''))

reqs['RENDERABLE_TYPE'].OPENGL = 0
reqs['RENDERABLE_TYPE'].OPENGL_ES = 1
c_es = get_configs(d, reqs)
print(len(c_es), 'configurations support OpenGL ES 1.x.')

reqs['RENDERABLE_TYPE'].OPENGL_ES = 0
reqs['RENDERABLE_TYPE'].OPENGL_ES2 = 1
c_es2 = get_configs(d, reqs)
print(len(c_es2), 'configurations support OpenGL ES 2.x.')

reqs['RENDERABLE_TYPE'].OPENGL_ES2 = 0
reqs['RENDERABLE_TYPE'].OPENVG = 1
c_vg = get_configs(d, reqs)
print(len(c_vg), 'configurations support OpenVG.')

reqs['RENDERABLE_TYPE'].OPENGL = 1
reqs['RENDERABLE_TYPE'].OPENGL_ES = 1
reqs['RENDERABLE_TYPE'].OPENGL_ES2 = 1
c_all = get_configs(d, reqs)
print(len(c_all), 'configurations support all four APIs.')

reqs[ConfigAttribs.BUFFER_SIZE] = 32
c_all_32 = get_configs(d, reqs)
print(len(c_all_32),
      'configurations support all four APIs and 32-bit colour.')

c_lum = get_configs(d, {'COLOR_BUFFER_TYPE': CBufferTypes.LUMINANCE})
print(len(c_lum), 'configurations support a luminance colour buffer.')

print()

# 3. Attribute access on a configuration.
def show_config_details(conf, label):
    cbuf = conf.color_buffer
    print('The {0} configuration (ID #{1}) has a {2[size]}-bit '
          '{2[type]} colour buffer.'.format(label, conf.config_id, cbuf))
    bit_alloc = {'RGB': 'Red/green/blue/alpha bits are allocated '
                        '{r}/{g}/{b}/{alpha_size}.',
                 'luminance': 'The buffer has {luminance} luminance and '
                              '{alpha_size} alpha bits.'}
    print(bit_alloc[cbuf['type']].format(**cbuf))
    print('The transparency type is {0!s}, with RGB values '
          '({1[r]},{1[g]},{1[b]}).'.format(*conf.transparent_pixels))
    print('The mask buffer has {} alpha mask bits, the depth '
          'buffer has {} bits of depth, and the stencil buffer '
          'has {} bits of depth.'.format(conf.alpha_mask_size,
                                         conf.depth_buffer_size,
                                         conf.stencil_buffer_size))
    print('The configuration comes with',
          'no caveats.' if conf.caveat is None else
          'the caveat that it is ' +
          ('{}.' if type(conf.caveat) is str else
           '"{}", whatever that means!').format(conf.caveat))
    print('It supports {}, and can render to {} '
          'contexts.'.format(*(and_list(clientAPIs(apis))
                               for apis in (conf.conformant_apis,
                                            conf.renderable_contexts))))
    print('It can render to surfaces with {} '
          'properties.'.format(and_list(conf.surface_types)))
    print()

show_config_details(c_vg[0], 'first OpenVG')
show_config_details(c_all_32[0], 'first all-API, 32-bit colour')

# 4. API binding and context creation.
print('Initially, the bound API is {} '
      '(ID {}).'.format(context.bound_api(), context.bound_api(raw=True)))
print('Trying to bind OpenGL by ID...')
context.bind_api(ContextAPIs.OPENGL)
print('Now', context.bound_api(), 'is bound.')
print('Trying to bind OpenVG by name...')
context.bind_api('OpenVG')
print('And now', context.bound_api(), 'is bound.')
print()

# 5. Surface creation.
print('Creating a pbuffer surface...')
surf = PbufferSurface(d, c_all_32[0], {'WIDTH': 640, 'HEIGHT': 480})
print('Got one. It is {} pixels wide by {} pixels high.'.format(*surf.size))
