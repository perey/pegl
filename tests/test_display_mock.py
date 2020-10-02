#!/usr/bin/env python3

'''Unit tests for the pegl.display module with EGL functions mocked.'''

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
from unittest.mock import patch
from warnings import warn

# Import test utilities.
from util_test_display import get_native_display

# Import the module to be tested.
import pegl
from pegl import display


class TestClassMethods(unittest.TestCase):
    """Test the class methods defined on the Display class."""
    @patch('pegl.display.Display._new_or_existing', return_value='a display')
    @patch('pegl.egl.eglGetCurrentDisplay', return_value='a handle')
    def test_get_current_display(self, mock_getcurrent, mock_cachelookup):
        """Try fetching the current display.

        This test passes if:

        - eglGetCurrentDisplay is called with no arguments

        """
        dpy = display.Display.get_current_display()

        mock_getcurrent.assert_called_with()
        self.assertEqual(dpy, 'a display')

    @unittest.skipIf(pegl.egl_version < (1, 5), 'EGL version too low')
    def test_get_platform_display(self):
        """Try fetching a platform-specific display.

        This test passes if:

        - eglGetPlatformDisplay is called with the given platform, native
          display, and no attribs
        - eglInitialize is called with the resulting display

        """
        with patch('pegl.egl.eglGetPlatformDisplay',
                   return_value='a handle') as mock_getplatdpy:
            with patch('pegl.egl.eglInitialize',
                       return_value=None) as mock_init:
                dpy = display.Display.get_platform_display('a platform',
                                                           'a native display')
                mock_getplatdpy.assert_called_with('a platform',
                                                   'a native display', None)
                mock_init.assert_called_with(dpy)
                self.assertEqual(dpy._as_parameter_, 'a handle')


class TestMethods(unittest.TestCase):
    """Test the methods of a Display instance."""
    def setUp(self):
        """Create a display for testing."""
        if pegl.egl_version < (1, 4):
            self.dpy = display.Display(get_native_display())
        else:
            self.dpy = display.Display()

    @patch('pegl.Image.__new__', return_value='an image')
    @patch('pegl.egl.eglCreateImage', return_value='a handle')
    @unittest.skipIf(pegl.egl_version < (1, 5), 'EGL version too low')
    def test_create_image(self, mock_createimage, mock_Image):
        """Try creating an image.

        This test passes if:

        - eglCreateImage is called with a display, EGL_NO_CONTEXT, the
          given target and buffer, and no attribs

        """
        img = self.dpy.create_image('a target', 'a buffer')
        mock_createimage.assert_called_with(self.dpy, pegl.egl.EGL_NO_CONTEXT,
                                            'a target', 'a buffer', None)
        self.assertEqual(img, 'an image')


if __name__ == '__main__':
    unittest.main(verbosity=2)
