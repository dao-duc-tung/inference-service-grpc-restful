import logging

from .constants import AppConst


def setup_logger():
    logger = logging.getLogger(AppConst.APP_NAME)
    file_handler = logging.FileHandler(AppConst.LOG_FILE)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    logger.setLevel(logging.DEBUG)
