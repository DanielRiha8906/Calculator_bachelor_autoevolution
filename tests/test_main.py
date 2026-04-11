"""Tests for the interactive calculator session in src/__main__.py.

Each test drives main() through one or more calculation cycles by mocking
builtins.input with a predetermined sequence of responses and then asserting
on the captured stdout.  Every sequence must end with 'q' so the loop exits,
unless the test exercises the max-retry termination path.
"""

import math
from unittest.mock import patch

import pytest

from src.__main__ import main, MAX_RETRIES


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _run(inputs: list[str], capsys) -> str:
    """Invoke main() with mocked input, return captured stdout."""
    with patch("builtins.input", side_effect=inputs):
        main()
    return capsys.readouterr().out


# ---------------------------------------------------------------------------
# Quit / navigation
# ---------------------------------------------------------------------------

def test_quit_immediately(capsys):
    out = _run(["q"], capsys)
    assert "Goodbye!" in out


def test_menu_lists_all_operations(capsys):
    out = _run(["q"], capsys)
    # Every operation label must appear in the menu.
    for keyword in ["Add", "Subtract", "Multiply", "Divide", "Factorial",
                    "Square", "Cube", "Square root", "Cube root",
                    "Power", "Log base-10", "Natural log"]:
        assert keyword in out


def test_invalid_choice_shows_message(capsys):
    out = _run(["99", "q"], capsys)
    assert "Invalid choice" in out


def test_invalid_choice_then_valid_operation(capsys):
    # After an invalid choice the loop should continue cleanly.
    out = _run(["abc", "1", "2", "3", "q"], capsys)
    assert "Invalid choice" in out
    assert "Result: 5" in out


# ---------------------------------------------------------------------------
# Retry logic — invalid menu selection
# ---------------------------------------------------------------------------

def test_invalid_menu_choice_shows_available_operations(capsys):
    # Error message for an unknown choice must list the available operation keys.
    out = _run(["99", "q"], capsys)
    assert "Available options" in out


def test_invalid_menu_choice_max_retries_terminates(capsys):
    # MAX_RETRIES consecutive invalid menu choices must end the session.
    out = _run(["bad"] * MAX_RETRIES, capsys)
    assert "Ending session" in out


def test_valid_choice_resets_menu_failure_counter(capsys):
    # A valid operation resets the failure counter; the session must not
    # terminate after (MAX_RETRIES - 1) invalid choices followed by a valid one.
    inputs = ["bad"] * (MAX_RETRIES - 1) + ["1", "2", "3", "q"]
    out = _run(inputs, capsys)
    assert "Result: 5" in out


# ---------------------------------------------------------------------------
# Retry logic — invalid operand input
# ---------------------------------------------------------------------------

def test_invalid_operand_retry_then_succeed(capsys):
    # An invalid first operand triggers a retry; a subsequent valid value
    # should allow the calculation to complete.
    out = _run(["1", "abc", "3", "4", "q"], capsys)
    assert "Error:" in out
    assert "Result: 7" in out


def test_invalid_operand_max_retries_terminates(capsys):
    # MAX_RETRIES consecutive invalid operands must end the session.
    out = _run(["1"] + ["abc"] * MAX_RETRIES, capsys)
    assert "Ending session" in out


# ---------------------------------------------------------------------------
# Two-operand operations
# ---------------------------------------------------------------------------

def test_add(capsys):
    out = _run(["1", "3", "4", "q"], capsys)
    assert "Result: 7" in out


def test_subtract(capsys):
    out = _run(["2", "10", "3", "q"], capsys)
    assert "Result: 7" in out


def test_multiply(capsys):
    out = _run(["3", "4", "5", "q"], capsys)
    assert "Result: 20" in out


def test_divide_exact(capsys):
    out = _run(["4", "10", "2", "q"], capsys)
    assert "Result: 5.0" in out


def test_divide_by_zero_shows_error(capsys):
    out = _run(["4", "5", "0", "q"], capsys)
    assert "Error:" in out


def test_power(capsys):
    out = _run(["10", "2", "3", "q"], capsys)
    assert "Result: 8.0" in out


def test_power_negative_base_fractional_exponent_shows_error(capsys):
    out = _run(["10", "-2", "0.5", "q"], capsys)
    assert "Error:" in out


# ---------------------------------------------------------------------------
# Single-operand operations
# ---------------------------------------------------------------------------

def test_factorial(capsys):
    out = _run(["5", "5", "q"], capsys)
    assert "Result: 120" in out


def test_factorial_zero(capsys):
    out = _run(["5", "0", "q"], capsys)
    assert "Result: 1" in out


def test_factorial_negative_shows_error(capsys):
    out = _run(["5", "-1", "q"], capsys)
    assert "Error:" in out


def test_factorial_float_input_shows_error(capsys):
    # "3.5" cannot be parsed as int; _prompt_number shows an error and retries.
    # Providing valid integer "5" on the next attempt completes the calculation.
    out = _run(["5", "3.5", "5", "q"], capsys)
    assert "Error:" in out
    assert "Result: 120" in out


def test_square(capsys):
    out = _run(["6", "4", "q"], capsys)
    assert "Result: 16" in out


def test_square_negative(capsys):
    out = _run(["6", "-3", "q"], capsys)
    assert "Result: 9" in out


def test_cube(capsys):
    out = _run(["7", "3", "q"], capsys)
    assert "Result: 27" in out


def test_sqrt(capsys):
    out = _run(["8", "9", "q"], capsys)
    assert "Result: 3.0" in out


def test_sqrt_negative_shows_error(capsys):
    out = _run(["8", "-1", "q"], capsys)
    assert "Error:" in out


def test_cbrt(capsys):
    out = _run(["9", "27", "q"], capsys)
    assert "Result: 3.0" in out


def test_cbrt_negative(capsys):
    out = _run(["9", "-27", "q"], capsys)
    assert "Result: -3.0" in out


def test_log10(capsys):
    out = _run(["11", "100", "q"], capsys)
    assert "Result: 2.0" in out


def test_log10_non_positive_shows_error(capsys):
    out = _run(["11", "0", "q"], capsys)
    assert "Error:" in out


def test_ln(capsys):
    out = _run(["12", "1", "q"], capsys)
    assert "Result: 0.0" in out


def test_ln_non_positive_shows_error(capsys):
    out = _run(["12", "-1", "q"], capsys)
    assert "Error:" in out


# ---------------------------------------------------------------------------
# Multi-calculation session
# ---------------------------------------------------------------------------

def test_multiple_calculations_in_one_session(capsys):
    # add 1+2=3, then square 4=16, then quit
    out = _run(["1", "1", "2", "6", "4", "q"], capsys)
    assert "Result: 3" in out
    assert "Result: 16" in out


def test_error_does_not_terminate_session(capsys):
    # divide-by-zero should show error but the loop must continue.
    out = _run(["4", "1", "0", "1", "3", "4", "q"], capsys)
    assert "Error:" in out
    assert "Result: 7" in out
