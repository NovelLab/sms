"""Utility module for this application logger."""

# Official Libraries
import logging
import logging.handlers
import os
import sys


# Define Constants
FILE_FORMATTER = logging.Formatter("[%(levelname)s:%(asctime)s:%(module)s]: %(message)s")
"""str: format for a log file."""

SIMPLE_FORMATTER = logging.Formatter("%(asctime)s: %(message)s")
"""str: format as a simple style."""

CONSOLE_FORMATTER = logging.Formatter("%(levelname)-8s %(asctime)s: %(message)s")
"""str: format for a console output."""

DEBUG_FORMATTER = logging.Formatter("%(levelname)-8s %(asctime)s [%(module)s.%(funcName)s:%(lineno)s]:%(message)s")
"""str: format for debug."""


# Main
logger = None
console_handler = None

def init_logger(app_name: str, cache_dir: str) -> bool:
    assert isinstance(app_name, str)
    assert isinstance(cache_dir, str)

    app_cache_dir = os.path.join(cache_dir, app_name)

    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    if not os.path.exists(app_cache_dir):
        os.makedirs(app_cache_dir)

    log_filename = os.path.join(app_cache_dir, f"{app_name}.log")

    loghandler = logging.handlers.RotatingFileHandler(log_filename, maxBytes=20971520, backupCount=5)
    loghandler.setFormatter(FILE_FORMATTER)

    global logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(loghandler)

    global console_handler
    console_handler = logging.StreamHandler(stream=sys.stderr)
    console_handler.setFormatter(CONSOLE_FORMATTER)
    logger.addHandler(console_handler)

    logger.setLevel(logging.INFO)

    return True


def set_for_debug(is_detail: bool = False) -> bool:

    logger.setLevel(logging.DEBUG)

    if is_detail:
        global console_handler
        logger.removeHandler(console_handler)
        console_handler = logging.StreamHandler(stream=sys.stderr)
        console_handler.setFormatter(DEBUG_FORMATTER)
        logger.addHandler(console_handler)

    logger.debug(f"> Start Logging. set level: {logger.getEffectiveLevel()}.")

    return True
