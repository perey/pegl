#!/usr/bin/env python3

'''Test creating a WindowSurface bound to an X11 window.'''

# Copyright © 2014 Tim Pederick.
# Based on examples/draw.py from python-x11:
#     Copyright © 2000 Peter Liljenberg <petli@ctrl-c.liu.se>
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

from pegl import display, config, surface
from Xlib import X, display as Xdisplay

class TestApp:
    '''A bare-bones X11 window.'''
    def __init__(self, dpy):
        self.Xdisplay = dpy
        self.screen = self.Xdisplay.screen()

        self.window = self.screen.root.create_window(5, 5, 640, 480, 1,
                                                     self.screen.root_depth)
        self.DELETE_WINDOW = self.Xdisplay.intern_atom('WM_DELETE_WINDOW')
        self.PROTOCOLS = self.Xdisplay.intern_atom('WM_PROTOCOLS')

        self.window.set_wm_name('Pegl test: X11')
        self.window.set_wm_protocols((self.DELETE_WINDOW,))

        self.EGLdisplay = display.Display()
        self.config = config.get_configs(self.EGLdisplay)[0]
        self.surface = surface.WindowSurface(self.EGLdisplay, self.config, {},
                                             self.window.id)
        self.window.map()

    def loop(self):
        while True:
            ev = self.Xdisplay.next_event()

            if ev.type == X.DestroyNotify:
                raise SystemExit()
            elif ev.type == X.ClientMessage:
                fmt, data = ev.data
                if fmt == 32 and data[0] == self.DELETE_WINDOW:
                    raise SystemExit()


if __name__ == '__main__':
    app = TestApp(Xdisplay.Display())
    app.loop()
