#!/usr/bin/env python3

'''Khronos OpenVG parent image binding for EGL.

http://www.khronos.org/registry/egl/extensions/KHR/EGL_KHR_vg_parent_image.txt

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
from .image import Image

# Extension image target type.
Image.extend('EGL_KHR_vg_parent_image', {'VG_PARENT_IMAGE': 0x30BA})
