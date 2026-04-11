"""Tests for error logging behavior.

Verifies that invalid usage and calculation failures are recorded by the
calculator error logger in both CLI and interactive modes.

caplog is used to capture log records in memory without writing to a file,
keeping tests hermetic.  One test per mode verifies that errors are also
written to the log file when setup_error_logging() is called for real.
"""
import logging
from unittest.mock import patch

import pytest

from main import main as cli_main
from src.__main__ import main as interactive_main
from src.error_logger import ERROR_LOG_FILE, _LOGGER_NAME, get_error_logger, setup_error_logging


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _run_cli(args, caplog):
    """Run CLI main() with log capture but no file side-effects."""
    with caplog.at_level(logging.ERROR, logger=_LOGGER_NAME):
        with patch("main.setup_error_logging"):
            try:
                cli_main(args)
            except SystemExit:
                pass


def _run_interactive(inputs, caplog, capsys):
    """Run interactive main() with log capture but no file side-effects."""
    with caplog.at_level(logging.ERROR, logger=_LOGGER_NAME):
        with patch("builtins.input", side_effect=inputs):
            with patch("src.__main__._write_history"):
                with patch("src.__main__.setup_error_logging"):
                    interactive_main()
    capsys.readouterr()


# ---------------------------------------------------------------------------
# CLI — error logging
# ---------------------------------------------------------------------------

def test_cli_logs_missing_operation(caplog, capsys):
    _run_cli([], caplog)
    messages = [r.message for r in caplog.records]
    assert any("[cli]" in m and "missing" in m for m in messages)


def test_cli_logs_unknown_operation(caplog, capsys):
    _run_cli(["modulo", "5", "3"], caplog)
    messages = [r.message for r in caplog.records]
    assert any("[cli]" in m and "unknown operation" in m for m in messages)


def test_cli_logs_incorrect_argument_count(caplog, capsys):
    _run_cli(["add", "5"], caplog)
    messages = [r.message for r in caplog.records]
    assert any("[cli]" in m and "incorrect argument count" in m for m in messages)


def test_cli_logs_invalid_operand(caplog, capsys):
    _run_cli(["add", "abc", "5"], caplog)
    messages = [r.message for r in caplog.records]
    assert any("[cli]" in m and "invalid operand" in m for m in messages)


def test_cli_logs_divide_by_zero(caplog, capsys):
    _run_cli(["divide", "5", "0"], caplog)
    messages = [r.message for r in caplog.records]
    assert any("[cli]" in m and "calculation error" in m for m in messages)


def test_cli_logs_sqrt_negative(caplog, capsys):
    _run_cli(["sqrt", "-1"], caplog)
    messages = [r.message for r in caplog.records]
    assert any("[cli]" in m and "calculation error" in m for m in messages)


def test_cli_logs_factorial_negative(caplog, capsys):
    _run_cli(["factorial", "-1"], caplog)
    messages = [r.message for r in caplog.records]
    assert any("[cli]" in m and "calculation error" in m for m in messages)


def test_cli_logs_log10_non_positive(caplog, capsys):
    _run_cli(["log10", "0"], caplog)
    messages = [r.message for r in caplog.records]
    assert any("[cli]" in m and "calculation error" in m for m in messages)


# ---------------------------------------------------------------------------
# Interactive mode — error logging
# ---------------------------------------------------------------------------

def test_interactive_logs_invalid_menu_choice(caplog, capsys):
    _run_interactive(["99", "q"], caplog, capsys)
    messages = [r.message for r in caplog.records]
    assert any("[interactive]" in m and "invalid menu choice" in m for m in messages)


def test_interactive_logs_max_retries_menu(caplog, capsys):
    from src.__main__ import MAX_RETRIES
    _run_interactive(["bad"] * MAX_RETRIES, caplog, capsys)
    messages = [r.message for r in caplog.records]
    assert any("[interactive]" in m and "max retries" in m for m in messages)


def test_interactive_logs_invalid_operand(caplog, capsys):
    # "abc" is not a valid number; logged inside _prompt_number
    _run_interactive(["1", "abc", "3", "4", "q"], caplog, capsys)
    messages = [r.message for r in caplog.records]
    assert any("[interactive]" in m and "invalid operand input" in m for m in messages)


def test_interactive_logs_divide_by_zero(caplog, capsys):
    _run_interactive(["4", "5", "0", "q"], caplog, capsys)
    messages = [r.message for r in caplog.records]
    assert any("[interactive]" in m and "calculation error" in m for m in messages)


def test_interactive_logs_sqrt_negative(caplog, capsys):
    _run_interactive(["8", "-1", "q"], caplog, capsys)
    messages = [r.message for r in caplog.records]
    assert any("[interactive]" in m and "calculation error" in m for m in messages)


def test_interactive_logs_ln_non_positive(caplog, capsys):
    _run_interactive(["12", "-1", "q"], caplog, capsys)
    messages = [r.message for r in caplog.records]
    assert any("[interactive]" in m and "calculation error" in m for m in messages)


# ---------------------------------------------------------------------------
# File writing — verify errors reach the log file
# ---------------------------------------------------------------------------

def _isolated_setup(log_file):
    """Clear any existing FileHandlers and attach a fresh one pointing to log_file."""
    logger = get_error_logger()
    for h in list(logger.handlers):
        if isinstance(h, logging.FileHandler):
            h.close()
            logger.removeHandler(h)
    setup_error_logging(str(log_file))
    return logger


def _teardown_file_handlers():
    """Remove all FileHandlers from the error logger (cleanup after file tests)."""
    logger = get_error_logger()
    for h in list(logger.handlers):
        if isinstance(h, logging.FileHandler):
            h.close()
            logger.removeHandler(h)


def test_cli_errors_written_to_log_file(tmp_path, capsys):
    """CLI calculation errors are written to the error log file."""
    log_file = tmp_path / "error.log"
    _isolated_setup(log_file)
    try:
        try:
            cli_main(["divide", "5", "0"])
        except SystemExit:
            pass
        capsys.readouterr()
        assert log_file.exists()
        content = log_file.read_text(encoding="utf-8")
        assert "calculation error" in content
        assert "[cli]" in content
    finally:
        _teardown_file_handlers()


def test_interactive_errors_written_to_log_file(tmp_path, capsys):
    """Interactive calculation errors are written to the error log file."""
    log_file = tmp_path / "error.log"
    _isolated_setup(log_file)
    try:
        with patch("builtins.input", side_effect=["4", "5", "0", "q"]):
            with patch("src.__main__._write_history"):
                with patch("src.__main__.setup_error_logging"):
                    # setup_error_logging already called above via _isolated_setup
                    interactive_main()
        capsys.readouterr()
        assert log_file.exists()
        content = log_file.read_text(encoding="utf-8")
        assert "calculation error" in content
        assert "[interactive]" in content
    finally:
        _teardown_file_handlers()
