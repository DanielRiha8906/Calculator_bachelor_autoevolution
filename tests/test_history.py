import pytest

import src.history as history_module
from src.history import clear_history, display_history, load_history, record_entry


@pytest.fixture(autouse=True)
def tmp_history_file(tmp_path, monkeypatch):
    """Redirect HISTORY_FILE to a temporary path for each test."""
    tmp_file = tmp_path / "history.txt"
    monkeypatch.setattr(history_module, "HISTORY_FILE", tmp_file)
    return tmp_file


# --- clear_history ---

def test_clear_history_creates_empty_file(tmp_history_file):
    tmp_history_file.write_text("existing content\n", encoding="utf-8")
    clear_history()
    assert tmp_history_file.read_text(encoding="utf-8") == ""


def test_clear_history_works_when_file_does_not_exist(tmp_history_file):
    assert not tmp_history_file.exists()
    clear_history()
    assert tmp_history_file.exists()
    assert tmp_history_file.read_text(encoding="utf-8") == ""


# --- record_entry ---

def test_record_entry_appends_single_entry(tmp_history_file):
    clear_history()
    record_entry("Add: 7.0")
    assert load_history() == ["Add: 7.0"]


def test_record_entry_appends_multiple_entries_in_order(tmp_history_file):
    clear_history()
    record_entry("Add: 7.0")
    record_entry("Multiply: 12.0")
    record_entry("Factorial: 120")
    assert load_history() == ["Add: 7.0", "Multiply: 12.0", "Factorial: 120"]


# --- load_history ---

def test_load_history_returns_empty_list_when_file_missing(tmp_history_file):
    # File has not been created yet
    assert load_history() == []


def test_load_history_returns_empty_list_when_file_empty(tmp_history_file):
    clear_history()
    assert load_history() == []


def test_load_history_ignores_blank_lines(tmp_history_file):
    tmp_history_file.write_text("Add: 7.0\n\nMultiply: 12.0\n", encoding="utf-8")
    assert load_history() == ["Add: 7.0", "Multiply: 12.0"]


# --- display_history ---

def test_display_history_shows_no_history_when_empty(tmp_history_file, capsys):
    clear_history()
    display_history()
    out = capsys.readouterr().out
    assert "No history yet" in out


def test_display_history_shows_entries_with_numbering(tmp_history_file, capsys):
    clear_history()
    record_entry("Add: 7.0")
    record_entry("Factorial: 120")
    display_history()
    out = capsys.readouterr().out
    assert "Add: 7.0" in out
    assert "Factorial: 120" in out
    assert "1." in out
    assert "2." in out


def test_display_history_shows_session_header(tmp_history_file, capsys):
    clear_history()
    record_entry("Add: 7.0")
    display_history()
    out = capsys.readouterr().out
    assert "Session history" in out


def test_display_history_shows_no_history_when_file_missing(tmp_history_file, capsys):
    # File not created at all
    display_history()
    out = capsys.readouterr().out
    assert "No history yet" in out
