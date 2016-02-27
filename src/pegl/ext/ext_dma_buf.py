#!/usr/bin/env python3

'''Cross-vendor Linux dma_buf image binding extension for EGL.

This extension allows file descriptors to be used to create EGL images,
on Linux kernels supporting dma_buf buffer sharing.

http://www.khronos.org/registry/egl/extensions/EXT/EGL_EXT_image_dma_buf_import.txt

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
from collections import namedtuple
from ctypes import c_uint32, c_ulong, c_int as c_fd # For clarity, use an alias
                                                    # type for file descriptors
# Local imports.
from .khr_image import Image, ImageAttribs

# New image target.
Image.extend('EGL_EXT_image_dma_buf_import', {'LINUX_DMA_BUF': 0x3270})

# New image attributes. None of these have defaults given in the specification
# (though they're all either required or merely hints), and even their types
# are a little vague.
ImageAttribs.extend('LINUX_DRM_FOURCC', 0x3271, c_uint32, None)

PLANE_ATTRIBS_START = 0x3272
for plane in range(3):
    for n, attrib in enumerate('FD', 'OFFSET', 'PITCH'):
        ImageAttribs.extend('DMA_BUF_PLANE{}_{}'.format(plane, attrib),
                            PLANE_ATTRIBS_START + plane + n,
                            c_fd if attrib is 'FD' else c_ulong, None)

YUVColorSpaceHints = namedtuple('YUVColorSpaceHints_tuple',
                                ('ITU_REC601', 'ITU_REC709', 'ITU_REC2020')
                                )(0x327F, 0x3280, 0x3281)
ImageAttribs.extend('YUV_COLOR_SPACE_HINT', 0x327B, YUVColorSpaceHints,
                    YUVColorSpaceHints.ITU_REC601)

SampleRangeHints = namedtuple('SampleRangeHints_tuple',
                              ('YUV_FULL_RANGE', 'YUV_NARROW_RANGE')
                              )(0x3282, 0x3283)
ImageAttribs.extend('SAMPLE_RANGE_HINT', 0x327C, SampleRangeHints,
                    SampleRangeHints.YUV_FULL_RANGE)

ChromaSitingHints = namedtuple('ChromaSitingHints_tuple',
                               ('YUV_CHROMA_SITING_0', 'YUV_CHROMA_SITING_0_5')
                               )(0x3284, 0x3285)
ImageAttribs.extend('YUV_CHROMA_HORIZONTAL_SITING_HINT', 0x327D,
                    ChromaSitingHints, ChromaSitingHints.YUV_CHROMA_SITING_0)
ImageAttribs.extend('YUV_CHROMA_VERTICAL_SITING_HINT', 0x327E,
                    ChromaSitingHints, ChromaSitingHints.YUV_CHROMA_SITING_0)
