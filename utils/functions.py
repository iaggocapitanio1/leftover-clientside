import cv2 as cv
import numpy
from typing import Tuple


# noinspection PyUnresolvedReferences

def get_ratio_pixels_millimeters(img: numpy.ndarray, aruco_type=cv.aruco.DICT_5X5_50) -> float:
    parameters = cv.aruco.DetectorParameters_create()
    aruco_dict = cv.aruco.getPredefinedDictionary(aruco_type)
    marker_size = aruco_dict.markerSize * 4  # cm
    corners, ids, _ = cv.aruco.detectMarkers(img, aruco_dict, parameters=parameters)
    aruco_perimeter = cv.arcLength(corners[0], True)
    return round(aruco_perimeter / marker_size, 7) / 100


def draw_enumerate(img: numpy.ndarray, corners: numpy.ndarray, color=(255, 0, 0), thickness=1, radius=2):
    for i, point in enumerate(corners):
        x, y = point[0]
        cv.circle(img, (x, y), radius=radius, color=color, thickness=thickness)
        cv.putText(img, str(i), (x + 10, y + 10), cv.FONT_HERSHEY_SIMPLEX, 0.65, (255, 0, 0), 1)


def draw_corners(img: numpy.ndarray, corners: numpy.ndarray, ratio: float, color: tuple = (0, 255, 0),
                 thickness: int = 1) -> numpy.ndarray:
    """
    Draw lines connecting the corners of a polygon on an image, and add text with the distance between the corners in
    both pixels and centimeters.

    :param img: Input image on which to draw the lines and text.
    :type img: numpy.ndarray
    :param corners: An array of corner coordinates (x, y) for the polygon.
    :type corners: numpy.ndarray
    :param ratio: Conversion factor from pixels to centimeters, used to calculate distance between corners.
    :type ratio: float
    :param color: The color of the lines and text in BGR format. Default is green (0, 255, 0).
    :type color: tuple
    :param thickness: The thickness of the lines and text. Default is 1.
    :type thickness: int
    :return: The input image with lines connecting the corners and text showing the distance in pixels and centimeters.
    :rtype: numpy.ndarray
    """
    length = len(corners)
    for i in range(length):
        j = i + 1
        if i == length - 1:
            i = 0
            j = length - 1
        pt1 = tuple(corners[i][0])
        pt2 = tuple(corners[j][0])
        dist = int(numpy.sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2))
        dist_cm = round(dist / ratio / 100, 1)
        cv.line(img, pt1, pt2, (0, 155, 0), thickness=2)
        cv.putText(img, f"d: {dist_cm} cm, {dist} ps", ((pt1[0] + pt2[0] - 50) // 2, (pt1[1] + pt2[1]) // 2),
                   cv.FONT_HERSHEY_SIMPLEX, 0.5, color=color, thickness=thickness)
    return img


def get_bounding_box(img: numpy.ndarray, corners: numpy.ndarray, color: tuple = (0, 0, 255),
                     draw: bool = False) -> Tuple[int, int, int, int]:
    x, y, w, h = cv.boundingRect(corners)
    if draw:
        cv.rectangle(img, (x, y), (x + w, y + h), color, 2, lineType=cv.LINE_AA)
    return x, y, w, h


def transform(corners: numpy.ndarray, x: int, y: int, w: int, h: int) -> numpy.ndarray:
    new_corners = corners - numpy.array([[[x, y]]])
    normalized = [(round(X / w, 2), round(Y / h, 2)) for X, Y in new_corners.reshape(-1, 2)]
    if normalized[-1] != normalized[0]:
        normalized.append(normalized[0])
    return numpy.array(normalized)
