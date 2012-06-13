#!/usr/bin/env python3

'''EGL display management.'''

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
from ctypes import c_void_p

# Local imports.
from . import make_int_p, native, NO_DISPLAY, NO_CONTEXT, NO_SURFACE

# EGL constants.
# TODO: Put these four in a namedtuple instance, like in all the other modules?
CLIENT_APIS, EXTENSIONS, VENDOR, VERSION = 0x308D, 0x3055, 0x3053, 0x3054
DEFAULT_DISPLAY = c_void_p(0)

# Version info structure.
Version = namedtuple('Version', ('major', 'minor', 'vendor'))
Version.__str__ = lambda self: '{0.major}.{0.minor} {0.vendor}'.format(self)

def current_display():
    '''Get the current EGL display.'''
    return Display(dhandle=native.eglGetCurrentDisplay())

class Display:
    '''An EGL display.

    In EGL, a display is not only a representation of a (physical or
    virtual) display device; it is also the overall context of all EGL
    operations (although "context" also has a different meaning in EGL).
    As such, details of the EGL implementation are accessed from a
    Display instance.

    Instance attributes:
        dhandle -- The foreign object handle for this display.
        client_apis -- A sequence listing the client APIs supported
            (such as OpenGL, OpenGL_ES, and OpenVG). Although I can't
            find it specified in the EGL standard, it seems likely that
            these will be limited to ASCII.
        extensions -- A sequence listing the EGL extensions supported;
            again, probably limited to ASCII.
        swap_interval -- An integer number of video frames between
            buffer swaps. This value is write-only and applies to the
            current context. It will be clamped to the range permitted
            by the context's configuration.
        vendor -- The vendor string for this EGL implementation.
        version -- A 3-tuple describing the implementation version, in
            the format (major, minor, vendor_info).

    '''
    def __init__(self, dhandle=None, native_id=None, delay_init=False):
        '''Get a display, either a specified one or the default one.

        Keyword arguments:
            dhandle -- As the instance attribute. If omitted, the
                native_id is used, if supplied, or else the EGL default
                display is requested.
            native_id -- An identifier for a platform-native display.
                This is ignored if dhandle is supplied. If both are
                omitted, the EGL default display is requested.
            delay_init -- If True, the display's initialize() method
                will not be called automatically. This should then be
                done by the application before doing any EGL operations.

        '''
        self.dhandle = (dhandle if dhandle is not None else
                        native.eglGetDisplay(DEFAULT_DISPLAY
                                             if native_id is None else
                                             native_id))
        if not delay_init:
            self.initialize()

    def __del__(self):
        '''Delete this display and all EGL resources in this thread.

        Multithreaded applications should also call release() from all
        all other threads in which this display has been used.

        '''
        release_thread()
        self.terminate()

    def __eq__(self, other):
        '''Compare two displays for equivalence.

        Two displays are considered equal if they have the same foreign
        function reference (i.e. the dhandle attribute).

        '''
        try:
            return self.dhandle == other.dhandle
        except AttributeError:
            # The other object doesn't have a dhandle.
            return False

    @property
    def _as_parameter_(self):
        '''Get the display reference for use by foreign functions.'''
        return self.dhandle

    def _attr(self, attr):
        '''Query an EGL instance parameter.

        Keyword arguments:
            attr -- A value identifying the parameter sought. This
                should be a symbolic constant from those defined in this
                module (CLIENT_APIS, EXTENSIONS, VENDOR, or VERSION).
        Returns:
            A string value for the EGL parameter requested.

        '''
        # TODO: The codec chosen is a bit arbitrary and might be best left off.
        # Client applications can just use the bytes or decode them themselves.
        return native.eglQueryString(self, attr).decode('ISO-8859-1')

    @property
    def client_apis(self):
        '''Get the client APIs available on this EGL instance.'''
        return tuple(self._attr(CLIENT_APIS).split())

    @property
    def extensions(self):
        '''Get the extensions available on this EGL instance.'''
        return tuple(self._attr(EXTENSIONS).split())

    def set_swap_interval(self, val):
        '''Set the number of video frames between buffer swaps.

        This value applies to the current context, and will be silently
        clamped to the range defined by the context's configuration.

        Keyword arguments:
            val -- The number of frames to set the interval to.

        '''
        native.eglSwapInterval(self, int(val))
    set_swap_interval = property(fset=set_swap_interval)

    @property
    def vendor(self):
        '''Get the vendor string for this EGL instance.'''
        return self._attr(VENDOR)

    @property
    def version(self):
        '''Get the EGL version of this EGL instance.'''
        major_minor, vendor = self._attr(VERSION).split(None, 1)
        major, minor = major_minor.split('.')
        return Version(int(major), int(minor), vendor)

    def initialize(self):
        '''Initialize EGL for this display.

        Returns:
            An EGL version number, in (major, minor, vendor) format.
            The vendor part is an empty string; after initialization
            it can be obtained from the version attribute.

        '''
        # Create and initialize the return pointers.
        major, minor = make_int_p(), make_int_p()

        native.eglInitialize(self, major, minor)
        return (major.contents.value, minor.contents.value, '')

    def load_extension(self, extname):
        '''Load an extension conditional on it being declared available.

        The extensions attribute of this display is used to determine
        whether the extension named is supported by the implementation
        of EGL that the display represents. An ImportError will be
        raised to signify that the extension is unavailable. Also, even
        when it is declared to be available, if an ImportError occurs
        anyway while the extension module is being loaded, it will be
        raised.

        Keyword arguments:
            extname -- The name string of the extension. Name strings
                are consistently of the form EGL_xxx_yyy, where xxx
                represents the vendor proposing the extension (or EXT
                for a cross-vendor proposal) and yyy is a descriptive
                name for the extension.

        '''
        # Ensure the name is a string.
        extname = str(extname)

        if extname not in self.extensions:
            raise ImportError('implementation does not declare support for ' +
                              extname)

        egl_prefix, vendor, name = extname.split('_', 2)
        if egl_prefix != 'EGL':
            # How on earth did we get this far?
            raise ValueError("extension names must begin with 'EGL_'")
        elif vendor == 'EXT':
            # Cross-vendor extensions live in the ext package.
            vendor_pkg = 'ext'
            from . import ext as ext_pkg
        else:
            # Extensions from vendor xxx live in the ext.xxx subpackage.
            vendor_pkg = 'ext.' + vendor.lower()
            top_ext_pkg = __import__(vendor_pkg, globals(), locals(), [], 1)
            ext_pkg = getattr(top_ext_pkg, vendor.lower())

        # What module has this extension?
        module_name = ext_pkg.extensions.get(extname)

        if module_name is None:
            raise ImportError("no module found for extension "
                              "'{}'".format(extname))
        else:
            pkg_with_module = __import__(vendor_pkg, globals(), locals(),
                                         [module_name], 1)
            return getattr(pkg_with_module, module_name)

    def terminate(self):
        '''Invalidate all resources associated with this display.

        The display handle itself remains valid, and so its release()
        method can still be called in any threads that have used it. The
        display can even be reinitialized (by calling initialize()),
        though the terminated resources will not be made valid again.

        It is not generally necessary to call this function directly, as
        it is called by the display's destructor method. The only
        difference is that the destructor also calls release().

        '''
        native.eglTerminate(self)

def release_thread():
    '''Release EGL resources used in this thread.

    This cleanup is performed automatically for the current thread when
    a display is deleted. Multithreaded applications that share one
    display across several threads must call this function in each
    thread to ensure all resources are deallocated.

    '''
    native.eglReleaseThread()
