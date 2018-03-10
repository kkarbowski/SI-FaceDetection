from gui import *
import sys

class Program():
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        mainWin = MainWindow()
        mainWin.show()
        window = Window()
        sys.exit( app.exec_() )

