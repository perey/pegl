#!/usr/bin/env python3

import pegl
from pegl.display import Display, init
from pegl.config import get_configs

d = Display()
print('Initialised EGL version {0[0]}.{0[1]} ({1} {2}).'.format(init(d),
                                                                 d.vendor,
                                                                 d.version))

c = get_configs(d)
print('There are', len(c), 'configurations available.')
