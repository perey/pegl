#!/usr/bin/env python3

'''Unit tests for the Pegl display module.'''

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
import sys

# Access the pegl package at ../pegl (relative to the tests directory).
sys.path.append('..')
from pegl import display

def test_version_structure():
    '''Test the named tuple that holds version information.'''
    v = display.Version(0, 1, 'Testing')
    assert v.major == 0
    assert v.minor == 1
    assert v.vendor == 'Testing'
    assert str(v) == '0.1 Testing'

def test_current_display():
    '''Test the function to fetch the current EGL display.'''
    cd = display.current_display()
    assert cd.version.major == 1 and cd.version.minor == 4
