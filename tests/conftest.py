"""Shared pytest fixtures for the calculator test suite."""
from unittest.mock import patch

import pytest


@pytest.fixture(autouse=True)
def isolate_error_log(tmp_path):
    """Redirect error log writes to a temporary file for every test.

    Without this fixture, any test that exercises an error path would
    create or append to a real ``error.log`` file in the working directory.
    Patching ``src.error_logger.ERROR_LOG_FILE`` at the module level ensures
    that ``log_error()`` always writes to a throw-away path instead.

    The fixture yields the temporary log path so individual tests can
    inspect log contents when needed.
    """
    log_path = str(tmp_path / "error.log")
    with patch("src.error_logger.ERROR_LOG_FILE", log_path):
        yield log_path
