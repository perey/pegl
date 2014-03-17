#!/usr/bin/env python3

'''Khronos texture stream consumer extension for EGL.

This extension allows an OpenGL or OpenGL ES texture to act as a
consumer of an image stream.

http://www.khronos.org/registry/egl/extensions/KHR/EGL_KHR_stream_consumer_gltexture.txt

'''
# Copyright © 2012-14 Tim Pederick.
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
from . import load_ext
from .khr_stream import c_stream, Stream, StreamAttribs
from ..native import c_ibool, c_display

# Get handles of extension functions.
native_streamconsumegl = load_ext(b'eglStreamConsumerGLTextureExternalKHR',
                                  c_ibool, (c_display, c_stream),
                                  fail_on=False)
native_streamacquire = load_ext(b'eglStreamConsumerAcquireKHR',
                                c_ibool, (c_display, c_stream),
                                fail_on=False)
native_streamrelease = load_ext(b'eglStreamConsumerReleaseKHR',
                                c_ibool, (c_display, c_stream),
                                fail_on=False)

# New stream attribute.
StreamAttribs.extend('CONSUMER_ACQUIRE_TIMEOUT_μs', 0x321E, c_int, 0)
StreamAttribs.CONSUMER_ACQUIRE_TIMEOUT_USEC = \
    StreamAttribs.CONSUMER_ACQUIRE_TIMEOUT_μs

# Extend the Stream class.
def consume_gl(stream):
    '''Bind an OpenGL texture as the stream consumer.'''
    return native_streamconsumegl(stream.display, stream)
Stream.register_consumer('OpenGL texture', # Also applies to OpenGL ES.
                         'EGL_KHR_stream_consumer_gltexture', consume_gl)

def acquire_timeout_getter(self):
    '''Get the current value of the consumer acquisition timeout.

    Returns:
        A value in microseconds.

    '''
    return self._attr(StreamAttribs.CONSUMER_ACQUIRE_TIMEOUT_μs)
def acquire_timeout_setter(self, val):
    '''Set a new value for the consumer acquisition timeout.

    Keyword arguments:
        val -- The new value in microseconds. If zero, the consumer will
        never wait for frames to become available. If negative, the
        consumer will wait indefinitely.

    '''
    self._setattr(StreamAttribs.CONSUMER_ACQUIRE_TIMEOUT_μs, int(val))
Stream.acquire_timeout = property(fget=acquire_timeout_getter,
                                  fset=acquire_timeout_setter)

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
