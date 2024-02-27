"""
This file was created by ]init[ AG 2023.

Package for Generic AI Development.
"""

from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
import sys

load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))  # Don't override
if os.getenv("TARGET") == "dev":
    load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env.dev"), override=True)
api_keys_filename = os.getenv("API_KEYS_FILENAME")
if api_keys_filename:
    load_dotenv(dotenv_path=os.path.join(os.getcwd(), api_keys_filename), override=True)


def configure_logging():
    """
    Configure logging if no handlers are set.
    """
    root_logger = logging.getLogger()
    if not root_logger.hasHandlers() or not root_logger.handlers[0].name:
        root_logger.setLevel(logging.INFO)
        logging.getLogger(__name__).setLevel(logging.DEBUG)

        if root_logger.hasHandlers():
            root_logger.removeHandler(root_logger.handlers[0])

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.name = "console"
        console_format = logging.Formatter(
            "[%(asctime)s - %(levelname)s - %(name)30s:%(lineno)4s - %(funcName)20s()] %(message)s"
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
                "[%(asctime)s - %(levelname)s - %(name)30s:%(lineno)4s - %(funcName)20s()] %(message)s"
            )
            file_handler.setFormatter(file_format)
            root_logger.addHandler(file_handler)


configure_logging()
