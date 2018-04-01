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
        # updated position of the tracked region and draw the
        # rectangle
        if tracking_quality >= 8.75:
            tracked_position = self._tracker.get_position()
            destination_face_area = fd.FaceArea(int(tracked_position.left()),
                                                int(tracked_position.top()),
                                                int(tracked_position.width()),
                                                int(tracked_position.height()))

            frame = swap_faces(frame, destination_face_area, self._source_img, self._source_face_area)
            # frame = face_swap(frame, destination_face_area, self._source_img, self._source_face_area)

        return frame


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
    white_img = np.zeros([destination_face_area.w, destination_face_area.h, 3], dtype=np.uint8)
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


'''
PREDICTOR_PATH = "predictor/shape_predictor_68_face_landmarks.dat"
FEATHER_AMOUNT = 11

FACE_POINTS = list(range(17, 68))
MOUTH_POINTS = list(range(48, 61))
RIGHT_BROW_POINTS = list(range(17, 22))
LEFT_BROW_POINTS = list(range(22, 27))
RIGHT_EYE_POINTS = list(range(36, 42))
LEFT_EYE_POINTS = list(range(42, 48))
NOSE_POINTS = list(range(27, 35))
JAW_POINTS = list(range(0, 17))

# Points used to line up the images.
ALIGN_POINTS = (LEFT_BROW_POINTS + RIGHT_EYE_POINTS + LEFT_EYE_POINTS +
                RIGHT_BROW_POINTS + NOSE_POINTS + MOUTH_POINTS)

# Points from the second image to overlay on the first. The convex hull of each
# element will be overlaid.
OVERLAY_POINTS = [
    LEFT_EYE_POINTS + RIGHT_EYE_POINTS + LEFT_BROW_POINTS + RIGHT_BROW_POINTS,
    NOSE_POINTS + MOUTH_POINTS,
]

# Amount of blur to use during colour correction, as a fraction of the
# pupillary distance.
COLOUR_CORRECT_BLUR_FRAC = 0.6

predictor = dlib.shape_predictor(PREDICTOR_PATH)
detector = dlib.get_frontal_face_detector()


def get_landmarks(im, im_face_area):
    rect = dlib.rectangle(im_face_area.x,  im_face_area.y, im_face_area.x+im_face_area.w,
                          im_face_area.y+im_face_area.h)

    return np.matrix([[p.x, p.y] for p in predictor(im, rect).parts()])


def annotate_landmarks(im, landmarks):
    im = im.copy()
    for idx, point in enumerate(landmarks):
        pos = (point[0, 0], point[0, 1])
        cv2.putText(im, str(idx), pos,
                    fontFace=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
                    fontScale=0.4,
                    color=(0, 0, 255))
        cv2.circle(im, pos, 3, color=(0, 255, 255))
    return im


def draw_convex_hull(im, points, color):
    points = cv2.convexHull(points)
    cv2.fillConvexPoly(im, points, color=color)


def get_face_mask(im, landmarks):
    im = np.zeros(im.shape[:2], dtype=np.float64)

    for group in OVERLAY_POINTS:
        draw_convex_hull(im,
                         landmarks[group],
                         color=1)

    im = np.array([im, im, im]).transpose((1, 2, 0))

    im = (cv2.GaussianBlur(im, (FEATHER_AMOUNT, FEATHER_AMOUNT), 0) > 0) * 1.0
    im = cv2.GaussianBlur(im, (FEATHER_AMOUNT, FEATHER_AMOUNT), 0)

    return im


def transformation_from_points(points1, points2):
    """
    Return an affine transformation [s * R | T] such that:
        sum ||s*R*p1,i + T - p2,i||^2
    is minimized.
    """
    # Solve the procrustes problem by subtracting centroids, scaling by the
    # standard deviation, and then using the SVD to calculate the rotation. See
    # the following for more details:
    #   https://en.wikipedia.org/wiki/Orthogonal_Procrustes_problem

    points1 = points1.astype(np.float64)
    points2 = points2.astype(np.float64)

    c1 = np.mean(points1, axis=0)
    c2 = np.mean(points2, axis=0)
    points1 -= c1
    points2 -= c2

    s1 = np.std(points1)
    s2 = np.std(points2)
    points1 /= s1
    points2 /= s2

    U, S, Vt = np.linalg.svd(points1.T * points2)

    # The R we seek is in fact the transpose of the one given by U * Vt. This
    # is because the above formulation assumes the matrix goes on the right
    # (with row vectors) where as our solution requires the matrix to be on the
    # left (with column vectors).
    R = (U * Vt).T

    return np.vstack([np.hstack(((s2 / s1) * R,
                                       c2.T - (s2 / s1) * R * c1.T)),
                         np.matrix([0., 0., 1.])])


def read_im_and_landmarks(img, img_face_area):
    im = img.copy()

    s = get_landmarks(im, img_face_area)

    return im, s


def warp_im(im, M, dshape):
    output_im = np.zeros(dshape, dtype=im.dtype)
    cv2.warpAffine(im,
                   M[:2],
                   (dshape[1], dshape[0]),
                   dst=output_im,
                   borderMode=cv2.BORDER_TRANSPARENT,
                   flags=cv2.WARP_INVERSE_MAP)
    return output_im


def correct_colours(im1, im2, landmarks1):
    blur_amount = COLOUR_CORRECT_BLUR_FRAC * np.linalg.norm(
        np.mean(landmarks1[LEFT_EYE_POINTS], axis=0) -
        np.mean(landmarks1[RIGHT_EYE_POINTS], axis=0))
    blur_amount = int(blur_amount)
    if blur_amount % 2 == 0:
        blur_amount += 1
    im1_blur = cv2.GaussianBlur(im1, (blur_amount, blur_amount), 0)
    im2_blur = cv2.GaussianBlur(im2, (blur_amount, blur_amount), 0)

    # Avoid divide-by-zero errors.
    im2_blur += (128 * (im2_blur <= 1.0)).astype(im2_blur.dtype)

    return (im2.astype(np.float64) * im1_blur.astype(np.float64) /
            im2_blur.astype(np.float64))


def face_swap(destination_img, destination_face_area, source_img, source_face_area):

    im1, landmarks1 = read_im_and_landmarks(destination_img, destination_face_area)
    im2, landmarks2 = read_im_and_landmarks(source_img, source_face_area)
    im2 = cv2.cvtColor(im2, cv2.COLOR_BGR2RGB)
    im1 = cv2.cvtColor(im1, cv2.COLOR_BGR2RGB)

    M = transformation_from_points(landmarks1[ALIGN_POINTS],
                                   landmarks2[ALIGN_POINTS])

    mask = get_face_mask(im2, landmarks2)

    warped_mask = warp_im(mask, M, im1.shape)
    combined_mask = np.max([get_face_mask(im1, landmarks1), warped_mask], axis=0)

    warped_im2 = warp_im(im2, M, im1.shape)
    warped_corrected_im2 = correct_colours(im1, warped_im2, landmarks1)

    output_im = im1 * (1.0 - combined_mask) + warped_corrected_im2 * combined_mask

    return output_im

'''
