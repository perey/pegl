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
    def test_version(self):
        """Check the reported EGL version.

        This test passes if:

        - The EGL version is available, and
        - It matches a known EGL version

        """
        self.assertIn(egl.egl_version, known_versions)


class TestEGLConstants(unittest.TestCase):
    pass


class TestEGLFunctions(unittest.TestCase):
    pass


# Dynamically build the tests for each version.
for (major, minor) in known_versions:
    @unittest.skipIf(SKIP_HEADER, 'egl.h not found')
    @unittest.skipIf(egl.egl_version < (major, minor), 'EGL version too low')
    def are_constants_defined(self):
        f"""Check values of EGL {major}.{minor} constants.

        This test passes if:

        - All EGL {major}.{minor} constants are defined
        - They have the correct values

        """
        for n, (name, value, is_ctypes_type) in enumerate(CONSTANTS[(major,
                                                                     minor)]):
            with self.subTest(msg=name, n=n):
                egl_constant = getattr(egl, name)
                if is_ctypes_type:
                    self.assertEqual(type(egl_constant), type(value), name)
                    self.assertEqual(egl_constant.value, value.value, name)
                else:
                    self.assertEqual(egl_constant, value, name)

    @unittest.skipIf(SKIP_HEADER, 'egl.h not found')
    @unittest.skipIf(egl.egl_version >= (major, minor), 'EGL version too high')
    def are_constants_omitted(self):
        f"""Check that EGL {major}.{minor} constants are not defined.

        This test passes if:

        - No EGL {major}.{minor} constants are defined

        """
        for n, (name, *_) in enumerate(CONSTANTS[(major, minor)]):
            with self.subTest(msg=name, n=n):
                self.assertRaises(AttributeError, getattr(egl, name))

    setattr(TestEGLConstants, f'test_egl{major}_{minor}_constants_defined',
            are_constants_defined)
    setattr(TestEGLConstants, f'test_egl{major}_{minor}_constants_omitted',
            are_constants_omitted)

    @unittest.skipIf(SKIP_HEADER, 'egl.h not found')
    @unittest.skipIf(egl.egl_version < (major, minor), 'EGL version too low')
    def are_functions_defined(self):
        f"""Check definitions of EGL {major}.{minor} functions.

        This test passes if:

        - All EGL {major}.{minor} functions are defined.
        - They have the correct return types.

        """
        for n, (name, restype) in enumerate(FUNCTIONS[(major, minor)]):
            with self.subTest(msg=name, n=n):
                egl_fn = getattr(egl, name)
                self.assertEqual(egl_fn.restype, restype, name)

    @unittest.skipIf(SKIP_HEADER, 'egl.h not found')
    @unittest.skipIf(egl.egl_version >= (1, 1), 'EGL version too high')
    def are_functions_omitted(self):
        f"""Check that EGL {major}.{minor} functions are not defined.

        This test passes if:

        - No EGL {major}.{minor} functions are defined.

        """
        for n, (name, *_) in enumerate(FUNCTIONS[(major, minor)]):
            with self.subTest(msg=name, n=n):
                self.assertRaises(AttributeError, getattr(egl, name))

    setattr(TestEGLFunctions, f'test_egl{major}_{minor}_constants_defined',
            are_constants_defined)
    setattr(TestEGLFunctions, f'test_egl{major}_{minor}_constants_omitted',
            are_constants_omitted)

if __name__ == '__main__':
    unittest.main(verbosity=2)
