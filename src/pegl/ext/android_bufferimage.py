#!/usr/bin/env python3

'''Android native-buffer image source extension for EGL.

This extension makes Android window buffers useable as sources by the
Image extension class.

http://www.khronos.org/registry/egl/extensions/ANDROID/EGL_ANDROID_image_native_buffer.txt

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
from .khr_image import Image

# New Image target type.
Image.extend('EGL_ANDROID_image_native_buffer', {'NATIVE_BUFFER': 0x3140})
