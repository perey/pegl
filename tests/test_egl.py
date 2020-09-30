#!/usr/bin/env python3

'''Unit tests for the pegl.egl subpackage.'''

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
from util_test_common import known_versions
from util_test_egl import CONSTANTS, FUNCTIONS, SKIP_HEADER

# Import the module to be tested.
from pegl import egl


class TestEGLVersion(unittest.TestCase):
    """Test the EGL version that Pegl reports."""
    def test_version(self):
        """Check the reported EGL version.

        This test passes if:

        - The EGL version is available, and
        - It matches a known EGL version

        """
        self.assertIn(egl.egl_version, known_versions)


# pylint: disable=unnecessary-pass

class TestEGLConstants(unittest.TestCase):
    """Test whether EGL constants have been defined correctly."""
    pass


class TestEGLFunctions(unittest.TestCase):
    """Test whether EGL functions have been defined correctly."""
    pass


# Dynamically build the tests for each version.
for (major, minor) in known_versions:
    scoped_version = (major, minor)

    @unittest.skipIf(SKIP_HEADER, 'egl.h not found')
    @unittest.skipIf(egl.egl_version < scoped_version, 'EGL version too low')
    def are_constants_defined(self, version=scoped_version):
        # pylint: disable=missing-function-docstring
        for n, (name, value, is_ctypes_type) in enumerate(CONSTANTS[version]):
            with self.subTest(msg=name, n=n):
                egl_constant = getattr(egl, name)
                if is_ctypes_type:
                    self.assertEqual(type(egl_constant), type(value), name)
                    self.assertEqual(egl_constant.value, value.value, name)
                else:
                    self.assertEqual(egl_constant, value, name)
    are_constants_defined.__doc__ = f"""\
Check values of EGL {major}.{minor} constants.

        This test passes if:

        - All EGL {major}.{minor} constants are defined
        - They have the correct values

        """

    @unittest.skipIf(SKIP_HEADER, 'egl.h not found')
    @unittest.skipIf(egl.egl_version >= scoped_version, 'EGL version too high')
    def are_constants_omitted(self, version=scoped_version):
        # pylint: disable=missing-function-docstring
        for n, (name, *_) in enumerate(CONSTANTS[version]):
            with self.subTest(msg=name, n=n):
                self.assertRaises(AttributeError, getattr(egl, name))
    are_constants_omitted.__doc__ = f"""\
Check that EGL {major}.{minor} constants are not defined.

        This test passes if:

        - No EGL {major}.{minor} constants are defined

        """

    setattr(TestEGLConstants, f'test_egl{major}_{minor}_constants_defined',
            are_constants_defined)
    setattr(TestEGLConstants, f'test_egl{major}_{minor}_constants_omitted',
            are_constants_omitted)

    @unittest.skipIf(SKIP_HEADER, 'egl.h not found')
    @unittest.skipIf(egl.egl_version < scoped_version, 'EGL version too low')
    def are_functions_defined(self, version=scoped_version):
        # pylint: disable=missing-function-docstring
        for n, (name, restype) in enumerate(FUNCTIONS[version]):
            with self.subTest(msg=name, n=n):
                egl_fn = getattr(egl, name)
                self.assertEqual(egl_fn.restype, restype, name)
    are_functions_defined.__doc__ = f"""\
Check definitions of EGL {major}.{minor} functions.

        This test passes if:

        - All EGL {major}.{minor} functions are defined.
        - They have the correct return types.

        """

    @unittest.skipIf(SKIP_HEADER, 'egl.h not found')
    @unittest.skipIf(egl.egl_version >= scoped_version, 'EGL version too high')
    def are_functions_omitted(self, version=scoped_version):
        # pylint: disable=missing-function-docstring
        for n, (name, *_) in enumerate(FUNCTIONS[version]):
            with self.subTest(msg=name, n=n):
                self.assertRaises(AttributeError, getattr(egl, name))
    are_functions_omitted.__doc__ = f"""\
Check that EGL {major}.{minor} functions are not defined.

        This test passes if:

        - No EGL {major}.{minor} functions are defined.

        """

    setattr(TestEGLFunctions, f'test_egl{major}_{minor}_constants_defined',
            are_constants_defined)
    setattr(TestEGLFunctions, f'test_egl{major}_{minor}_constants_omitted',
            are_constants_omitted)

if __name__ == '__main__':
    unittest.main(verbosity=2)
