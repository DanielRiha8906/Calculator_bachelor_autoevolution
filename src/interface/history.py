"""Session history and error-log file helpers.

Constants
---------
HISTORY_FILE   : default path for the per-session operation history.
ERROR_LOG_FILE : default path for the append-only error log.

Both constants use the None-sentinel pattern in function signatures so that
monkeypatching the module attribute in tests takes effect at call time rather
than at definition time.
"""
from datetime import datetime

HISTORY_FILE = "history.txt"
ERROR_LOG_FILE = "error.log"


def clear_history(filepath: "str | None" = None) -> None:
    """Clear (or create) the history file, removing any previous session data."""
    if filepath is None:
        filepath = HISTORY_FILE
    with open(filepath, "w", encoding="utf-8") as fh:
        fh.write("")


def append_to_history(entry: str, filepath: "str | None" = None) -> None:
    """Append a single history entry (one line) to the history file."""
    if filepath is None:
        filepath = HISTORY_FILE
    with open(filepath, "a", encoding="utf-8") as fh:
        fh.write(entry + "\n")


def show_history(filepath: "str | None" = None) -> None:
    """Print all history entries from the current session to stdout."""
    if filepath is None:
        filepath = HISTORY_FILE
    try:
        with open(filepath, "r", encoding="utf-8") as fh:
            lines = fh.read().splitlines()
    except FileNotFoundError:
        lines = []
    if not lines:
        print("  No history yet.")
    else:
        print("\n--- History ---")
        for i, line in enumerate(lines, start=1):
            print(f"  {i}. {line}")


def append_to_error_log(message: str, filepath: "str | None" = None) -> None:
    """Append a timestamped error entry to the error log file.

    The log is append-only and never cleared — it persists across sessions.
    """
    if filepath is None:
        filepath = ERROR_LOG_FILE
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filepath, "a", encoding="utf-8") as fh:
        fh.write(f"[{timestamp}] {message}\n")
