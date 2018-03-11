from gui import *
import sys
import threading


class Program():
    def __init__(self):
        self._app = QtWidgets.QApplication(sys.argv)
        self._main_win = MainWindow()
        self._main_win.show()
        sys.exit( self._app.exec_() )

