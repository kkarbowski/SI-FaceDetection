import cv2
import numpy as np
import time

'''
cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml') for Haar Cascade
cv2.CascadeClassifier('cascades/lbpcascade_frontalface.xml') for LBP Cascade
'''
def detect_faces(f_cascade, colored_img, scale_factor=1.2):
    t1 = time.time()
    img_copy = np.copy(colored_img)

    gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)

    faces = f_cascade.detectMultiScale(gray, scaleFactor=scale_factor, minNeighbors=5)
    positions_of_faces = []
    for (x, y, w, h) in faces:
        positions_of_faces.append((x, y, w, h))

    t2 = time.time()
    return positions_of_faces, t2-t1




