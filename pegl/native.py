#!/usr/bin/env python3

'''EGL library interface.'''

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

__all__ = ('eglGetDisplay', 'eglInitialize', 'eglTerminate', 'eglQueryString',
           'eglGetConfigs', 'eglChooseConfig', 'eglGetConfigAttrib',
           'eglCreateWindowSurface', 'eglCreatePbufferSurface',
           'eglCreatePbufferFromClientBuffer', 'eglCreatePixmapSurface',
           'eglDestroySurface', 'eglSurfaceAttrib', 'eglQuerySurface',
           'eglBindTexImage', 'eglReleaseTexImage', 'eglBindAPI',
           'eglQueryAPI', 'eglCreateContext', 'eglDestroyContext',
           'eglMakeCurrent', 'eglGetCurrentContext', 'eglGetCurrentSurface',
           'eglGetCurrentDisplay', 'eglQueryContext', 'eglWaitClient',
           'eglWaitGL', 'eglWaitNative', 'eglSwapBuffers', 'eglCopyBuffers',
           'eglSwapInterval', 'eglGetProcAddress', 'eglReleaseThread',
           'ebool', 'enum', 'attr_list', 'display', 'surface', 'client_buffer',
           'config')

# Standard library imports.
import ctypes
from ctypes import POINTER, c_char_p, c_int, c_uint, c_void_p
import sys

# Local imports.
from . import EGLError, error_codes, int_p, NO_CONTEXT, NO_SURFACE

# Native library import.
libname = 'libEGL'
if sys.platform == 'linux2':
    libclass, libext = ctypes.CDLL, '.so'
elif sys.platform == 'darwin':
    libclass, libext = ctypes.CDLL, '.dylib'
elif sys.platform == 'win32':
    libclass, libext = ctypes.WinDLL, '.dll'
else:
    raise ImportError('Pegl not supported on {}'.format(sys.platform))
       
egl = libclass(libname + libext)

# Type definitions.
ebool = enum = c_uint
config = context = surface = display = c_void_p
native_display = native_pixmap = native_window = c_void_p
client_buffer = c_void_p
attr_list = int_p
configs = POINTER(config)
void_func = c_void_p # The function ext.load_ext() will cast this to a function
                     # pointer with the correct argument and return types.

# Trap EGL errors. We set the argument type for "EGLint eglGetError(void)"
# here, since we use it for error_check. We don't set a return type, because
# it's just an int, which is the default.
egl.eglGetError.argtypes = ()

def error_check(fn, fail_on=None, always_check=False, fallback_error=EGLError,
                fallback_msg=None, fail_on_null=False):
    '''Check the EGL error trap after a function is called.

    Keyword arguments:
        fn -- The function to wrap with EGL error checking.
        fail_on -- A return value that indicates an error. If the
            function returns this value, an exception will be raised,
            even if the error trap has no error code. If omitted or
            None, no return value will be treated as an error.
        always_check -- Check the trap even if the return value did not
            match fail_on. This defaults to False, but even then, the
            error trap will always be checked if fail_on is not supplied
            (otherwise no error checking would be done, and so there
            would be no point having wrapped the function).
        fallback_error -- An exception to raise if an error is signalled
            but no error code is available. The default is EGLError.
        fallback_msg -- An optional message to pass to the fallback
            exception's constructor. If omitted, the exception's default
            message will be used.
        fail_on_null -- HACK! Since None is both the ctypes null pointer
            and the fail_on "nothing", we need a way to signal that the
            fail_on value is the null pointer. This is it. It defaults
            to False.

    Returns:
        A function object with error checking included.

    '''
    def wrapped_fn(*args, **kwargs):
        result = fn(*args, **kwargs)

        if (always_check or (fail_on_null and result is None) or
            (not fail_on_null and (fail_on is None or fail_on == result or
                                   (fn.restype is ebool and # ebool maps to a
                                    fail_on == bool(result))# Python int, not
                                   )                        # bool, because EGL
             )):                                            # uses an integer,
            # Check the error trap.                         # not a C boolean.
            errcode = error_codes.get(egl.eglGetError(), EGLError)
            if errcode is not None:
                # The error trap held something other than the success code.
                raise errcode()
            elif ((fail_on is not None and fail_on == result) or
                  (fail_on_null and result is None)):
                # The error trap held the success code, but the returned value
                # still signals an error.
                raise fallback_error(fallback_msg)
            # ...else fall through.
        return result
    return wrapped_fn

# Set argument and return types, and wrap with error checking. Functions are
# listed by their order in the EGL 1.4 specification, with section numbers.
# Just about every function can cause a NotInitializedError if passed an
# uninitialized display, so these aren't listed here. Likewise, functions
# taking a display as an argument can generally cause a BadDisplayError.

################ 3.2 ################

# EGLDisplay eglGetDisplay(EGLNativeDisplayType display_id);
egl.eglGetDisplay.argtypes = (native_display,)
egl.eglGetDisplay.restype = display
# TODO: Remove error_check? The EGL spec indicates no errors for this function.
eglGetDisplay = error_check(egl.eglGetDisplay)

# EGLBoolean eglInitialize(EGLDisplay dpy, EGLint *major, EGLint *minor);
egl.eglInitialize.argtypes = (display, int_p, int_p)
egl.eglInitialize.restype = ebool
# Errors: BadDisplayError, NotInitializedError
eglInitialize = error_check(egl.eglInitialize, fail_on=False)

# EGLBoolean eglTerminate(EGLDisplay dpy);
egl.eglTerminate.argtypes = (display,)
egl.eglTerminate.restype = ebool
# Errors: BadDisplayError
eglTerminate = error_check(egl.eglTerminate, fail_on=False)

################ 3.3 ################

# const char *eglQueryString(EGLDisplay dpy, EGLint name);
egl.eglQueryString.argtypes = (display, c_int)
egl.eglQueryString.restype = c_char_p
# Errors: BadDisplayError, BadParameterError
eglQueryString = error_check(egl.eglQueryString, fail_on_null=True)

################ 3.4 ################

# EGLBoolean eglGetConfigs(EGLDisplay dpy, EGLConfig *configs,
#                          EGLint config_size, EGLint *num_config);
egl.eglGetConfigs.argtypes = (display, configs, c_int, int_p)
egl.eglGetConfigs.restype = ebool
# Errors: BadDisplayError, BadParameterError
eglGetConfigs = error_check(egl.eglGetConfigs, fail_on=False)

# EGLBoolean eglChooseConfig(EGLDisplay dpy, const EGLint *attrib_list,
#                            EGLConfig *configs, EGLint config_size,
#                            EGLint *num_config);
egl.eglChooseConfig.argtypes = (display, attr_list, configs, c_int, int_p)
egl.eglChooseConfig.restype = ebool
# Errors: BadAttributeError, BadDisplayError?, BadParameterError?
eglChooseConfig = error_check(egl.eglChooseConfig, fail_on=False)

# EGLBoolean eglGetConfigAttrib(EGLDisplay dpy, EGLConfig config,
#                               EGLint attribute, EGLint *value);
egl.eglGetConfigAttrib.argtypes = (display, config, c_int, int_p)
egl.eglGetConfigAttrib.restype = ebool
# Errors: BadAttributeError, BadConfigError?, BadDisplayError?
eglGetConfigAttrib = error_check(egl.eglGetConfigAttrib, fail_on=False)

################ 3.5 ################

# EGLSurface eglCreateWindowSurface(EGLDisplay dpy, EGLConfig config,
#                                   EGLNativeWindowType win,
#                                   const EGLint *attrib_list);
egl.eglCreateWindowSurface.argtypes = (display, config, native_window,
                                       attr_list)
egl.eglCreateWindowSurface.restype = surface
# Errors: BadAllocError, BadConfigError, BadMatchError, BadNativeWindowError
eglCreateWindowSurface = error_check(egl.eglCreateWindowSurface,
                                     fail_on=NO_SURFACE)

# EGLSurface eglCreatePbufferSurface(EGLDisplay dpy, EGLConfig config,
#                                    const EGLint *attrib_list);
egl.eglCreatePbufferSurface.argtypes = (display, config, attr_list)
egl.eglCreatePbufferSurface.restype = surface
# Errors: BadAllocError, BadAttributeError, BadConfigError, BadMatchError,
#         BadParameterError
eglCreatePbufferSurface = error_check(egl.eglCreatePbufferSurface,
                                      fail_on=NO_SURFACE)

# EGLSurface eglCreatePbufferFromClientBuffer(EGLDisplay dpy, EGLenum buftype,
#                                             EGLClientBuffer buffer,
#                                             EGLConfig config,
#                                             const EGLint *attrib_list);
egl.eglCreatePbufferFromClientBuffer.argtypes = (display, enum, client_buffer,
                                                 config, attr_list)
egl.eglCreatePbufferFromClientBuffer.restype = surface
# Errors: BadAccessError, BadAllocError, BadAttributeError, BadConfigError,
#         BadMatchError, BadParameterError
eglCreatePbufferFromClientBuffer =\
    error_check(egl.eglCreatePbufferFromClientBuffer, fail_on=NO_SURFACE)

# EGLSurface eglCreatePixmapSurface(EGLDisplay dpy, EGLConfig config,
#                                   EGLNativePixmapType pixmap,
#                                   const EGLint *attrib_list);
egl.eglCreatePixmapSurface.argtypes = (display, config, native_pixmap,
                                       attr_list)
egl.eglCreatePixmapSurface.restype = surface
# Errors: BadAllocError, BadConfigError, BadMatchError, BadNativePixmapError
eglCreatePixmapSurface = error_check(egl.eglCreatePixmapSurface,
                                     fail_on=NO_SURFACE)

# EGLBoolean eglDestroySurface(EGLDisplay dpy, EGLSurface surface);
egl.eglDestroySurface.argtypes = (display, surface)
egl.eglDestroySurface.restype = ebool
# Errors: BadSurfaceError
eglDestroySurface = error_check(egl.eglDestroySurface, fail_on=False)

# EGLBoolean eglSurfaceAttrib(EGLDisplay dpy, EGLSurface surface,
#                             EGLint attribute, EGLint value);
egl.eglSurfaceAttrib.argtypes = (display, surface, c_int, c_int)
egl.eglSurfaceAttrib.restype = ebool
# Errors: BadMatchError, BadParameterError, BadSurfaceError?
eglSurfaceAttrib = error_check(egl.eglSurfaceAttrib, fail_on=False) # I assume.

# EGLBoolean eglQuerySurface(EGLDisplay dpy, EGLSurface surface,
#                            EGLint attribute, EGLint *value);
egl.eglQuerySurface.argtypes = (display, surface, c_int, int_p)
egl.eglQuerySurface.restype = ebool
# Errors: BadAttributeError, BadParameterError?, BadSurfaceError
eglQuerySurface = error_check(egl.eglQuerySurface, fail_on=False)

################ 3.6 ################

# EGLBoolean eglBindTexImage(EGLDisplay dpy, EGLSurface surface,
#                            EGLint buffer);
egl.eglBindTexImage.argtypes = (display, surface, c_int)
egl.eglBindTexImage.restype = ebool
# Errors: BadAccessError, BadMatchError, BadParameterError, BadSurfaceError
eglBindTexImage = error_check(egl.eglBindTexImage, fail_on=False) # presumably.

# EGLBoolean eglReleaseTexImage(EGLDisplay dpy, EGLSurface surface,
#                               EGLint buffer);
egl.eglReleaseTexImage.argtypes = (display, surface, c_int)
egl.eglReleaseTexImage.restype = ebool
# Errors: BadMatchError, BadParameterError, BadSurfaceError
eglReleaseTexImage = error_check(egl.eglReleaseTexImage, fail_on=False) # ditto

################ 3.7 ################

# EGLBoolean eglBindAPI(EGLenum api);
egl.eglBindAPI.argtypes = (enum,)
egl.eglBindAPI.restype = ebool
# Errors: BadParameterError
eglBindAPI = error_check(egl.eglBindAPI, fail_on=False)

# EGLenum eglQueryAPI(void);
egl.eglQueryAPI.argtypes = ()
egl.eglQueryAPI.restype = enum
# TODO: Remove error_check? The EGL spec indicates no errors for this function.
eglQueryAPI = error_check(egl.eglQueryAPI)

# EGLContext eglCreateContext(EGLDisplay dpy, EGLConfig config,
#                             EGLContext share_context,
#                             const EGLint *attrib_list);
egl.eglCreateContext.argtypes = (display, config, context, attr_list)
egl.eglCreateContext.restype = context
# Errors: BadAllocError, BadConfigError, BadContextError, BadDisplayError?,
#         BadMatchError
eglCreateContext = error_check(egl.eglCreateContext, fail_on=NO_CONTEXT)

# EGLBoolean eglDestroyContext(EGLDisplay dpy, EGLContext ctx);
egl.eglDestroyContext.argtypes = (display, context)
egl.eglDestroyContext.restype = ebool
# Errors: BadContextError
eglDestroyContext = error_check(egl.eglDestroyContext, fail_on=False)

# EGLBoolean eglMakeCurrent(EGLDisplay dpy, EGLSurface draw, EGLSurface read,
#                           EGLContext ctx);
egl.eglMakeCurrent.argtypes = (display, surface, surface, context)
egl.eglMakeCurrent.restype = ebool
# Errors: BadAccessError, BadContextError, BadCurrentSurfaceError,
#         BadMatchError, BadNativeWindowError, BadSurfaceError,
#         ContextLostError
eglMakeCurrent = error_check(egl.eglMakeCurrent, fail_on=False)

# EGLContext eglGetCurrentContext(void);
egl.eglGetCurrentContext.argtypes = ()
egl.eglGetCurrentContext.restype = context
# TODO: Remove error_check? The EGL spec indicates no errors for this function.
eglGetCurrentContext = error_check(egl.eglGetCurrentContext)

# EGLSurface eglGetCurrentSurface(EGLint readdraw);
egl.eglGetCurrentSurface.argtypes = (c_int,)
egl.eglGetCurrentSurface.restype = surface
# Errors: BadParameterError
eglGetCurrentSurface = error_check(egl.eglGetCurrentSurface)

# EGLDisplay eglGetCurrentDisplay(void);
egl.eglGetCurrentDisplay.argtypes = ()
egl.eglGetCurrentDisplay.restype = display
# TODO: Remove error_check? The EGL spec indicates no errors for this function.
eglGetCurrentDisplay = error_check(egl.eglGetCurrentDisplay)

# EGLBoolean eglQueryContext(EGLDisplay dpy, EGLContext ctx, EGLint attribute,
#                            EGLint *value);
egl.eglQueryContext.argtypes = (display, context, c_int, int_p)
egl.eglQueryContext.restype = ebool
# Errors: BadAttributeError, BadContextError, BadParameterError?
eglQueryContext = error_check(egl.eglQueryContext, fail_on=False)

################ 3.8 ################

# EGLBoolean eglWaitClient(void);
egl.eglWaitClient.argtypes = ()
egl.eglWaitClient.restype = ebool
# Errors: BadCurrentSurfaceError
eglWaitClient = error_check(egl.eglWaitClient, fail_on=False)

# EGLBoolean eglWaitGL(void);
egl.eglWaitGL.argtypes = ()
egl.eglWaitGL.restype = ebool
# Errors: BadCurrentSurfaceError
eglWaitGL = error_check(egl.eglWaitGL, fail_on=False)

# EGLBoolean eglWaitNative(EGLint engine);
egl.eglWaitNative.argtypes = (c_int,)
egl.eglWaitNative.restype = ebool
# Errors: BadCurrentSurfaceError, BadParameterError
eglWaitNative = error_check(egl.eglWaitNative, fail_on=False)

################ 3.9 ################

# EGLBoolean eglSwapBuffers(EGLDisplay dpy, EGLSurface surface);
egl.eglSwapBuffers.argtypes = (display, surface)
egl.eglSwapBuffers.restype = ebool
# Errors: BadNativeWindowError, BadSurfaceError, ContextLostError
eglSwapBuffers = error_check(egl.eglSwapBuffers, fail_on=False)

# EGLBoolean eglCopyBuffers(EGLDisplay dpy, EGLSurface surface,
#                           EGLNativePixmapType target);
egl.eglCopyBuffers.argtypes = (display, surface, native_pixmap)
egl.eglCopyBuffers.restype = ebool
# Errors: BadMatchError, BadNativePixmapError, BadSurfaceError,
#         ContextLostError
eglCopyBuffers = error_check(egl.eglCopyBuffers, fail_on=False)

# EGLBoolean eglSwapInterval(EGLDisplay dpy, EGLint interval);
egl.eglSwapInterval.argtypes = (display, c_int)
egl.eglSwapInterval.restype = ebool
# Errors: BadContextError, BadSurfaceError
eglSwapInterval = error_check(egl.eglSwapInterval, fail_on=False)

################ 3.10 ###############

# void (*eglGetProcAddress(const char *procname))(void);
egl.eglGetProcAddress.argtypes = (c_char_p,)
egl.eglGetProcAddress.restype = void_func
# TODO: Remove error_check? The EGL spec indicates no errors for this function.
# Alternatively, add fail_on_null=True and change the error handling in the
# ext.load_ext() function that calls this.
eglGetProcAddress = error_check(egl.eglGetProcAddress)

################ 3.11 ###############

# EGLBoolean eglReleaseThread(void);
egl.eglReleaseThread.argtypes = ()
egl.eglReleaseThread.restype = ebool
# The EGL spec defines no failure modes, but it fails on False anyway.
eglReleaseThread = error_check(egl.eglReleaseThread, fail_on=False)
