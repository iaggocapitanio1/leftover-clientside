from typing import Dict
import io
import cv2
import numpy as np
import requests
import settings
import logging

from client import oauth

logger = logging.getLogger(__name__)


def ends_with_slash(url: str) -> str:
    return url if url.endswith('/') else url + '/'


def send_frame(frame: np.ndarray, payload: Dict) -> bool:
    """
    This function sends a frame (image) to a specified API endpoint as a POST request.

    :param: frame: Image to be sent
    :param: payload: Data to be sent along with the image
    :return: True if the image was sent successfully, False otherwise
    """
    try:
        # Encode the frame as a JPEG image
        _, img_encoded = cv2.imencode('.jpg', frame)

        # Convert the image to bytes
        img_bytes = img_encoded.tobytes()

        # Convert bytes to BytesIO, as it behaves like a file object
        img_io = io.BytesIO(img_bytes)
        files = {'file': ('image.jpg', img_io, 'image/jpeg')}
        url = ends_with_slash(settings.LEFTOVER_URL)
        # Send a POST request to the API endpoint
        response: requests.Response = requests.post(url, data=payload, files=files, auth=oauth)

        # Check if the request was successful
        if response.status_code != 201:
            logger.error("Failed to upload file, status code: %s", response.status_code)
            logger.error("Failed to upload file, error content: %s", response.content)
            return False

        logger.info("File has been successfully uploaded!")
        return True

    except requests.exceptions.RequestException as req_error:
        if len(str(req_error)) <= 500:
            logger.error("A network problem occurred: %s", req_error)
        else:
            logger.error(f"A network problem occurred.")
    except Exception as error:
        if len(str(error)) <= 500:
            logger.error("An error occurred while sending the frame: %s", error)
        else:
            logger.error("An error occurred while sending the frame.")

    # Return False in case of any exception
    return False
