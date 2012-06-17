#!/usr/bin/env python3

'''Imagination Technologies context priority extension for EGL.

With this extension, contexts may be created with hints (not
requirements) as to the priority of its processing, and the actual
priority assigned may be queried.

http://www.khronos.org/registry/egl/extensions/IMG/EGL_IMG_context_priority.txt

'''
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

# Standard library imports.
from collections import namedtuple

# Local imports.
from ...attribs.context import ContextAttribs
from ...context import Context

# New context attribute.
PriorityLevels = namedtuple('PriorityLevels_tuple',
                            ('HIGH', 'MEDIUM', 'LOW')
                            )(0x3101, 0x3012, 0x3103)
ContextAttribs.extend('PRIORITY_LEVEL', 0x3100, PriorityLevels,
                      PriorityLevels.MEDIUM)

# New Context property, for querying the new attribute in ContextAttribs.
def priority(self):
    '''Get the actual priority level that this context was assigned.

    Returns:
        A value from the PriorityLevels tuple.

    '''
    return self._attr(ContextAttribs.PRIORITY_LEVEL)
Context.priority = property(priority)
