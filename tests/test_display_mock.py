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
from itertools import zip_longest
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

    @patch('pegl.config.Config._new_or_existing', return_value='a config')
    def test_choose_config(self, mock_cachelookup):
        """Try choose a config by its attributes.

        This test passes if:

        - eglChooseConfig is called with a display, the given attributes,
          and the given number of configs
        - A number of Config objects equal to the (mocked) returned number
          are created

        """
        attrib_dict = {1: 2, 3: 4}
        expect_attrib_list = [1, 2, 3, 4, pegl.egl.EGL_NONE]
        ask_for = 20
        get_back = 7
        with patch('pegl.egl.eglChooseConfig',
                   return_value=get_back) as mock_choosecfg:
            cfgs = self.dpy.choose_config(attrib_dict, ask_for)
            config_list = (pegl.egl._common.EGLConfig * ask_for)()
            # ctypes arrays don't compare equal even if they have the same
            # items, so let's use call_args instead of assert_called_with
            (dpy, attrib_list, configs,
             config_size), kwargs = mock_choosecfg.call_args

            self.assertIs(dpy, self.dpy)
            # Surely there's a better way to unpack a ctypes array than by
            # iterating over its items...
            for expected, got in zip_longest(expect_attrib_list, attrib_list):
                self.assertEqual(expected, got)
            self.assertEqual(config_size, ask_for)
            self.assertEqual(kwargs, {})

        self.assertEqual(len(mock_cachelookup.call_args_list), get_back)
        self.assertEqual(cfgs, tuple(['a config'] * get_back))

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
