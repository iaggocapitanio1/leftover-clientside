import logging.config

import cv2 as cv

import settings
from utils.functions import load_image, process_frame, turn_to_polygon, crop
from utils.rest import send_frame

logging.config.dictConfig(settings.LOGGER)
logger = logging.getLogger(__name__)


def main():
    path = settings.BASE_DIR.joinpath(
        "images/images_fundo_verde/classe8a.jpg")  # replace it with the version that enables image reception from
    # the IDS camera
    name, frame = load_image(path)

    while True:
        logging.info(f"Attempting to process the frame {name}")
        frame, payload = process_frame(frame, name, show_frame=True)
        logging.info(f"Frame successfully processed and payload obtained: {payload}")
        # data = dict(klass="Oak", **payload.get('bbox'), ratio=payload.get('ratio'))
        data = dict(klass="Oak", corners=turn_to_polygon(payload.get('corners')), ratio=payload.get('ratio'),
                    confirmed=False)
        send_frame(frame=frame, payload=data)
        cv.imwrite("outputs/48.1x21.7.png", crop(frame, percentage_h=8, percentage_w=.35,
                                                 left_m=200, top_m=30))
        key = cv.waitKey(0)  # Wait for user input
        if key:
            break
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
