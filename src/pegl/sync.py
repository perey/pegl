#!/usr/bin/env python3

'''EGL thread controls.'''

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

# Local imports.
from . import native

CORE_NATIVE_ENGINE = 0x305B

def wait_client():
    '''Instruct native rendering to wait on any client API rendering.

    This is an EGL-level instruction equivalent to API-specific calls
    such as glFinish().

    '''
    native.eglWaitClient()

def wait_GL():
    '''Instruct native rendering to wait on any OpenGL rendering.

    EGL provides this function for backwards compatibility; it is
    defined to be equivalent to saving the bound API, binding the
    OpenGL ES API, calling wait_client(), and then rebinding the
    original API. New code should just use wait_client() instead.

    '''
    native.eglWaitGL()

def wait_native(engine=CORE_NATIVE_ENGINE):
    '''Instruct client API rendering to wait on any native rendering.

    Keyword arguments:
        engine -- An implementation-defined reference to a native
            rendering engine. If omitted, the reference points to the
            EGL core native engine.

    '''
    native.eglWaitNative(engine)
