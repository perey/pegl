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
import re
import unittest

# Import test utilities.
from util_test_common import needs_config, needs_display
from util_test_config import has_unknown_apis, has_unknown_surfaces

# Import the module to be tested.
import pegl


@needs_display
class TestGetConfig(unittest.TestCase):
    """Test the get_configs method defined on displays."""
    def test_get_configs(self):
        """Try to get all available configs.

        This test passes if:

        - The get_configs method can be called with no argument
        - It returns a tuple of configs
        - The tuple's size is equal to the value returned by
          get_config_count

        """
        cfgs = self.dpy.get_configs()
        self.assertEqual(len(cfgs), self.dpy.get_config_count())
        self.assertTrue(all(isinstance(cfg, pegl.Config) for cfg in cfgs))

    def test_get_configs_limited(self):
        """Try to get a limited number of configs.

        This test passes if:

        - The get_configs method can be called with an integer argument
        - It returns a tuple of configs
        - The tuple's size is equal to the supplied argument, given that
          this is less than the value returned by get_config_count

        """
        max_configs = self.dpy.get_config_count() // 2
        cfgs = self.dpy.get_configs(max_configs)
        self.assertEqual(len(cfgs), max_configs)
        self.assertTrue(all(isinstance(cfg, pegl.Config) for cfg in cfgs))


@needs_display
class TestChooseConfig(unittest.TestCase):
    """Test the choose_config method defined on displays."""
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
          attributes, and a limit on the number of configurations
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


@needs_config
class TestMethods(unittest.TestCase):
    """Test methods of config instances not tested elsewhere."""
    def test_repr(self):
        """Check the repr of a config.

        This test passes if:

        - The repr of a config is a string in the format
          '<Config: ...>'
        - The part represented by the ellipsis is the config's EGLConfig
          handle in hexadecimal (at least eight hex digits wide)

        """
        repr_re = re.compile(r'^<Config: (0x[0-9a-f]{8}[0-9a-f]*)>$')
        self.assertRegex(repr(self.cfg), repr_re)
        match = repr_re.match(repr(self.cfg))
        self.assertEqual(match.group(1), hex(self.cfg._as_parameter_))

    def test_str(self):
        """Check the string form of a config.

        This test passes if:

        - Calling str on a config producess a string in the format
          'Config(... at ..., ...-bit ...)'
        - The part represented by the first ellipsis is the config's
          config_id
        - The part represented by the second ellipsis is the config's
          EGLConfig handle in hexadecimal (at least eight hex digits
          wide)
        - The part represented by the third ellipsis is the config's
          color buffer bit size (buffer_size)
        - The part represented by the fourth ellipsis is the config's color
          type (RGB, RGBA, L, or LA)

        """
        str_re = re.compile(r'^<Config #([0-9]+): '
                             '(0x[0-9a-f]{8}[0-9a-f]*), '
                             r'([0-9]+)-bit (RGBA?|LA?)')
        self.assertRegex(str(self.cfg), str_re)
        match = str_re.match(str(self.cfg))
        self.assertEqual(match.group(1), str(self.cfg.config_id))
        self.assertEqual(match.group(2), hex(self.cfg._as_parameter_))
        self.assertEqual(match.group(3), str(self.cfg.buffer_size))
        try:
            expected = ('RGB' if (self.cfg.color_buffer_type ==
                                  pegl.ColorBufferType.RGB) else
                        'L')
        except AttributeError:
            self.assertLess(pegl.egl_version, (1, 2))
            expected = 'RGB'
        if self.cfg.alpha_size > 0:
            expected += 'A'
        self.assertEqual(match.group(4), expected)


@needs_config
class TestProperties(unittest.TestCase):
    """Test the properties defined on configs."""
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

    def test_blue_size(self):
        """Check the blue_size property.

        This test passes if:

        - The blue_size property exists
        - It is a non-negative integer
        - It cannot be set

        """
        self.assertIsInstance(self.cfg.blue_size, int)
        self.assertGreaterEqual(self.cfg.blue_size, 0)
        with self.assertRaises(AttributeError):
            self.cfg.blue_size = 16

    def test_buffer_size(self):
        """Check the buffer_size property.

        This test passes if:

        - The buffer_size property exists
        - It is a non-negative integer
        - It cannot be set

        """
        self.assertIsInstance(self.cfg.buffer_size, int)
        self.assertGreaterEqual(self.cfg.buffer_size, 0)
        with self.assertRaises(AttributeError):
            self.cfg.buffer_size = 16

    @unittest.skipIf(pegl.egl_version < (1, 2), 'EGL version too low')
    def test_color_buffer_type(self):
        """Check the color_buffer_type property.

        This test passes if:

        - The color_buffer_type property exists
        - It is a value from the ColorBufferType enum
        - It cannot be set

        """
        self.assertIsInstance(self.cfg.color_buffer_type,
                              pegl.enums.ColorBufferType)
        with self.assertRaises(AttributeError):
            self.cfg.color_buffer_type = pegl.enums.ColorBufferType.LUMINANCE

    def test_config_caveat(self):
        """Check the config_caveat property.

        This test passes if:

        - The config_caveat property exists
        - It is None, or a value from the ConfigCaveat enum
        - It cannot be set

        """
        self.assertTrue(isinstance(self.cfg.config_caveat,
                                   pegl.enums.ConfigCaveat) or
                        self.cfg.config_caveat is None)
        with self.assertRaises(AttributeError):
            self.cfg.config_caveat = pegl.enums.ConfigCaveat.SLOW

    def test_config_id(self):
        """Check the config_id property.

        This test passes if:

        - The config_id property exists
        - It is an integer
        - It cannot be set

        """
        self.assertIsInstance(self.cfg.config_id, int)
        with self.assertRaises(AttributeError):
            self.cfg.green_size = -1

    @unittest.skipIf(pegl.egl_version < (1, 3), 'EGL version too low')
    def test_conformant(self):
        """Check the conformant property.

        This test passes if:

        - The conformant property exists
        - It is a flag (or combination of flags) from ClientAPIFlag
        - It cannot be set

        """
        self.assertIsInstance(self.cfg.conformant, pegl.enums.ClientAPIFlag)
        self.assertFalse(has_unknown_apis(self.cfg.conformant))
        with self.assertRaises(AttributeError):
            self.cfg.conformant |= pegl.enums.ClientAPIFlag.OPENVG

    def test_depth_size(self):
        """Check the depth_size property.

        This test passes if:

        - The depth_size property exists
        - It is a non-negative integer
        - It cannot be set

        """
        self.assertIsInstance(self.cfg.depth_size, int)
        self.assertGreaterEqual(self.cfg.depth_size, 0)
        with self.assertRaises(AttributeError):
            self.cfg.depth_size = 16

    def test_green_size(self):
        """Check the green_size property.

        This test passes if:

        - The green_size property exists
        - It is a non-negative integer
        - It cannot be set

        """
        self.assertIsInstance(self.cfg.green_size, int)
        self.assertGreaterEqual(self.cfg.green_size, 0)
        with self.assertRaises(AttributeError):
            self.cfg.green_size = 16

    def test_level(self):
        """Check the level property.

        This test passes if:

        - The level property exists
        - It is an integer
        - It cannot be set

        """
        self.assertIsInstance(self.cfg.level, int)
        with self.assertRaises(AttributeError):
            self.cfg.level = -1

    @unittest.skipIf(pegl.egl_version < (1, 2), 'EGL version too low')
    def test_luminance_size(self):
        """Check the luminance_size property.

        This test passes if:

        - The luminance_size property exists
        - It is a non-negative integer
        - It cannot be set

        """
        self.assertIsInstance(self.cfg.luminance_size, int)
        self.assertGreaterEqual(self.cfg.luminance_size, 0)
        with self.assertRaises(AttributeError):
            self.cfg.luminance_size = 16

    def test_max_pbuffer_height(self):
        """Check the max_pbuffer_height property.

        This test passes if:

        - The max_pbuffer_height property exists
        - It is a non-negative integer
        - It cannot be set

        """
        self.assertIsInstance(self.cfg.max_pbuffer_height, int)
        self.assertGreaterEqual(self.cfg.max_pbuffer_height, 0)
        with self.assertRaises(AttributeError):
            self.cfg.max_pbuffer_height = 768

    def test_max_pbuffer_pixels(self):
        """Check the max_pbuffer_pixels property.

        This test passes if:

        - The max_pbuffer_pixels property exists
        - It is a non-negative integer
        - It is equal to max_pbuffer_height × max_pbuffer_width
        - It cannot be set

        """
        self.assertIsInstance(self.cfg.max_pbuffer_pixels, int)
        self.assertEqual(self.cfg.max_pbuffer_pixels,
                         self.cfg.max_pbuffer_height *
                         self.cfg.max_pbuffer_width)
        with self.assertRaises(AttributeError):
            self.cfg.max_pbuffer_pixels = 786432

    def test_max_pbuffer_width(self):
        """Check the max_pbuffer_width property.

        This test passes if:

        - The max_pbuffer_width property exists
        - It is a non-negative integer
        - It cannot be set

        """
        self.assertIsInstance(self.cfg.max_pbuffer_width, int)
        self.assertGreaterEqual(self.cfg.max_pbuffer_width, 0)
        with self.assertRaises(AttributeError):
            self.cfg.max_pbuffer_width = 1024

    @unittest.skipIf(pegl.egl_version < (1, 1), 'EGL version too low')
    def test_max_swap_interval(self):
        """Check the max_swap_interval property.

        This test passes if:

        - The max_swap_interval property exists
        - It is a non-negative integer
        - It cannot be set

        """
        self.assertIsInstance(self.cfg.max_swap_interval, int)
        self.assertGreaterEqual(self.cfg.max_swap_interval, 0)
        with self.assertRaises(AttributeError):
            self.cfg.max_swap_interval = 60

    @unittest.skipIf(pegl.egl_version < (1, 1), 'EGL version too low')
    def test_min_swap_interval(self):
        """Check the min_swap_interval property.

        This test passes if:

        - The min_swap_interval property exists
        - It is a non-negative integer
        - It is not greater than max_swap_interval
        - It cannot be set

        """
        self.assertIsInstance(self.cfg.min_swap_interval, int)
        self.assertGreaterEqual(self.cfg.min_swap_interval, 0)
        self.assertGreaterEqual(self.cfg.max_swap_interval,
                                self.cfg.min_swap_interval)
        with self.assertRaises(AttributeError):
            self.cfg.min_swap_interval = 60

    def test_native_renderable(self):
        """Check the native_renderable property.

        This test passes if:

        - The native_renderable property exists
        - It is a boolean
        - It cannot be set

        """
        self.assertIsInstance(self.cfg.native_renderable, bool)
        with self.assertRaises(AttributeError):
            self.cfg.native_renderable = True

    def test_native_visual_id(self):
        """Check the native_visual_id property.

        This test passes if:

        - The native_visual_id property exists
        - It is an integer
        - It cannot be set

        """
        self.assertIsInstance(self.cfg.native_visual_id, int)
        with self.assertRaises(AttributeError):
            self.cfg.native_visual_id = -1

    def test_native_visual_type(self):
        """Check the native_visual_type property.

        This test passes if:

        - The native_visual_type property exists
        - It cannot be set

        """
        self.cfg.native_visual_type # pylint: disable=pointless-statement
        with self.assertRaises(AttributeError):
            self.cfg.native_visual_type = None

    def test_red_size(self):
        """Check the red_size property.

        This test passes if:

        - The red_size property exists
        - It is a non-negative integer
        - It cannot be set

        """
        self.assertIsInstance(self.cfg.red_size, int)
        self.assertGreaterEqual(self.cfg.red_size, 0)
        with self.assertRaises(AttributeError):
            self.cfg.red_size = 16

    @unittest.skipIf(pegl.egl_version < (1,23), 'EGL version too low')
    def test_renderable_type(self):
        """Check the renderable_type property.

        This test passes if:

        - The renderable_type property exists
        - It is a flag (or combination of flags) from ClientAPIFlag
        - It cannot be set

        """
        self.assertIsInstance(self.cfg.renderable_type,
                              pegl.enums.ClientAPIFlag)
        self.assertFalse(has_unknown_apis(self.cfg.renderable_type))
        with self.assertRaises(AttributeError):
            self.cfg.renderable_type |= pegl.enums.ClientAPIFlag.OPENVG

    def test_samples(self):
        """Check the samples property.

        This test passes if:

        - The samples property exists
        - It is a non-negative integer
        - It cannot be set

        """
        self.assertIsInstance(self.cfg.samples, int)
        self.assertGreaterEqual(self.cfg.samples, 0)
        with self.assertRaises(AttributeError):
            self.cfg.samples = 4

    def test_sample_buffers(self):
        """Check the sample_buffers property.

        This test passes if:

        - The sample_buffers property exists
        - It is an integer, either 0 or 1
        - It cannot be set

        """
        self.assertIsInstance(self.cfg.sample_buffers, int)
        self.assertIn(self.cfg.sample_buffers, (0, 1))
        with self.assertRaises(AttributeError):
            self.cfg.sample_buffers = 1

    def test_stencil_size(self):
        """Check the stencil_size property.

        This test passes if:

        - The stencil_size property exists
        - It is a non-negative integer
        - It cannot be set

        """
        self.assertIsInstance(self.cfg.stencil_size, int)
        self.assertGreaterEqual(self.cfg.stencil_size, 0)
        with self.assertRaises(AttributeError):
            self.cfg.stencil_size = 16

    def test_surface_type(self):
        """Check the surface_type property.

        This test passes if:

        - The surface_type property exists
        - It is a flag (or combination of flags) from SurfaceTypeFlag
        - It cannot be set

        """
        self.assertIsInstance(self.cfg.surface_type,
                              pegl.enums.SurfaceTypeFlag)
        self.assertFalse(has_unknown_surfaces(self.cfg.surface_type))
        with self.assertRaises(AttributeError):
            self.cfg.surface_type |= pegl.enums.SurfaceTypeFlag.PBUFFER

    def test_transparent_blue_value(self):
        """Check the transparent_blue_value property.

        This test passes if:

        - The transparent_blue_value property exists
        - It is an integer
        - If transparent_type is RGB, it is between 0 and
          2 ** blue_size - 1, inclusive
        - It cannot be set

        """
        self.assertIsInstance(self.cfg.transparent_blue_value, int)
        if self.cfg.transparent_type == pegl.enums.TransparentType.RGB:
            self.assertGreaterEqual(self.cfg.transparent_blue_value, 0)
            self.assertLessEqual(self.cfg.transparent_blue_value,
                                 2 ** self.cfg.blue_size - 1)
        with self.assertRaises(AttributeError):
            self.cfg.transparent_blue_value = 0xFF

    def test_transparent_green_value(self):
        """Check the transparent_green_value property.

        This test passes if:

        - The transparent_green_value property exists
        - It is an integer
        - If transparent_type is RGB, it is between 0 and
          2 ** green_size - 1, inclusive
        - It cannot be set

        """
        self.assertIsInstance(self.cfg.transparent_green_value, int)
        if self.cfg.transparent_type == pegl.enums.TransparentType.RGB:
            self.assertGreaterEqual(self.cfg.transparent_green_value, 0)
            self.assertLessEqual(self.cfg.transparent_green_value,
                                 2 ** self.cfg.green_size - 1)
        with self.assertRaises(AttributeError):
            self.cfg.transparent_green_value = 0x00

    def test_transparent_red_value(self):
        """Check the transparent_red_value property.

        This test passes if:

        - The transparent_red_value property exists
        - It is an integer
        - If transparent_type is RGB, it is between 0 and
          2 ** red_size - 1, inclusive
        - It cannot be set

        """
        self.assertIsInstance(self.cfg.transparent_red_value, int)
        if self.cfg.transparent_type == pegl.enums.TransparentType.RGB:
            self.assertGreaterEqual(self.cfg.transparent_red_value, 0)
            self.assertLessEqual(self.cfg.transparent_red_value,
                                 2 ** self.cfg.red_size - 1)
        with self.assertRaises(AttributeError):
            self.cfg.transparent_red_value = 0xFF

    def test_transparent_type(self):
        """Check the transparent_type property.

        This test passes if:

        - The transparent_type property exists
        - It is None, or a value from the TransparentType enum
        - It cannot be set

        """
        self.assertTrue(isinstance(self.cfg.transparent_type,
                                   pegl.enums.TransparentType) or
                        self.cfg.transparent_type is None)
        with self.assertRaises(AttributeError):
            self.cfg.transparent_type = pegl.enums.TransparentType.RGB


if __name__ == '__main__':
    unittest.main(verbosity=2)
