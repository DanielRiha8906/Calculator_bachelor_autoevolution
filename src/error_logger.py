"""Error logging for the calculator application.

Provides a factory function that returns a Logger configured to write
ERROR-level records to a local file.  The log file is kept separate from
the session history (history.txt) so normal operation records and error
records are never mixed.
"""
import logging

ERROR_LOG_FILE = "calculator_errors.log"
_LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"


def get_error_logger(log_file: str = ERROR_LOG_FILE) -> logging.Logger:
    """Return a logger that appends ERROR-level messages to *log_file*.

    A unique logger name is derived from the file path so that calls with
    different paths — as happens in tests using tmp_path — each receive their
    own isolated logger without shared state.
    """
    name = f"calculator.errors|{log_file}"
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.FileHandler(log_file, encoding="utf-8")
        handler.setFormatter(logging.Formatter(_LOG_FORMAT))
        logger.addHandler(handler)
        logger.setLevel(logging.ERROR)
        logger.propagate = False
    return logger
