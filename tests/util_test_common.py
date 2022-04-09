#!/usr/bin/env python3

'''Common definitions and utilities for Pegl unit tests.'''

# Copyright © 2020, 2021 Tim Pederick.
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

# Import other test utilities.
from util_test_display import get_native_display

# Import library being tested.
import pegl

# List known EGL versions.
known_versions = ((1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5))

# Class decorators for common set-up and tear-down stages.
def needs_display(cls):
    """Decorator for test cases that need a display."""
    def setUp(self):
        """Set up a display for testing."""
        if pegl.egl_version < (1, 4):
            ndhandle, self.ndobj = get_native_display()
            self.dpy = pegl.Display(ndhandle)
        else:
            self.ndobj = None
            self.dpy = pegl.Display()
    setattr(cls, 'setUp', setUp)

    def tearDown(self):
        """Finalize the display used for testing."""
        del self.dpy
        del self.ndobj
    setattr(cls, 'tearDown', tearDown)

    return cls

def needs_config(cls):
    """Decorator for test cases that need a config."""
    def setUp(self):
        """Set up a display and config for testing."""
        if pegl.egl_version < (1, 4):
            ndhandle, self.ndobj = get_native_display()
            self.dpy = pegl.Display(ndhandle)
        else:
            self.ndobj = None
            self.dpy = pegl.Display()
        self.cfg = self.dpy.get_configs(1)[0]
    setattr(cls, 'setUp', setUp)

    def tearDown(self):
        """Finalize the display used for testing."""
        # Configs don't need finalizing.
        del self.dpy
        del self.ndobj
    setattr(cls, 'tearDown', tearDown)

    return cls

def needs_context(cls):
    """Decorator for test cases that need a current context."""
    def setUp(self):
        """Set up a context and its requirements for testing."""
        if pegl.egl_version < (1, 4):
            ndhandle, self.ndobj = get_native_display()
            self.dpy = pegl.Display(ndhandle)
        else:
            self.ndobj = None
            self.dpy = pegl.Display()
        self.cfg = self.dpy.get_configs(1)[0]
        self.ctx = self.cfg.create_context()
        self.surf = self.cfg.create_pbuffer_surface(
            {pegl.SurfaceAttrib.WIDTH: 20,
             pegl.SurfaceAttrib.HEIGHT: 20})
        self.ctx.make_current(self.surf)
    setattr(cls, 'setUp', setUp)

    def tearDown(self):
        """Finalize the EGL objects used for testing."""
        pegl.Context.release_current()
        del self.surf
        del self.ctx
        del self.dpy
        del self.ndobj
    setattr(cls, 'tearDown', tearDown)

    return cls
