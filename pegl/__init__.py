#!/usr/bin/env python3

'''Pegl: A Python wrapper for the EGL 1.4 API.'''

# Copyright © 2012 Tim Pederick.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

__author__ = 'Tim Pederick'
__version__ = '0.1a3~1.4' # The ~N.n part is the EGL API version wrapped.
__all__ = ['attribs', 'config', 'context', 'display', 'native', 'surface',
           'sync', 'int_p', 'make_int_p',
           'NO_DISPLAY', 'NO_CONTEXT', 'NO_SURFACE',
           'EGLError', 'NotInitializedError', 'BadAccessError',
           'BadAllocError', 'BadAttributeError', 'BadConfigError',
           'BadContextError', 'BadCurrentSurfaceError', 'BadDisplayError',
           'BadMatchError', 'BadNativePixmapError', 'BadNativeWindowError',
           'BadParameterError', 'BadSurfaceError', 'ContextLostError']

# TODO: Streamline the setup code. Take a look at README.rst -- see how many
# imports are needed? Slim it down!

# Standard library imports.
from ctypes import POINTER, c_int, c_void_p

# Types and symbolic constants.
int_p = POINTER(c_int)

def make_int_p(ival=0):
    '''Create and initialise a pointer to an integer.

    Keyword arguments:
        ival -- The initial value of the referenced integer. The default
            is 0.

    '''
    p = int_p()
    p.contents = c_int(ival)
    return p

NO_DISPLAY, NO_CONTEXT, NO_SURFACE = c_void_p(0), c_void_p(0), c_void_p(0)

# Exceptions for handling EGL errors.
class EGLError(Exception):
    '''Base class for all EGL errors.'''
    default_msg = 'encountered an unspecified error'

    def __init__(self, msg=None):
        '''Create the exception, with a given message or the default.'''
        if msg is None:
            msg = self.default_msg
        super().__init__(msg)


class NotInitializedError(EGLError):
    '''The EGL system was not, or could not be initialized.'''
    default_msg = 'EGL not initialized or initialization failed'


class BadAccessError(EGLError):
    '''A requested resource could not be accessed.'''
    default_msg = 'requested resource could not be accessed'


class BadAllocError(EGLError):
    '''Necessary memory allocation failed.'''
    default_msg = 'memory allocation failed'


class BadAttributeError(EGLError):
    '''An invalid attribute key or value was supplied.'''
    default_msg = 'invalid attribute key or value'


class BadConfigError(EGLError):
    '''The configuration supplied was not valid.'''
    default_msg = 'invalid configuration given'


class BadContextError(EGLError):
    '''The context supplied was not valid.'''
    default_msg = 'invalid context given'


class BadCurrentSurfaceError(EGLError):
    '''The current surface is no longer valid.'''
    default_msg = 'current surface is no longer valid'


class BadDisplayError(EGLError):
    '''The display supplied was not valid.'''
    default_msg = 'invalid display given'


class BadMatchError(EGLError):
    '''Supplied arguments were inconsistent with each other.'''
    default_msg = 'inconsistent arguments given'


class BadNativePixmapError(EGLError):
    '''The native pixmap supplied was not valid.'''
    default_msg = 'invalid native pixmap given'


class BadNativeWindowError(EGLError):
    '''The native window supplied was not valid.'''
    default_msg = 'invalid native window given'


class BadParameterError(EGLError):
    '''An invalid argument was supplied.'''
    default_msg = 'invalid argument given'


class BadSurfaceError(EGLError):
    '''The surface supplied was not valid.'''
    default_msg = 'invalid surface given'


class ContextLostError(EGLError):
    '''Context has been lost due to a power management event.'''
    default_msg = 'context lost due to power management event'


error_codes = {0x3000: None, # Success code.
               0x3001: NotInitializedError, 0x3002: BadAccessError,
               0x3003: BadAllocError, 0x3004: BadAttributeError,
               0x3005: BadConfigError, 0x3006: BadContextError,
               0x3007: BadCurrentSurfaceError, 0x3008: BadDisplayError,
               0x3009: BadMatchError, 0x300A: BadNativePixmapError,
               0x300B: BadNativeWindowError, 0x300C: BadParameterError,
               0x300D: BadSurfaceError, 0x300E: ContextLostError}

