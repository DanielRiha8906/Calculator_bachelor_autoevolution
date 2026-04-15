"""Dedicated error logger for the calculator application.

Appends error events to a local log file so that invalid usage and
calculation failures are recorded separately from user-facing history.

The log format is one entry per line::

    2026-04-15T12:00:00 [source] message

where ``source`` identifies the entry point that generated the error
(``"interactive"`` for the menu-driven session, ``"cli"`` for the
bash argument-based interface).
"""

import datetime

# Path to the error log file. Kept as a module-level name (not a default
# argument) so tests can patch it without breaking the function signature.
ERROR_LOG_FILE = "error.log"


def log_error(source: str, message: str) -> None:
    """Append one error entry to the error log file.

    Args:
        source: Short label identifying the caller (e.g. ``"interactive"``
            or ``"cli"``).
        message: Human-readable description of the error.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    entry = f"{timestamp} [{source}] {message}\n"
    with open(ERROR_LOG_FILE, "a", encoding="utf-8") as fh:
        fh.write(entry)
