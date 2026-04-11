"""Session history management for the interactive calculator.

History is stored in a local text file (history.txt) and is cleared at the
start of each interactive session so it does not persist between sessions.
"""
import pathlib

HISTORY_FILE = pathlib.Path("history.txt")


def clear_history() -> None:
    """Clear the history file to start a fresh session."""
    HISTORY_FILE.write_text("", encoding="utf-8")


def record_entry(entry: str) -> None:
    """Append one history entry to the history file."""
    with HISTORY_FILE.open("a", encoding="utf-8") as f:
        f.write(entry + "\n")


def load_history() -> list[str]:
    """Read and return all history entries as a list of strings.

    Returns an empty list if the history file does not exist or is empty.
    """
    if not HISTORY_FILE.exists():
        return []
    text = HISTORY_FILE.read_text(encoding="utf-8")
    return [line for line in text.splitlines() if line.strip()]


def display_history() -> None:
    """Print all history entries to stdout."""
    entries = load_history()
    if not entries:
        print("No history yet.")
        return
    print("Session history:")
    for i, entry in enumerate(entries, 1):
        print(f"  {i}. {entry}")
