"""Tests for the interactive CLI session in src/__main__.py."""
import math
import os
import tempfile
from unittest.mock import patch

import pytest

from src.__main__ import (
    OPERATIONS,
    MAX_ATTEMPTS,
    HISTORY_FILE,
    display_menu,
    format_history_entry,
    get_number,
    main,
    save_history,
)


# ---------------------------------------------------------------------------
# OPERATIONS mapping invariants
# ---------------------------------------------------------------------------

def test_operations_contains_all_twelve_ops():
    names = {name for name, _ in OPERATIONS.values()}
    assert names == {
        "add", "subtract", "multiply", "divide", "factorial",
        "square", "cube", "square_root", "cube_root", "power", "log", "ln",
    }


def test_binary_operations_have_arity_2():
    binary = {"add", "subtract", "multiply", "divide", "power"}
    for name, arity in OPERATIONS.values():
        if name in binary:
            assert arity == 2, f"{name} should have arity 2"


def test_unary_operations_have_arity_1():
    unary = {"factorial", "square", "cube", "square_root", "cube_root", "log", "ln"}
    for name, arity in OPERATIONS.values():
        if name in unary:
            assert arity == 1, f"{name} should have arity 1"


# ---------------------------------------------------------------------------
# get_number helper
# ---------------------------------------------------------------------------

def test_get_number_parses_integer():
    with patch("builtins.input", return_value="42"):
        assert get_number("") == 42


def test_get_number_parses_float():
    with patch("builtins.input", return_value="3.14"):
        assert get_number("") == pytest.approx(3.14)


def test_get_number_require_int_accepts_integer_string():
    with patch("builtins.input", return_value="7"):
        assert get_number("", require_int=True) == 7


def test_get_number_require_int_rejects_float_string():
    with patch("builtins.input", return_value="3.5"):
        with pytest.raises(ValueError):
            get_number("", require_int=True)


def test_get_number_raises_for_non_numeric_input():
    with patch("builtins.input", return_value="abc"):
        with pytest.raises(ValueError):
            get_number("")


# ---------------------------------------------------------------------------
# Helper: run main() with a sequence of simulated inputs
# ---------------------------------------------------------------------------

def run_main_with_inputs(inputs):
    """Run main() with a canned list of inputs; return all printed strings."""
    with patch("builtins.input", side_effect=inputs), \
         patch("builtins.print") as mock_print:
        main()
    # Flatten all positional args from every print() call into a single list.
    output = []
    for call in mock_print.call_args_list:
        output.extend(str(a) for a in call.args)
    return output


def output_contains(output, substring):
    return any(substring in line for line in output)


# ---------------------------------------------------------------------------
# Quit behaviour
# ---------------------------------------------------------------------------

def test_quit_immediately_prints_goodbye():
    output = run_main_with_inputs(["q"])
    assert output_contains(output, "Goodbye")


def test_quit_case_insensitive():
    output = run_main_with_inputs(["Q"])
    assert output_contains(output, "Goodbye")


# ---------------------------------------------------------------------------
# Binary operations (arity == 2)
# ---------------------------------------------------------------------------

def test_add():
    output = run_main_with_inputs(["1", "3", "4", "q"])
    assert output_contains(output, "7")


def test_subtract():
    output = run_main_with_inputs(["2", "10", "4", "q"])
    assert output_contains(output, "6")


def test_multiply():
    output = run_main_with_inputs(["3", "6", "7", "q"])
    assert output_contains(output, "42")


def test_divide():
    output = run_main_with_inputs(["4", "10", "2", "q"])
    assert output_contains(output, "5")


def test_power():
    output = run_main_with_inputs(["10", "2", "10", "q"])
    assert output_contains(output, "1024")


# ---------------------------------------------------------------------------
# Unary operations (arity == 1)
# ---------------------------------------------------------------------------

def test_factorial():
    output = run_main_with_inputs(["5", "5", "q"])
    assert output_contains(output, "120")


def test_square():
    output = run_main_with_inputs(["6", "4", "q"])
    assert output_contains(output, "16")


def test_cube():
    output = run_main_with_inputs(["7", "3", "q"])
    assert output_contains(output, "27")


def test_square_root():
    output = run_main_with_inputs(["8", "9", "q"])
    assert output_contains(output, "3")


def test_cube_root():
    output = run_main_with_inputs(["9", "27", "q"])
    assert output_contains(output, "3")


def test_log_base10():
    output = run_main_with_inputs(["11", "100", "q"])
    assert output_contains(output, "2")


def test_ln():
    output = run_main_with_inputs(["12", "1", "q"])
    assert output_contains(output, "0")


# ---------------------------------------------------------------------------
# Error handling — operation errors shown, session continues
# ---------------------------------------------------------------------------

def test_divide_by_zero_shows_error():
    output = run_main_with_inputs(["4", "10", "0", "q"])
    assert output_contains(output, "Error")


def test_square_root_negative_shows_error():
    output = run_main_with_inputs(["8", "-1", "q"])
    assert output_contains(output, "Error")


def test_log_zero_shows_error():
    output = run_main_with_inputs(["11", "0", "q"])
    assert output_contains(output, "Error")


def test_ln_negative_shows_error():
    output = run_main_with_inputs(["12", "-5", "q"])
    assert output_contains(output, "Error")


def test_factorial_negative_shows_error():
    output = run_main_with_inputs(["5", "-1", "q"])
    assert output_contains(output, "Error")


def test_factorial_float_input_shows_error():
    # "3.5" cannot be parsed as int; error is shown, then retry with valid input.
    output = run_main_with_inputs(["5", "3.5", "4", "q"])
    assert output_contains(output, "Error")


def test_non_numeric_input_shows_error():
    # "abc" cannot be parsed; error is shown, then retry with valid numbers for add.
    output = run_main_with_inputs(["1", "abc", "5", "3", "q"])
    assert output_contains(output, "Error")


# ---------------------------------------------------------------------------
# Unknown operation key
# ---------------------------------------------------------------------------

def test_unknown_operation_shows_message_and_continues():
    # After unknown key the menu loop continues; next valid op works fine.
    output = run_main_with_inputs(["99", "1", "2", "3", "q"])
    assert output_contains(output, "Unknown")
    assert output_contains(output, "5")  # 2+3=5


def test_unknown_operation_error_includes_operation_list():
    # The error message must name the available operations so the user knows
    # what to enter next.
    output = run_main_with_inputs(["99", "q"])
    assert output_contains(output, "Unknown operation '99'. Available operations")


# ---------------------------------------------------------------------------
# Retry-logic: invalid operand inputs
# ---------------------------------------------------------------------------

def test_invalid_operand_shows_retry_attempts_remaining():
    # After first invalid number, the message says how many retries are left.
    output = run_main_with_inputs(["1", "abc", "5", "3", "q"])
    assert output_contains(output, "remaining")


def test_session_terminates_after_max_invalid_operand_attempts():
    # MAX_ATTEMPTS consecutive bad numbers exhaust retries and end the session.
    inputs = ["1"] + ["abc"] * MAX_ATTEMPTS
    output = run_main_with_inputs(inputs)
    assert output_contains(output, "Maximum attempts")


# ---------------------------------------------------------------------------
# Retry-logic: invalid operation selections
# ---------------------------------------------------------------------------

def test_session_terminates_after_max_invalid_operation_attempts():
    # MAX_ATTEMPTS consecutive unknown operation keys end the session.
    inputs = ["99"] * MAX_ATTEMPTS
    output = run_main_with_inputs(inputs)
    assert output_contains(output, "Maximum attempts")


def test_session_continues_before_max_invalid_operation_attempts():
    # Fewer than MAX_ATTEMPTS invalid selections do not end the session.
    valid_op_inputs = ["1", "2", "3", "q"]  # add(2,3)=5
    inputs = ["99"] * (MAX_ATTEMPTS - 1) + valid_op_inputs
    output = run_main_with_inputs(inputs)
    assert output_contains(output, "5")


# ---------------------------------------------------------------------------
# Multiple calculations in one session
# ---------------------------------------------------------------------------

def test_multiple_calculations_in_session():
    # add(2, 3) = 5, subtract(10, 4) = 6, then quit
    output = run_main_with_inputs(["1", "2", "3", "2", "10", "4", "q"])
    assert output_contains(output, "Result: 5")
    assert output_contains(output, "Result: 6")


def test_three_calculations_then_quit():
    # multiply(3,4)=12, log(10)=1, square_root(16)=4
    output = run_main_with_inputs(["3", "3", "4", "11", "10", "8", "16", "q"])
    assert output_contains(output, "12")
    assert output_contains(output, "1")
    assert output_contains(output, "4")


# ---------------------------------------------------------------------------
# format_history_entry helper
# ---------------------------------------------------------------------------

def test_format_history_entry_binary():
    assert format_history_entry("add", (2, 3), 5) == "add(2, 3) = 5"


def test_format_history_entry_unary():
    assert format_history_entry("factorial", (5,), 120) == "factorial(5) = 120"


def test_format_history_entry_float_result():
    assert format_history_entry("square_root", (9,), 3.0) == "square_root(9) = 3.0"


# ---------------------------------------------------------------------------
# save_history helper
# ---------------------------------------------------------------------------

def test_save_history_writes_entries(tmp_path):
    path = str(tmp_path / "hist.txt")
    save_history(["add(2, 3) = 5", "factorial(5) = 120"], path)
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    assert lines == ["add(2, 3) = 5", "factorial(5) = 120"]


def test_save_history_empty_writes_empty_file(tmp_path):
    path = str(tmp_path / "hist.txt")
    save_history([], path)
    with open(path, encoding="utf-8") as fh:
        content = fh.read()
    assert content == ""


def test_save_history_overwrites_previous_content(tmp_path):
    path = str(tmp_path / "hist.txt")
    save_history(["old_entry(1) = 1"], path)
    save_history(["new_entry(2) = 2"], path)
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    assert lines == ["new_entry(2) = 2"]


# ---------------------------------------------------------------------------
# Session history: display during session ('h' key)
# ---------------------------------------------------------------------------

def test_history_empty_message_before_any_calculation():
    output = run_main_with_inputs(["h", "q"])
    assert output_contains(output, "No history yet")


def test_history_shows_entry_after_calculation():
    # add(2, 3) = 5, then display history
    output = run_main_with_inputs(["1", "2", "3", "h", "q"])
    assert output_contains(output, "add(2, 3) = 5")


def test_history_shows_multiple_entries():
    # add(2,3)=5, factorial(5)=120, then show history
    output = run_main_with_inputs(["1", "2", "3", "5", "5", "h", "q"])
    assert output_contains(output, "add(2, 3) = 5")
    assert output_contains(output, "factorial(5) = 120")


def test_history_header_printed_when_non_empty():
    output = run_main_with_inputs(["1", "2", "3", "h", "q"])
    assert output_contains(output, "Session history")


# ---------------------------------------------------------------------------
# Session history: written to file on session end
# ---------------------------------------------------------------------------

def _run_main_with_history_file(inputs, tmp_path):
    """Run main() capturing output and redirecting HISTORY_FILE to tmp_path."""
    hist_path = str(tmp_path / "history.txt")
    with patch("builtins.input", side_effect=inputs), \
         patch("builtins.print"), \
         patch("src.__main__.HISTORY_FILE", hist_path):
        main()
    return hist_path


def test_history_file_written_on_quit(tmp_path):
    hist_path = _run_main_with_history_file(["1", "2", "3", "q"], tmp_path)
    assert os.path.exists(hist_path)
    with open(hist_path, encoding="utf-8") as fh:
        content = fh.read()
    assert "add(2, 3) = 5" in content


def test_history_file_written_on_session_expiry(tmp_path):
    # Exhaust invalid operation attempts so session terminates
    hist_path = _run_main_with_history_file(
        ["1", "2", "3"] + ["99"] * MAX_ATTEMPTS, tmp_path
    )
    assert os.path.exists(hist_path)
    with open(hist_path, encoding="utf-8") as fh:
        content = fh.read()
    assert "add(2, 3) = 5" in content


def test_history_file_empty_when_no_calculations(tmp_path):
    hist_path = _run_main_with_history_file(["q"], tmp_path)
    assert os.path.exists(hist_path)
    with open(hist_path, encoding="utf-8") as fh:
        content = fh.read()
    assert content == ""


def test_new_session_starts_with_fresh_history(tmp_path):
    # First session: add(2,3)=5; second session: multiply(3,4)=12
    hist_path = str(tmp_path / "history.txt")
    with patch("src.__main__.HISTORY_FILE", hist_path):
        with patch("builtins.input", side_effect=["1", "2", "3", "q"]), \
             patch("builtins.print"):
            main()
        with patch("builtins.input", side_effect=["3", "3", "4", "q"]), \
             patch("builtins.print"):
            main()
    with open(hist_path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    # Only the second session's entry should be present
    assert lines == ["multiply(3, 4) = 12"]


# ---------------------------------------------------------------------------
# History: display_menu includes 'h' option
# ---------------------------------------------------------------------------

def test_display_menu_includes_history_option():
    with patch("builtins.print") as mock_print:
        display_menu()
    output = []
    for call in mock_print.call_args_list:
        output.extend(str(a) for a in call.args)
    assert any("h" in line and "history" in line for line in output)
