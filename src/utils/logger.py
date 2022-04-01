import logging

from .constants import AppConst


def setup_logger():
    logger = logging.getLogger(AppConst.APP_NAME)
    file_handler = logging.FileHandler(AppConst.LOG_FILE)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)
