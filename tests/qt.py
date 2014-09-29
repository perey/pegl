#!/usr/bin/env python3

'''Test creating a WindowSurface bound to a Qt window.'''

# Copyright © 2012-14 Tim Pederick.
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
from PySide import QtGui

class TestApp(QtGui.QMainWindow):
    def __init__(self):
        super().__init__()

        self.render = QtGui.QWidget()
        self.setCentralWidget(self.render)

        self.display = display.Display()
        self.config = config.get_configs(self.display)[0]
        self.surface = surface.WindowSurface(self.display, self.config, {},
                                             self.render.winId())

        self.resize(640, 480)
        self.setWindowTitle('Pegl test: Qt')

        self.show()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    win = TestApp()
    sys.exit(app.exec_())
