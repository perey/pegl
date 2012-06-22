#!/usr/bin/env python3

'''Khronos stream-producer surface extension for EGL.

This extension allows an EGL surface to provide image frames to a stream
as a producer.

http://www.khronos.org/registry/egl/extensions/KHR/EGL_KHR_stream_producer_eglsurface.txt

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
from ..stream import stream
from ...import NO_SURFACE
from ...attribs.config import SurfaceTypes
from ...native import attr_list, display, config, surface

# New surface type.
SurfaceTypes.extend(11, 'STREAM')

# Get the handle of the extension function.
native_createstream = load_ext(b'eglCreateStreamProducerSurfaceKHR', surface,
                               (display, config, stream, attr_list),
                               fail_on=NO_SURFACE)

# Define the new Surface subclass.
class StreamSurface(Surface):
    '''Represents a surface that renders to a stream.

    Instance attributes:
        shandle, display, config, attribs -- Inherited from Surface.
        stream -- The stream that this surface renders to. An instance
            of Stream.

    '''
    def __init__(self, display, config, stream, attribs):
        '''Create the stream surface.

        The following attributes from SurfaceAttribs are accepted when
        creating a stream surface:
            * WIDTH and HEIGHT

        Keyword arguments:
            display, config, stream, attribs -- As the instance
                attributes.

        '''
        super().__init__(display, config, attribs)
        self.stream = stream
        self.shandle = native_createstream(self.display, self.config,
                                           self.stream, self.attribs)
