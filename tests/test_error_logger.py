"""Tests for the error_logger module."""
import logging

import pytest

import src.error_logger as error_logger_module
from src.error_logger import get_error_logger


# conftest.py provides the autouse tmp_error_log fixture that redirects
# ERROR_LOG_FILE to a temp path and resets logger handlers before each test.


def test_get_error_logger_returns_logger():
    logger = get_error_logger()
    assert isinstance(logger, logging.Logger)


def test_get_error_logger_name():
    logger = get_error_logger()
    assert logger.name == error_logger_module._LOGGER_NAME


def test_error_logger_creates_log_file(tmp_error_log):
    logger = get_error_logger()
    logger.error("test error message")
    assert tmp_error_log.exists()


def test_error_logger_records_error_message(tmp_error_log):
    logger = get_error_logger()
    logger.error("division by zero attempted")
    content = tmp_error_log.read_text(encoding="utf-8")
    assert "division by zero attempted" in content


def test_error_logger_ignores_info_level(tmp_error_log):
    logger = get_error_logger()
    logger.info("this info message should not appear")
    if tmp_error_log.exists():
        content = tmp_error_log.read_text(encoding="utf-8")
        assert "this info message should not appear" not in content


def test_error_logger_ignores_warning_level(tmp_error_log):
    logger = get_error_logger()
    logger.warning("this warning should not appear")
    if tmp_error_log.exists():
        content = tmp_error_log.read_text(encoding="utf-8")
        assert "this warning should not appear" not in content


def test_error_logger_appends_multiple_errors(tmp_error_log):
    logger = get_error_logger()
    logger.error("first error")
    logger.error("second error")
    content = tmp_error_log.read_text(encoding="utf-8")
    assert "first error" in content
    assert "second error" in content


def test_get_error_logger_does_not_duplicate_handlers(tmp_error_log):
    logger1 = get_error_logger()
    logger2 = get_error_logger()
    assert logger1 is logger2
    assert len(logger1.handlers) == 1


def test_error_log_does_not_propagate(tmp_error_log):
    logger = get_error_logger()
    assert logger.propagate is False


def test_error_log_format_includes_level(tmp_error_log):
    logger = get_error_logger()
    logger.error("format check")
    content = tmp_error_log.read_text(encoding="utf-8")
    assert "[ERROR]" in content


def test_error_log_does_not_mix_with_normal_output(tmp_error_log, capsys):
    """Errors go to the log file, not to stdout."""
    logger = get_error_logger()
    logger.error("silent error")
    captured = capsys.readouterr()
    assert "silent error" not in captured.out
    assert "silent error" not in captured.err
