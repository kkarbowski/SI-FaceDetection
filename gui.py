import cv2

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QPushButton, QDialog
from PyQt5.QtCore import QSize, QPoint, QTimer   
from PyQt5.QtGui import QImage, QPainter, QPixmap

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setObjectName("Face Swaping Application")
        self.resize(1024, 768)
        self._central_widget = QtWidgets.QWidget(self)
        self._central_widget.setObjectName("_central_widget")
        

        self._video = QtWidgets.QLabel(self._central_widget)
        self._video.setGeometry(QtCore.QRect(460, 60, 551, 371))
        self._video.setObjectName("video")
        self._capturing = Capture(self._video)

        self._push_button = QtWidgets.QPushButton(self._central_widget)
        self._push_button.setGeometry(QtCore.QRect(30, 60, 151, 31))
        self._push_button.setObjectName("_push_button")
        self._push_button.clicked.connect(self.handle_button)
       
        self._font_combo_box = QtWidgets.QFontComboBox(self._central_widget)
        self._font_combo_box.setGeometry(QtCore.QRect(20, 160, 381, 22))
        self._font_combo_box.setObjectName("_font_combo_box")
        
        self._text_edit = QtWidgets.QTextEdit(self._central_widget)
        self._text_edit.setGeometry(QtCore.QRect(20, 100, 381, 21))
        self._text_edit.setObjectName("_text_edit")
        
        self._plain__text_edit = QtWidgets.QPlainTextEdit(self._central_widget)
        self._plain__text_edit.setGeometry(QtCore.QRect(20, 130, 381, 21))
        self._plain__text_edit.setObjectName("_plain__text_edit")
        
        self._text_browser = QtWidgets.QTextBrowser(self._central_widget)
        self._text_browser.setGeometry(QtCore.QRect(20, 220, 381, 221))
        self._text_browser.setObjectName("_text_browser")
        
        self._plain__text_edit_2 = QtWidgets.QPlainTextEdit(self._central_widget)
        self._plain__text_edit_2.setGeometry(QtCore.QRect(20, 190, 381, 21))
        self._plain__text_edit_2.setObjectName("_plain__text_edit_2")
       
        self._widget = QtWidgets.QWidget(self._central_widget)
        self._widget.setGeometry(QtCore.QRect(50, 510, 111, 111))
        self._widget.setObjectName("_widget")
        self._widget_2 = QtWidgets.QWidget(self._central_widget)
        self._widget_2.setGeometry(QtCore.QRect(180, 510, 111, 111))
        self._widget_2.setObjectName("_widget_2")
        self._widget_3 = QtWidgets.QWidget(self._central_widget)
        self._widget_3.setGeometry(QtCore.QRect(320, 510, 111, 111))
        self._widget_3.setObjectName("_widget_3")
        self._widget_4 = QtWidgets.QWidget(self._central_widget)
        self._widget_4.setGeometry(QtCore.QRect(460, 510, 111, 111))
        self._widget_4.setObjectName("_widget_4")
        self._widget_5 = QtWidgets.QWidget(self._central_widget)
        self._widget_5.setGeometry(QtCore.QRect(600, 510, 111, 111))
        self._widget_5.setObjectName("_widget_5")
        self._widget_6 = QtWidgets.QWidget(self._central_widget)
        self._widget_6.setGeometry(QtCore.QRect(740, 510, 111, 111))
        self._widget_6.setObjectName("_widget_6")
        self._widget_7 = QtWidgets.QWidget(self._central_widget)
        self._widget_7.setGeometry(QtCore.QRect(880, 510, 111, 111))
        self._widget_7.setObjectName("_widget_7")
        
        self._check_box = QtWidgets.QCheckBox(self._central_widget)
        self._check_box.setGeometry(QtCore.QRect(460, 440, 121, 21))
        self._check_box.setObjectName("_check_box")
        
        self._push_button_2 = QtWidgets.QPushButton(self._central_widget)
        self._push_button_2.setGeometry(QtCore.QRect(240, 60, 151, 31))
        self._push_button_2.setObjectName("_push_button_2")
        
        self.setCentralWidget(self._central_widget)
        
        self._menubar = QtWidgets.QMenuBar(self)
        self._menubar.setGeometry(QtCore.QRect(0, 0, 1038, 21))
        self._menubar.setObjectName("_menubar")
        
        self.setMenuBar(self._menubar)
        self._statusbar = QtWidgets.QStatusBar(self)
        self._statusbar.setObjectName("_statusbar")
        self.setStatusBar(self._statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def handle_button(self):
        self._capturing.capture()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self._push_button.setText(_translate("MainWindow", "PushButton"))
        self._check_box.setText(_translate("MainWindow", "CheckBox"))
        self._push_button_2.setText(_translate("MainWindow", "PushButton"))





class Capture():
    def __init__(self, video_elem):
        self._video_elem = video_elem
        self._capturing = False
        self._c = cv2.VideoCapture(0)

    def capture(self):
        cvRGBImg = cv2.cvtColor(self._c.read()[1], cv2.COLOR_BGR2RGB)
        qimg = QtGui.QImage(cvRGBImg.data,cvRGBImg.shape[1], cvRGBImg.shape[0], QtGui.QImage.Format_RGB888)
        qpm = QtGui.QPixmap.fromImage(qimg)
        self._video_elem.setPixmap(qpm)
        cv2.waitKey(5)




        #class MyDialog(QtWidgets.QDialog):
#    def __init__(self, parent=None):
#        super(MyDialog, self).__init__(parent)

#        self.cvImage = cv2.imread(r'cat.jpg')
#        height, width, byteValue = self.cvImage.shape
#        byteValue = byteValue * width

#        cv2.cvtColor(self.cvImage, cv2.COLOR_BGR2RGB, self.cvImage)

#        self.mQImage = QImage(self.cvImage, width, height, byteValue, QImage.Format_RGB888)

#    def paintEvent(self, QPaintEvent):
#        painter = QPainter()
#        painter.begin(self)
#        painter.drawImage(0, 0, self.mQImage)
#        painter.end()

#    def keyPressEvent(self, QKeyEvent):
#        super(MyDialog, self).keyPressEvent(QKeyEvent)
#        if 's' == QKeyEvent.text():
#            cv2.imwrite("cat2.png", self.cvImage)
#        else:
#            app.exit(1)



    #    class Capture():
    #def __init__(self, video_elem):
    #    self._video_elem = video_elem
    #    self._capturing = False
    #    self._c = cv2.VideoCapture(0)

    #def start_capture(self):
    #    print("pressed start")
    #    self._capturing = True
    #    while(self._capturing):
    #        cv2.imshow("Capture", self._c.read()[1])
    #        cvRGBImg = cv2.cvtColor(cvBGRImg, cv2.cv.CV_BGR2RGB)
    #        qimg = QtGui.QImage(cvRGBImg.data,cvRGBImg.shape[1], cvRGBImg.shape[0], QtGui.QImage.Format_RGB888)
    #        qpm = QtGui.QPixmap.fromImage(qimg)
    #        imageLabel.setPixmap(qpm)
    #        setPixmap(pixmap)
    #        cv2.waitKey(5)
    #    cv2.destroyAllWindows()

    #def end_capture(self):
    #    print("pressed End")
    #    self._capturing = False

    #def quit_capture(self):
    #    print("pressed Quit")
    #    self._capturing = False
    #    cv2.destroyAllWindows()
    #    self._c.release()
    #    QtCore.QCoreApplication.quit()

#class Window(QtWidgets.QWidget):
#    def __init__(self):

#        QtWidgets.QWidget.__init__(self)
#        self.setWindowTitle('Control Panel')

#        self._capture = Capture()
#        self._start_button = QtWidgets.QPushButton('Start',self)
#        self._start_button.clicked.connect(self._capture.start_capture)

#        self._end_button = QtWidgets.QPushButton('End',self)
#        self._end_button.clicked.connect(self._capture.end_capture)

#        self._quit_button = QtWidgets.QPushButton('Quit',self)
#        self._quit_button.clicked.connect(self._capture.quit_capture)

#        vbox = QtWidgets.QVBoxLayout(self)
#        vbox.addWidget(self._start_button)
#        vbox.addWidget(self._end_button)
#        vbox.addWidget(self._quit_button)

#        self.setLayout(vbox)
#        self.setGeometry(100,100,200,200)
#        self.show()

 

 
