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
image = c_void_p
NO_IMAGE = c_void_p(0)

# Get handles of extension functions.
native_create = load_ext(b'eglCreateImageKHR', image,
                         (display, context, enum, client_buffer, attr_list),
                         fail_on=NO_IMAGE)
native_destroy = load_ext(b'eglDestroyImageKHR', ebool,
                          (display, image), fail_on=False)

# Define the targets that Image knows how to accept.
# TODO: Have I grossly overengineered this? (Probably.) Does Image only need
# to know values and extensions?
class _Targets:
    '''A three-way mapping of target names, values, and extension names.

    When used as a sequence type, a Targets instance gives its values.
    Its names can be used as instance attributes, and queried by passing
    the value as an index (thus targets[val] == name). Extension names
    are supplied only by the method extension_for().

    '''
    def __init__(self, mapping=None, extension=None):
        '''Create the mapping of targets.

        Keyword arguments:
            mapping -- An optional mapping object containing the initial
                names and values that the instance will contain.
            extension -- The name of the extension providing the initial
                contents of this instance. This is required if mapping
                is supplied, and is not meaningful otherwise.

        '''
        self.names = {}
        self.values = {}

        if mapping is not None:
            if extension is None:
                raise TypeError('an extension name must be supplied if '
                                'initial contents are specified')

            for name, val in mapping.items():
                self.names[name] = val
                self.values[val] = (name, extension)

    def __contains__(self, val):
        '''Determine whether a given value is present in the mapping.'''
        return val in self.values

    def __iter__(self):
        '''Iterate over the values in the mapping.'''
        return iter(self.values)

    def __getattr__(self, attr):
        '''Get the value that matches a given name.'''
        try:
            return self.names[attr]
        except KeyError:
            # Hack! Avoid overcomplicating the backtrace.
            pass
        raise AttributeError("'{}' has no attribute "
                             "'{}'".format(self.__class__.__name__, attr))

    def __getitem__(self, val):
        '''Get the name that matches a given value.'''
        # The name is item #0 in the tuple.
        return self.values[val][0]

    # __setitem__() is not supported; use extend() instead.

    def __delitem__(self, val_or_name):
        '''Delete a name/value pair from the mapping.

        Keyword arguments:
            val_or_name -- The value or name to remove. If the argument
                should happen to be valid as both a value and a name
                (which shouldn't ever be the case), it will be used as
                a value.

        '''
        if val_or_name in self.values:
            # Given a value.
            val = val_or_name
            name = self[val]
        else:
            # Given a name (or nonsense, in which case let the error pass).
            name = val_or_name
            val = self.names[name]

        del self.names[name]
        del self.values[val]

    def extend(self, name, val, extension, override=False):
        '''Extend the mapping.

        Keyword arguments:
            name -- The new name to add.
            val -- The new value for that name to take.
            extension -- The name string of the extension specifying
                this name-value pair.
            override -- Whether or not the new name and value can
                replace an existing name or value. The default is False.

        '''
        if not override and (name in self.names or val in self.values):
            raise ValueError('could not replace existing name or value '
                             '(use override argument to force change)')
        self.names[name] = val
        self.values[val] = (name, extension)

    def extension_for(self, val_or_name):
        '''Get the extension that specified a value or a name.

        Keyword arguments:
            val_or_name -- The value or name to look up. If the argument
                should happen to be valid as both a value and a name
                (which shouldn't ever be the case), it will be used as
                a value.

        '''
        if val_or_name in self.values:
            # Given a value.
            val = val_or_name
        else:
            # Given a name (or nonsense, in which case let the error pass up).
            val = self.names[val_or_name]

        # The extension is item #1 in the tuple.
        return self.values[val][1]


ACCEPTABLE_TARGETS = _Targets({'NATIVE_PIXMAP': 0x30B0},
                              'EGL_KHR_image_pixmap')

# Define the new Image type and its attributes.
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

    Instance attributes:
        ihandle -- The foreign object handle for this image.
        attribs -- The attributes with which this surface was created.
            An instance of AttribList.
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
                support will be supported.

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
        extension_needed = ACCEPTABLE_TARGETS[target]
        if extension_needed not in self.support:
            raise NotImplementedError("need extension '{}' for that "
                                      "target".format(extension_needed))

        # FIXME: This isn't right. If the base extension is not supported, only
        # IMAGE_PRESERVED is disallowed. Other extensions could add attributes.
        self.attribs = (AttribList(ImageAttribs) # If the base extension is not
                        if 'EGL_KHR_image_base'  # supported, nothing can be in
                        not in self.support else # the list of attributes.
                        attribs if isinstance(attribs, AttribList) else
                        # The AttribList constructor can accept attribs=None.
                        AttribList(ImageAttribs, attribs))

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