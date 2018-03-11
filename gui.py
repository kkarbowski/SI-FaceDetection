import cv2

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QPushButton, QDialog, QFileDialog
from PyQt5.QtCore import QSize, QPoint, QTimer   
from PyQt5.QtGui import QImage, QPainter, QPixmap

class MainWindow(QMainWindow):
    BUTTON_X_POS = 30
    TEXT_BOX_HEIGHT = 24
    def __init__(self):
        QMainWindow.__init__(self)
        self.setObjectName("Face Swaping Application")
        self.resize(1024, 768)
        self._central_widget = QtWidgets.QWidget(self)
        self._central_widget.setObjectName("_central_widget")
        
        #video widget
        self._video = QtWidgets.QLabel(self._central_widget)
        self._video.setGeometry(QtCore.QRect(460, 60, 555, 370))
        self._video.setObjectName("video")
        self._capturing = Capture(self._video)

        #video frame rate
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.show_frame)
        self.timer.start(60) #10 fps

        #choose file button
        self._choose_file_button = QtWidgets.QPushButton(self._central_widget)
        self._choose_file_button.setGeometry(QtCore.QRect(30, self.BUTTON_X_POS, 151, 31))
        self._choose_file_button.setObjectName("Input_File")
        self._choose_file_button.clicked.connect(self.get_file)
       
        #start button
        self._start_button = QtWidgets.QPushButton(self._central_widget)
        self._start_button.setGeometry(QtCore.QRect(240, self.BUTTON_X_POS, 151, 31))
        self._start_button.setObjectName("_push_button_2")

        #file input path (text box)
        self._input_box = QtWidgets.QTextEdit(self._central_widget)
        self._input_box.setGeometry(QtCore.QRect(20, 100, 381, self.TEXT_BOX_HEIGHT))
        self._input_box.setObjectName("Input File")

        #input file label
        self._input_label = QtWidgets.QLabel(self._central_widget)
        self._input_label.setGeometry(QtCore.QRect(20, 70, 381, self.TEXT_BOX_HEIGHT))
        self._input_label.setObjectName("_input_label")
        self._input_label.setText("Input file path:")

        #text label "Choose a method"
        self._method_label = QtWidgets.QLabel(self._central_widget)
        self._method_label.setGeometry(QtCore.QRect(20, 130, 381, self.TEXT_BOX_HEIGHT))
        self._method_label.setObjectName("_method_label")
        self._method_label.setText("Choose a method of face detection:")
        
        #choose method
        self._method_box = QtWidgets.QComboBox(self._central_widget)
        self._method_box.setGeometry(QtCore.QRect(20, 160, 381, self.TEXT_BOX_HEIGHT))
        self._method_box.setObjectName("_font_combo_box")
        self._method_box.addItems(["1 met", "2 met", "3 met", "4 met"])

        # infos about FR
        self._text_browser = QtWidgets.QTextBrowser(self._central_widget)
        self._text_browser.setGeometry(QtCore.QRect(20, 220, 381, 221))
        self._text_browser.setObjectName("_text_browser")
        self._text_browser.setText("Adsasdasd ads asd asd asd as das das d")
        
        #label infos about process of FD
        self._info_label = QtWidgets.QLabel(self._central_widget)
        self._info_label.setGeometry(QtCore.QRect(20, 190, 381, self.TEXT_BOX_HEIGHT))
        self._info_label.setObjectName("_info_label")
        self._info_label.setText("Information about face detection:")

        # on/off face swap checkbutton
        self._check_box = QtWidgets.QCheckBox(self._central_widget)
        self._check_box.setGeometry(QtCore.QRect(460, 440, 150, self.TEXT_BOX_HEIGHT))
        self._check_box.setObjectName("_check_box")


        pic_face=QPixmap("./bach.jpg")
        pic_face=pic_face.scaled(110, 110)

        self._face_slot = []
        for i in range(0,14):
            self._face_slot.append(QtWidgets.QLabel(self._central_widget))
            if i < 7:
                self._face_slot[i].setGeometry(QtCore.QRect(50 + i*130, 510, 111, 111))
            else:
                self._face_slot[i].setGeometry(QtCore.QRect(50 + (i-7)*130, 630, 111, 111))
            self._face_slot[i].setObjectName("_face_slot_"+str(i))
            self._face_slot[i].setPixmap(pic_face)
            self._face_slot[i].mousePressEvent = self.select_method
              
        self.setCentralWidget(self._central_widget)
        
        #self._menubar = QtWidgets.QMenuBar(self)
        #self._menubar.setGeometry(QtCore.QRect(0, 0, 1038, 21))
        #self._menubar.setObjectName("_menubar") 
        #self.setMenuBar(self._menubar)

        #self._statusbar = QtWidgets.QStatusBar(self)
        #self._statusbar.setObjectName("_statusbar")
        #self.setStatusBar(self._statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def show_frame(self):
        self._capturing.capture()

    def get_file(self):
        self._file_path = QFileDialog.getOpenFileName(self, 'Choose file','c:\\',"Image files (*.jpg *.gif)")
        self._input_box.setText(self._file_path[0])

    def select_method(self, event):
        print("lol xd")

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Face Swaping Application"))
        self._choose_file_button.setText(_translate("MainWindow", "Choose input File"))
        self._check_box.setText(_translate("MainWindow", "Turn off face swaping"))
        self._start_button.setText(_translate("MainWindow", "Start"))





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

 

 
