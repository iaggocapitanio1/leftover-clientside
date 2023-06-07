import json
import os
import logging
from pathlib import Path
from typing import Union, Tuple, Dict, Optional
from shapely.geometry import Polygon
import geojson
import cv2 as cv
import numpy
import itertools
import settings

logger = logging.getLogger(__name__)


def load_image(filepath: Union[str, Path]) -> Tuple[str, numpy.ndarray]:
    """
    This function loads the image using cv2's imread function
    """
    file = os.path.basename(filepath)
    name, ext = os.path.splitext(file)
    frame = cv.imread(filepath.__str__())
    return name, frame


def crop(image, percentage_w, percentage_h, left_m: int = 0, top_m: int = 0):
    height, width, _ = image.shape

    # Calculate the coordinates for the center crop
    crop_width = int(width * percentage_w)  # Set the desired width of the center crop
    crop_height = int(height * percentage_h)  # Set the desired height of the center crop
    start_x = int((width - crop_width) / 2) + int(left_m)
    start_y = int((height - crop_height) / 2) + int(top_m)
    end_x = start_x + crop_width
    end_y = start_y + crop_height

    # Perform the center crop
    return image[start_y:end_y, start_x:end_x]


def process_frame(frame: numpy.ndarray, name: str, show_frame: bool = False) -> Optional[Tuple[numpy.ndarray, Dict]]:
    """
    Processes an image using OpenCV operations including conversion to grayscale, blurring, Canny edge detection,
    dilation, erosion, and contour detection. If a contour passes a specified area filter, an approximation of
    the contour is drawn on the original image, and the bounding box around it is determined.

    Args:
        frame (np.ndarray): The original image to process.
        name (str): The name to give to the output frame.
        show_frame (bool, optional): Determines whether the result should be displayed using cv.imshow. Defaults to False.

    Returns:
        Optional[Tuple[np.ndarray, Dict]]: Returns a tuple of the processed image and a dictionary containing bounding
                                           box information and cleaned contour points, or None if no contour passes
                                           the area filter.
    """

    # Convert frame to gray, apply Gaussian blur and Canny edge detection
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blurred_frame = cv.GaussianBlur(gray_frame, ksize=settings.GAUSSIAN_KERNEL_SIZE, sigmaX=1)
    canny_frame = cv.Canny(blurred_frame, threshold1=settings.THRESHOLD_MIN, threshold2=settings.THRESHOLD_MAX)
    # Dilate and erode the frame to clean up noise
    dilatation = numpy.ones(settings.DILATATION_SIZE, numpy.uint8)
    dilated_frame = cv.dilate(canny_frame, dilatation, iterations=2)
    eroded_frame = cv.erode(dilated_frame, dilatation, iterations=2)
    # Find contours
    contours, _ = cv.findContours(eroded_frame, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    logger.info("Initiating process to establish the ratio between pixels and millimeters.")
    ratio = get_ratio_pixels_millimeters(img=frame)
    logger.info(f"Ratio found: {ratio} pixels/mm ")
    for contour in contours:
        if cv.contourArea(contour) > settings.MIN_AREA_FILTER:
            # Approximate the contour and draw it on the original image
            clean_contour_points = cv.approxPolyDP(contour, epsilon=0.01 * cv.arcLength(contour, True), closed=True)
            processed_frame = cv.polylines(frame.copy(), pts=clean_contour_points, isClosed=True, color=(255, 0, 0),
                                           thickness=12, lineType=cv.LINE_AA)
            bbox = get_bounding_box(img=processed_frame, corners=clean_contour_points, draw=True)
            # If show_frame is True, perform additional operations and display the image
            if show_frame:
                draw_corners(img=processed_frame, corners=clean_contour_points, ratio=ratio, color=(0, 0, 15),
                             thickness=2)
                draw_enumerate(img=processed_frame, corners=clean_contour_points)
                # cv.imshow(f"Processed Frame: {name}", crop(processed_frame, percentage_h=.55, percentage_w=.35,
                #                                            left_m=0, top_m=-100))
                frame = processed_frame
            return frame, dict(bbox=dict(x=bbox[0], y=bbox[1], width=bbox[2], height=bbox[3]), ratio=ratio,
                               corners=clean_contour_points.tolist())
    return None


def get_ratio_pixels_millimeters(img: numpy.ndarray, aruco_type=cv.aruco.DICT_5X5_50) -> float:
    parameters = cv.aruco.DetectorParameters_create()
    aruco_dict = cv.aruco.getPredefinedDictionary(aruco_type)
    marker_size = aruco_dict.markerSize * 4  # cm
    corners, ids, _ = cv.aruco.detectMarkers(img, aruco_dict, parameters=parameters)
    aruco_perimeter = cv.arcLength(corners[0], True)  # pixels
    return round(aruco_perimeter / marker_size / 10, 7)


def draw_enumerate(img: numpy.ndarray, corners: numpy.ndarray, color=(0, 255, 0), thickness=1, radius=2):
    for i, point in enumerate(corners):
        x, y = point[0]
        cv.circle(img, (x, y), radius=radius, color=color, thickness=thickness)
        cv.putText(img, str(i), (x + 10, y + 10), cv.FONT_HERSHEY_SIMPLEX, 0.65, (255, 0, 0), 1)


def draw_corners(img: numpy.ndarray, corners: numpy.ndarray, ratio: float, color: tuple = (0, 255, 0),
                 color_line: tuple = (0, 50, 150),
                 thickness: int = 1) -> numpy.ndarray:
    """
    Draw lines connecting the corners of a polygon on an image, and add text with the distance between the corners in
    both pixels and centimeters.

    :param: img: Input image on which to draw the lines and text.
    :type: img: numpy.ndarray
    :param: corners: An array of corner coordinates (x, y) for the polygon.
    :type: corners: numpy.ndarray
    :param: ratio: Conversion factor from pixels to centimeters, used to calculate distance between corners.
    :type: ratio: float
    :param: color: The color of the lines and text in BGR format. Default is green (0, 255, 0).
    :type: color: tuple
    :param: thickness: The thickness of the lines and text. Default is 1.
    :type: thickness: int
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
        dist_cm = round(dist / ratio / 10, 1)
        cv.line(img, pt1, pt2, color_line, thickness=2)
        cv.putText(img, f"d: {dist_cm} cm, "
                     #   f"{dist} pixels"
                   , ((pt1[0] + pt2[0] - 50) // 2, (pt1[1] + pt2[1]) // 2),
                   cv.FONT_HERSHEY_SIMPLEX, 0.65, color=color, thickness=thickness)
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


def turn_to_polygon(corners) -> str:
    # Flatten the list of coordinates
    flattened_coordinates = list(itertools.chain(*corners))
    flattened_coordinates.append(flattened_coordinates[0])
    geojson_polygon = geojson.Polygon(flattened_coordinates)
    return json.dumps(geojson_polygon)
