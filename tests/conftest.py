"""Shared pytest fixtures for the Calculator test suite."""
import logging

import pytest

import src.error_logger as error_logger_module


@pytest.fixture(autouse=True)
def tmp_error_log(tmp_path, monkeypatch):
    """Redirect ERROR_LOG_FILE to a temporary path for every test.

    Also resets the error logger's file handler before each test so that
    get_error_logger() re-creates it against the patched path rather than
    writing to the real calculator_errors.log in the project root.
    """
    tmp_log = tmp_path / "calculator_errors.log"
    monkeypatch.setattr(error_logger_module, "ERROR_LOG_FILE", tmp_log)

    # Clear any handlers left over from a previous test so that the next
    # call to get_error_logger() opens a fresh handler on the patched path.
    logger = logging.getLogger(error_logger_module._LOGGER_NAME)
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)

    yield tmp_log

    # Close and remove handlers after the test to prevent file-handle leaks.
    logger = logging.getLogger(error_logger_module._LOGGER_NAME)
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)
