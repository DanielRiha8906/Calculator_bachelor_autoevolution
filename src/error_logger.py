"""Error logging for the calculator application.

Provides a shared logger that writes error events to ERROR_LOG_FILE.
Call setup_error_logging() once at application startup (inside main())
to attach the file handler.  The logger level is set at import time so
pytest's caplog fixture can capture records even when the file handler
is patched out in tests.

Logged events cover both the bash CLI (main.py) and the interactive
session (src/__main__.py).  Both modes tag their records with a source
prefix — ``[cli]`` or ``[interactive]`` — so entries remain distinguishable
when the two modes share the same error.log file.
"""
import logging

ERROR_LOG_FILE = "error.log"
_LOGGER_NAME = "calculator.errors"

# Set the level at import time so caplog can capture records in tests
# even when setup_error_logging() is patched to a no-op.
_logger = logging.getLogger(_LOGGER_NAME)
_logger.setLevel(logging.ERROR)
_logger.propagate = True  # allows pytest caplog to capture records


def setup_error_logging(log_file: str = ERROR_LOG_FILE) -> None:
    """Attach a FileHandler writing to *log_file* at ERROR level.

    Safe to call multiple times — a second FileHandler is never added.
    Intended to be called once at application startup, not at import time,
    so that tests can patch this function to prevent file side-effects.

    Args:
        log_file: Path to the error log file.  Defaults to ERROR_LOG_FILE.
    """
    if any(isinstance(h, logging.FileHandler) for h in _logger.handlers):
        return
    handler = logging.FileHandler(log_file, encoding="utf-8")
    handler.setLevel(logging.ERROR)
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )
    handler.setFormatter(formatter)
    _logger.addHandler(handler)


def get_error_logger() -> logging.Logger:
    """Return the shared calculator error logger."""
    return _logger
