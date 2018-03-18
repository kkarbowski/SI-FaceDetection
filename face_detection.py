import cv2
import numpy as np
import time
import dlib

from enum import Enum
from skimage import io


class FaceArea:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h


class DetectionMethods(Enum):
    HAAR = 1
    LBP = 2
    DLIB = 3
    CNN = 4


class FaceDetector:
    LBP_CASCADE = cv2.CascadeClassifier('cascades/lbpcascade_frontalface.xml')
    HAAR_CASCADE = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')
    DLIB_SCALE = 580/240
    CNN_SCALE = 580/320

    def __init__(self, method):
        if isinstance(method, DetectionMethods):
            self._method = method
        else:
            self._method = DetectionMethods.HAAR

    def set_method(self, method):
        if isinstance(method, DetectionMethods):
            self._method = method

    def detect(self, que, img_que):
        while(True):
            if not img_que.empty():
                image = img_que.get()
                if isinstance(image, DetectionMethods):
                    self._method = image
                else:
                    if self._method == DetectionMethods.HAAR:
                        que.put(self._detect_faces(self.HAAR_CASCADE, image))
                    elif self._method == DetectionMethods.LBP:
                        que.put(self._detect_faces(self.LBP_CASCADE, image))
                    elif self._method == DetectionMethods.DLIB:
                        que.put(self._detect_faces_dlib(image))
                    elif self._method == DetectionMethods.CNN:
                        que.put(self._detect_faces_cnn(image))

    def _detect_faces(self, f_cascade, colored_img, scale_factor=1.2):
        t1 = time.time()
        img_copy = np.copy(colored_img)

        gray = cv2.cvtColor(img_copy, cv2.COLOR_RGB2GRAY)

        faces = f_cascade.detectMultiScale(gray, scaleFactor=scale_factor, minNeighbors=5)
        positions_of_faces = []
        for (x, y, w, h) in faces:
            positions_of_faces.append(FaceArea(x, y, w, h))

        t2 = time.time()
        return positions_of_faces, t2 - t1

    def _detect_faces_dlib(self, image):
        # Resizing and converting to gray scale
        img_resized = cv2.resize(image, (240, 180))
        gray = cv2.cvtColor(img_resized, cv2.COLOR_RGB2GRAY)

        t1 = time.time()

        # Create a HOG face detector using the built-in dlib class
        face_detector = dlib.get_frontal_face_detector()

        # Run the HOG face detector on the image data.
        # The result will be the bounding boxes of the faces in our image.
        detected_faces = face_detector(gray, 1)

        positions_of_faces = []

        # Loop through each face we found in the image
        for i, face_rect in enumerate(detected_faces):
            positions_of_faces.append(
                FaceArea(face_rect.left() * self.DLIB_SCALE, face_rect.top() * self.DLIB_SCALE,
                         face_rect.width() * self.DLIB_SCALE, face_rect.height() * self.DLIB_SCALE))

        t2 = time.time()
        return positions_of_faces, t2 - t1

    def _detect_faces_cnn(self, image):
        # Resizing and converting to gray scale
        img_resized = cv2.resize(image, (320, 240))
        gray = cv2.cvtColor(img_resized, cv2.COLOR_RGB2GRAY)

        t1 = time.time()

        cnn_face_detector = dlib.cnn_face_detection_model_v1("cascades/mmod_human_face_detector.dat")

        dets = cnn_face_detector(gray, 0)

        positions_of_faces = []

        for i, face_rect in enumerate(dets):
            positions_of_faces.append(
                FaceArea(face_rect.rect.left() * self.CNN_SCALE, face_rect.rect.top() * self.CNN_SCALE,
                         face_rect.rect.width() * self.CNN_SCALE, face_rect.rect.height() * self.CNN_SCALE))

        t2 = time.time()
        return positions_of_faces, t2 - t1

