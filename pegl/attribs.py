#!/usr/bin/env python3

'''EGL 1.4 attribute lists.'''

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

def dont_care_or(expected_type):
    '''Create a type for when a don't-care value is permissible.'''
    DONT_CARE = -1

    class WrappedType:
        '''Wrap a C type so that its value can be DONT_CARE.'''
        def __init__(self, val):
            self.value = val
        def __setattr__(self, attr, val):
            if attr == 'value' and value is not DONT_CARE:
                val = expected_type(val)
            super().__setattr__(attr, val)
        def __repr__(self):
            if self.value is DONT_CARE:
                return 'DONT_CARE'
            else:
                return repr(self.value)
        @property
        def _as_parameter_(self):
            if self.value is DONT_CARE:
                return DONT_CARE
            try:
                return self.value._as_parameter_
            except AttributeError:
                return self.value

    return WrappedType
