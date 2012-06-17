#!/usr/bin/env python3

'''Mesa DRM image extension for EGL.

This extension maps EGL images (from the Khronos image extensions) to
the Linux DRM (Direct Rendering Manager) system.

http://www.khronos.org/registry/egl/extensions/MESA/EGL_MESA_drm_image.txt

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
from collections import namedtuple
from ctypes import c_int

# Local imports.
from .. import load_ext
from ..khr.image import image, Image, ImageAttribs, NO_IMAGE
from ... import int_p, make_int_p
from ...attribs import Attribs, AttribList, BitMask, Details
from ...attribs.surface import SurfaceAttribs
from ...native import ebool, display, attr_list

# Symbolic constants for values used more than once.
DRM_BUFFER_FORMAT = 0x31D0

# Get handles of extension functions.
native_create = load_ext(b'eglCreateDRMImageMESA', image, (display, attr_list),
                         fail_on=NO_IMAGE) # Not actually in the spec.
native_export = load_ext(b'eglExportDRMImageMESA', ebool,
                         (display, image, int_p, int_p, int_p),
                         fail_on=False) # Also not in the spec, but implied...

# New image attributes, for importing a shared buffer into an image.
ImageAttribs.extend('DRM_BUFFER_STRIDE', 0x31D4, c_int, 0)
ImageAttribs.extend('DRM_BUFFER_FORMAT', DRM_BUFFER_FORMAT, c_int, 0)
ImageAttribs.extend('WIDTH', SurfaceAttribs.WIDTH, c_int, 0)
ImageAttribs.extend('HEIGHT', SurfaceAttribs.WIDTH, c_int, 0)

Image.extend('EGL_MESA_drm_image', {'DRM_BUFFER': 0x31D3})

# Brand new attributes for creating entirely new DRM-linked images.
DRMBufferFormats = namedtuple('DRMBufferFormats_tuple',
                              ('ARGB32',)
                              )(0x31B2,)

class DRMBufferUses(BitMask):
    '''A bit mask denoting uses for DRM image buffers.'''
    bit_names = ['SCANOUT', 'SHARE']


class DRMImageAttribs(Attribs):
    '''The set of EGL extension attributes applicable to DRM images.

    Class attributes:
        details -- As per the superclass, Attribs.
        Additionally, symbolic constants for all the known attributes
        are available as class attributes. Their names are the same as
        in the extension specification, except without the EGL_ prefix
        and _MESA suffix.

    '''
    WIDTH, HEIGHT = SurfaceAttribs.WIDTH, SurfaceAttribs.HEIGHT
    DRM_BUFFER_FORMAT = DRM_BUFFER_FORMAT
    DRM_BUFFER_USE = 0x31D1

    details = {WIDTH: Details('Width in pixels of the image', c_int, 0),
               HEIGHT: Details('Height in pixels of the image', c_int, 0),
               DRM_BUFFER_FORMAT: Details('The format of the DRM color buffer',
                                          DRMBufferFormats,
                                          DRMBufferFormats.ARGB32),
               DRM_BUFFER_USE: Details('A bit mask requesting that the image '
                                       'be usable as particular DRM buffers',
                                       DRMBufferUses, DRMBufferUses())}


# Subclass the Image class.
class DRMImage(Image):
    '''Represents a 2D image associated with a DRM buffer.

    Class attributes:
        supportable -- A list of the name strings for EGL extensions
            that instances will support.

    Instance attributes:
        ihandle -- The foreign object handle for this image.
        attribs -- The DRM image attributes with which this image was
            created. An instance of AttribList.
        display -- The EGL display to which this image belongs. An
            instance of Display.

    '''
    # Generally ignored, since the parent class uses these to determine the
    # acceptable targets. But there's no harm in defining them, and they stop
    # the inherited extend() class method from raising an exception.
    supportable = ['EGL_KHR_image_base', 'EGL_MESA_drm_image']
    acceptable_targets = {}
    extensions = {}

    def __init__(self, display, attribs=None):
        '''Create the image and its DRM buffer.

        Keyword arguments:
            display -- As the instance attribute.
            attribs -- As the instance attribute. If omitted, all
                attributes will take on their default values.

        '''
        self.display = display
        self.attribs = (attribs if isinstance(attribs, AttribList) else
                        # The AttribList constructor can accept attribs=None.
                        AttribList(DRMImageAttribs, attribs))

        self.ihandle = native_create(self.display, self.attribs)

        # Unneeded attributes from the superclass.
        self.context = self.support = self.target = None

    def export(self, assign_name=True, assign_handle=True, assign_stride=True):
        '''Assign a global name or process-local handle to the buffer.

        Keyword arguments:
            assign_name -- Whether to assign a global name to the
                buffer. The default is True.
            assign_name -- Whether to assign a process-local handle to
                the buffer. The default is True.
            assign_stride -- Whether to get the stride of the buffer
                (bytes between rows). The default is True.

        Returns:
            A 3-tuple with the resulting values, or None for any where
            the relevant assign_* argument was False.

        '''
        name = make_int_p() if assign_name else int_p(None)
        handle = make_int_p() if assign_handle else int_p(None)
        stride = make_int_p() if assign_stride else int_p(None)

        native_export(self.display, self, name, handle, stride)

        # Dereference the pointers.
        return (name.contents.value if assign_name else None,
                handle.contents.value if assign_handle else None,
                stride.contents.value if assign_stride else None)
