"""
This file was created by ]init[ AG 2023.

Package for Generic AI Development.
"""
import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
import sys


def configure_logging():
    """
    Configure logging if no handlers are set.
    """
    root_logger = logging.getLogger()

    if not root_logger.handlers:
        root_logger.setLevel(logging.WARNING)
        logging.getLogger(__name__).setLevel(logging.DEBUG)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_format = logging.Formatter(
            "[%(asctime)s - %(levelname)s - %(filename)30s:%(lineno)4s - %(funcName)20s()] %(message)s"
        )
        console_handler.setFormatter(console_format)
        root_logger.addHandler(console_handler)

        # File handler with rotation
        log_filename = os.environ.get("LOG_FILENAME")
        if log_filename:
            log_filepath = Path(log_filename)
            log_filepath.parent.mkdir(parents=True, exist_ok=True)
            file_handler = RotatingFileHandler(str(log_filepath), maxBytes=1000000, backupCount=10)
            file_format = logging.Formatter(
                "[%(asctime)s - %(levelname)s - %(filename)30s:%(lineno)4s - %(funcName)20s()] %(message)s"
            )
            file_handler.setFormatter(file_format)
            root_logger.addHandler(file_handler)


configure_logging()
