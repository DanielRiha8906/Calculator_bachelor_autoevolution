"""Error logging for the calculator application.

Failures and invalid usage are recorded to a dedicated log file
(calculator_errors.log), kept separate from the session operation
history (history.txt).

Usage::

    from .error_logger import get_error_logger

    get_error_logger().error("[cli] divide: Cannot divide by zero")
"""
import logging
import pathlib

ERROR_LOG_FILE = pathlib.Path("calculator_errors.log")
_LOGGER_NAME = "calculator.errors"


def get_error_logger() -> logging.Logger:
    """Return the calculator error logger.

    Configures a FileHandler targeting ERROR_LOG_FILE on the first call.
    Subsequent calls return the same logger without adding duplicate handlers.
    """
    logger = logging.getLogger(_LOGGER_NAME)
    if not logger.handlers:
        logger.setLevel(logging.ERROR)
        handler = logging.FileHandler(ERROR_LOG_FILE, encoding="utf-8")
        handler.setLevel(logging.ERROR)
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False
    return logger
