"""Tests for the interactive CLI session in src/__main__.py."""
import math
from unittest.mock import patch

import pytest

from src.__main__ import OPERATIONS, display_menu, get_number, main


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
    # "3.5" cannot be parsed as int, so ValueError is caught
    output = run_main_with_inputs(["5", "3.5", "q"])
    assert output_contains(output, "Error")


def test_non_numeric_input_shows_error():
    # "abc" cannot be parsed as a number; error is shown, then user quits.
    output = run_main_with_inputs(["1", "abc", "q"])
    assert output_contains(output, "Error")


# ---------------------------------------------------------------------------
# Unknown operation key
# ---------------------------------------------------------------------------

def test_unknown_operation_shows_message_and_continues():
    # After unknown key the menu loop continues; next valid op works fine.
    output = run_main_with_inputs(["99", "1", "2", "3", "q"])
    assert output_contains(output, "Unknown")
    assert output_contains(output, "5")  # 2+3=5


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
