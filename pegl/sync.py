#!/usr/bin/env python3

'''EGL 1.4 thread controls.'''

# Local imports.
from . import egl, error_check

@error_check
def release_thread():
    return bool(egl.eglReleaseThread())

@error_check
def wait_client():
    return bool(egl.eglWaitClient())

@error_check
def wait_GL():
    return bool(egl.eglWaitGL())

@error_check
def wait_native():
    return bool(egl.eglWaitNative())
