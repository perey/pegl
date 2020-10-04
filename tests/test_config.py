#!/usr/bin/env python3

'''Unit tests for the pegl.config module.'''

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
from util_test_display import get_native_display

# Import the module to be tested.
import pegl
from pegl import config


class TestProperties(unittest.TestCase):
    """Test the properties defined on configs."""
    def setUp(self):
        """Set up a config for testing."""
        if pegl.egl_version < (1, 4):
            self.dpy = pegl.display.Display(get_native_display())
        else:
            self.dpy = pegl.display.Display()
        self.cfg = self.dpy.get_configs()[0]

    @unittest.skipIf(pegl.egl_version < (1, 2), 'EGL version too low')
    def test_alpha_mask_size(self):
        """Check the alpha_mask_size property.

        This test passes if:

        - The alpha_mask_size property exists
        - It is a non-negative integer
        - It cannot be set

        """
        self.assertIsInstance(self.cfg.alpha_mask_size, int)
        self.assertGreaterEqual(self.cfg.alpha_mask_size, 0)
        with self.assertRaises(AttributeError):
            self.cfg.alpha_mask_size = 16

    def test_alpha_size(self):
        """Check the alpha_size property.

        This test passes if:

        - The alpha_size property exists
        - It is a non-negative integer
        - It cannot be set

        """
        self.assertIsInstance(self.cfg.alpha_size, int)
        self.assertGreaterEqual(self.cfg.alpha_size, 0)
        with self.assertRaises(AttributeError):
            self.cfg.alpha_size = 16

    @unittest.skipIf(pegl.egl_version < (1, 1), 'EGL version too low')
    def test_bind_to_texture_rgb(self):
        """Check the bind_to_texture_rgb property.

        This test passes if:

        - The bind_to_texture_rgb property exists
        - It is a boolean
        - It cannot be set

        """
        self.assertIsInstance(self.cfg.bind_to_texture_rgb, bool)
        with self.assertRaises(AttributeError):
            self.cfg.bind_to_texture_rgb = True

    @unittest.skipIf(pegl.egl_version < (1, 1), 'EGL version too low')
    def test_bind_to_texture_rgba(self):
        """Check the bind_to_texture_rgba property.

        This test passes if:

        - The bind_to_texture_rgba property exists
        - It is a boolean
        - It cannot be set

        """
        self.assertIsInstance(self.cfg.bind_to_texture_rgba, bool)
        with self.assertRaises(AttributeError):
            self.cfg.bind_to_texture_rgba = True


if __name__ == '__main__':
    unittest.main(verbosity=2)
