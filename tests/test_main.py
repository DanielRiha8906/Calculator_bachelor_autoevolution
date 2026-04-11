"""Tests for the interactive calculator session in src/__main__.py.

Each test drives main() through one or more calculation cycles by mocking
builtins.input with a predetermined sequence of responses and then asserting
on the captured stdout.  Every sequence must end with 'q' so the loop exits,
unless the test exercises the max-retry termination path.

The interactive session now starts with a mode selection step:
  "1" selects Normal mode (add, subtract, multiply, divide, square, sqrt)
  "2" selects Scientific mode (power, cube, cbrt, factorial, log10, ln,
                               sin, cos, tan, cot, asin, acos)

Operation key assignments by mode:
  Normal:      1=add  2=subtract  3=multiply  4=divide  5=square  6=sqrt
  Scientific:  1=power  2=cube  3=cbrt  4=factorial  5=log10  6=ln
               7=sin  8=cos  9=tan  10=cot  11=asin  12=acos

_run() mocks src.session._write_history to prevent file side-effects during
tests.  Tests that specifically verify file writing call main() directly with
src.session.HISTORY_FILE patched to a tmp_path location.
"""

import math
from unittest.mock import patch

import pytest

from src.__main__ import main, MAX_RETRIES


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _run(inputs: list[str], capsys) -> str:
    """Invoke main() with mocked input and no-op file writes, return captured stdout.

    setup_error_logging is patched to a no-op so tests produce no file
    side-effects; use test_error_logging.py for logging-specific assertions.
    """
    with patch("builtins.input", side_effect=inputs):
        with patch("src.session._write_history"):
            with patch("src.session.setup_error_logging"):
                main()
    return capsys.readouterr().out


# ---------------------------------------------------------------------------
# Mode selection
# ---------------------------------------------------------------------------

def test_mode_selection_normal(capsys):
    out = _run(["1", "q"], capsys)
    assert "Normal" in out


def test_mode_selection_scientific(capsys):
    out = _run(["2", "q"], capsys)
    assert "Scientific" in out


def test_mode_selection_invalid_then_valid(capsys):
    out = _run(["9", "1", "q"], capsys)
    assert "Invalid choice" in out
    assert "Normal" in out


def test_mode_selection_max_retries_terminates(capsys):
    out = _run(["bad"] * MAX_RETRIES, capsys)
    assert "Ending session" in out


# ---------------------------------------------------------------------------
# Quit / navigation
# ---------------------------------------------------------------------------

def test_quit_immediately(capsys):
    out = _run(["1", "q"], capsys)
    assert "Goodbye!" in out


def test_normal_mode_menu_lists_operations(capsys):
    out = _run(["1", "q"], capsys)
    for keyword in ["Add", "Subtract", "Multiply", "Divide", "Square", "Square root"]:
        assert keyword in out


def test_scientific_mode_menu_lists_operations(capsys):
    out = _run(["2", "q"], capsys)
    for keyword in ["Power", "Cube", "Cube root", "Factorial",
                    "Log base-10", "Natural log",
                    "Sin", "Cos", "Tan", "Cot", "Arcsin", "Arccos"]:
        assert keyword in out


def test_menu_lists_history_option(capsys):
    out = _run(["1", "q"], capsys)
    assert "Show history" in out


def test_menu_lists_switch_mode_option(capsys):
    out = _run(["1", "q"], capsys)
    assert "Switch mode" in out


def test_invalid_choice_shows_message(capsys):
    out = _run(["1", "99", "q"], capsys)
    assert "Invalid choice" in out


def test_invalid_choice_then_valid_operation(capsys):
    # After an invalid choice the loop should continue cleanly.
    # Normal mode: key 1=add; inputs: mode=1, bad, op=1, a=2, b=3, quit
    out = _run(["1", "abc", "1", "2", "3", "q"], capsys)
    assert "Invalid choice" in out
    assert "Result: 5" in out


# ---------------------------------------------------------------------------
# Mode switching
# ---------------------------------------------------------------------------

def test_switch_mode_changes_menu(capsys):
    # Start in normal mode, switch to scientific, then quit.
    out = _run(["1", "s", "2", "q"], capsys)
    assert "Normal" in out
    assert "Scientific" in out


def test_switch_mode_allows_scientific_operation(capsys):
    # Start normal, switch to scientific, run power(2, 3)=8, quit.
    out = _run(["1", "s", "2", "1", "2", "3", "q"], capsys)
    assert "Result: 8.0" in out


def test_switch_mode_invalid_then_valid(capsys):
    # 's' triggers mode selection; an invalid entry should re-prompt.
    out = _run(["1", "s", "bad", "2", "q"], capsys)
    assert "Scientific" in out


# ---------------------------------------------------------------------------
# Retry logic — invalid menu selection
# ---------------------------------------------------------------------------

def test_invalid_menu_choice_shows_available_operations(capsys):
    # Error message for an unknown choice must list the available operation keys.
    out = _run(["1", "99", "q"], capsys)
    assert "Available options" in out


def test_invalid_menu_choice_max_retries_terminates(capsys):
    # MAX_RETRIES consecutive invalid menu choices must end the session.
    out = _run(["1"] + ["bad"] * MAX_RETRIES, capsys)
    assert "Ending session" in out


def test_valid_choice_resets_menu_failure_counter(capsys):
    # A valid operation resets the failure counter; the session must not
    # terminate after (MAX_RETRIES - 1) invalid choices followed by a valid one.
    # Normal mode: key 1=add
    inputs = ["1"] + ["bad"] * (MAX_RETRIES - 1) + ["1", "2", "3", "q"]
    out = _run(inputs, capsys)
    assert "Result: 5" in out


# ---------------------------------------------------------------------------
# Retry logic — invalid operand input
# ---------------------------------------------------------------------------

def test_invalid_operand_retry_then_succeed(capsys):
    # An invalid first operand triggers a retry; a subsequent valid value
    # should allow the calculation to complete.
    # Normal mode: key 1=add; abc invalid, then 3, then 4
    out = _run(["1", "1", "abc", "3", "4", "q"], capsys)
    assert "Error:" in out
    assert "Result: 7" in out


def test_invalid_operand_max_retries_terminates(capsys):
    # MAX_RETRIES consecutive invalid operands must end the session.
    # Normal mode: key 1=add
    out = _run(["1", "1"] + ["abc"] * MAX_RETRIES, capsys)
    assert "Ending session" in out


# ---------------------------------------------------------------------------
# Normal mode — two-operand operations
# ---------------------------------------------------------------------------

def test_add(capsys):
    # Normal mode key 1=add
    out = _run(["1", "1", "3", "4", "q"], capsys)
    assert "Result: 7" in out


def test_subtract(capsys):
    # Normal mode key 2=subtract
    out = _run(["1", "2", "10", "3", "q"], capsys)
    assert "Result: 7" in out


def test_multiply(capsys):
    # Normal mode key 3=multiply
    out = _run(["1", "3", "4", "5", "q"], capsys)
    assert "Result: 20" in out


def test_divide_exact(capsys):
    # Normal mode key 4=divide
    out = _run(["1", "4", "10", "2", "q"], capsys)
    assert "Result: 5.0" in out


def test_divide_by_zero_shows_error(capsys):
    # Normal mode key 4=divide
    out = _run(["1", "4", "5", "0", "q"], capsys)
    assert "Error:" in out


# ---------------------------------------------------------------------------
# Normal mode — single-operand operations
# ---------------------------------------------------------------------------

def test_square(capsys):
    # Normal mode key 5=square
    out = _run(["1", "5", "4", "q"], capsys)
    assert "Result: 16" in out


def test_square_negative(capsys):
    # Normal mode key 5=square
    out = _run(["1", "5", "-3", "q"], capsys)
    assert "Result: 9" in out


def test_sqrt(capsys):
    # Normal mode key 6=sqrt
    out = _run(["1", "6", "9", "q"], capsys)
    assert "Result: 3.0" in out


def test_sqrt_negative_shows_error(capsys):
    # Normal mode key 6=sqrt
    out = _run(["1", "6", "-1", "q"], capsys)
    assert "Error:" in out


# ---------------------------------------------------------------------------
# Scientific mode — two-operand operations
# ---------------------------------------------------------------------------

def test_power(capsys):
    # Scientific mode key 1=power
    out = _run(["2", "1", "2", "3", "q"], capsys)
    assert "Result: 8.0" in out


def test_power_negative_base_fractional_exponent_shows_error(capsys):
    # Scientific mode key 1=power
    out = _run(["2", "1", "-2", "0.5", "q"], capsys)
    assert "Error:" in out


# ---------------------------------------------------------------------------
# Scientific mode — single-operand operations
# ---------------------------------------------------------------------------

def test_cube(capsys):
    # Scientific mode key 2=cube
    out = _run(["2", "2", "3", "q"], capsys)
    assert "Result: 27" in out


def test_cbrt(capsys):
    # Scientific mode key 3=cbrt
    out = _run(["2", "3", "27", "q"], capsys)
    assert "Result: 3.0" in out


def test_cbrt_negative(capsys):
    # Scientific mode key 3=cbrt
    out = _run(["2", "3", "-27", "q"], capsys)
    assert "Result: -3.0" in out


def test_factorial(capsys):
    # Scientific mode key 4=factorial
    out = _run(["2", "4", "5", "q"], capsys)
    assert "Result: 120" in out


def test_factorial_zero(capsys):
    # Scientific mode key 4=factorial
    out = _run(["2", "4", "0", "q"], capsys)
    assert "Result: 1" in out


def test_factorial_negative_shows_error(capsys):
    # Scientific mode key 4=factorial
    out = _run(["2", "4", "-1", "q"], capsys)
    assert "Error:" in out


def test_factorial_float_input_shows_error(capsys):
    # "3.5" cannot be parsed as int; _prompt_number shows an error and retries.
    # Providing valid integer "5" on the next attempt completes the calculation.
    # Scientific mode key 4=factorial
    out = _run(["2", "4", "3.5", "5", "q"], capsys)
    assert "Error:" in out
    assert "Result: 120" in out


def test_log10(capsys):
    # Scientific mode key 5=log10
    out = _run(["2", "5", "100", "q"], capsys)
    assert "Result: 2.0" in out


def test_log10_non_positive_shows_error(capsys):
    # Scientific mode key 5=log10
    out = _run(["2", "5", "0", "q"], capsys)
    assert "Error:" in out


def test_ln(capsys):
    # Scientific mode key 6=ln
    out = _run(["2", "6", "1", "q"], capsys)
    assert "Result: 0.0" in out


def test_ln_non_positive_shows_error(capsys):
    # Scientific mode key 6=ln
    out = _run(["2", "6", "-1", "q"], capsys)
    assert "Error:" in out


def test_sin(capsys):
    # Scientific mode key 7=sin; sin(90°)=1.0 (exact in IEEE 754)
    out = _run(["2", "7", "90", "q"], capsys)
    assert "Result: 1.0" in out


def test_cos(capsys):
    # Scientific mode key 8=cos; cos(0°)=1.0 (exact in IEEE 754)
    out = _run(["2", "8", "0", "q"], capsys)
    assert "Result: 1.0" in out


def test_tan(capsys):
    # Scientific mode key 9=tan; tan(0°)=0.0 (exact in IEEE 754)
    out = _run(["2", "9", "0", "q"], capsys)
    assert "Result: 0.0" in out


def test_tan_undefined_shows_error(capsys):
    # Scientific mode key 9=tan; tan(90°) is undefined
    out = _run(["2", "9", "90", "q"], capsys)
    assert "Error:" in out


def test_cot(capsys):
    # Scientific mode key 10=cot; cot(45°)=1.0
    out = _run(["2", "10", "45", "q"], capsys)
    assert "Result:" in out
    assert "1.0" in out


def test_cot_undefined_shows_error(capsys):
    # Scientific mode key 10=cot; cot(0°) is undefined
    out = _run(["2", "10", "0", "q"], capsys)
    assert "Error:" in out


def test_asin(capsys):
    # Scientific mode key 11=asin; asin(1)=90°
    out = _run(["2", "11", "1", "q"], capsys)
    assert "Result: 90.0" in out


def test_asin_out_of_range_shows_error(capsys):
    # Scientific mode key 11=asin; asin(2) is undefined
    out = _run(["2", "11", "2", "q"], capsys)
    assert "Error:" in out


def test_acos(capsys):
    # Scientific mode key 12=acos; acos(0)=90°
    out = _run(["2", "12", "0", "q"], capsys)
    assert "Result: 90.0" in out


def test_acos_out_of_range_shows_error(capsys):
    # Scientific mode key 12=acos; acos(2) is undefined
    out = _run(["2", "12", "2", "q"], capsys)
    assert "Error:" in out


# ---------------------------------------------------------------------------
# Multi-calculation session
# ---------------------------------------------------------------------------

def test_multiple_calculations_in_one_session(capsys):
    # Normal mode: add 1+2=3, then square 4=16, then quit
    # key 1=add, key 5=square
    out = _run(["1", "1", "1", "2", "5", "4", "q"], capsys)
    assert "Result: 3" in out
    assert "Result: 16" in out


def test_error_does_not_terminate_session(capsys):
    # Normal mode: divide-by-zero should show error but the loop must continue.
    # key 4=divide, key 1=add
    out = _run(["1", "4", "1", "0", "1", "3", "4", "q"], capsys)
    assert "Error:" in out
    assert "Result: 7" in out


# ---------------------------------------------------------------------------
# Session history — display
# ---------------------------------------------------------------------------

def test_history_empty_before_first_calculation(capsys):
    """'h' before any calculation shows 'No calculations yet.'"""
    out = _run(["1", "h", "q"], capsys)
    assert "No calculations yet." in out


def test_history_records_binary_operation(capsys):
    """A successful binary calculation appears in the history when 'h' is entered."""
    # Normal mode key 1=add; add(2, 3)=5
    out = _run(["1", "1", "2", "3", "h", "q"], capsys)
    assert "add(2, 3) = 5" in out


def test_history_records_unary_operation(capsys):
    """A successful unary calculation appears in the history when 'h' is entered."""
    # Scientific mode key 4=factorial; factorial(4)=24
    out = _run(["2", "4", "4", "h", "q"], capsys)
    assert "factorial(4) = 24" in out


def test_history_multiple_entries(capsys):
    """All successful calculations in a session appear in history."""
    # Normal mode: add(1,2)=3, then square(4)=16, then show history
    # key 1=add, key 5=square
    out = _run(["1", "1", "1", "2", "5", "4", "h", "q"], capsys)
    assert "add(1, 2) = 3" in out
    assert "square(4) = 16" in out


def test_history_error_not_recorded(capsys):
    """A calculation that raises an error is not added to the history."""
    # Normal mode key 4=divide: divide 5 by 0 → error → history still empty
    out = _run(["1", "4", "5", "0", "h", "q"], capsys)
    assert "No calculations yet." in out


def test_history_h_is_not_invalid_choice(capsys):
    """'h' must not trigger the 'Invalid choice' error message."""
    out = _run(["1", "h", "q"], capsys)
    assert "Invalid choice" not in out


# ---------------------------------------------------------------------------
# Session history — file writing
# ---------------------------------------------------------------------------

def test_history_written_to_file_on_quit(tmp_path, capsys):
    """History is written to HISTORY_FILE when the user quits."""
    history_file = tmp_path / "history.txt"
    with patch("src.session.HISTORY_FILE", str(history_file)):
        # Normal mode key 1=add; add(2, 3)=5
        with patch("builtins.input", side_effect=["1", "1", "2", "3", "q"]):
            with patch("src.session.setup_error_logging"):
                main()
    capsys.readouterr()
    assert history_file.exists()
    assert "add(2, 3) = 5" in history_file.read_text()


def test_history_fresh_each_session(tmp_path, capsys):
    """A new session overwrites any existing history file; old entries are not loaded."""
    history_file = tmp_path / "history.txt"
    history_file.write_text("old_op(1) = 999\n")
    with patch("src.session.HISTORY_FILE", str(history_file)):
        # Normal mode key 1=add; add(4, 5)=9
        with patch("builtins.input", side_effect=["1", "1", "4", "5", "q"]):
            with patch("src.session.setup_error_logging"):
                main()
    capsys.readouterr()
    content = history_file.read_text()
    assert "old_op" not in content
    assert "add(4, 5) = 9" in content


def test_history_written_on_retry_termination(tmp_path, capsys):
    """History is written to HISTORY_FILE when the session ends due to max retries."""
    history_file = tmp_path / "history.txt"
    with patch("src.session.HISTORY_FILE", str(history_file)):
        # Normal mode key 1=add; add(3, 4)=7, then exhaust menu retries
        with patch("builtins.input", side_effect=["1", "1", "3", "4"] + ["bad"] * MAX_RETRIES):
            with patch("src.session.setup_error_logging"):
                main()
    capsys.readouterr()
    assert history_file.exists()
    assert "add(3, 4) = 7" in history_file.read_text()
