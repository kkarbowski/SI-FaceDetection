import cv2

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtCore import QSize, QPoint, QTimer   
from PyQt5.QtGui import QImage, QPainter

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
 
        self.setMinimumSize(QSize(1024, 768))    
        self.setWindowTitle("Face Swaping Application") 
        
        self._centralWidget = QWidget(self)          
        self.setCentralWidget(self._centralWidget)   
 
        self._gridLayout = QGridLayout(self)     
        self._centralWidget.setLayout(self._gridLayout)  
 
        title = QLabel("123", self) 
        title.setAlignment(QtCore.Qt.AlignCenter) 
        self._gridLayout.addWidget(title, 0, 0)

class Capture():
    def __init__(self):
        self._capturing = False
        self._c = cv2.VideoCapture(0)

    def startCapture(self):
        print("pressed start")
        self._capturing = True
        while(self._capturing):
            cv2.imshow("Capture", self._c.read()[1])
            cv2.waitKey(5)
        cv2.destroyAllWindows()

    def endCapture(self):
        print("pressed End")
        self._capturing = False

    def quitCapture(self):
        print("pressed Quit")
        self._capturing = False
        cv2.destroyAllWindows()
        self._c.release()
        QtCore.QCoreApplication.quit()


class Window(QtWidgets.QWidget):
    def __init__(self):

        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Control Panel')

        self._capture = Capture()
        self._start_button = QtWidgets.QPushButton('Start',self)
        self._start_button.clicked.connect(self._capture.startCapture)

        self._end_button = QtWidgets.QPushButton('End',self)
        self._end_button.clicked.connect(self._capture.endCapture)

        self._quit_button = QtWidgets.QPushButton('Quit',self)
        self._quit_button.clicked.connect(self._capture.quitCapture)

        vbox = QtWidgets.QVBoxLayout(self)
        vbox.addWidget(self._start_button)
        vbox.addWidget(self._end_button)
        vbox.addWidget(self._quit_button)

        self.setLayout(vbox)
        self.setGeometry(100,100,200,200)
        self.show()

 

 
