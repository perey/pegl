#!/usr/bin/env python3

'''Khronos sync extensions for EGL.

This module contains two "sync object" extensions available in EGL.

A "reusable sync object" is similar to a semaphore, and is used to
synchronize activity between client APIs or threads. Each thread can
manually signal and unsignal the sync object to release or hold a lock.
This can happen many times in the life of a sync object, hence reusable.

A "fence sync object", on the other hand, cannot be manually signaled.
It is created in the unsignaled state and is automatically signaled when
a condition is met. The condition depends on the completion of "fence
commands", a concept from OpenGL that has been extended to other client
APIs.

http://www.khronos.org/registry/egl/extensions/KHR/EGL_KHR_reusable_sync.txt
http://www.khronos.org/registry/egl/extensions/KHR/EGL_KHR_fence_sync.txt

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
native_createsync = load_ext(b'eglCreateSyncKHR', sync,
                             (display, enum, attr_list), fail_on=NO_SYNC)
native_destroysync = load_ext(b'eglDestroySyncKHR', ebool,
                              (display, sync), fail_on=False)
native_clientwait = load_ext(b'eglClientWaitSyncKHR', c_int,
                             (display, sync, c_int, time_ns), fail_on=False)
native_signal = load_ext(b'eglSignalSyncKHR', ebool,
                         (display, sync, enum), fail_on=False)
native_getattrib = load_ext(b'eglGetSyncAttribKHR', ebool,
                            (display, sync, c_int, int_p), fail_on=False)

# Attributes for sync objects.
SyncStatus = namedtuple('SyncStatus_tuple',
                       ('SIGNALED', 'UNSIGNALED')
                       )(0x30F2, 0x30F3)
SyncTypes = namedtuple('SyncTypes_tuple',
                       ('REUSABLE', 'FENCE')
                       )(0x30FA, 0x30F9)
SyncConditions = namedtuple('SyncConditions_tuple',
                            ('PRIOR_COMMANDS_COMPLETE',)
                            )(0x30F0,)

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
        and _KHR suffix.

    '''
    # Only for querying; this is not set at creation, but can be toggled later.
    SYNC_STATUS = 0x30F1
    # Only for querying; at creation, this is passed as its own parameter.
    SYNC_TYPE = 0x30F7
    # As above, plus only valid for fence sync objects.
    SYNC_CONDITION = 0x30F8

    details = {SYNC_TYPE: Details('The type of this sync object', c_int, 0),
               SYNC_STATUS: Details('Which state this sync object is in',
                                    c_int, SyncStatus.UNSIGNALED),
               SYNC_CONDITION: Details('Under what condition this sync object '
                                       'will be automatically signaled', c_int,
                                       SyncConditions.PRIOR_COMMANDS_COMPLETE)}


# TODO: This reuses a fair chunk of code from similar classes, like Surface.
# Can I roll the common code into a base class and then inherit from it?
class Sync:
    '''The base class for all types of EGL sync objects.

    Class attributes:
        extension -- The name string of the extension that defines this
            type of sync object.
        sync_type -- Which type of sync object this class creates. For
            this base class, the value is None. Each subclass will set
            this to a value from the SyncTypes tuple.

    Instance attributes:
        synchandle -- The foreign object handle for this sync object.
        display -- The EGL display to which this sync object belongs. An
            instance of Display.
        attribs -- The attributes with which this sync object was
            created. An instance of AttribList.
        status -- The current status of the sync object. A value from
            the SyncStatus tuple.
        signaled -- Whether the sync object is signaled or not. This
            information is also available from the status attribute,
            but signaled presents it as a boolean.
        sync_type -- The actual type of sync object that the instance
            represents. It is expected that this will always be the same
            as the class attribute.

    '''
    extension = ''
    sync_type = None

    def __init__(self, display, attribs):
        '''Create the sync object.

        Keyword arguments:
            display, attribs -- As the instance attributes.

        '''
        if self.__class__.extension not in display.extensions:
            raise TypeError("extension for '{}' sync objects "
                            "unavailable".format(self.__class__.__name__))
        self.display = display
        self.attribs = (attribs if isinstance(attribs, AttribList) else
                        AttribList(SyncAttribs, attribs))
        self.synchandle = native_createsync(self.display,
                                            self.__class__.sync_type,
                                            self.attribs)

    def __del__(self):
        '''Destroy the sync object.'''
        native_destroysync(self.display, self)

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
        native_getattrib(self.display, self, attr, result)

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
            True if the sync object was signaled, or False if the
            timeout expired.

        '''
        TIMEOUT_EXPIRED, CONDITION_SATISFIED = 0x30F5, 0x30F6

        result = native_clientwait(self.display, self,
                                   WaitFlags(FLUSH_COMMANDS=flush_commands),
                                   timeout_ns)
        if result == CONDITION_SATISFIED:
            return True
        elif result == TIMEOUT_EXPIRED:
            return False
        else:
            raise ValueError('got an unknown result code')


class ReusableSync(Sync):
    '''Represents the "reusable" type of sync object.

    Class attributes:
        extension -- The name string of the reusable sync extension.
        sync_type -- SyncTypes.REUSABLE.

    Instance attributes:
        synchandle, display, status, signaled, sync_type -- As per the
            superclass, Sync.
        attribs -- Always an empty AttribList.

    '''
    extension = 'EGL_KHR_reusable_sync'
    sync_type = SyncTypes.REUSABLE

    def __init__(self, display):
        '''Create the reusable sync object.

        Keyword arguments:
            display -- As the instance attribute.

        '''
        # Reusable sync objects have empty attribute lists.
        super().__init__(display, {})

    def signal(self, signaled=True):
        '''Signal (or unsignal) the sync object.

        Keyword arguments:
            signaled -- Whether to set the sync object status to
                signaled (True, the default) or unsignaled (False).

        '''
        native_signal(self.display, self,
                      SyncStatus.SIGNALED if signaled else
                      SyncStatus.UNSIGNALED)


class FenceSync(Sync):
    '''Represents the "fence" type of sync object.

    Class attributes:
        extension -- The name string of the fence sync extension.
        sync_type -- SyncTypes.FENCE.

    Instance attributes:
        synchandle, display, status, signaled, sync_type -- As per the
            superclass, Sync.
        attribs -- Always an empty AttribList.
        sync_condition -- The condition under which this sync object
            will be automatically set to signaled. A value from the
            SyncConditions tuple.

    '''
    extension = 'EGL_KHR_fence_sync'
    sync_type = SyncTypes.FENCE

    def __init__(self, display):
        '''Create the fence sync object.

        Keyword arguments:
            display -- As the instance attribute.

        '''
        # Fence sync objects have empty attribute lists.
        super().__init__(display, {})

    @property
    def sync_condition(self):
        '''Get the condition under which this sync object gets signaled.'''
        return self._attr(SyncAttribs.SYNC_CONDITION)
