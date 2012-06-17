#!/usr/bin/env python3

'''NVIDIA sync extension for EGL.

This module defines a "fence sync object" that is very similar to the
one defined by the pegl.ext.khr.sync module. A fence sync object is a
synchronization primitive that is automatically signaled when a
condition is met. The condition depends on the completion of "fence
commands" from client APIs.

http://www.khronos.org/registry/egl/extensions/NV/EGL_NV_sync.txt

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
from ctypes import c_int, c_ulonglong, c_void_p
from collections import namedtuple

# Local imports.
from .. import load_ext
from ... import int_p, make_int_p
from ...attribs import attr_convert, Attribs, AttribList, BitMask, Details
from ...native import ebool, enum, attr_list, display

# Extension types and symbolic constants.
sync = c_void_p
time_ns = c_ulonglong
NO_SYNC = c_void_p(0)
FOREVER = 0xFFFFFFFFFFFFFFFF

# Get handles of extension functions.
native_createsync = load_ext(b'eglCreateFenceSyncNV', sync,
                             (display, enum, attr_list), fail_on=NO_SYNC)
native_destroysync = load_ext(b'eglDestroySyncNV', ebool,
                              (sync,), fail_on=False)
native_fence = load_ext(b'eglFenceNV', ebool, (sync,), fail_on=False)
native_clientwait = load_ext(b'eglClientWaitSyncNV', c_int,
                             (sync, c_int, time_ns), fail_on=False)
native_signal = load_ext(b'eglSignalSyncNV', ebool,
                         (sync, enum), fail_on=False)
native_getattrib = load_ext(b'eglGetSyncAttribNV', ebool,
                            (sync, c_int, int_p), fail_on=False)

# Attributes for sync objects.
SyncStatus = namedtuple('SyncStatus_tuple',
                       ('SIGNALED', 'UNSIGNALED')
                       )(0x30E8, 0x30E9)
SyncTypes = namedtuple('SyncTypes_tuple',
                       ('FENCE',)
                       )(0x30EF,)
SyncConditions = namedtuple('SyncConditions_tuple',
                            ('PRIOR_COMMANDS_COMPLETE',)
                            )(0x30E6,)
WaitResults = namedtuple('WaitResults_tuple',
                         ('ALREADY_SIGNALED', 'TIMEOUT_EXPIRED',
                          'CONDITION_SATISFIED')
                         )(0x30EA, 0x30EB, 0x30EC)

class WaitFlags(BitMask):
    '''A bit mask representing flags to the client-wait command.'''
    bit_names = ['FLUSH_COMMANDS']


class SyncAttr(Attribs):
    '''The set of attributes relevant to sync objects.

    Class attributes:
        details -- As per the superclass, Attribs.
        Additionally, symbolic constants for all the known attributes
        are available as class attributes. Their names are the same as
        in the extension specification, except without the EGL_ prefix
        and _NV suffix.

    '''
    # For creating and querying sync objects.
    SYNC_STATUS = 0x30E7
    # Only for querying; at creation, these are passed as their own parameters.
    SYNC_TYPE, SYNC_CONDITION = 0x30ED, 0x30EE

    details = {SYNC_TYPE: Details('The type of this sync object', c_int, 0),
               SYNC_STATUS: Details('Which state this sync object is in',
                                    c_int, SyncStatus.SIGNALED),
               SYNC_CONDITION: Details('Under what condition this sync object '
                                       'will be automatically signaled', c_int,
                                       SyncConditions.PRIOR_COMMANDS_COMPLETE)}


class Sync:
    '''Represents the fence sync object from the NVIDIA EGL extension.

    Instance attributes:
        synchandle -- The foreign object handle for this sync object.
        display -- The EGL display to which this sync object belongs. An
            instance of Display.
        attribs -- The attributes with which this sync object was
            created. An instance of AttribList.
        sync_type -- The type of sync object that the instance
            represents. It is expected that this will always be
            SyncTypes.FENCE.
        sync_condition -- The condition under which this sync object
            will be automatically signaled. A value from the
            SyncConditions tuple.

    '''
    def __init__(self, display, attribs, sync_condition):
        '''Create the sync object.

        Keyword arguments:
            display, attribs, sync_condition -- As the instance
                attributes.

        '''
        self.display = display
        self.attribs = (attribs if isinstance(attribs, AttribList) else
                        AttribList(SyncAttribs, attribs))
        self.sync_condition = sync_condition
        self.synchandle = native_createsync(self.display, self.sync_condition,
                                            self.attribs)

    def __del__(self):
        '''Destroy the sync object.'''
        native_destroysync(self)

    @property
    def _as_parameter_(self):
        '''Get the sync handle for use by foreign functions.'''
        return self.synchandle

    def _attr(self, attr):
        '''Get the value of a sync object attribute.

        Keyword arguments:
            attr -- The identifier of the attribute requested.

        '''
        # Query the attribute, storing the result in a pointer.
        result = make_int_p()
        native_getattrib(self, attr, result)

        # Dereference the pointer and convert to an appropriate type.
        return attr_convert(attr, result.contents.value, SyncAttribs)

    @property
    def status(self):
        '''Get the status of the sync object.'''
        return self._attr(SyncAttribs.SYNC_STATUS)

    @property
    def sync_type(self):
        '''Get the type of the sync object.'''
        return self._attr(SyncAttribs.SYNC_TYPE)

    @property
    def signaled(self):
        '''Get whether or not this sync object is in the signaled state.

        This is a simple wrapper around the status attribute that checks
        it against the SIGNALED and UNSIGNALED statuses.

        Returns:
            True if the sync status is SIGNALED, False if UNSIGNALED, or
            None if the status is something else.

        '''
        return {SyncStatus.SIGNALED: True,
                SyncStatus.UNSIGNALED: False
                # Or None if it's neither of these.
                }.get(self._attr(SyncAttribs.SYNC_STATUS))

    @property
    def sync_condition(self):
        '''Get the condition under which this sync object gets signaled.'''
        return self._attr(SyncAttribs.SYNC_CONDITION)

    def client_wait(self, timeout_ns=FOREVER, flush_commands=False):
        '''Block the calling thread until this sync object is signaled.

        Keyword arguments:
            timeout_ns -- The maximum number of nanoseconds to wait,
                before unblocking regardless of the sync object status.
                If this is zero, the current status is checked and
                the thread is not blocked. If omitted, the blocking will
                never time out.
            flush_commands -- Whether or not to flush any client API
                commands in the current context before blocking. The
                default is False.

        Returns:
            A value from the WaitResults tuple.

        '''
        return native_clientwait(self,
                                 WaitFlags(FLUSH_COMMANDS=flush_commands),
                                 timeout_ns)

    def fence(self):
        '''Insert a fence command into the current context.

        When the condition of this sync object is satisfied by the fence
        command, this object will be signaled.

        '''
        native_fence(self)

    def signal(self, signaled=True):
        '''Signal (or unsignal) the sync object.

        Keyword arguments:
            signaled -- Whether to set the sync object status to
                signaled (True, the default) or unsignaled (False).

        '''
        native_signal(self, SyncStatus.SIGNALED if signaled else
                      SyncStatus.UNSIGNALED)
