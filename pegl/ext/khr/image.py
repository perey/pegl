#!/usr/bin/env python3

'''Khronos 2D image array extension for EGL.

Image support is defined in three separate extension specifications. The
original specification has been redefined as the union of the two later
ones (henceforth the "base" and "pixmap" extensions), except for one
property that is not defined if the base extension is not supported.

http://www.khronos.org/registry/egl/extensions/KHR/EGL_KHR_image.txt
http://www.khronos.org/registry/egl/extensions/KHR/EGL_KHR_image_base.txt
http://www.khronos.org/registry/egl/extensions/KHR/EGL_KHR_image_pixmap.txt

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
from ctypes import c_void_p

# Local imports.
from .. import load_ext
from ... import NO_CONTEXT
from ...attribs import (Attribs, AttribList, Details)
from ...context import Context
from ...native import ebool, enum, client_buffer, display, surface, attr_list

# Extension types.
image = c_void_p       # TODO: Rename to something less collision-prone, like
NO_IMAGE = c_void_p(0) # c_image or image_type. This would imply an overhaul of
                       # type naming across the whole library. Whee...
# Get handles of extension functions.
native_create = load_ext(b'eglCreateImageKHR', image,
                         (display, context, enum, client_buffer, attr_list),
                         fail_on=NO_IMAGE)
native_destroy = load_ext(b'eglDestroyImageKHR', ebool,
                          (display, image), fail_on=False)

# Define the new Image type and its attributes.
NATIVE_PIXMAP = 0x30B0

class ImageAttribs(Attribs):
    IMAGE_PRESERVED = 0x30D2 # This is only supported in the base extension,
                             # not in the original!
    details = {IMAGE_PRESERVED: Details('Whether or not existing pixel data '
                                        'should be preserved while creating '
                                        'the image', bool, False)}

class Image:
    '''Represents a 2D image that can be shared between EGL client APIs.

    Class attributes:
        supportable -- A list of the name strings for EGL extensions
            that instances can support.
        acceptable_targets -- A dict mapping target values that can be
            accepted by the constructor to the name strings of the
            extensions that define them.
        extensions -- A mapping of target names loaded onto this class
            to their integer values. By default, this is empty (the
            extensions that define the Image class are built into it).

    Instance attributes:
        ihandle -- The foreign object handle for this image.
        attribs -- The attributes with which this image was created. An
            instance of AttribList.
        context -- The client API context to which this image belongs.
            An instance of Context, or None if no client context is
            required for this image to be created.
        display -- The EGL display to which this image belongs. An
            instance of Display.
        support -- A tuple of the name strings for EGL extensions that
            this image will support. These are chosen from those in the
            class attribute supportable.

    '''
    supportable = ['EGL_KHR_image_base', 'EGL_KHR_image_pixmap']
    acceptable_targets = {NATIVE_PIXMAP: 'EGL_KHR_image_pixmap'}
    extensions = {}

    def __init__(self, buffer, target, attribs=None, context=None,
                 display=None, support=None):
        '''Create the image.

        Keyword arguments:
            buffer -- The existing client image buffer to turn into an
                image for sharing with other client APIs.
            target -- The type of resource being turned into an image.
            attribs -- As the instance attribute. If omitted, all
                attributes will take on their default values.
            context -- As the instance attribute. This may be omitted if
                no client API context is required.
            display -- As the instance attribute. This may be omitted if
                and only if a context is supplied.
            support -- As the instance attribute. If omitted, all
                relevant extensions for which the display declares
                support will be supported. It is not an error if the
                supplied list contains an extension name that the
                display does not support, but it may cause errors later
                on if an unsupported value is passed to a foreign
                function.

        '''
        # The property setter will handle validation of the context.
        self.context = context

        if display is None:
            if self.context is None:
                raise TypeError('must provide a display, a context, or both')
            else:
                # Get the display from the context.
                self.display = self.context.display
        else:
            # TODO: So what happens if self.display != self.context.display?
            # Does the native function complain? Test it!
            self.display = display

        if support is None:
            # Get the extensions from the display.
            self.support = tuple(name for name in self.display.extensions
                                 if name in self.supportable)
        else:
            self.support = support

        # If this raises a KeyError, let it pass upwards.
        extension_needed = self.acceptable_targets[target]
        if extension_needed not in self.support:
            ValueError("need extension '{}' for that "
                       "target".format(extension_needed))

        self.attribs = (attribs if isinstance(attribs, AttribList) else
                        # The AttribList constructor can accept attribs=None.
                        AttribList(ImageAttribs, attribs))
        if ('EGL_KHR_image_base' not in self.support and
            self.attribs['IMAGE_PRESERVED'] is not None):
            # IMAGE_PRESERVED is specifically excluded from the original
            # specification; it needs the base extension.
            raise ValueError("attribute 'IMAGE_PRESERVED' requires extension "
                             "'EGL_KHR_image_base'")

        self.ihandle = native_create(self.display, self.context, target,
                                     buffer, self.attribs)

    def __del__(self):
        '''Destroy the image.'''
        native_destroy(self.display, self)

    @property
    def _as_parameter_(self):
        '''Get the image reference for use by foreign functions.'''
        return self.ihandle

    @property
    def context(self):
        '''Get the context to which this image belongs.

        This property will be None if no context is required, which is
        useful for the user-facing Python interface. The native side of
        things can directly use the _context attribute, which will be
        NO_CONTEXT in that case.

        '''
        return None if self._context == NO_CONTEXT else self._context
    @context.setter
    def context(self, val):
        '''Set the context to which this image will belong.'''
        if val is None:
            self._context = NO_CONTEXT
        elif isinstance(val, Context):
            self._context = val
        else:
            # Look, I know it breaks duck typing, but we're dealing with a
            # native library here. Let's play it safe.
            raise TypeError('context must be an instance of Context')

    @classmethod
    def extend(cls, extension, targets, override=False):
        '''Extend the image class with new target types.

        Keyword arguments:
            extension -- The name string of the extension for which
                support is being added.
            targets -- A mapping of names to values for the new target
                types supported.
            override -- Whether or not the new target types can replace
                existing target types that are represented by the same
                value. The default is False.

        '''
        for name, val in targets.items():
            if not override and val in cls.acceptable_targets:
                raise ValueError('cannot replace existing target type with {} '
                                 '(use override argument to force '
                                 'change)'.format(name))
            cls.extensions[name] = val
            cls.acceptable_targets[val] = extension

        cls.supportable.append(extension)
