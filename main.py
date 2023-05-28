import cv2 as cv
import logging.config
import settings
from utils.functions import load_image, process_frame
from utils.rest import send_frame

logging.config.dictConfig(settings.LOGGER)
logger = logging.getLogger(__name__)


def main():
    path = settings.BASE_DIR.joinpath("images/1.jpg")  # replace it with the version that enables image reception from
    # the IDS camera
    name, frame = load_image(path)

    while True:
        frame, payload = process_frame(frame, name, show_frame=True)
        send_frame(frame=frame, payload=payload)
        key = cv.waitKey(0)  # Wait for user input
        if key:
            break
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
