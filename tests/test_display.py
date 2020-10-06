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
import re
import unittest

# Import test utilities.
from util_test_common import known_versions, needs_context, needs_display
from util_test_display import get_native_display, warn_on_version_mismatch

# Import the module to be tested.
import pegl
from pegl import display


@needs_display
class TestDunderMethods(unittest.TestCase):
    """Test the special methods defined on displays."""
    def test_bool_true(self):
        """Ensure a display evaluates as True.

        This test passes if:

        - A display that compares not equal to NoDisplay evaluates to
          True in a boolean context

        """
        self.assertNotEqual(self.dpy, display.NoDisplay)
        self.assertTrue(self.dpy)

    def test_bool_false(self):
        """Ensure that NoDisplay evaluates as False.

        This test passes if:

        - The NoDisplay instance evaluates to False in a boolean context

        """
        self.assertFalse(display.NoDisplay)

    def test_eq_self(self):
        """Ensure a display compares equal to itself.

        This test passes if:

        - A display compares equal to itself

        """
        self.assertEqual(self.dpy, self.dpy)

    def test_neq_somethingelse(self):
        """Ensure a display compares not equal to a non-Display.

        This test passes if:

        - A display compares not equal to an object that happens to be its
          _as_parameter_ attribute

        """
        self.assertNotEqual(self.dpy, self.dpy._as_parameter_)

    def test_repr(self):
        """Check the repr of a display.

        This test passes if:

        - The repr of a display is a string in the format
          'Display(..., EGL ...)'
        - The part represented by the first ellipsis is the display's
          EGLDisplay handle in hexadecimal (at least eight hex digits
          wide)
        - The part represented by the second ellipsis is the display's
          version string

        """
        repr_re = re.compile(r'^Display\((0x[0-9a-f]{8}[0-9a-f]*), '
                             r'EGL (.*)\)$')
        self.assertRegex(repr(self.dpy), repr_re)
        match = repr_re.match(repr(self.dpy))
        self.assertEqual(match.group(1), hex(self.dpy._as_parameter_))
        self.assertEqual(match.group(2), self.dpy.version_string)


class TestClassMethods(unittest.TestCase):
    """Test the class methods defined on the Display class."""
    def test_get_current_display(self):
        """Try fetching the current display when there is none.

        This test passes if:

        - get_current_display can be called
        - It returns a Display instance
        - The instance's _as_parameter_ handle is EGL_NO_DISPLAY
        - The instance compares equal to NoDisplay
        - The instance is NoDisplay

        """
        dpy = display.Display.get_current_display()
        self.assertIsInstance(dpy, display.Display)
        self.assertEqual(dpy._as_parameter_, pegl.egl.EGL_NO_DISPLAY)
        self.assertEqual(dpy, display.NoDisplay)
        self.assertIs(dpy, display.NoDisplay)


class TestDisplayCreation(unittest.TestCase):
    """Test the different ways to get a display."""
    def setUp(self):
        """Get a native display handle to use."""
        self.native_display = get_native_display()

    @unittest.skipIf(pegl.egl_version < (1, 4), 'EGL version too low')
    def test_get_default_display(self):
        """Try getting the default display.

        This test passes if:

        - The Display constructor can be called with no arguments
        - It creates a Display instance

        """
        dpy = display.Display()
        self.assertIsInstance(dpy, display.Display)

    @unittest.skipIf(pegl.egl_version >= (1, 4), 'EGL version too high')
    def test_cant_get_default_display(self):
        """Try getting the default display prior to EGL 1.4.

        This test passes if:

        - The Display constructor cannot be called with no arguments

        """
        with self.assertRaises(ValueError):
            dpy = display.Display()

    def test_get_display(self):
        """Try getting a display using a display handle.

        This test passes if:

        - The Display constructor can be called with a native display
        - It creates a Display instance
        - The instance is not NoDisplay and does not compare equal to it

        """
        dpy = display.Display(self.native_display)
        self.assertIsInstance(dpy, display.Display)
        self.assertIsNot(dpy, display.NoDisplay)
        self.assertNotEqual(dpy, display.NoDisplay)

    def test_get_same_display(self):
        """Ensure two displays with the same handle are the same object.

        This test passes if:

        - Two Display instances created from the same native display
          handle are the same object (compared with ``is``)

        """
        dpy1 = display.Display(self.native_display)
        dpy2 = display.Display(self.native_display)
        self.assertIs(dpy1, dpy2)

    @unittest.skipIf(pegl.egl_version < (1, 4), 'EGL version too low')
    def test_get_same_default_display(self):
        """Ensure two default displays are the same object.

        This test passes if:

        - Two Display instances created with default-display syntax are
          the same object (compared with ``is``)

        """
        dpy1 = display.Display()
        dpy2 = display.Display()
        self.assertIs(dpy1, dpy2)

    @unittest.skipIf(pegl.egl_version < (1, 5), 'EGL version too low')
    def test_get_platform_display(self):
        """Try creating a display belonging to a platform.

        This test passes if:

        - get_platform_display can be called with all platforms defined
          in the pegl.Platform enumeration
        - It returns a Display instance

        """
        if len(pegl.Platform) == 0:
            self.skipTest('no platforms defined')
        for platform in pegl.Platform:
            dpy = display.Display.get_platform_display(platform,
                                                       self.native_display)
            self.assertIsInstance(dpy, display.Display)


@needs_display
class TestMethods(unittest.TestCase):
    """Test methods of displays not elsewhere covered."""
    def test_get_config_count(self):
        """Try to get the number of available configs.

        This test passes if:

        - The get_config_count method can be called
        - It returns a non-negative integer

        """
        count = self.dpy.get_config_count()
        self.assertIsInstance(count, int)
        self.assertGreaterEqual(count, 0)


@needs_display
class TestProperties(unittest.TestCase):
    """Test the properties defined on displays."""
    def test_attribs(self):
        """Check the attribs property.

        This test passes if:

        - The attribs property exists
        - It is an empty mapping
        - It cannot be set
        - Its items cannot be assigned to

        """
        self.assertEqual(self.dpy.attribs, {})
        with self.assertRaises(AttributeError):
            self.dpy.attribs = {'a': 'b'}
        with self.assertRaises(TypeError):
            self.dpy.attribs['fail'] = 'not mutable'

    @unittest.skipIf(pegl.egl_version < (1, 2), 'EGL version too low')
    def test_client_apis(self):
        """Check the client_apis property.

        This test passes if:

        - The client_apis property exists
        - It is a string
        - It contains at least one of 'OpenGL', 'OpenGL_ES', or 'OpenVG'
        - It cannot be set

        """
        self.assertIsInstance(self.dpy.client_apis, str)
        self.assertTrue(any(api in self.dpy.client_apis
                            for api in ('OpenGL', 'OpenGL_ES', 'OpenVG')))
        with self.assertRaises(AttributeError):
            self.dpy.client_apis = 'DirectX'

    def test_extensions(self):
        """Check the extensions property.

        This test passes if:

        - The extensions property exists
        - It is a string
        - If it is non-empty, then it is a space-separated list of
          extension names that all start with EGL_
        - It cannot be set

        """
        self.assertIsInstance(self.dpy.extensions, str)
        self.assertTrue(all(ext.startswith('EGL_')
                            for ext in self.dpy.extensions.split()))
        with self.assertRaises(AttributeError):
            self.dpy.extensions = 'EGL_EXT_not_a_real_extension'

    @unittest.skipIf(pegl.egl_version < (1, 1), 'EGL version too low')
    def test_swap_interval(self):
        """Check the swap_interval property.

        This test passes if:

        - The swap_interval property exists
        - Its value is 1
        - It cannot be set, because there is no current context

        """
        # Property defaults to 1, according to § 3.10.3.
        self.assertEqual(self.dpy.swap_interval, 1)
        # Can't be set without a current context.
        with self.assertRaises(pegl.errors.BadContextError):
            self.dpy.swap_interval = 0

    def test_vendor(self):
        """Check the vendor property.

        This test passes if:

        - The vendor property exists
        - It is a string
        - It cannot be set

        """
        self.assertIsInstance(self.dpy.vendor, str)
        with self.assertRaises(AttributeError):
            self.dpy.vendor = 'ACME'

    def test_version(self):
        """Check the version property.

        This test passes if:

        - The version property exists
        - It is a length-3 sequence of int, int, and string
        - It cannot be set
        - The two ints define a known version of EGL

        """
        major, minor, vendor_info = self.dpy.version
        self.assertIsInstance(major, int)
        self.assertIsInstance(minor, int)
        self.assertIsInstance(vendor_info, str)
        with self.assertRaises(AttributeError):
            self.dpy.version = (2, 50, 'ACME')

        self.assertIn((major, minor), known_versions)

        warn_on_version_mismatch(pegl.egl_version, (major, minor))

    def test_version_string(self):
        """Check the version_string property.

        This test passes if:

        - The version_string property exists
        - It is a string
        - It agrees with the values in the version property
        - It cannot be set

        """
        vstr = self.dpy.version_string
        self.assertIsInstance(vstr, str)
        self.assertEqual(vstr, '{}.{} {}'.format(*self.dpy.version).rstrip())
        with self.assertRaises(AttributeError):
            self.dpy.version_string = '2.50 ACME'


@needs_context
class TestWithContext(unittest.TestCase):
    """Test display properties and methods that require a context."""
    def test_get_current_display(self):
        """Try getting the current display.

        This test passes if:

        - get_current_display can be called
        - It returns a Display instance
        - The instance is the display used

        """
        dpy = display.Display.get_current_display()
        self.assertIsInstance(dpy, display.Display)
        self.assertIs(dpy, self.dpy)

    @unittest.skipIf(pegl.egl_version < (1, 1), 'EGL version too low')
    def test_swap_interval(self):
        """Check the swap_interval property with a context.

        This test passes if:

        - The swap_interval can be set
        - It can then be queried and is equal to the value that was set

        """
        self.dpy.swap_interval = 0
        self.assertEqual(self.dpy.swap_interval, 0)

    @unittest.skipIf(pegl.egl_version < (1, 1), 'EGL version too low')
    def test_swap_interval_too_high(self):
        """Try setting the swap_interval property too high.

        This test passes if:

        - The swap_interval property can be set to a value that is higher
          than allowed by the config.

        """
        # This should work, although it will be silently clamped to the
        # maximum.
        self.dpy.swap_interval = self.cfg.max_swap_interval + 1
        # No way to query the actual value!

    @unittest.skipIf(pegl.egl_version < (1, 1), 'EGL version too low')
    def test_swap_interval_too_low(self):
        """Try setting the swap_interval property too low.

        This test passes if:

        - The swap_interval property can be set to a value that is lower
          than allowed by the config.

        """
        # This should work, although it will be silently clamped to the
        # minimum.
        self.dpy.swap_interval = self.cfg.min_swap_interval - 1
        # No way to query the actual value!


class TestNoDisplay(unittest.TestCase):
    """Test the NoDisplay object."""
    @unittest.skipIf(pegl.egl_version < (1, 4), 'EGL version too low')
    def test_extensions(self):
        """Check the extensions property of NoDisplay.

        Accessing this property on NoDisplay is a part of core EGL 1.5,
        but it is also available on EGL 1.4 if the
        EGL_EXT_client_extensions extension is supported. Of course, it
        is impossible to check for this extension without first assuming
        that it exists, so a BadDisplayError is still possible!

        This test passes if:

        - The extensions property can be queried, is a string, and
          contains the EGL_EXT_client_extensions extension, or
        - The extensions property cannot be queried, and the EGL version
          is below 1.5

        """
        try:
            exts = display.NoDisplay.extensions
        except pegl.BadDisplayError:
            self.assertLess(pegl.egl_version, (1, 5))
        else:
            self.assertIsInstance(exts, str)
            self.assertIn('EGL_EXT_client_extensions', exts)

    @unittest.skipIf(pegl.egl_version < (1, 4), 'EGL version too low')
    def test_extensions_disjoint(self):
        """Check that client and display extensions are disjoint.

        This test passes if:

        - The extensions property can be queried from both NoDisplay and
          an initialized display
        - The two extensions lists are disjoint

        """
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

        This test passes if:

        - The version property exists
        - It is a length-3 sequence of int, int, and string
        - It cannot be set
        - The two ints define a known version of EGL

        """
        try:
            major, minor, vendor_info = display.NoDisplay.version
        except pegl.BadDisplayError:
            self.skipTest('Implementation does not support 2014-05-21 update '
                          'to EGL 1.5')
        self.assertIsInstance(major, int)
        self.assertIsInstance(minor, int)
        self.assertIsInstance(vendor_info, str)
        with self.assertRaises(AttributeError):
            display.NoDisplay.version = (2, 50, 'ACME')

        self.assertIn((major, minor), known_versions)

        warn_on_version_mismatch(pegl.egl_version, (major, minor))

    @unittest.skipIf(pegl.egl_version < (1, 5), 'EGL version too low')
    def test_version_string(self):
        """Test the version_string property.

        This test passes if:

        - The version_string property exists
        - It is a string
        - It agrees with the values in the version property
        - It cannot be set

        """
        try:
            vstr = display.NoDisplay.version_string
        except pegl.BadDisplayError:
            self.skipTest('Implementation does not support 2014-05-21 update '
                          'to EGL 1.5')
        self.assertIsInstance(vstr, str)
        self.assertEqual(vstr, '{}.{} {}'.format(*display.NoDisplay.version))


class TestUninitializedDisplay(unittest.TestCase):
    """Test what happens on an uninitialized display."""
    def setUp(self):
        """Set up an uninitialized display for testing."""
        if pegl.egl_version < (1, 4):
            self.dpy = display.Display(get_native_display(), init=False)
        else:
            self.dpy = display.Display(init=False)

    @unittest.skipIf(pegl.egl_version < (1, 2), 'EGL version too low')
    def test_client_apis(self):
        """Ensure the client_apis property cannot be accessed.

        This test passes if:

        - The client_apis property cannot be queried

        """
        with self.assertRaises(pegl.NotInitializedError):
            self.dpy.client_apis # pylint: disable=pointless-statement

    def test_extensions(self):
        """Ensure the extensions property cannot be accessed.

        This test passes if:

        - The extensions property cannot be queried

        """
        with self.assertRaises(pegl.NotInitializedError):
            self.dpy.extensions # pylint: disable=pointless-statement

    def test_initialize(self):
        """Test display initialization.

        This test passes if:

        - The initialize() method can be called
        - It returns two ints
        - These ints together define a known EGL version
        - The version is the same as that reported by the version property

        """
        major, minor = self.dpy.initialize()
        self.assertIsInstance(major, int)
        self.assertIsInstance(minor, int)
        self.assertIn((major, minor), known_versions)

        also_major, also_minor, _ = self.dpy.version
        self.assertEqual((major, minor), (also_major, also_minor))

        warn_on_version_mismatch(pegl.egl_version, (major, minor))

    def test_vendor(self):
        """Ensure the vendor property cannot be accessed.

        This test passes if:

        - The vendor property cannot be queried

        """
        with self.assertRaises(pegl.NotInitializedError):
            self.dpy.vendor # pylint: disable=pointless-statement

    def test_version(self):
        """Ensure the version property cannot be accessed.

        This test passes if:

        - The version property cannot be queried

        """
        with self.assertRaises(pegl.NotInitializedError):
            self.dpy.version # pylint: disable=pointless-statement

    def test_version_string(self):
        """Ensure the version_string property cannot be accessed.

        This test passes if:

        - The version_string property cannot be queried

        """
        with self.assertRaises(pegl.NotInitializedError):
            self.dpy.vendor # pylint: disable=pointless-statement

    def tearDown(self):
        """Finalize the display used for testing."""
        # Configs don't need finalizing.
        del self.dpy


class TestTerminatedDisplay(TestUninitializedDisplay):
    """Test what happens on a terminated display.

    A terminated display is equivalent to an uninitialized one, so the
    tests from that test case will be reused.

    """
    def setUp(self):
        """Set up and terminate a display for testing."""
        if pegl.egl_version < (1, 4):
            self.dpy = display.Display(get_native_display())
        else:
            self.dpy = display.Display()
        self.dpy.terminate()


class TestReleaseThread(unittest.TestCase):
    """Test thread releasing."""
    @unittest.skipIf(pegl.egl_version < (1, 2), 'EGL version too low')
    def test_release_thread(self): # pylint: disable=no-self-use
        """Try calling the release_thread() function.

        This test passes if:

        - The release_thread function can be called
        - Its return value is None

        """
        result = display.release_thread()
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main(verbosity=2)
