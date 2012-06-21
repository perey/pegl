#!/usr/bin/env python3

'''Khronos FIFO stream extension for EGL.

This extension alters the behavior of the base stream extension to
operate in FIFO, rather than mailbox, fashion. That is, instead of
holding at most one frame (the most recent) and dropping any excess
frames, all frames up to a limit are held until consumed and the
producer may be blocked from adding more.

http://www.khronos.org/registry/egl/extensions/KHR/EGL_KHR_stream_fifo.txt

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
from ctypes import POINTER, c_int, c_ulonglong
from collections import namedtuple

# Local imports.
from .. import load_ext
from ..stream import Stream, StreamAttribs
from ...native import ebool, enum, display

# New extension types.
time_ns = c_ulonglong
time_ns_p = POINTER(time_ns)

# Get the handle of the new extension function.
native_streamtime = load_ext(b'eglQueryStreamTimeKHR', ebool,
                             (display, stream, enum, time_ns_p), fail_on=False)

# New attributes for stream objects.
StreamAttribs.extend('STREAM_FIFO_LENGTH', 0x31FC, c_int, 0)

StreamTimeReferences = namedtuple('StreamTimeReferences_tuple',
                                  ('NOW', 'CONSUMER', 'PRODUCER')
                                  )(0x31FD, 0x31FE, 0x31FF)

# Add the new extension function to the Stream class.
def time_of(self, reference=StreamTimeReferences.NOW):
    '''Get the time now, or from the last frame produced or consumed.

    Keyword arguments:
        reference -- Which timestamp to fetch. This may be a value from
            the StreamTimeReferences tuple, or the string name of such a
            value ('NOW', 'CONSUMER' or 'PRODUCER'). If omitted or NOW,
            the current time is provided. If CONSUMER, the timestamp of
            the last frame consumed is returned, and if PRODUCER, the
            timestamp of the last frame inserted.

    Returns:
        A system time (i.e. the interval since power on or another
        system-defined event), in nanoseconds.

    '''
    # Ready a pointer to store the result.
    result = time_ns_p()
    result.contents = time_ns(0)

    # Convert string arguments to their equivalent values.
    reference = {'NOW': StreamTimeReferences.NOW,
                 'CONSUMER': StreamTimeReferences.CONSUMER,
                 'PRODUCER': StreamTimeReferences.PRODUCER
                 }.get(str(reference).upper(),
                       reference) # Leave it unchanged if not in the dict.

    # Get the time value.
    native_streamtime(self.display, self, reference, result)

    # Dereference the pointer.
    return result.contents.value
Stream.time_of = time_of
