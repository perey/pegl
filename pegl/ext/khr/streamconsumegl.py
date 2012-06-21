#!/usr/bin/env python3

'''Khronos OpenGL/OpenGL ES texture stream consumer extension for EGL.

This extension enables OpenGL and OpenGL ES textures as consumers of
image streams from the related stream extension.

http://www.khronos.org/registry/egl/extensions/KHR/EGL_KHR_stream_consumer_gltexture.txt

'''
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
from .. import load_ext
from ..stream import stream, StreamAttribs
from ...native import ebool, display

# Get handles for extension functions.
native_streamconsumegl = load_ext(b'eglStreamConsumerGLTextureExternalKHR',
                                  ebool, (display, stream), fail_on=False)
native_streamacquire = load_ext(b'eglStreamConsumerAcquireKHR',
                                ebool, (display, stream), fail_on=False)
native_streamrelease = load_ext(b'eglStreamConsumerReleaseKHR',
                                ebool, (display, stream), fail_on=False)

# New attribute for stream objects.
StreamAttribs.extend('CONSUMER_ACQUIRE_TIMEOUT_USEC', 0x321E, c_int, 0)

# Add new property and extension functions to the Stream class.
def _acquire_timeout_get(self):
    '''Get the current value of the consumer acquisition timeout.

    Returns:
        A value in microseconds.

    '''
    return self._attr(StreamAttribs.CONSUMER_ACQUIRE_TIMEOUT_USEC)
def _acquire_timeout_set(self, val):
    '''Set a new value for the consumer acquisition timeout.

    Keyword arguments:
        val -- The new value in microseconds. If zero, the consumer will
        never wait for frames to become available. If negative, the
        consumer will wait indefinitely.

    '''
    self._setattr(StreamAttribs.CONSUMER_ACQUIRE_TIMEOUT_USEC, int(val))
Stream.acquire_timeout = property(_acquire_timeout_get, _acquire_timeout_set)

def acquire(self):
    '''Cause the stream consumer to acquire or "latch" a frame.

    This function will block until the acquisition succeeds or times
    out. The timeout value is set in the stream's acquire_timeout
    attribute.

    '''
    native_streamacquire(self.display, self)
Stream.acquire = acquire

def release(self):
    '''Cause the stream consumer to release a "latched" frame.'''
    native_streamrelease(self.display, self)
Stream.release = release
