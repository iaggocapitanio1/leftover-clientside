import logging.config

import cv2 as cv

import settings
from utils.functions import load_image, process_frame, turn_to_polygon, crop
from utils.rest import send_frame

logging.config.dictConfig(settings.LOGGER)
logger = logging.getLogger(__name__)


def main():
    path = settings.BASE_DIR.joinpath(f"images/img/1.jpg")
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
        cv.imwrite(f"outputs/normal/22x22.5_1.png", crop(frame, percentage_h=.55, percentage_w=.35, left_m=0,
                                                         top_m=-250))
        key = cv.waitKey(0)  # Wait for user input
        if key:
            break
    cv.destroyAllWindows()


def process():
    for i in range(1, 13):
        path = settings.BASE_DIR.joinpath(f"images/img/{i}.jpg")
        name, frame = load_image(path)
        frame = crop(frame, percentage_h=.65, percentage_w=.35, left_m=0, top_m=-250)
        frame, payload = process_frame(frame, name, show_frame=True)
        data = dict(klass="Oak", corners=turn_to_polygon(payload.get('corners')), ratio=payload.get('ratio'),
                    confirmed=False)
        send_frame(frame=frame, payload=data)
        cv.imwrite(f"outputs/normal/21.2x21_{i}.png", frame)


if __name__ == '__main__':
    # main()
    process()
