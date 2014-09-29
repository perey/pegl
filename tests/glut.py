#!/usr/bin/env python3

'''Test creating a WindowSurface bound to a GLUT window.'''

# Copyright © 2014 Tim Pederick.
# Based on GLUT/gears.py from PyOpenGL-Demo, by Brian Paul, Mark J. Kilgard
# and Peter Barth, placed in the public domain by the authors.
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

import sys

from pegl import display, config, surface

from OpenGL.GL import glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT
from OpenGL.GLUT import *

class TestApp:
    '''A bare-bones GLUT window.'''
    def __init__(self):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)

        glutInitWindowPosition(0, 0)
        glutInitWindowSize(640, 480)
        self.win_id = glutCreateWindow('Pegl test: GLUT'.encode())

        # As GLUT provides no mechanism to access the window system's
        # identifier for the window, it seems we have nothing that can be
        # passed to WindowSurface, and this test will not be workable.
##        self.display = display.Display()
##        self.config = config.get_configs(self.display)[0]
##        self.surface = surface.WindowSurface(self.display, self.config, {},
##                                             self.win_id)

        glutDisplayFunc(self.draw)
        glutKeyboardFunc(self.key_handler)

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glutSwapBuffers()

    def key_handler(self, k, x, y):
        if ord(k) == 27: # Esc key
            self.exit()
        glutPostRedisplay()

    def run(self):
        glutMainLoop()

    def exit(self):
        glutDestroyWindow(self.win_id)
        sys.exit(0)


if __name__ == '__main__':
    app = TestApp()
    app.run()
