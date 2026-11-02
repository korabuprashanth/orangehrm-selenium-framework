import logging
import os

LOGGER_NAME = "OrangeHRM"


def get_logger(name=LOGGER_NAME):
    """Return a logger that writes to the console and to reports/test.log (UTF-8)."""
    logger = logging.getLogger(name)

    # Only add handlers once, or every message prints multiple times
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s  [%(levelname)-7s]  %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reports")
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, "test.log")

        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger