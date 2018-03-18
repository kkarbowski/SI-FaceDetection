import cv2
import multiprocessing
from face_detection import *
from gui import *

from PyQt5 import QtGui


class Capture:
    def __init__(self, video_elem, gui):
        self._video_elem = video_elem
        self._capturing = False
        self._gui = gui
        self._c = cv2.VideoCapture(0)
        self._detector = FaceDetector(DetectionMethods.HAAR)
        self._process = None
        self._queue = multiprocessing.Queue()
        self._img_queue = multiprocessing.Queue()
        self._positions = []
        self._time = 0
        self._video = self._c
        self._cv_img = None

    def capture(self):
        if self._gui.is_detetcion():
            ret, frame = self._video.read()
            if ret:
                self._cv_img = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),
                                          (self._gui.VIDEO_WIDTH, self._gui.VIDEO_HEIGHT))

                if not self._queue.empty():
                    self._positions, time = self._queue.get()
                    if self._positions:
                        informations = str(self._positions[0].x) + " " + str(self._positions[0].y) + "\n"
                    else:
                        informations = "No faces\n"
                    informations += " %+2.2f" % time
                    self._gui.send_infos(informations)

                    self._img_queue.put(self._cv_img)
                elif self._process is None:
                    print("NONE")
                    self._img_queue.put(self._cv_img)
                    self._process = multiprocessing.Process(target=self._detector.detect,
                                                            args=(self._queue, self._img_queue))
                    self._process.start()
                self.show_frame()
            else:
                self._gui.turn_off_detection()

    def show_frame(self):
        for face in self._positions:
            cv2.rectangle(self._cv_img, (int(face.x), int(face.y)), (int(face.x + face.w), int(face.y + face.h)),
                          (0, 255, 0), 1)
        qimg = QtGui.QImage(self._cv_img.data, self._cv_img.shape[1], self._cv_img.shape[0], QtGui.QImage.Format_RGB888)
        qpm = QtGui.QPixmap.fromImage(qimg)
        self._video_elem.setPixmap(qpm)

    def change_method(self, method):
        self._img_queue.put(method)

    def change_video_source(self, source):
        self._video = cv2.VideoCapture(source)

    def set_camera_source(self):
        self._video = self._c

    def kill_process(self):
        if self._process is not None:
            self._process.terminate()
            self._process = None
