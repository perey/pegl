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
        self.setWindowTitle('Pegl test')

        self.show()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    win = TestApp()
    sys.exit(app.exec_())
