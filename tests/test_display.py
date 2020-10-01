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
from util_test_display import get_native_display

# Import the module to be tested.
import pegl
from pegl import display


class TestClassMethods(unittest.TestCase):
    """Test the class methods defined on the Display class."""
    def test_get_current_display(self):
        """Try fetching the current display when there is none.

        This test passes if:

        - get_current_display can be called
        - It returns a Display instance
        - The instance compares equal to NoDisplay
        - The instance is NoDisplay

        """
        dpy = display.Display.get_current_display()
        self.assertIsInstance(dpy, display.Display)
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

    @unittest.skipIf(pegl.egl_version < (1, 5), 'EGL version too low')
    @unittest.skipIf(len(pegl.Platform) == 0, 'no platforms defined')
    def test_get_platform_display(self):
        """Try creating a display belonging to a platform.

        This test passes if:

        - get_platform_display can be called with all platforms defined
          in the pegl.Platform enumeration
        - It returns a Display instance

        """
        for platform in pegl.Platform:
            dpy = display.Display.get_platform_display(platform,
                                                       self.native_display)
            self.assertIsInstance(dpy, display.Display)


class TestChooseConfig(unittest.TestCase):
    """Test the choose_config method defined on displays."""
    def setUp(self):
        """Set up a display for testing."""
        if pegl.egl_version < (1, 4):
            self.dpy = display.Display(get_native_display())
        else:
            self.dpy = display.Display()

    def check_config_defaults(self, cfg):
        """Check that a config matches the default attributes."""
        self.assertGreaterEqual(cfg.buffer_size, 0)
        self.assertGreaterEqual(cfg.red_size, 0)
        self.assertGreaterEqual(cfg.green_size, 0)
        self.assertGreaterEqual(cfg.blue_size, 0)
        self.assertGreaterEqual(cfg.alpha_size, 0)
        self.assertGreaterEqual(cfg.depth_size, 0)
        self.assertEqual(cfg.level, 0)
        self.assertGreaterEqual(cfg.samples, 0)
        self.assertGreaterEqual(cfg.sample_buffers, 0)
        self.assertGreaterEqual(cfg.stencil_size, 0)
        self.assertIn(pegl.SurfaceTypeFlag.WINDOW, cfg.surface_type)

        if pegl.egl_version >= (1, 2):
            self.assertGreaterEqual(cfg.luminance_size, 0)
            self.assertGreaterEqual(cfg.alpha_mask_size, 0)
            self.assertEqual(cfg.color_buffer_type, pegl.ColorBufferType.RGB)
            self.assertIn(pegl.ClientAPIFlag.OPENGL_ES, cfg.renderable_type)

        if pegl.egl_version >= (1, 3):
            self.assertIn(pegl.ClientAPIFlag.NONE, cfg.conformant)

    def test_choose_config_blank(self):
        """Try choosing configurations with no attributes.

        This test passes if:

        - The choose_config method can be called with an empty dict
        - It returns a (possibly empty) tuple of Config instances
        - Each returned config matches the default requirements

        """
        cfgs = self.dpy.choose_config({})
        for cfg in cfgs:
            self.assertIsInstance(cfg, pegl.Config)
            self.check_config_defaults(cfg)

    def test_choose_config_limited(self):
        """Try choosing a limited number of configurations.

        This test passes if:

        - The choose_config method can be called with an empty dict for
          attributes, and a maximum number of configurations
        - It returns a (possibly empty) tuple of Config instances
        - The number of configs returned is not greater than the number
          requested
        - Each returned config matches the default requirements

        """
        MAX_CONFIGS = 5
        cfgs = self.dpy.choose_config({}, MAX_CONFIGS)
        self.assertLessEqual(len(cfgs), MAX_CONFIGS)
        for cfg in cfgs:
            self.assertIsInstance(cfg, pegl.Config)
            self.check_config_defaults(cfg)

    def test_choose_config_defaults(self):
        """Try choosing configurations with default EGL 1.0 attributes.

        All EGL 1.0 config attributes are supplied, but are explicitly
        equal to their defaults (§ 3.4.1.2, table 3.4).

        This test passes if:

        - The choose_config method can be called with a dict containing
          the mentioned attributes
        - It returns a (possibly empty) tuple of Config instances
        - Each returned config matches the default requirements

        """
        defaults = {
            pegl.ConfigAttrib.BUFFER_SIZE: 0,
            pegl.ConfigAttrib.RED_SIZE: 0,
            pegl.ConfigAttrib.GREEN_SIZE: 0,
            pegl.ConfigAttrib.BLUE_SIZE: 0,
            pegl.ConfigAttrib.ALPHA_SIZE: 0,
            pegl.ConfigAttrib.CONFIG_CAVEAT: pegl.DONT_CARE,
            pegl.ConfigAttrib.CONFIG_ID: pegl.DONT_CARE,
            pegl.ConfigAttrib.DEPTH_SIZE: 0,
            pegl.ConfigAttrib.LEVEL: 0,
            pegl.ConfigAttrib.NATIVE_RENDERABLE: pegl.DONT_CARE,
            pegl.ConfigAttrib.NATIVE_VISUAL_TYPE: pegl.DONT_CARE,
            pegl.ConfigAttrib.SAMPLE_BUFFERS: 0,
            pegl.ConfigAttrib.SAMPLES: 0,
            pegl.ConfigAttrib.STENCIL_SIZE: 0,
            pegl.ConfigAttrib.SURFACE_TYPE: pegl.SurfaceTypeFlag.WINDOW,
            pegl.ConfigAttrib.TRANSPARENT_TYPE: pegl.TransparentType.NONE,
            pegl.ConfigAttrib.TRANSPARENT_RED_VALUE: pegl.DONT_CARE,
            pegl.ConfigAttrib.TRANSPARENT_GREEN_VALUE: pegl.DONT_CARE,
            pegl.ConfigAttrib.TRANSPARENT_BLUE_VALUE: pegl.DONT_CARE,
        }

        cfgs = self.dpy.choose_config(defaults)
        for cfg in cfgs:
            self.assertIsInstance(cfg, pegl.Config)
            self.check_config_defaults(cfg)

    def test_choose_config_nondefaults(self):
        """Try choosing configurations with different attributes.

        A selection of EGL 1.0 config attributes are supplied, set to
        something other than their defaults.

        This test passes if:

        - The choose_config method can be called with a dict containing
          the mentioned attributes
        - It returns a (possibly empty) tuple of Config instances
        - Each returned config matches the specified requirements

        """
        defaults = {
            pegl.ConfigAttrib.BUFFER_SIZE: 16,
            pegl.ConfigAttrib.RED_SIZE: 4,
            pegl.ConfigAttrib.GREEN_SIZE: 4,
            pegl.ConfigAttrib.BLUE_SIZE: 4,
            pegl.ConfigAttrib.ALPHA_SIZE: 4,
            pegl.ConfigAttrib.CONFIG_CAVEAT: pegl.ConfigCaveat.NONE,
            pegl.ConfigAttrib.CONFIG_ID: pegl.DONT_CARE,
            pegl.ConfigAttrib.DEPTH_SIZE: 4,
            pegl.ConfigAttrib.SAMPLE_BUFFERS: 1,
            pegl.ConfigAttrib.SAMPLES: 1,
            pegl.ConfigAttrib.STENCIL_SIZE: 4,
            pegl.ConfigAttrib.SURFACE_TYPE: pegl.SurfaceTypeFlag.PBUFFER,
            pegl.ConfigAttrib.TRANSPARENT_TYPE: pegl.TransparentType.RGB,
        }

        cfgs = self.dpy.choose_config(defaults)
        for cfg in cfgs:
            self.assertIsInstance(cfg, pegl.Config)

            self.assertGreaterEqual(cfg.buffer_size, 16)
            self.assertGreaterEqual(cfg.red_size, 4)
            self.assertGreaterEqual(cfg.green_size, 4)
            self.assertGreaterEqual(cfg.blue_size, 4)
            self.assertGreaterEqual(cfg.alpha_size, 4)
            self.assertGreaterEqual(cfg.depth_size, 4)
            self.assertGreaterEqual(cfg.samples, 1)
            self.assertGreaterEqual(cfg.sample_buffers, 1)
            self.assertGreaterEqual(cfg.stencil_size, 4)
            self.assertIn(pegl.SurfaceTypeFlag.PBUFFER, cfg.surface_type)
            self.assertEqual(cfg.transparent_type, pegl.TransparentType.RGB)

    @unittest.skipIf(pegl.egl_version < (1, 1), 'EGL version too low')
    def test_choose_config_defaults_egl1_1(self):
        """Try choosing configurations with default EGL 1.1 attributes.

        All EGL 1.1 config attributes are supplied, but are explicitly
        equal to their defaults (§ 3.4.1.2, table 3.4).

        This test passes if:

        - The choose_config method can be called with a dict containing
          the mentioned attributes
        - It returns a (possibly empty) tuple of Config instances
        - Each returned config matches the default requirements

        """
        defaults = {
            pegl.ConfigAttrib.BIND_TO_TEXTURE_RGB: pegl.DONT_CARE,
            pegl.ConfigAttrib.BIND_TO_TEXTURE_RGBA: pegl.DONT_CARE,
            pegl.ConfigAttrib.MAX_SWAP_INTERVAL: pegl.DONT_CARE,
            pegl.ConfigAttrib.MIN_SWAP_INTERVAL: pegl.DONT_CARE,
        }

        cfgs = self.dpy.choose_config(defaults)
        for cfg in cfgs:
            self.assertIsInstance(cfg, pegl.Config)
            self.check_config_defaults(cfg)

    @unittest.skipIf(pegl.egl_version < (1, 2), 'EGL version too low')
    def test_choose_config_defaults_egl1_2(self):
        """Try choosing configurations with default EGL 1.2 attributes.

        All EGL 1.2 config attributes are supplied, but are explicitly
        equal to their defaults (§ 3.4.1.2, table 3.4).

        This test passes if:

        - The choose_config method can be called with a dict containing
          the mentioned attributes
        - It returns a (possibly empty) tuple of Config instances
        - Each returned config matches the default requirements

        """
        defaults = {
            pegl.ConfigAttrib.LUMINANCE_SIZE: 0,
            pegl.ConfigAttrib.ALPHA_MASK_SIZE: 0,
            pegl.ConfigAttrib.COLOR_BUFFER_TYPE: pegl.ColorBufferType.RGB,
            pegl.ConfigAttrib.RENDERABLE_TYPE: pegl.ClientAPIFlag.OPENGL_ES,
        }

        cfgs = self.dpy.choose_config(defaults)
        for cfg in cfgs:
            self.assertIsInstance(cfg, pegl.Config)
            self.check_config_defaults(cfg)

    @unittest.skipIf(pegl.egl_version < (1, 3), 'EGL version too low')
    def test_choose_config_defaults_egl1_3(self):
        """Try choosing configurations with default EGL 1.3 attributes.

        All EGL 1.3 config attributes are supplied, but are explicitly
        equal to their defaults (§ 3.4.1.2, table 3.4).

        This test passes if:

        - The choose_config method can be called with a dict containing
          the mentioned attributes
        - It returns a (possibly empty) tuple of Config instances
        - Each returned config matches the default requirements

        """
        defaults = {
            pegl.ConfigAttrib.CONFORMANT: pegl.ClientAPIFlag.NONE,
            pegl.ConfigAttrib.MATCH_NATIVE_PIXMAP: pegl.egl.EGL_NONE,
        }

        cfgs = self.dpy.choose_config(defaults)
        for cfg in cfgs:
            self.assertIsInstance(cfg, pegl.Config)
            self.check_config_defaults(cfg)


class TestProperties(unittest.TestCase):
    """Test the properties defined on displays."""
    def setUp(self):
        """Set up a display for testing."""
        if pegl.egl_version < (1, 4):
            self.dpy = display.Display(get_native_display())
        else:
            self.dpy = display.Display()

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
        # Can't be queried without a current context.
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
        # It's not a failed test if the Pegl-detected version doesn't match
        # with the implementation-reported version, but it's worth noting.
        if (major, minor) != pegl.egl_version:
            warn('Version mismatch: Pegl detected {0}.{1} but implementation '
                 'reported {2[0]}.{2[1]}'.format(major, minor,
                                                 pegl.egl_version))

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
        self.assertEqual(vstr, '{}.{} {}'.format(*self.dpy.version))
        with self.assertRaises(AttributeError):
            self.dpy.version_string = '2.50 ACME'

class TestPropertiesWithContext(unittest.TestCase):
    """Test display properties that require a current context."""
    def setUp(self):
        """Set up a display, config, context, and surface for testing."""
        if pegl.egl_version < (1, 4):
            self.dpy = display.Display(get_native_display())
        else:
            self.dpy = display.Display()
        self.cfg = self.dpy.get_configs(1)[0]
        self.ctx = self.cfg.create_context()
        self.surf = self.cfg.create_pbuffer_surface()
        self.ctx.make_current(self.surf)

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
        # It's not a failed test if the Pegl-detected version doesn't match
        # with the implementation-reported version, but it's worth noting.
        if (major, minor) != pegl.egl_version:
            warn('Version mismatch: Pegl detected {0}.{1} but implementation '
                 'reported {2[0]}.{2[1]}'.format(major, minor,
                                                 pegl.egl_version))

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

        # It's not a failed test if the Pegl-detected version doesn't match
        # with the implementation-reported version, but it's worth noting.
        if (major, minor) != pegl.egl_version:
            warn('Version mismatch: Pegl detected {0}.{1} but implementation '
                 'reported {2[0]}.{2[1]}'.format(major, minor,
                                                 pegl.egl_version))

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
