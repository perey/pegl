#!/usr/bin/env python3

'''EGL 1.4 Python wrapper.'''

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
__version__ = '0.0+1.4' # The +N.n part is the EGL API version wrapped.
__all__ = ['attribs', 'config', 'display', 'egl', 'error_check', 'sync',
           'EGLError', 'NotInitializedError', 'BadAccessError',
           'BadAllocError', 'BadAttributeError', 'BadConfigError',
           'BadContextError', 'BadCurrentSurfaceError', 'BadDisplayError',
           'BadMatchError', 'BadNativePixmapError', 'BadNativeWindowError',
           'BadParameterError', 'BadSurfaceError', 'ContextLostError']

# Standard library imports.
from ctypes import CDLL, POINTER, c_char_p, c_int, c_uint, c_void_p

# Foreign library imports and definitions.
egl = CDLL('libEGL.so')
ebool = enum = c_uint
config = context = surface = display = c_void_p
n_display = n_pixmap = n_window = c_void_p
client_buffer = c_void_p
attr_list = int_p = POINTER(c_int)
configs = POINTER(config)

egl.eglGetError.argtypes = ()

egl.eglGetDisplay.argtypes = (n_display,)
egl.eglGetDisplay.restype = display

egl.eglGetCurrentDisplay.argtypes = ()
egl.eglGetCurrentDisplay.restype = display

egl.eglInitialize.argtypes = (display, int_p, int_p)
egl.eglInitialize.restype = ebool

egl.eglTerminate.argtypes = (display,)
egl.eglTerminate.restype = ebool

egl.eglQueryString.argtypes = (display, c_int)
egl.eglQueryString.restype = c_char_p

egl.eglReleaseThread.argtypes = ()
egl.eglReleaseThread.restype = ebool

egl.eglGetConfigs.argtypes = (display, configs, c_int, int_p)
egl.eglGetConfigs.restype = ebool

egl.eglGetConfigAttrib.argtypes = (display, config, c_int, int_p)
egl.eglGetConfigAttrib.restype = ebool

egl.eglChooseConfig.argtypes = (display, attr_list, configs, c_int, int_p)
egl.eglChooseConfig.restype = ebool

egl.eglCreateWindowSurface.argtypes = (display, config, n_window, attr_list)
egl.eglCreateWindowSurface.restype = surface

egl.eglCreatePbufferSurface.argtypes = (display, config, attr_list)
egl.eglCreatePbufferSurface.restype = surface

egl.eglCreatePbufferFromClientBuffer.argtypes = (display, enum, client_buffer,
                                                 config, attr_list)
egl.eglCreatePbufferFromClientBuffer.restype = surface

egl.eglCreatePixmapSurface.argtypes = (display, config, n_pixmap, attr_list)
egl.eglCreatePixmapSurface.restype = surface

egl.eglGetCurrentSurface.argtypes = (c_int,)
egl.eglGetCurrentSurface.restype = surface

egl.eglSurfaceAttrib.argtypes = (display, surface, c_int, c_int)
egl.eglSurfaceAttrib.restype = ebool

egl.eglQuerySurface.argtypes = (display, surface, c_int, int_p)
egl.eglQuerySurface.restype = ebool

egl.eglDestroySurface.argtypes = (display, surface)
egl.eglDestroySurface.restype = ebool

egl.eglBindAPI.argtypes = (c_int,)
egl.eglBindAPI.restype = ebool

egl.eglQueryAPI.argtypes = ()
egl.eglQueryAPI.restype = c_int

egl.eglCreateContext.argtypes = (display, config, context, attr_list)
egl.eglCreateContext.restype = context

egl.eglMakeCurrent.argtypes = (display, surface, surface, context)
egl.eglMakeCurrent.restype = ebool

egl.eglQueryContext.argtypes = (display, context, c_int, int_p)
egl.eglQueryContext.restype = ebool

egl.eglGetCurrentContext.argtypes = ()
egl.eglGetCurrentContext.restype = context

egl.eglDestroyContext.argtypes = (display, context)
egl.eglDestroyContext.restype = ebool

egl.eglWaitClient.argtypes = ()
egl.eglWaitClient.restype = ebool

egl.eglWaitGL.argtypes = ()
egl.eglWaitGL.restype = ebool

egl.eglWaitNative.argtypes = (c_int,)
egl.eglWaitNative.restype = ebool

egl.eglSwapBuffers.argtypes = (display, surface)
egl.eglSwapBuffers.restype = ebool

egl.eglCopyBuffers.argtypes = (display, surface, n_pixmap)
egl.eglCopyBuffers.restype = ebool

egl.eglSwapInterval.argtypes = (display, c_int)
egl.eglSwapInterval.restype = ebool

egl.eglBindTexImage.argtypes = (display, surface, c_int)
egl.eglBindTexImage.restype = ebool

egl.eglReleaseTexImage.argtypes = (display, surface, c_int)
egl.eglReleaseTexImage.restype = ebool

# Exceptions for EGL errors.
class EGLError(Exception):
    '''Base class for all EGL errors.'''
    pass
class NotInitializedError(EGLError):
    '''The EGL system was not, or could not be initialized.'''
    pass
class BadAccessError(EGLError):
    '''A requested resource could not be accessed.'''
    pass
class BadAllocError(EGLError):
    '''Necessary memory allocation failed.'''
    pass
class BadAttributeError(EGLError):
    '''An invalid attribute key or value was supplied.'''
    pass
class BadConfigError(EGLError):
    '''The configuration supplied was not valid.'''
    pass
class BadContextError(EGLError):
    '''The context supplied was not valid.'''
    pass
class BadCurrentSurfaceError(EGLError):
    '''The current surface is no longer valid.'''
    pass
class BadDisplayError(EGLError):
    '''The display supplied was not valid.'''
    pass
class BadMatchError(EGLError):
    '''Supplied arguments were inconsistent with each other.'''
    pass
class BadNativePixmapError(EGLError):
    '''The native pixmap supplied was not valid.'''
    pass
class BadNativeWindowError(EGLError):
    '''The native window supplied was not valid.'''
    pass
class BadParameterError(EGLError):
    '''An invalid argument was supplied.'''
    pass
class BadSurfaceError(EGLError):
    '''The surface supplied was not valid.'''
    pass
class ContextLostError(EGLError):
    '''Context has been lost due to a power management event.'''
    pass
error_codes = {0x3000: None, 0x3001: NotInitializedError,
               0x3002: BadAccessError, 0x3003: BadAllocError,
               0x3004: BadAttributeError, 0x3005: BadConfigError,
               0x3006: BadContextError, 0x3007: BadCurrentSurfaceError,
               0x3008: BadDisplayError, 0x3009: BadMatchError,
               0x300A: BadNativePixmapError, 0x300B: BadNativeWindowError,
               0x300C: BadParameterError, 0x300D: BadSurfaceError,
               0x300E: ContextLostError}
def error_check(fn):
    '''Check the EGL error trap after a function is called.'''
    def wrapped_fn(*args, **kwargs):
        result = fn(*args, **kwargs)
        errcode = error_codes.get(egl.eglGetError(), EGLError)
        if errcode is not None:
            raise errcode()
        return result
    return wrapped_fn
