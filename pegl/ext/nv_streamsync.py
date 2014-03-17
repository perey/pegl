#!/usr/bin/env python3

'''NVIDIA stream-wait sync extension for EGL.

A stream-wait sync object is a kind of reusable sync object. Instead of
being manually signaled, it is signaled each time a new frame becomes
available in a stream. It is then manually unsignaled.

http://www.khronos.org/registry/egl/extensions/NV/EGL_NV_stream_sync.txt

'''
# Copyright © 2014 Tim Pederick.
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
from ctypes import c_int

# Local imports.
from . import load_ext
from .khr_stream import c_stream
from .khr_sync import (c_sync, NO_SYNC, native_signal, Sync, SyncAttribs,
                       SyncStatus)
from ..native import c_display, c_enum, c_attr_list

# Get the handle of the extension function.
native_createstreamsync = load_ext(b'eglCreateStreamSyncNV', c_sync,
                                   (c_display, c_stream, c_enum, c_attr_list),
                                   fail_on=NO_SYNC)

# TODO: Replace the SyncTypes named tuple with an extensible enumeration?
SYNC_NEW_FRAME = 0x321F

# Wrap the new sync type in a subclass of Sync.
class StreamSync(Sync):
    '''Represents the "stream" type of sync object.

    Class attributes:
        extension -- The name string of the stream sync extension.
        sync_type -- 0x321F, under the symbolic name SYNC_NEW_FRAME.

    Instance attributes:
        synchandle, display, status, signaled, sync_type -- As per the
            superclass, Sync.
        attribs -- Always an empty AttribList.
        stream -- The EGL stream to which this sync object refers.

    '''
    extension = 'EGL_NV_stream_sync'
    sync_type = SYNC_NEW_FRAME

    def __init__(self, display, stream):
        '''Create the stream sync object, aimed at the given stream.

        Keyword arguments:
            display, stream -- As the instance attributes.

        '''
        self.stream = stream
        # Stream sync objects have empty attribute lists.
        super().__init__(display, {})

    def _create_handle(self):
        '''Call the native function that generates the sync handle.

        Returns:
            The new native sync handle.

        '''
        return native_createstreamsync(self.display, self.stream,
                                       self.__class__.sync_type,
                                       self.attribs)

    def unsignal(self):
        '''Unsignal the sync object.'''
        native_signal(self.display, self, SyncStatus.UNSIGNALED)
