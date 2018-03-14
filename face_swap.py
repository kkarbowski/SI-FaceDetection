import cv2

"""
@:param destination_img - the face we will swap
@:param source_img - the source face that will be in the final img
@:param destination_face_area FaceArea object that contains the area of a face - a rectangle
"""


def swap_faces(destination_img, destination_face_area, source_img, source_face_area):
    #crop the source face
    crop_source_img = source_img[source_face_area.y:source_face_area.y + source_face_area.h,
                      source_face_area.x:source_face_area.x + source_face_area.w]
    # resize and blend the face to be swapped in
    face = cv2.resize(crop_source_img, (destination_face_area.h, destination_face_area.w), interpolation=cv2.INTER_CUBIC)
    face = cv2.addWeighted(destination_img[destination_face_area.y:destination_face_area.y + destination_face_area.h,
                           destination_face_area.x:destination_face_area.x + destination_face_area.w], .5, face, .5, 1)
    # swap faces
    swapped_img = destination_img
    swapped_img[destination_face_area.y:destination_face_area.y + destination_face_area.h,
                            destination_face_area.x:destination_face_area.x + destination_face_area.w] = face
    return swapped_img

