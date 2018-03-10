from gui import *
import sys

class Program():
    def __init__(self):
        self._app = QtWidgets.QApplication(sys.argv)
        self._mainWin = MainWindow()
        self._mainWin.show()
        self._window = Window()
        sys.exit( self._app.exec_() )

