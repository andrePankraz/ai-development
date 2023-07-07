"""
This file was created by ]init[ AG 2023.

Module for Generic AI Development Service.
"""
import logging

logger = logging.getLogger(__name__)


def hello_world():
    logger.debug("Hello World!")


def _test():
    import sys

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    hello_world()


if __name__ == "__main__":
    _test()
