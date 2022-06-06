#!/usr/bin/env python3

"""Unit tests for the pegl.attribs module."""

# Copyright © 2020 Tim Pederick.
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
import unittest

# Import test utilities.
from util_test_attribs import compare_array

# Import the module to be tested.
import pegl
from pegl import attribs


class TestAttribList(unittest.TestCase):
    """Test attrib list construction."""
    def test_none(self):
        """Test attrib list construction from None.

        This test passes if:

        - The resulting attrib list is None

        """
        attrlist = attribs.attrib_list(None)
        self.assertIs(attrlist, None)

    def test_empty(self):
        """Test attrib list construction from an empty dict.

        This test passes if:

        - The resulting attrib list has one item, EGL_NONE

        """
        attrlist = attribs.attrib_list({})
        self.assertTrue(compare_array(attrlist, [pegl.egl.EGL_NONE]))

    def test_attrib_list(self):
        """Test attrib list construction from a typical dict.

        This test passes if:

        - The resulting attrib list has all of the correct items,
          terminated by EGL_NONE

        """
        attrlist = attribs.attrib_list(
            {pegl.SurfaceAttrib.HEIGHT: 640,
             pegl.SurfaceAttrib.WIDTH: 480,
             pegl.SurfaceAttrib.LARGEST_PBUFFER: False})
        self.assertTrue(compare_array(
            attrlist,
            [pegl.SurfaceAttrib.HEIGHT, 640,
             pegl.SurfaceAttrib.WIDTH, 480,
             pegl.SurfaceAttrib.LARGEST_PBUFFER, False,
             pegl.egl.EGL_NONE]))
