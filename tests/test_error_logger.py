"""Tests for the error logger module (src/error_logger.py)."""
import os
from unittest.mock import patch

import pytest

from src.error_logger import ERROR_LOG_FILE, log_error


# ---------------------------------------------------------------------------
# log_error: basic write behaviour
# ---------------------------------------------------------------------------

def test_log_error_creates_file(isolate_error_log):
    log_error("test", "something failed")
    assert os.path.exists(isolate_error_log)


def test_log_error_writes_source_and_message(isolate_error_log):
    log_error("cli", "unknown operation 'foo'")
    with open(isolate_error_log, encoding="utf-8") as fh:
        content = fh.read()
    assert "[cli]" in content
    assert "unknown operation 'foo'" in content


def test_log_error_writes_timestamp(isolate_error_log):
    log_error("interactive", "division by zero")
    with open(isolate_error_log, encoding="utf-8") as fh:
        content = fh.read()
    # Timestamp format: YYYY-MM-DDTHH:MM:SS
    import re
    assert re.search(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", content)


def test_log_error_appends_multiple_entries(isolate_error_log):
    log_error("cli", "first error")
    log_error("cli", "second error")
    with open(isolate_error_log, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    assert len(lines) == 2
    assert "first error" in lines[0]
    assert "second error" in lines[1]


def test_log_error_each_entry_on_own_line(isolate_error_log):
    log_error("interactive", "error one")
    log_error("interactive", "error two")
    with open(isolate_error_log, encoding="utf-8") as fh:
        content = fh.read()
    assert content.count("\n") == 2


# ---------------------------------------------------------------------------
# ERROR_LOG_FILE constant
# ---------------------------------------------------------------------------

def test_error_log_file_constant_is_string():
    assert isinstance(ERROR_LOG_FILE, str)


def test_error_log_file_constant_has_log_extension():
    assert ERROR_LOG_FILE.endswith(".log")
