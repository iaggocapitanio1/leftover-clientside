from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# Define base directory
BASE_DIR = Path(__file__).resolve().parent


def fetch_env(var, default):
    return os.environ.get(var, default)


# Fetch all environment variables
LEFTOVER_URL = fetch_env("LEFTOVER_URL", "http://localhost:8000/api/v1/storages/leftover/")
LOGS_DIR = Path(fetch_env("LOGS_DIR", BASE_DIR.joinpath('logs')))
CLIENT_ID = fetch_env("CLIENT_ID", "")
CLIENT_SECRET = fetch_env("CLIENT_SECRET", "")
TOKEN_URL = fetch_env("TOKEN_URL", "http://localhost:8000/auth/token")
URL = fetch_env("URL", "http://127.0.0.1:8000/api/v1")

if not LOGS_DIR.exists():
    LOGS_DIR.mkdir(parents=True)
# Define constants
THRESHOLD_MIN = 100
THRESHOLD_MAX = 250
GAUSSIAN_KERNEL_SIZE = (9, 9)
DILATATION_SIZE = (3, 3)
MIN_AREA_FILTER = 12e4  # square pixels

# Define logger configuration
LOGGER = {
    "version": 1,
    "formatters": {"simple": {
        "format": "%(asctime)s - level: %(levelname)s - loc: %(name)s - func: %(funcName)s - msg: %(message)s"}},
    "handlers": {
        "console": {"class": "logging.StreamHandler", "level": "DEBUG", "formatter": "simple",
                    "stream": "ext://sys.stdout"},
        "file": {"class": "logging.handlers.RotatingFileHandler", "filename": "logs/watchdog.log", "level": "DEBUG",
                 "maxBytes": 1048574, "backupCount": 3, "formatter": "simple"},
    },
    "loggers": {
        module: {"level": "DEBUG", "handlers": ["console", "file"], "propagate": True}
        for module in
        ["client", "utils.functions", "utils.rest", "__main__"]
    },
    "root": {"level": "DEBUG", "handlers": ["console", "file"]},
}

