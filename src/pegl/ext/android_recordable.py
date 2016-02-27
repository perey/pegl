#!/usr/bin/env python3

'''Android recordable configuration extension for EGL.

This extension makes it possible for a configuration to check whether
Android native windows (ANativeWindow) can be used for EGL surfaces when
their rendered images are being recorded to a video.

http://www.khronos.org/registry/egl/extensions/ANDROID/EGL_ANDROID_recordable.txt

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

# Local imports.
from ..attribs import DONT_CARE
from ..attribs.config import ConfigAttribs

# New config attribute.
ConfigAttribs.extend('RECORDABLE_ANDROID', 0x3142, bool, DONT_CARE,
                     'Whether a Surface can be created from an Android '
                     'ANativeWindow that is being recorded to a video')

# New Config property, for querying the new attribute in ConfigAttribs.
def recordable_android(self):
    '''Check whether recorded windows are usable as surfaces.

    Android native windows that record rendered images to a video may
    not be suitable for use as EGL surfaces, so this attribute
    determines whether such use is supported on the current device.

    '''
    return self._attr(ConfigAttribs.RECORDABLE_ANDROID)
Config.recordable_android = property(recordable_android)
