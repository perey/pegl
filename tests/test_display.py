#!/usr/bin/env python3

'''Unit tests for the pegl.display module.'''

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
from warnings import warn

# Import test utilities.
from util_test_common import known_versions

# Import the module to be tested.
import pegl
from pegl import display


class TestProperties(unittest.TestCase):
    """Test the properties defined on the Display class."""
    def setUp(self):
        """Set up a display for testing."""
        self.dpy = display.Display()

    def test_attribs(self):
        """Test the attribs property."""
        self.assertEqual(self.dpy.attribs, {})
        with self.assertRaises(AttributeError):
            self.dpy.attribs = {'a': 'b'}
        with self.assertRaises(TypeError):
            self.dpy.attribs['fail'] = 'not mutable'

    @unittest.skipIf(pegl.egl_version < (1, 2), 'EGL version too low')
    def test_client_apis(self):
        """Test the client_apis property."""
        self.assertIsInstance(self.dpy.client_apis, str)
        self.assertTrue(any(api in self.dpy.client_apis
                            for api in ('OpenGL', 'OpenGL_ES', 'OpenVG')))
        with self.assertRaises(AttributeError):
            self.dpy.client_apis = 'DirectX'

    def test_extensions(self):
        """Test the extensions property."""
        self.assertIsInstance(self.dpy.extensions, str)
        self.assertTrue(all(ext.startswith('EGL_')
                            for ext in self.dpy.extensions.split()))
        with self.assertRaises(AttributeError):
            self.dpy.extensions = 'EGL_EXT_not_a_real_extension'

    @unittest.skipIf(pegl.egl_version < (1, 1), 'EGL version too low')
    def test_swap_interval(self):
        """Test the swap_interval property."""
        # Property defaults to 1, according to § 3.10.3.
        self.assertEqual(self.dpy.swap_interval, 1)
        # Can't be queried without a current context.
        with self.assertRaises(pegl.errors.BadContextError):
            self.dpy.swap_interval = 0

    def test_vendor(self):
        """Test the vendor property."""
        self.assertIsInstance(self.dpy.vendor, str)
        with self.assertRaises(AttributeError):
            self.dpy.vendor = 'ACME'

    def test_version(self):
        """Test the version property."""
        major, minor, vendor_info = self.dpy.version
        self.assertIsInstance(major, int)
        self.assertIsInstance(minor, int)
        self.assertIsInstance(vendor_info, str)
        self.assertIn((major, minor), known_versions)
        # It's not a failed test if the Pegl-detected version doesn't match
        # with the implementation-reported version, but it's worth noting.
        if (major, minor) != pegl.egl_version:
            warn('Version mismatch: Pegl detected {0}.{1} but implementation '
                 'reported {2[0]}.{2[1]}'.format(major, minor,
                                                 pegl.egl_version))

    def test_version_string(self):
        """Test the version_string property."""
        vstr = self.dpy.version_string
        self.assertIsInstance(vstr, str)
        self.assertEqual(vstr, '{}.{} {}'.format(*self.dpy.version))

class TestPropertiesWithContext(unittest.TestCase):
    """Test Display properties that require a current context."""
    def setUp(self):
        """Set up a display, config, context, and surface for testing."""
        self.dpy = display.Display()
        self.cfg = self.dpy.get_configs(1)[0]
        self.ctx = self.cfg.create_context()
        self.surf = self.cfg.create_pbuffer_surface()
        self.ctx.make_current(self.surf)

    @unittest.skipIf(pegl.egl_version < (1, 1), 'EGL version too low')
    def test_swap_interval(self):
        """Test the swap_interval property with a context."""
        self.dpy.swap_interval = 0
        self.assertEqual(self.dpy.swap_interval, 0)

    @unittest.skipIf(pegl.egl_version < (1, 1), 'EGL version too low')
    def test_swap_interval_too_high(self):
        """Test setting the swap_interval property too high."""
        # This should work, although it will be silently clamped to the
        # maximum.
        self.dpy.swap_interval = self.cfg.max_swap_interval + 1
        # No way to query the actual value!

    @unittest.skipIf(pegl.egl_version < (1, 1), 'EGL version too low')
    def test_swap_interval_too_low(self):
        """Test setting the swap_interval property too low."""
        # This should work, although it will be silently clamped to the
        # minimum.
        self.dpy.swap_interval = self.cfg.min_swap_interval - 1
        # No way to query the actual value!

    def tearDown(self):
        """Finalize EGL objects created for testing."""
        pegl.Context.release_current()
        del self.surf
        del self.ctx
        del self.dpy


class TestNoDisplay(unittest.TestCase):
    """Test the NoDisplay object."""
    @unittest.skipIf(pegl.egl_version < (1, 4), 'EGL version too low')
    def test_extensions(self):
        """Test the extensions property of NoDisplay.

        Accessing this property on NoDisplay is a part of core EGL 1.5,
        but it is also available on EGL 1.4 if the
        EGL_EXT_client_extensions extension is supported. Of course, it
        is impossible to check for this extension without first assuming
        that it exists, so a BadDisplayError is still possible!

        """
        try:
            exts = display.NoDisplay.extensions
        except pegl.BadDisplayError:
            self.assertLess(pegl.egl_version, (1, 5))
        else:
            self.assertIn('EGL_EXT_client_extensions', exts)

    @unittest.skipIf(pegl.egl_version < (1, 4), 'EGL version too low')
    def test_extensions_disjoint(self):
        """Test whether client and display extensions are disjoint."""
        try:
            client_exts = set(display.NoDisplay.extensions.split())
        except pegl.BadDisplayError:
            self.skipTest('client extensions extension not supported')

        dpy = display.Display()
        display_exts = set(dpy.extensions.split())

        self.assertEqual(set(), client_exts & display_exts)

    @unittest.skipIf(pegl.egl_version < (1, 5), 'EGL version too low')
    def test_version(self):
        """Test the version property of NoDisplay.

        Note that accessing this property on NoDisplay was allowed in an
        update to the EGL 1.5 spec, so this may fail on EGL 1.5
        implementations that do not incorporate that update.

        """
        try:
            major, minor, vendor_info = display.NoDisplay.version
        except pegl.BadDisplayError:
            self.skipTest('Implementation does not support 2014-05-21 update '
                          'to EGL 1.5')
        self.assertIsInstance(major, int)
        self.assertIsInstance(minor, int)
        self.assertIsInstance(vendor_info, str)
        self.assertIn((major, minor), known_versions)
        # It's not a failed test if the Pegl-detected version doesn't match
        # with the implementation-reported version, but it's worth noting.
        if (major, minor) != pegl.egl_version:
            warn('Version mismatch: Pegl detected {0}.{1} but implementation '
                 'reported {2[0]}.{2[1]}'.format(major, minor,
                                                 pegl.egl_version))

    @unittest.skipIf(pegl.egl_version < (1, 5), 'EGL version too low')
    def test_version_string(self):
        """Test the version_string property."""
        try:
            vstr = display.NoDisplay.version_string
        except pegl.BadDisplayError:
            self.skipTest('Implementation does not support 2014-05-21 update '
                          'to EGL 1.5')
        self.assertIsInstance(vstr, str)
        self.assertEqual(vstr, '{}.{} {}'.format(*display.NoDisplay.version))


class TestUninitializedDisplay(unittest.TestCase):
    """Test what happens on an uninitialized Display instance."""
    def setUp(self):
        """Set up an uninitialized display for testing."""
        self.dpy = display.Display(init=False)

    def test_client_apis(self):
        """Ensure the client_apis property cannot be accessed."""
        with self.assertRaises(pegl.NotInitializedError):
            self.dpy.client_apis

    def test_extensions(self):
        """Ensure the extensions property cannot be accessed."""
        with self.assertRaises(pegl.NotInitializedError):
            self.dpy.extensions

    def test_initialize(self):
        """Test display initialization."""
        major, minor = self.dpy.initialize()
        self.assertIn((major, minor), known_versions)

        also_major, also_minor, _ = self.dpy.version
        self.assertEqual((major, minor), (also_major, also_minor))

        # It's not a failed test if the Pegl-detected version doesn't match
        # with the implementation-reported version, but it's worth noting.
        if (major, minor) != pegl.egl_version:
            warn('Version mismatch: Pegl detected {0}.{1} but implementation '
                 'reported {2[0]}.{2[1]}'.format(major, minor,
                                                 pegl.egl_version))

    def test_vendor(self):
        """Ensure the vendor property cannot be access."""
        with self.assertRaises(pegl.NotInitializedError):
            self.dpy.vendor

    def test_version(self):
        """Ensure the version property cannot be access."""
        with self.assertRaises(pegl.NotInitializedError):
            self.dpy.version

    def test_version_string(self):
        """Ensure the version_string property cannot be access."""
        with self.assertRaises(pegl.NotInitializedError):
            self.dpy.vendor


class TestTerminatedDisplay(TestUninitializedDisplay):
    """Test what happens on a terminated Display instance.

    A terminated display is equivalent to an uninitialized one, so the
    tests from that test case will be reused.

    """
    def setUp(self):
        """Set up and terminate a display for testing."""
        self.dpy = display.Display()
        self.dpy.terminate()


class TestReleaseThread(unittest.TestCase):
    """Test thread releasing."""
    @unittest.skipIf(pegl.egl_version < (1, 2), 'EGL version too low')
    def test_release_thread(self):
        """Test calling the release_thread() function."""
        display.release_thread()


if __name__ == '__main__':
    unittest.main(verbosity=2)
