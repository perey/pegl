#!/usr/bin/env python3

'''Khronos cross-process stream extension for EGL.

This extension allows access to a file descriptor for a stream, so that
the stream producer and consumer can be in difference processes.

http://www.khronos.org/registry/egl/extensions/KHR/EGL_KHR_stream_cross_process_fd.txt

'''
# Copyright © 2013-14 Tim Pederick.
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
from .khr_stream import (c_stream, NO_STREAM, native_createstream, Stream,
                         StreamAttribs)
from ..attribs import AttribList

# Extension types and symbolic constants.
c_streamfd = c_int
NO_FD = c_streamfd(-1)

# Get handles of extension functions.
native_getstreamfd = load_ext(b'eglGetStreamFileDescriptorKHR', c_streamfd,
                              (c_display, c_stream), fail_on=NO_FD)
native_createstreamfromfd = load_ext(b'eglCreateStreamFromFileDescriptorKHR',
                                     c_stream, (c_display, c_streamfd),
                                     fail_on=NO_STREAM)

# Add the extension functions to the Stream class.
def _get_fd(self):
    '''Get a file descriptor for this stream.

    This function must not be called more than once for a given stream.
    It should be accessed using the fd property to ensure this is so.

    '''
    if self._fd is None:
        self._fd = native_getstreamfd(self.display, self)
    return self._fd
Stream.fd = property(_get_fd)

def new_init(self, display, attribs=None, fd=None):
    '''Create the stream.

    Keyword arguments:
        display -- As the instance attribute.
        attribs -- As the instance attribute. If omitted, all
            attributes will take on their default values.
        fd -- A file descriptor for an existing stream in another
            process. If provided, this stream will duplicate that
            existing one for use in the current process and the
            attribs argument will be ignored.

    '''
    self._fd = None
    self.display = display
    if fd is None:
        self.attribs = (attribs if isinstance(attribs, AttribList) else
                        AttribList(StreamAttribs, attribs))
        self.sthandle = native_createstream(self.display, self.attribs)
    else:
        self.attribs = None
        self.sthandle = native_createstreamfromfd(self.display, fd)
Stream.__init__ = new_init
