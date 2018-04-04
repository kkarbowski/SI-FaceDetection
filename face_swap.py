from enum import Enum

import cv2
import dlib
import face_detection as fd
import numpy as np

VIDEO_WIDTH = 580
VIDEO_HEIGHT = 435

"""
Class Tracker - it tracks the face and swaps it

@method __init__ 
@:params are similar to faceSwap method
In initializer we initialize the dlib tracker so at this point we have to have the source img and destination img
as well as detected proper faces
"""


class TrackingMethods(Enum):
    DLIB = 0
    BOOSTING = 1
    MIL = 2
    KCF = 3
    TLD = 4
    MEDIANFLOW = 5
    GOTURN = 6


class Tracker:
    def __init__(self):
        self._tracker = None
        self._source_img = None
        self._source_face_area = None
        self.is_tracking = False

    def init_tracker(self, destination_img, destination_face_area, source_img, source_face_area):
        self._tracker = dlib.correlation_tracker()
        self._source_img = source_img
        self._source_face_area = source_face_area
        # Define an initial bounding box
        self._tracker.start_track(destination_img,
                                  dlib.rectangle(int(destination_face_area.x),
                                                 int(destination_face_area.y),
                                                 int(destination_face_area.x) + int(destination_face_area.w),
                                                 int(destination_face_area.y) + int(destination_face_area.h)))

        self.is_tracking = True

    def track_and_swap_faces(self, destination_img):
        # Read a new frame
        frame = destination_img.copy()

        # Update the tracker and request information about the
        # quality of the tracking update
        tracking_quality = self._tracker.update(frame)

        # If the tracking quality is good enough, determine the
        # updated position of the tracked region
        if tracking_quality >= 8.75:
            tracked_position = self._tracker.get_position()
            destination_face_area = fd.FaceArea(int(tracked_position.left()),
                                                int(tracked_position.top()),
                                                int(tracked_position.width()),
                                                int(tracked_position.height()))

            if VIDEO_WIDTH > destination_face_area.x + destination_face_area.w \
                    and destination_face_area.x > 0 \
                    and destination_face_area.y > 0 \
                    and destination_face_area.y + destination_face_area.h < VIDEO_HEIGHT:
                frame = swap_faces(frame, destination_face_area, self._source_img, self._source_face_area)

        return frame


class TrackerOpenCV:
    def __init__(self, track_method):
        self._source_img = None
        self._source_face_area = None
        self._tracker = None
        self.is_tracking = False
        self._track_method = TrackingMethods(track_method)
        #
        self.create_tracker()

    def create_tracker(self):
        if self._track_method == TrackingMethods.BOOSTING:
            self._tracker = cv2.TrackerBoosting_create()
        if self._track_method == TrackingMethods.MIL:
            self._tracker = cv2.TrackerMIL_create()
        if self._track_method == TrackingMethods.KCF:
            self._tracker = cv2.TrackerKCF_create()
        if self._track_method == TrackingMethods.TLD:
            self._tracker = cv2.TrackerTLD_create()
        if self._track_method == TrackingMethods.MEDIANFLOW:
            self._tracker = cv2.TrackerMedianFlow_create()
        if self._track_method == TrackingMethods.GOTURN:
            self._tracker = cv2.TrackerGOTURN_create()

    def init_tracker(self, destination_img, destination_face_area, source_img, source_face_area):
        self._tracker.clear()
        self.create_tracker()
        self._source_img = source_img
        self._source_face_area = source_face_area
        # Define an initial bounding box
        bbox = (destination_face_area.x, destination_face_area.y,
                destination_face_area.w, destination_face_area.h)

        # Initialize tracker with first frame and bounding box
        self._tracker.init(destination_img, bbox)
        self.is_tracking = True

    def track_and_swap_faces(self, destination_img):
        # Read a new frame
        frame = destination_img.copy()

        # Update tracker
        ok, bbox = self._tracker.update(frame)
        destination_face_area = fd.FaceArea(np.int32(bbox[0]), np.int32(bbox[1]), np.int32(bbox[2]),
                                            np.int32(bbox[3]))
        if ok:
            if VIDEO_WIDTH > destination_face_area.x + destination_face_area.w \
                    and destination_face_area.x > 0 \
                    and destination_face_area.y > 0 \
                    and destination_face_area.y + destination_face_area.h < VIDEO_HEIGHT:
                frame = swap_faces(frame, destination_face_area, self._source_img, self._source_face_area)

        return frame


"""
@:param destination_img - the face we will swap
@:param source_img - the source face that will be in the final img
@:param destination_face_area FaceArea object that contains the area of a face - a rectangle
"""


def swap_faces(destination_img, destination_face_area, source_img, source_face_area):
    # crop the source face
    source_img_tmp = cv2.cvtColor(source_img, cv2.COLOR_RGB2BGR)
    crop_source_img = source_img_tmp[source_face_area.y:source_face_area.y + source_face_area.h,
                      source_face_area.x:source_face_area.x + source_face_area.w]

    # resize and blend the face to be swapped in
    face = cv2.resize(crop_source_img, (destination_face_area.w, destination_face_area.h),
                      interpolation=cv2.INTER_CUBIC)

    # extracting face area
    destination_face = destination_img[destination_face_area.y:destination_face_area.y + destination_face_area.h,
                                       destination_face_area.x:destination_face_area.x + destination_face_area.w]

    # mask divisor to get values in range 0..1
    white_img = np.zeros([destination_face_area.h, destination_face_area.w, 3], dtype=np.uint8)
    white_img.fill(255)

    # face transparency mask
    mask = cv2.resize(cv2.imread("mask.png", cv2.IMREAD_COLOR), (destination_face_area.w, destination_face_area.h))
    mask_invert = cv2.bitwise_not(mask)

    # applying mask and reversed mask
    face = face * (mask / white_img)
    destination_face = destination_face * (mask_invert / white_img)

    # swapped face
    face = cv2.addWeighted(destination_face, 0.99, face, 0.99, 3)

    # replacing face area
    swapped_img = destination_img.copy()
    swapped_img[destination_face_area.y:destination_face_area.y + destination_face_area.h,
                destination_face_area.x:destination_face_area.x + destination_face_area.w] = face
    return swapped_img
