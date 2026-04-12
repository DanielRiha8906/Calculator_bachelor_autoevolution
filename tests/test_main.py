"""Tests for the interactive CLI in src/__main__.py."""

import pytest
from unittest.mock import patch
from src.__main__ import parse_number, run_operation, main, MENU_MAP
from src.calculator import Calculator


# --- parse_number ---

def test_parse_number_valid_integer(capsys):
    with patch("builtins.input", return_value="42"):
        result = parse_number("prompt: ")
    assert result == 42.0


def test_parse_number_valid_float(capsys):
    with patch("builtins.input", return_value="3.14"):
        result = parse_number("prompt: ")
    assert result == pytest.approx(3.14)


def test_parse_number_negative(capsys):
    with patch("builtins.input", return_value="-7"):
        result = parse_number("prompt: ")
    assert result == -7.0


def test_parse_number_retries_on_invalid(capsys):
    # First input is invalid, second is valid
    with patch("builtins.input", side_effect=["abc", "5"]):
        result = parse_number("prompt: ")
    captured = capsys.readouterr()
    assert "Invalid number" in captured.out
    assert result == 5.0


# --- MENU_MAP completeness ---

def test_menu_map_covers_all_12_operations():
    expected_ops = {
        "add", "subtract", "multiply", "divide", "factorial",
        "square", "cube", "square_root", "cube_root", "power", "log", "ln",
    }
    assert set(MENU_MAP.values()) == expected_ops


def test_menu_map_keys_are_1_to_12():
    assert set(MENU_MAP.keys()) == {str(i) for i in range(1, 13)}


# --- run_operation ---

def test_run_operation_add(capsys):
    calc = Calculator()
    with patch("builtins.input", side_effect=["3", "4"]):
        run_operation(calc, "add")
    out = capsys.readouterr().out
    assert "7" in out


def test_run_operation_subtract(capsys):
    calc = Calculator()
    with patch("builtins.input", side_effect=["10", "3"]):
        run_operation(calc, "subtract")
    out = capsys.readouterr().out
    assert "7" in out


def test_run_operation_multiply(capsys):
    calc = Calculator()
    with patch("builtins.input", side_effect=["6", "7"]):
        run_operation(calc, "multiply")
    out = capsys.readouterr().out
    assert "42" in out


def test_run_operation_divide(capsys):
    calc = Calculator()
    with patch("builtins.input", side_effect=["10", "2"]):
        run_operation(calc, "divide")
    out = capsys.readouterr().out
    assert "5" in out


def test_run_operation_divide_by_zero_prints_error(capsys):
    calc = Calculator()
    with patch("builtins.input", side_effect=["10", "0"]):
        run_operation(calc, "divide")
    out = capsys.readouterr().out
    assert "Error" in out


def test_run_operation_factorial(capsys):
    calc = Calculator()
    with patch("builtins.input", return_value="5"):
        run_operation(calc, "factorial")
    out = capsys.readouterr().out
    assert "120" in out


def test_run_operation_factorial_negative_prints_error(capsys):
    calc = Calculator()
    with patch("builtins.input", return_value="-1"):
        run_operation(calc, "factorial")
    out = capsys.readouterr().out
    assert "Error" in out


def test_run_operation_square(capsys):
    calc = Calculator()
    with patch("builtins.input", return_value="4"):
        run_operation(calc, "square")
    out = capsys.readouterr().out
    assert "16" in out


def test_run_operation_cube(capsys):
    calc = Calculator()
    with patch("builtins.input", return_value="3"):
        run_operation(calc, "cube")
    out = capsys.readouterr().out
    assert "27" in out


def test_run_operation_square_root(capsys):
    calc = Calculator()
    with patch("builtins.input", return_value="9"):
        run_operation(calc, "square_root")
    out = capsys.readouterr().out
    assert "3" in out


def test_run_operation_square_root_negative_prints_error(capsys):
    calc = Calculator()
    with patch("builtins.input", return_value="-4"):
        run_operation(calc, "square_root")
    out = capsys.readouterr().out
    assert "Error" in out


def test_run_operation_cube_root(capsys):
    calc = Calculator()
    with patch("builtins.input", return_value="8"):
        run_operation(calc, "cube_root")
    out = capsys.readouterr().out
    assert "2" in out


def test_run_operation_power(capsys):
    calc = Calculator()
    with patch("builtins.input", side_effect=["2", "10"]):
        run_operation(calc, "power")
    out = capsys.readouterr().out
    assert "1024" in out


def test_run_operation_log(capsys):
    calc = Calculator()
    with patch("builtins.input", return_value="100"):
        run_operation(calc, "log")
    out = capsys.readouterr().out
    assert "2" in out


def test_run_operation_log_non_positive_prints_error(capsys):
    calc = Calculator()
    with patch("builtins.input", return_value="0"):
        run_operation(calc, "log")
    out = capsys.readouterr().out
    assert "Error" in out


def test_run_operation_ln(capsys):
    calc = Calculator()
    with patch("builtins.input", return_value="1"):
        run_operation(calc, "ln")
    out = capsys.readouterr().out
    assert "0" in out


def test_run_operation_ln_non_positive_prints_error(capsys):
    calc = Calculator()
    with patch("builtins.input", return_value="-1"):
        run_operation(calc, "ln")
    out = capsys.readouterr().out
    assert "Error" in out


# --- main loop ---

def test_main_quit_immediately(capsys):
    with patch("builtins.input", return_value="q"):
        main()
    out = capsys.readouterr().out
    assert "Goodbye" in out


def test_main_unknown_choice_then_quit(capsys):
    with patch("builtins.input", side_effect=["99", "q"]):
        main()
    out = capsys.readouterr().out
    assert "Unknown choice" in out


def test_main_perform_add_then_quit(capsys):
    # Choose add (1), enter 3 and 4, then quit
    with patch("builtins.input", side_effect=["1", "3", "4", "q"]):
        main()
    out = capsys.readouterr().out
    assert "7" in out
