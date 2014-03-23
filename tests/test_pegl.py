#!/usr/bin/env python3

'''Unit tests for the Pegl package top-level namespace.'''

# Copyright © 2012 Tim Pederick.
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
import ctypes
import sys

# Access the pegl package at ../pegl (relative to the tests directory).
sys.path.append('..')
import pegl

class TestErrors:
    '''Test the exception objects that represent EGL errors.'''
    @staticmethod
    def test_base_error():
        '''Test EGLError, the base class for all Pegl exceptions.'''
        # With default message.
        e = pegl.EGLError()
        assert str(e) == 'encountered an unspecified error'

        # With custom message.
        e = pegl.EGLError('testing, testing')
        assert str(e) == 'testing, testing'

    @staticmethod
    def test_other_errors():
        all_errors = {pegl.NotInitializedError:
                      'EGL not initialized or initialization failed',
                      pegl.BadAccessError:
                      'requested resource could not be accessed',
                      pegl.BadAllocError:
                      'memory allocation failed',
                      pegl.BadAttributeError:
                      'invalid attribute key or value',
                      pegl.BadConfigError:
                      'invalid configuration given',
                      pegl.BadContextError:
                      'invalid context given',
                      pegl.BadCurrentSurfaceError:
                      'current surface is no longer valid',
                      pegl.BadDisplayError:
                      'invalid display given',
                      pegl.BadMatchError:
                      'inconsistent arguments given',
                      pegl.BadNativePixmapError:
                      'invalid native pixmap given',
                      pegl.BadNativeWindowError:
                      'invalid native window given',
                      pegl.BadParameterError:
                      'invalid argument given',
                      pegl.BadSurfaceError:
                      'invalid surface given',
                      pegl.ContextLostError:
                      'context lost due to power management event'}
        for code, error in pegl.error_codes.items():
            if error is None:
                assert code == 0x3000 # Success code.
                continue

            assert error in all_errors
            e = error()
            assert str(e) == all_errors[error]

            e = error('testing, testing')
            assert str(e) == 'testing, testing'
