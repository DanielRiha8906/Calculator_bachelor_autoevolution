"""Tests for the interactive CLI loop in src/__main__.py."""
import math
from unittest.mock import patch, call
import pytest

from src.__main__ import (
    show_menu,
    parse_number,
    parse_int,
    run_operation,
    main,
    OPERATIONS,
)
from src.calculator import Calculator


@pytest.fixture
def calc():
    return Calculator()


# ---------------------------------------------------------------------------
# show_menu
# ---------------------------------------------------------------------------

def test_show_menu_prints_all_operations(capsys):
    show_menu()
    captured = capsys.readouterr().out
    for key, name in OPERATIONS.items():
        assert name in captured
    assert "q" in captured


# ---------------------------------------------------------------------------
# parse_number
# ---------------------------------------------------------------------------

def test_parse_number_valid_int():
    with patch("builtins.input", return_value="42"):
        assert parse_number("Enter: ") == 42.0


def test_parse_number_valid_float():
    with patch("builtins.input", return_value="3.14"):
        assert math.isclose(parse_number("Enter: "), 3.14)


def test_parse_number_negative():
    with patch("builtins.input", return_value="-7"):
        assert parse_number("Enter: ") == -7.0


def test_parse_number_retries_on_invalid_then_accepts(capsys):
    # First call returns invalid, second returns valid
    with patch("builtins.input", side_effect=["abc", "5"]):
        result = parse_number("Enter: ")
    assert result == 5.0
    captured = capsys.readouterr().out
    assert "Invalid number" in captured


# ---------------------------------------------------------------------------
# parse_int
# ---------------------------------------------------------------------------

def test_parse_int_valid():
    with patch("builtins.input", return_value="10"):
        assert parse_int("Enter: ") == 10


def test_parse_int_retries_on_float_string_then_accepts(capsys):
    with patch("builtins.input", side_effect=["3.5", "3"]):
        result = parse_int("Enter: ")
    assert result == 3
    captured = capsys.readouterr().out
    assert "Invalid integer" in captured


# ---------------------------------------------------------------------------
# run_operation — two-argument operations
# ---------------------------------------------------------------------------

def test_run_operation_add(calc, capsys):
    with patch("builtins.input", side_effect=["3", "4"]):
        run_operation(calc, "add")
    assert "7" in capsys.readouterr().out


def test_run_operation_subtract(calc, capsys):
    with patch("builtins.input", side_effect=["10", "3"]):
        run_operation(calc, "subtract")
    assert "7" in capsys.readouterr().out


def test_run_operation_multiply(calc, capsys):
    with patch("builtins.input", side_effect=["6", "7"]):
        run_operation(calc, "multiply")
    assert "42" in capsys.readouterr().out


def test_run_operation_divide(calc, capsys):
    with patch("builtins.input", side_effect=["10", "2"]):
        run_operation(calc, "divide")
    assert "5" in capsys.readouterr().out


def test_run_operation_divide_by_zero_shows_error(calc, capsys):
    with patch("builtins.input", side_effect=["10", "0"]):
        run_operation(calc, "divide")
    captured = capsys.readouterr().out
    assert "Error" in captured
    assert "Division by zero" in captured


def test_run_operation_power(calc, capsys):
    with patch("builtins.input", side_effect=["2", "10"]):
        run_operation(calc, "power")
    assert "1024" in capsys.readouterr().out


def test_run_operation_log(calc, capsys):
    with patch("builtins.input", side_effect=["100", "10"]):
        run_operation(calc, "log")
    captured = capsys.readouterr().out
    assert "Result" in captured


# ---------------------------------------------------------------------------
# run_operation — single-argument operations
# ---------------------------------------------------------------------------

def test_run_operation_factorial(calc, capsys):
    with patch("builtins.input", return_value="5"):
        run_operation(calc, "factorial")
    assert "120" in capsys.readouterr().out


def test_run_operation_factorial_negative_shows_error(calc, capsys):
    with patch("builtins.input", return_value="-1"):
        run_operation(calc, "factorial")
    assert "Error" in capsys.readouterr().out


def test_run_operation_square(calc, capsys):
    with patch("builtins.input", return_value="4"):
        run_operation(calc, "square")
    assert "16" in capsys.readouterr().out


def test_run_operation_cube(calc, capsys):
    with patch("builtins.input", return_value="3"):
        run_operation(calc, "cube")
    assert "27" in capsys.readouterr().out


def test_run_operation_square_root(calc, capsys):
    with patch("builtins.input", return_value="9"):
        run_operation(calc, "square_root")
    assert "3" in capsys.readouterr().out


def test_run_operation_square_root_negative_shows_error(calc, capsys):
    with patch("builtins.input", return_value="-4"):
        run_operation(calc, "square_root")
    assert "Error" in capsys.readouterr().out


def test_run_operation_cube_root(calc, capsys):
    with patch("builtins.input", return_value="27"):
        run_operation(calc, "cube_root")
    captured = capsys.readouterr().out
    assert "Result" in captured


def test_run_operation_ln(calc, capsys):
    with patch("builtins.input", return_value="1"):
        run_operation(calc, "ln")
    assert "0" in capsys.readouterr().out


def test_run_operation_unknown(calc, capsys):
    run_operation(calc, "unknown_op")
    assert "Unknown operation" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# main — full interactive loop
# ---------------------------------------------------------------------------

def test_main_quit_immediately(capsys):
    """User selects 'q' on first prompt — loop exits cleanly."""
    with patch("builtins.input", return_value="q"):
        main()
    assert "Goodbye" in capsys.readouterr().out


def test_main_invalid_choice_then_quit(capsys):
    """Invalid menu choice shows error; 'q' exits cleanly."""
    with patch("builtins.input", side_effect=["99", "q"]):
        main()
    captured = capsys.readouterr().out
    assert "Invalid choice" in captured
    assert "Goodbye" in captured


def test_main_add_then_quit(capsys):
    """User picks add, enters two numbers, sees result, then quits."""
    with patch("builtins.input", side_effect=["1", "3", "4", "q"]):
        main()
    captured = capsys.readouterr().out
    assert "7" in captured
    assert "Goodbye" in captured


def test_main_two_operations_then_quit(capsys):
    """User performs two operations in sequence before quitting."""
    # op 1 = add (inputs: 2 and 3)
    # op 2 = square (input: 4)
    with patch("builtins.input", side_effect=["1", "2", "3", "6", "4", "q"]):
        main()
    captured = capsys.readouterr().out
    assert "5" in captured   # 2 + 3
    assert "16" in captured  # 4^2
    assert "Goodbye" in captured


def test_main_error_then_continue(capsys):
    """Division-by-zero error is reported but the loop continues."""
    # op: divide 10 by 0 → error, then quit
    with patch("builtins.input", side_effect=["4", "10", "0", "q"]):
        main()
    captured = capsys.readouterr().out
    assert "Error" in captured
    assert "Goodbye" in captured
