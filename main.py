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
        logging.info(f"Attempting to process the frame {name}")
        frame, payload = process_frame(frame, name, show_frame=True)
        logging.info(f"Frame successfully processed and payload obtained: {payload}")
        data = dict(klass="Oak", **payload.get('bbox'), ratio=payload.get('ratio'))
        send_frame(frame=frame, payload=data)
        key = cv.waitKey(0)  # Wait for user input
        if key:
            break
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
