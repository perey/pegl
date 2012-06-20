#!/usr/bin/env python3

'''Khronos stream extension for EGL.

This extension adds objects to handle frame streams that can flow
between EGL client APIs. Other extensions provide particular "producers"
and "consumers" for these streams.

http://www.khronos.org/registry/egl/extensions/KHR/EGL_KHR_stream.txt

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

# Standard library imports.
from ctypes import POINTER, c_ulonglong, c_void_p
from collections import namedtuple

# Local imports.
from .. import load_ext
from ... import int_p, make_int_p, EGLError, error_codes
from ...attribs import attr_convert, Attribs, AttribList, BitMask, Details
from ...native import ebool, enum, attr_list, display

# Extension types and symbolic constants.
ull_p = POINTER(c_ulonglong)
stream = c_void_p
NO_STREAM = c_void_p(0)

# New errors.
class BadStreamError(EGLError):
    '''The stream supplied was not valid.'''
    default_msg = 'invalid stream given'


class BadStateError(EGLError):
    '''The stream was not in the necessary state.'''
    default_msg = 'stream in wrong state for operation'


error_codes[0x321B] = BadStreamError
error_codes[0x321C] = BadStateError

# Get handles of extension functions.
native_createstream = load_ext(b'eglCreateStreamKHR', stream,
                               (display, attr_list), fail_on=NO_STREAM)
native_destroystream = load_ext(b'eglCreateStreamKHR', ebool,
                                (display, stream), fail_on=False)
native_streamattrib = load_ext(b'eglStreamAttribKHR', ebool,
                               (display, stream, enum, c_int), fail_on=False)
native_querystream = load_ext(b'eglQueryStreamKHR', ebool,
                              (display, stream, enum, int_p), fail_on=False)
native_querystream64 = load_ext(b'eglQueryStreamu64KHR', ebool,
                                (display, stream, enum, ull_p), fail_on=False)

# Attributes for stream objects.
StreamStates = namedtuple('StreamStates_tuple',
                          ('CREATED', 'CONNECTING', 'EMPTY',
                           'NEW_FRAME_AVAILABLE', 'OLD_FRAME_AVAILABLE',
                           'DISCONNECTED')
                          )(*range(0x3215, 0x321B))

class StreamAttribs(Attribs):
    '''The set of EGL attributes relevant to stream objects.'''
    # For creating streams, and setting and querying attributes.
    CONSUMER_LATENCY_μs = CONSUMER_LATENCY_USEC = 0x3210
    # For querying attributes only.
    STREAM_STATE = 0x3214
    # For querying attributes using the 64-bit function.
    PRODUCER_FRAME, CONSUMER_FRAME = 0x3212, 0x3213
    details = {CONSUMER_LATENCY_μs: Details('The average delay before an '
                                            'inserted frame is visible to the '
                                            'user, in microseconds', c_int, 0),
               STREAM_STATE: Details('The current state of the stream',
                                     StreamStates, StreamStates.CREATED),
               PRODUCER_FRAME: Details('The number of frames inserted into '
                                       'this stream by the producer',
                                       c_ulonglong, 0),
               CONSUMER_FRAME: Details('The number of frames retrieved from '
                                       'this stream by the consumer',
                                       c_ulonglong, 0)}

# The stream class itself.
class Stream:
    '''Represents a stream of image frames.

    Instance attributes:
        sthandle -- The foreign object handle for this stream.
        display -- The EGL display to which this stream belongs. An
            instance of Display.
        attribs -- The attributes with which this stream was created. An
            instance of AttribList.

    '''
    def __init__(self, display, attribs=None):
        '''Create the stream.

        Keyword arguments:
            display -- As the instance attribute.
            attribs -- As the instance attribute. If omitted, all
                attributes will take on their default values.

        '''
        self.display = display
        self.attribs = (attribs if isinstance(attribs, AttribList) else
                        AttribList(StreamAttribs, attribs))
        self.sthandle = native_createstream(self.display, self.attribs)

    def __del__(self):
        '''Destroy the stream.'''
        native_destroystream(self.display, self)

    @property
    def _as_parameter_(self):
        '''Get the stream handle for use by foreign functions.'''
        return self.sthandle

    def _attr(self, attr):
        '''Get the value of a stream attribute.

        Keyword arguments:
            attr -- The identifier of the attribute requested.

        '''
        # Query the attribute, storing the result in a pointer.
        result = make_int_p()
        native_querystream(self.display, self, attr, result)

        # Dereference the pointer and convert to an appropriate type.
        return attr_convert(attr, result.contents.value, StreamAttribs)

    def _attr64(self, attr):
        '''Get the value of a 64-bit stream attribute.

        Keyword arguments:
            attr -- The identifier of the attribute requested.

        '''
        # Query the attribute, storing the result in a pointer.
        result = ull_p()
        result.contents = c_ulonglong(0)
        native_querystream64(self.display, self, attr, result)

        # Dereference the pointer and convert to an appropriate type.
        return attr_convert(attr, result.contents.value, StreamAttribs)

    def _setattr(self, attr, value):
        '''Set the value of a stream attribute.

        Keyword arguments:
            attr -- The identifier of the attribute requested.
            value -- The value to set for this attribute.

        '''
        native_streamattrib(self.display, self, attr, value)

    @property
    def consumer_frame(self):
        '''Get the number of frames consumed from this stream.'''
        return self._attr(StreamAttribs.CONSUMER_FRAME)

    @property
    def producer_frame(self):
        '''Get the number of frames inserted into this stream.'''
        return self._attr(StreamAttribs.PRODUCER_FRAME)

    @property
    def state(self):
        '''Get the current state of the stream.'''
        return self._attr(StreamAttribs.STREAM_STATE)

    @property
    def latency(self):
        '''Get the consumer latency of the stream, in microseconds.'''
        return self._attr(StreamAttribs.CONSUMER_LATENCY_μs)
