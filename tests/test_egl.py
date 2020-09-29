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
#
# This file is based on the header file egl.h, which carries the following
# copyright statement and licensing information:
#
#     Copyright (c) 2013-2017 The Khronos Group Inc.
#
#     Permission is hereby granted, free of charge, to any person obtaining a
#     copy of this software and/or associated documentation files (the
#     "Materials"), to deal in the Materials without restriction, including
#     without limitation the rights to use, copy, modify, merge, publish,
#     distribute, sublicense, and/or sell copies of the Materials, and to
#     permit persons to whom the Materials are furnished to do so, subject to
#     the following conditions:
#
#     The above copyright notice and this permission notice shall be included
#     in all copies or substantial portions of the Materials.
#
#     THE MATERIALS ARE PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#     EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#     MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#     IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
#     CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#     TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#     MATERIALS OR THE USE OR OTHER DEALINGS IN THE MATERIALS.

from __future__ import annotations

# Standard library imports.
import ctypes
from pathlib import Path
import re
from typing import Any, TextIO
import unittest

# Import the module to be tested.
from pegl import egl

# Define EGL types per § 2.1.1
egl_types = {
    'EGLBoolean': ctypes.c_bool,
    'EGLint':     ctypes.c_int,
    'EGLAttrib':  ctypes.c_ssize_t, # ...because ctypes doesn't have intptr_t
    'EGLTime':    ctypes.c_uint64,
    # Opaque handles all represented as void *
    'EGLContext': ctypes.c_void_p,
    'EGLImage':   ctypes.c_void_p,
    'EGLSurface': ctypes.c_void_p,
    'EGLSync':    ctypes.c_void_p,
    # Not listed in § 2.1.1 for some reason
    'EGLenum':    ctypes.c_uint,
    'EGLDisplay': ctypes.c_void_p,
    # Platform-defined types represented as void *
    'EGLNativeDisplayType': ctypes.c_void_p,
    # And here's a unique one from the source code!
    '__eglMustCastToProperFunctionPointerType': ctypes.c_void_p,
}

# Parse egl.h to get constants.
def parse_c_int(s: str) -> int:
    """Parse a C integer literal."""
    # Strip a positive or negative prefix and save it for later.
    negative = False
    sans_prefix = s.lstrip('+-')
    if sans_prefix != s:
        negative = (s[0] == '-')

    # U (unsigned) and L (long) suffixes can be ignored.
    sans_suffix = sans_prefix.rstrip('UuLl')

    if sans_suffix.startswith('0x'):
        # Hexadecimal literal.
        base = 16
    elif sans_suffix.startswith('0b'):
        # Binary literal.
        base = 2
    elif sans_suffix.startswith('0'):
        # Octal literal.
        base = 8
    else:
        # Decimal literal.
        assert sans_suffix[0] in '123456789', s
        base = 10

    return int(sans_suffix, base) * (-1 if negative else 1)

define_pattern = re.compile(r'#define\s+(?P<defname>\S+)\s+(?P<defval>\S+)')
cast_pattern = re.compile(r'EGL_CAST\((?P<casttype>\w+),\s*(?P<castval>\S+)\)')
proto_pattern = re.compile(r'EGLAPI\s+(?P<restype>\S+)\s+'
                           r'EGLAPIENTRY\s+(?P<procname>\w+)\s*') # Arguments?

def get_defines(file: TextIO, guard_name: str) -> tuple[
                                                      list[tuple[str, Any,
                                                                 bool]],
                                                      list[tuple[str, Any]]
                                                  ]:
    """Get C definitions within a guard block.

    The block must start with::

        #ifndef <guard_name>

    ...and end with::

        #endif /* <guard_name> */

    All values #define'd between these lines (except #define <guard_name>)
    are returned in a list. All functions prototyped between these lines are
    returned in another list.

    Keyword arguments:
        file -- An open file (or file-like object) of C code to search.
        guard_name -- The name used at the start and end of the guard
            block.

    Returns:
        Two lists, one of #define'd constants, and one of prototyped
        functions.

        The constants list is a list of 3-tuples. The first element of
        each tuple is the name that is being defined, and the second
        element is its value. The third element is a boolean indicating
        whether the value is wrapped in a ctypes type, which should have
        its value extracted before doing comparisons (because, for
        instance, c_long(3) != c_long(3)).

        The prototypes list is a list of 2-tuples. The first element of
        each type is the name of the function, and the second is its
        return value.

    """
    escaped_name = re.escape(guard_name)
    start_pattern = r'#ifndef\s+' + escaped_name
    end_pattern = r'#endif\s+/\*\s*' + escaped_name + r'\s*\*/'

    constants = []
    prototypes = []

    in_block = False
    for line in file:
        # Search for the start of the block.
        if not in_block:
            if re.match(start_pattern, line):
                in_block = True
            continue

        # Check whether this line is a #define, a function prototype, or the
        # end of the block.
        define = define_pattern.match(line)
        proto = proto_pattern.match(line)
        if define:
            defname, defval = define.group('defname'), define.group('defval')

            # Skip the line that defines the guard name
            if defname == guard_name:
                continue

            # Parse the defined value.
            cast = cast_pattern.match(defval)
            if cast:
                # A cast to an EGL type. The value being cast is an integer
                # literal.
                casttype, castval = (cast.group('casttype'),
                                     cast.group('castval'))
                parsed_val = egl_types[casttype](parse_c_int(castval))
                is_ctypes_type = True
            else:
                parsed_val = parse_c_int(defval)
                is_ctypes_type = False

            constants.append((defname, parsed_val, is_ctypes_type))
        elif proto:
            procname = proto.group('procname')
            restype = egl_types[proto.group('restype')]

            prototypes.append((procname, restype))
        elif re.match(end_pattern, line):
            return constants, prototypes

SKIP_HEADER = False
egl_header = Path(__file__).parent / 'egl.h'

try:
    with egl_header.open(mode='rt') as f:
        # Note that this assumes that versions are defined in order.
        EGL1_0_CONSTANTS, EGL1_0_FUNCTIONS = get_defines(f, 'EGL_VERSION_1_0')
        EGL1_1_CONSTANTS, EGL1_1_FUNCTIONS = get_defines(f, 'EGL_VERSION_1_1')
        EGL1_2_CONSTANTS, EGL1_2_FUNCTIONS = get_defines(f, 'EGL_VERSION_1_2')
        EGL1_3_CONSTANTS, EGL1_3_FUNCTIONS = get_defines(f, 'EGL_VERSION_1_3')
        EGL1_4_CONSTANTS, EGL1_4_FUNCTIONS = get_defines(f, 'EGL_VERSION_1_4')
        EGL1_5_CONSTANTS, EGL1_5_FUNCTIONS = get_defines(f, 'EGL_VERSION_1_5')
except FileNotFoundError:
    SKIP_HEADER = True

# The tests.
class TestEGLVersion(unittest.TestCase):
    def test_version(self):
        """Check the reported EGL version.

        This test passes if:

        - The EGL version is available, and
        - It matches a known EGL version

        """
        self.assertIn(egl.egl_version, ((1, 0),
                                        (1, 1),
                                        (1, 2),
                                        (1, 3),
                                        (1, 4),
                                        (1, 5)))


class TestEGLConstants(unittest.TestCase):
    @unittest.skipIf(SKIP_HEADER, 'egl.h not found')
    def test_egl1_0_constants_defined(self):
        """Check values of EGL 1.0 constants.

        This test passes if:

        - All EGL 1.0 constants are defined
        - They have the correct values

        """
        for n, (name, value, is_ctypes_type) in enumerate(EGL1_0_CONSTANTS):
            with self.subTest(msg=name, n=n):
                egl_constant = getattr(egl, name)
                if is_ctypes_type:
                    self.assertEqual(type(egl_constant), type(value), name)
                    self.assertEqual(egl_constant.value, value.value, name)
                else:
                    self.assertEqual(egl_constant, value, name)

    @unittest.skipIf(SKIP_HEADER, 'egl.h not found')
    @unittest.skipIf(egl.egl_version < (1, 1), 'EGL version too low')
    def test_egl1_1_constants_defined(self):
        """Check values of EGL 1.1 constants.

        This test passes if:

        - All EGL 1.1 constants are defined
        - They have the correct values

        """
        for n, (name, value, is_ctypes_type) in enumerate(EGL1_1_CONSTANTS):
            with self.subTest(msg=name, n=n):
                egl_constant = getattr(egl, name)
                if is_ctypes_type:
                    self.assertEqual(type(egl_constant), type(value), name)
                    self.assertEqual(egl_constant.value, value.value, name)
                else:
                    self.assertEqual(egl_constant, value, name)

    @unittest.skipIf(SKIP_HEADER, 'egl.h not found')
    @unittest.skipIf(egl.egl_version >= (1, 1), 'EGL version too high')
    def test_egl1_1_constants_omitted(self):
        """Check that EGL 1.1 constants are not defined.

        This test passes if:

        - No EGL 1.1 constants are defined

        """
        for n, (name, *_) in enumerate(EGL1_1_CONSTANTS):
            with self.subTest(msg=name, n=n):
                self.assertRaises(AttributeError, getattr(egl, name))

    @unittest.skipIf(SKIP_HEADER, 'egl.h not found')
    @unittest.skipIf(egl.egl_version < (1, 2), 'EGL version too low')
    def test_egl1_2_constants_defined(self):
        """Check values of EGL 1.1 constants.

        This test passes if:

        - All EGL 1.2 constants are defined
        - They have the correct values

        """
        for n, (name, value, is_ctypes_type) in enumerate(EGL1_2_CONSTANTS):
            with self.subTest(msg=name, n=n):
                egl_constant = getattr(egl, name)
                if is_ctypes_type:
                    self.assertEqual(type(egl_constant), type(value), name)
                    self.assertEqual(egl_constant.value, value.value, name)
                else:
                    self.assertEqual(egl_constant, value, name)

    @unittest.skipIf(SKIP_HEADER, 'egl.h not found')
    @unittest.skipIf(egl.egl_version >= (1, 2), 'EGL version too high')
    def test_egl1_2_constants_omitted(self):
        """Check that EGL 1.2 constants are not defined.

        This test passes if:

        - No EGL 1.2 constants are defined

        """
        for n, (name, *_) in enumerate(EGL1_2_CONSTANTS):
            with self.subTest(msg=name, n=n):
                self.assertRaises(AttributeError, getattr(egl, name))

    @unittest.skipIf(SKIP_HEADER, 'egl.h not found')
    @unittest.skipIf(egl.egl_version < (1, 3), 'EGL version too low')
    def test_egl1_3_constants_defined(self):
        """Check values of EGL 1.3 constants.

        This test passes if:

        - All EGL 1.3 constants are defined
        - They have the correct values

        """
        for n, (name, value, is_ctypes_type) in enumerate(EGL1_3_CONSTANTS):
            with self.subTest(msg=name, n=n):
                egl_constant = getattr(egl, name)
                if is_ctypes_type:
                    self.assertEqual(type(egl_constant), type(value), name)
                    self.assertEqual(egl_constant.value, value.value, name)
                else:
                    self.assertEqual(egl_constant, value, name)

    @unittest.skipIf(SKIP_HEADER, 'egl.h not found')
    @unittest.skipIf(egl.egl_version >= (1, 3), 'EGL version too high')
    def test_egl1_3_constants_omitted(self):
        """Check that EGL 1.3 constants are not defined.

        This test passes if:

        - No EGL 1.3 constants are defined

        """
        for n, (name, *_) in enumerate(EGL1_3_CONSTANTS):
            with self.subTest(msg=name, n=n):
                self.assertRaises(AttributeError, getattr(egl, name))

    @unittest.skipIf(SKIP_HEADER, 'egl.h not found')
    @unittest.skipIf(egl.egl_version < (1, 4), 'EGL version too low')
    def test_egl1_4_constants_defined(self):
        """Check values of EGL 1.4 constants.

        This test passes if:

        - All EGL 1.4 constants are defined
        - They have the correct values

        """
        for n, (name, value, is_ctypes_type) in enumerate(EGL1_4_CONSTANTS):
            with self.subTest(msg=name, n=n):
                egl_constant = getattr(egl, name)
                if is_ctypes_type:
                    self.assertEqual(type(egl_constant), type(value), name)
                    self.assertEqual(egl_constant.value, value.value, name)
                else:
                    self.assertEqual(egl_constant, value, name)

    @unittest.skipIf(SKIP_HEADER, 'egl.h not found')
    @unittest.skipIf(egl.egl_version >= (1, 4), 'EGL version too high')
    def test_egl1_4_constants_omitted(self):
        """Check that EGL 1.4 constants are not defined.

        This test passes if:

        - No EGL 1.4 constants are defined

        """
        for n, (name, *_) in enumerate(EGL1_4_CONSTANTS):
            with self.subTest(msg=name, n=n):
                self.assertRaises(AttributeError, getattr(egl, name))

    @unittest.skipIf(SKIP_HEADER, 'egl.h not found')
    @unittest.skipIf(egl.egl_version < (1, 5), 'EGL version too low')
    def test_egl1_5_constants_defined(self):
        """Check values of EGL 1.5 constants.

        This test passes if:

        - All EGL 1.5 constants are defined
        - They have the correct values

        """
        for n, (name, value, is_ctypes_type) in enumerate(EGL1_5_CONSTANTS):
            with self.subTest(msg=name, n=n):
                egl_constant = getattr(egl, name)
                if is_ctypes_type:
                    self.assertEqual(type(egl_constant), type(value), name)
                    self.assertEqual(egl_constant.value, value.value, name)
                else:
                    self.assertEqual(egl_constant, value, name)

    @unittest.skipIf(SKIP_HEADER, 'egl.h not found')
    @unittest.skipIf(egl.egl_version >= (1, 5), 'EGL version too high')
    def test_egl1_5_constants_omitted(self):
        """Check that EGL 1.5 constants are not defined.

        This test passes if:

        - No EGL 1.5 constants are defined

        """
        for n, (name, *_) in enumerate(EGL1_5_CONSTANTS):
            with self.subTest(msg=name, n=n):
                self.assertRaises(AttributeError, getattr(egl, name))


class TestEGLFunctions(unittest.TestCase):
    @unittest.skipIf(SKIP_HEADER, 'egl.h not found')
    def test_egl1_0_functions_defined(self):
        """Check definitions of EGL 1.0 functions.

        This test passes if:

        - All EGL 1.0 functions are defined.
        - They have the correct return types.

        """
        for n, (name, restype) in enumerate(EGL1_0_FUNCTIONS):
            with self.subTest(msg=name, n=n):
                egl_fn = getattr(egl, name)
                self.assertEqual(egl_fn.restype, restype, name)

    @unittest.skipIf(SKIP_HEADER, 'egl.h not found')
    @unittest.skipIf(egl.egl_version < (1, 1), 'EGL version too low')
    def test_egl1_1_functions_defined(self):
        """Check definitions of EGL 1.1 functions.

        This test passes if:

        - All EGL 1.1 functions are defined.
        - They have the correct return types.

        """
        for n, (name, restype) in enumerate(EGL1_1_FUNCTIONS):
            with self.subTest(msg=name, n=n):
                egl_fn = getattr(egl, name)
                self.assertEqual(egl_fn.restype, restype, name)

    @unittest.skipIf(SKIP_HEADER, 'egl.h not found')
    @unittest.skipIf(egl.egl_version >= (1, 1), 'EGL version too high')
    def test_egl1_1_functions_omitted(self):
        """Check that EGL 1.1 functions are not defined.

        This test passes if:

        - No EGL 1.1 functions are defined.

        """
        for n, (name, *_) in enumerate(EGL1_1_FUNCTIONS):
            with self.subTest(msg=name, n=n):
                self.assertRaises(AttributeError, getattr(egl, name))

    @unittest.skipIf(SKIP_HEADER, 'egl.h not found')
    @unittest.skipIf(egl.egl_version < (1, 2), 'EGL version too low')
    def test_egl1_2_functions_defined(self):
        """Check definitions of EGL 1.2 functions.

        This test passes if:

        - All EGL 1.2 functions are defined.
        - They have the correct return types.

        """
        for n, (name, restype) in enumerate(EGL1_2_FUNCTIONS):
            with self.subTest(msg=name, n=n):
                egl_fn = getattr(egl, name)
                self.assertEqual(egl_fn.restype, restype, name)

    @unittest.skipIf(SKIP_HEADER, 'egl.h not found')
    @unittest.skipIf(egl.egl_version >= (1, 2), 'EGL version too high')
    def test_egl1_2_functions_omitted(self):
        """Check that EGL 1.2 functions are not defined.

        This test passes if:

        - No EGL 1.2 functions are defined.

        """
        for n, (name, *_) in enumerate(EGL1_2_FUNCTIONS):
            with self.subTest(msg=name, n=n):
                self.assertRaises(AttributeError, getattr(egl, name))

    @unittest.skipIf(SKIP_HEADER, 'egl.h not found')
    @unittest.skipIf(egl.egl_version < (1, 3), 'EGL version too low')
    def test_egl1_3_functions_defined(self):
        """Check definitions of EGL 1.3 functions.

        This test passes if:

        - All EGL 1.3 functions are defined.
        - They have the correct return types.

        """
        for n, (name, restype) in enumerate(EGL1_3_FUNCTIONS):
            with self.subTest(msg=name, n=n):
                egl_fn = getattr(egl, name)
                self.assertEqual(egl_fn.restype, restype, name)

    @unittest.skipIf(SKIP_HEADER, 'egl.h not found')
    @unittest.skipIf(egl.egl_version >= (1, 3), 'EGL version too high')
    def test_egl1_3_functions_omitted(self):
        """Check that EGL 1.3 functions are not defined.

        This test passes if:

        - No EGL 1.3 functions are defined.

        """
        for n, (name, *_) in enumerate(EGL1_3_FUNCTIONS):
            with self.subTest(msg=name, n=n):
                self.assertRaises(AttributeError, getattr(egl, name))

    @unittest.skipIf(SKIP_HEADER, 'egl.h not found')
    @unittest.skipIf(egl.egl_version < (1, 4), 'EGL version too low')
    def test_egl1_4_functions_defined(self):
        """Check definitions of EGL 1.4 functions.

        This test passes if:

        - All EGL 1.4 functions are defined.
        - They have the correct return types.

        """
        for n, (name, restype) in enumerate(EGL1_4_FUNCTIONS):
            with self.subTest(msg=name, n=n):
                egl_fn = getattr(egl, name)
                self.assertEqual(egl_fn.restype, restype, name)

    @unittest.skipIf(SKIP_HEADER, 'egl.h not found')
    @unittest.skipIf(egl.egl_version >= (1, 4), 'EGL version too high')
    def test_egl1_4_functions_omitted(self):
        """Check that EGL 1.4 functions are not defined.

        This test passes if:

        - No EGL 1.4 functions are defined.

        """
        for n, (name, *_) in enumerate(EGL1_4_FUNCTIONS):
            with self.subTest(msg=name, n=n):
                self.assertRaises(AttributeError, getattr(egl, name))

    @unittest.skipIf(SKIP_HEADER, 'egl.h not found')
    @unittest.skipIf(egl.egl_version < (1, 5), 'EGL version too low')
    def test_egl1_5_functions_defined(self):
        """Check definitions of EGL 1.5 functions.

        This test passes if:

        - All EGL 1.5 functions are defined.
        - They have the correct return types.

        """
        for n, (name, restype) in enumerate(EGL1_5_FUNCTIONS):
            with self.subTest(msg=name, n=n):
                egl_fn = getattr(egl, name)
                self.assertEqual(egl_fn.restype, restype, name)

    @unittest.skipIf(SKIP_HEADER, 'egl.h not found')
    @unittest.skipIf(egl.egl_version >= (1, 5), 'EGL version too high')
    def test_egl1_5_functions_omitted(self):
        """Check that EGL 1.5 functions are not defined.

        This test passes if:

        - No EGL 1.5 functions are defined.

        """
        for n, (name, *_) in enumerate(EGL1_5_FUNCTIONS):
            with self.subTest(msg=name, n=n):
                self.assertRaises(AttributeError, getattr(egl, name))
