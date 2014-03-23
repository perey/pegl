#!/usr/bin/env python3

'''Cross-vendor graphics platform support extension for EGL.

This extension allows multiple platforms (window systems and non-window
graphics servers) to be supported by an EGL implementation. Other
extensions add the specific details for each particular platform.

http://www.khronos.org/registry/egl/extensions/EXT/EGL_EXT_platform_base.txt

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
from ctypes import c_void_p

# Local imports.
from . import load_ext
from ..attribs import Attribs, AttribList
from ..display import Display
from ..native import c_attr_list, c_config, c_display, c_enum, c_surface
from ..surface import PixmapSurface, WindowSurface

# Get handles of the new extension functions.
native_getdisplay = load_ext(b'eglGetPlatformDisplayEXT', c_display,
                             (c_enum, c_void_p, c_attr_list))
native_windowsurface = load_ext(b'eglCreatePlatformWindowSurfaceEXT',
                                c_surface,
                                (c_display, c_config, c_void_p, c_attr_list))
native_pixmapsurface = load_ext(b'eglCreatePlatformPixmapSurfaceEXT',
                                c_surface,
                                (c_display, c_config, c_void_p, c_attr_list))

# New Attribs subclass.
class DisplayAttribs(Attribs):
    '''The set of EGL attributes relevant to platform displays.

    Class attributes:
        details -- As per the superclass, Attribs.

    '''
    detail = {} # Nothing here! Other extensions can put stuff in.

# New Display and Surface subclasses.
# TODO: Consider whether functions (perhaps a new method on each base class)
# might not be a better idea than new class hierarchies.

class PlatformDisplay(Display):
    '''Superclass for all platform-specific displays.

    Class attributes:
        platform -- The numeric identifier for the native platform. All
            subclasses must define this; it is None in this class, and
            so this class cannot be instantiated.

    Instance attributes:
        dhandle, client_apis, extensions, swap_interval, vendor,
        version -- Inherited from Display.
        attribs -- The attributes with which this display was created.
            An instance of AttribList.

    '''
    platform = None

    def __init__(self, native_id, attribs, delay_init=False):
        '''Get a display for this platform.

        Keyword arguments:
            native_id -- As the superclass constructor, but not optional.
            attribs -- As the instance attribute.
            delay_init -- As the superclass constructor.

        '''
        # We're not trying to instantiate THIS class, are we?
        if self.__class__.platform is None:
            raise NotImplementedError("use a subclass of PlatformDisplay that "
                                      "defines class attribute 'platform'")

        self.attribs = (attribs if isinstance(attribs, AttribList) else
                        AttribList(DisplayAttribs, attribs))
        dhandle = native_getdisplay(self.__class__.platform, native_id,
                                    attribs)

        # Call the parent class constructor.
        super().__init__(dhandle=dhandle, delay_init=delay_init)


class PlatformPixmapSurface(PixmapSurface):
    '''Represents a surface that renders to a window pixmap.

    Instance attributes:
        shandle, display, config, attribs -- Inherited from
            PixmapSurface.

    '''
    def __init__(self, display, config, attribs, pixmap):
        '''Create the pixmap surface.

        Only the following attributes from SurfaceAttribs are accepted
        when creating a pixmap surface:
            * VG_COLORSPACE and VG_ALPHA_FORMAT (only used by OpenVG)

        Keyword arguments:
            display, config, attribs -- As the instance attributes.
            pixmap -- The platform pixmap to render to.

        '''
        super().__init__(display, config, attribs)
        self.shandle = native_pixmapsurface(self.display, self.config,
                                            pixmap, self.attribs)


class PlatformWindowSurface(WindowSurface):
    '''Represents an on-screen surface bound to a platform window.

    Instance attributes:
        shandle, display, config, attribs -- Inherited from
            WindowSurface.

    '''
    def __init__(self, display, config, attribs, window):
        '''Create the window surface.

        The following attributes from SurfaceAttribs are accepted when
        creating a window surface:
            * RENDER_BUFFER
            * VG_COLORSPACE and VG_ALPHA_FORMAT (only used by OpenVG)

        Keyword arguments:
            display, config, attribs -- As the instance attributes.
            window -- The platform window to which this surface belongs.

        '''
        super().__init__(display, config, attribs)
        self.shandle = native_windowsurface(self.display, self.config,
                                            window, self.attribs)
