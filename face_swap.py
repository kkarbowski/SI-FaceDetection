import cv2
import dlib
import face_detection as fd
import numpy as np

"""
Class Tracker - it tracks the face and swaps it

@method __init__ 
@:params are similar to faceSwap method
In initializer we initialize the dlib tracker so at this point we have to have the source img and destination img
as well as detected proper faces
"""


class Tracker:
    def __init__(self, destination_img, destination_face_area, detection_method, source_img, source_face_area):
        self._tracker = dlib.correlation_tracker()
        self._face_detector = fd.FaceDetector(detection_method)
        self._source_img = source_img
        self._source_face_area = source_face_area
        self._tracker.start_track(destination_img,
                                  dlib.rectangle(int(destination_face_area.x) - 10,
                                                 int(destination_face_area.y) - 20,
                                                 int(destination_face_area.x) + int(destination_face_area.w) + 10,
                                                 int(destination_face_area.y) + int(destination_face_area.h) + 20))
        self.tracking_face = True

    def detect_and_track_faces(self, destination_img, destination_face_area):
        output_size_width, output_size_height, _ = destination_img.shape
        base_image = cv2.resize(destination_img, (320, 240))
        result_image = base_image.copy()
        output_image = result_image.copy()
        # Check if the tracker is actively tracking a region in the image
        if self.tracking_face:

            # Update the tracker and request information about the
            # quality of the tracking update
            tracking_quality = self._tracker.update(base_image)

            # If the tracking quality is good enough, determine the
            # updated position of the tracked region and draw the
            # rectangle
            if tracking_quality >= 8.75:
                tracked_position = self._tracker.get_position()

                destination_face_area.x = int(tracked_position.left())
                destination_face_area.y = int(tracked_position.top())
                destination_face_area.w = int(tracked_position.width())
                destination_face_area.h = int(tracked_position.height())
                result_image = swap_faces(result_image, destination_face_area, self._source_img, self._source_face_area)

            else:
                self.tracking_face = 0

            output_image = cv2.resize(result_image, (output_size_width, output_size_height))

        return output_image


class TrackerOpenCV:
    def __init__(self):
        self._source_img = None
        self._source_face_area = None
        self._tracker = None
        self.is_tracking = False
        self.create_tracker()

    def create_tracker(self):
        tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN']
        tracker_type = tracker_types[2]
        if tracker_type == 'BOOSTING':
            self._tracker = cv2.TrackerBoosting_create()
        if tracker_type == 'MIL':
            self._tracker = cv2.TrackerMIL_create()
        if tracker_type == 'KCF':
            self._tracker = cv2.TrackerKCF_create()
        if tracker_type == 'TLD':
            self._tracker = cv2.TrackerTLD_create()
        if tracker_type == 'MEDIANFLOW':
            self._tracker = cv2.TrackerMedianFlow_create()
        if tracker_type == 'GOTURN':
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
            frame = swap_faces(frame, destination_face_area, self._source_img, self._source_face_area)

        return frame


"""
@:param destination_img - the face we will swap
@:param source_img - the source face that will be in the final img
@:param destination_face_area FaceArea object that contains the area of a face - a rectangle
"""


def swap_faces(destination_img, destination_face_area, source_img, source_face_area):
    # crop the source face
    crop_source_img = source_img[source_face_area.y:source_face_area.y + source_face_area.h,
                                 source_face_area.x:source_face_area.x + source_face_area.w]
    # resize and blend the face to be swapped in
    face = cv2.resize(crop_source_img, (destination_face_area.w, destination_face_area.h),
                      interpolation=cv2.INTER_CUBIC)

    destination_face = destination_img[destination_face_area.y:destination_face_area.y + destination_face_area.h,
                                       destination_face_area.x:destination_face_area.x + destination_face_area.w]

    face = cv2.addWeighted(destination_face, .5, face, .5, 3)
    # swap faces
    swapped_img = destination_img.copy()
    swapped_img[destination_face_area.y:destination_face_area.y + destination_face_area.h,
                destination_face_area.x:destination_face_area.x + destination_face_area.w] = face
    return swapped_img
