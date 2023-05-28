from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

NUM_WORKER_THREADS = int(os.environ.get("NUM_WORKER_THREADS", 4))

LEFTOVER_URL = os.environ.get("LEFTOVER_URL", "http://localhost:8000/api/v1/storages/leftover/")

CLIENT_ID = os.environ.get("CLIENT_ID", "")

CLIENT_SECRET = os.environ.get("CLIENT_SECRET", "")

TOKEN_URL = os.environ.get("TOKEN_URL", "http://localhost:8000/auth/token")

URL = os.environ.get("URL", "http://127.0.0.1:8000/api/v1")

THRESHOLD_MIN = 100

THRESHOLD_MAX = 250

GAUSSIAN_KERNEL_SIZE = (9, 9)

DILATATION_SIZE = (3, 3)

MIN_AREA_FILTER = 2000  # square pixels


LOGGER = {
    "version": 1,
    "formatters": {
        "simple": {
            "format": "%(asctime)s - level: %(levelname)s - loc: %(name)s - func: %(funcName)s - msg: %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/watchdog.log",
            "level": "DEBUG",
            "maxBytes": 1048574,
            "backupCount": 3,
            "formatter": "simple"
        }
    },
    "loggers": {
        "client": {
            "level": "DEBUG",
            "handlers": [
                "console",
                "file"
            ],
            "propagate": True
        },
        "utilities.query": {
            "level": "DEBUG",
            "handlers": [
                "console",
                "file"
            ],
            "propagate": True
        },
        "utilities.functions": {
            "level": "DEBUG",
            "handlers": [
                "console",
                "file"
            ],
            "propagate": True
        },
        "utilities.folders": {
            "level": "DEBUG",
            "handlers": [
                "console",
                "file"
            ],
            "propagate": True
        },
        "utilities.files": {
            "level": "DEBUG",
            "handlers": [
                "console",
                "file"
            ],
            "propagate": True
        },
        "__main__": {
            "level": "DEBUG",
            "handlers": [
                "console",
                "file"
            ],
            "propagate": True
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": [
            "console",
            "file"
        ],
    }
}
