import logging
import os
import sys
from datetime import datetime
from functools import wraps

# Logging features are meant for internal library use

LOG_DIR = "./log_info"
LOG_FORMAT = (
    "%(name)s - %(asctime)s - %(levelname)s - %(funcName)s: (%(lineno)d) - %(message)s",  # noqa: E501
)


def stream_handler(log_level):
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter(LOG_FORMAT),
    )
    handler.setLevel(log_level)

    return handler


def file_handler(log_level):
    os.makedirs(LOG_DIR, exist_ok=True)
    handler = logging.FileHandler(
        LOG_DIR + "/log_" + datetime.now().strftime("%Y-%m-%d %H-%M-%S"),
        "w",
    )
    handler.setFormatter(
        logging.Formatter(LOG_FORMAT),
    )
    handler.setLevel(log_level)

    return handler


def get_logger(name):
    return logging.getLogger(name)


def init_logger(name, log_level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    logger.addHandler(stream_handler(log_level))
    logger.addHandler(file_handler(log_level))
    return logger


def log_time(logger):
    def real_decorator(func):
        @wraps(func)
        def log_wrapper(*args, **kwargs):
            start = datetime.now()
            result = func(*args, **kwargs)
            duration = datetime.now() - start
            logger.info(f"Duration for {func.__name__}: {duration}")
            return result

        return log_wrapper

    return real_decorator
