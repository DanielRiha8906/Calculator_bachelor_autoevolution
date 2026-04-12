"""Tests for the interactive CLI in src/__main__.py."""

import pytest
from unittest.mock import patch
from src.__main__ import parse_number, run_operation, main, MENU_MAP, cli_main, _format_result, _show_history, MAX_INPUT_ATTEMPTS
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


def test_parse_number_exhausts_retries_raises_value_error(capsys):
    # All MAX_INPUT_ATTEMPTS inputs are invalid — should raise ValueError
    bad_inputs = ["x"] * MAX_INPUT_ATTEMPTS
    with patch("builtins.input", side_effect=bad_inputs):
        with pytest.raises(ValueError, match="No valid number entered"):
            parse_number("prompt: ")
    captured = capsys.readouterr()
    assert "Invalid number" in captured.out
    assert "No more attempts remaining" in captured.out


def test_parse_number_remaining_count_shown(capsys):
    # With max_attempts=3: first failure should show "2 attempt(s) remaining"
    with patch("builtins.input", side_effect=["bad", "5"]):
        result = parse_number("prompt: ", max_attempts=3)
    captured = capsys.readouterr()
    assert "2 attempt(s) remaining" in captured.out
    assert result == 5.0


def test_run_operation_too_many_invalid_inputs_prints_error(capsys):
    # Provide MAX_INPUT_ATTEMPTS invalid inputs — run_operation should print Error
    calc = Calculator()
    bad_inputs = ["x"] * MAX_INPUT_ATTEMPTS
    with patch("builtins.input", side_effect=bad_inputs):
        run_operation(calc, "add")
    out = capsys.readouterr().out
    assert "Error" in out


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
    with patch("sys.argv", ["prog"]), patch("builtins.input", return_value="q"):
        main()
    out = capsys.readouterr().out
    assert "Goodbye" in out


def test_main_unknown_choice_then_quit(capsys):
    with patch("sys.argv", ["prog"]), patch("builtins.input", side_effect=["99", "q"]):
        main()
    out = capsys.readouterr().out
    assert "Unknown choice" in out


def test_main_perform_add_then_quit(capsys):
    # Choose add (1), enter 3 and 4, then quit
    with patch("sys.argv", ["prog"]), patch("builtins.input", side_effect=["1", "3", "4", "q"]):
        main()
    out = capsys.readouterr().out
    assert "7" in out


# --- _format_result ---

def test_format_result_whole_float_returns_int_string():
    assert _format_result(7.0) == "7"


def test_format_result_fractional_float_returns_float_string():
    assert _format_result(3.5) == "3.5"


def test_format_result_int_returns_int_string():
    assert _format_result(120) == "120"


# --- cli_main ---

def test_cli_main_add(capsys):
    rc = cli_main(["add", "3", "4"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "7" in out


def test_cli_main_subtract(capsys):
    rc = cli_main(["subtract", "10", "3"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "7" in out


def test_cli_main_multiply(capsys):
    rc = cli_main(["multiply", "6", "7"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "42" in out


def test_cli_main_divide(capsys):
    rc = cli_main(["divide", "10", "2"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "5" in out


def test_cli_main_power(capsys):
    rc = cli_main(["power", "2", "10"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "1024" in out


def test_cli_main_factorial(capsys):
    rc = cli_main(["factorial", "5"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "120" in out


def test_cli_main_square(capsys):
    rc = cli_main(["square", "4"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "16" in out


def test_cli_main_cube(capsys):
    rc = cli_main(["cube", "3"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "27" in out


def test_cli_main_square_root(capsys):
    rc = cli_main(["square_root", "9"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "3" in out


def test_cli_main_cube_root(capsys):
    rc = cli_main(["cube_root", "8"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "2" in out


def test_cli_main_log(capsys):
    rc = cli_main(["log", "100"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "2" in out


def test_cli_main_ln(capsys):
    rc = cli_main(["ln", "1"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "0" in out


def test_cli_main_no_args_prints_usage(capsys):
    rc = cli_main([])
    out = capsys.readouterr().out
    assert rc == 1
    assert "Usage" in out


def test_cli_main_unknown_op_prints_error(capsys):
    rc = cli_main(["modulo", "10", "3"])
    out = capsys.readouterr().out
    assert rc == 1
    assert "Error" in out


def test_cli_main_binary_op_wrong_arg_count(capsys):
    rc = cli_main(["add", "3"])
    out = capsys.readouterr().out
    assert rc == 1
    assert "Error" in out


def test_cli_main_unary_op_wrong_arg_count(capsys):
    rc = cli_main(["square", "4", "5"])
    out = capsys.readouterr().out
    assert rc == 1
    assert "Error" in out


def test_cli_main_divide_by_zero_error(capsys):
    rc = cli_main(["divide", "10", "0"])
    out = capsys.readouterr().out
    assert rc == 1
    assert "Error" in out


def test_cli_main_factorial_negative_error(capsys):
    rc = cli_main(["factorial", "-1"])
    out = capsys.readouterr().out
    assert rc == 1
    assert "Error" in out


def test_cli_main_factorial_non_whole_error(capsys):
    rc = cli_main(["factorial", "3.5"])
    out = capsys.readouterr().out
    assert rc == 1
    assert "Error" in out


def test_cli_main_invalid_number_error(capsys):
    rc = cli_main(["add", "abc", "3"])
    out = capsys.readouterr().out
    assert rc == 1
    assert "Error" in out


def test_cli_main_square_root_negative_error(capsys):
    rc = cli_main(["square_root", "-4"])
    out = capsys.readouterr().out
    assert rc == 1
    assert "Error" in out


# --- main dispatches to cli_main when sys.argv has args ---

def test_main_cli_dispatch(capsys):
    with patch("sys.argv", ["prog", "add", "2", "3"]):
        with pytest.raises(SystemExit) as exc_info:
            main()
    assert exc_info.value.code == 0
    out = capsys.readouterr().out
    assert "5" in out


def test_main_cli_dispatch_error_exits_1(capsys):
    with patch("sys.argv", ["prog", "divide", "1", "0"]):
        with pytest.raises(SystemExit) as exc_info:
            main()
    assert exc_info.value.code == 1


# --- history ---

def test_run_operation_records_binary_op_in_history(capsys):
    calc = Calculator()
    with patch("builtins.input", side_effect=["3", "4"]):
        run_operation(calc, "add")
    assert len(calc.history) == 1
    entry = calc.history[0]
    assert entry["op"] == "add"
    assert entry["operands"] == (3.0, 4.0)
    assert entry["result"] == 7.0


def test_run_operation_records_unary_op_in_history(capsys):
    calc = Calculator()
    with patch("builtins.input", return_value="9"):
        run_operation(calc, "square_root")
    assert len(calc.history) == 1
    entry = calc.history[0]
    assert entry["op"] == "square_root"
    assert entry["operands"] == (9.0,)
    assert entry["result"] == pytest.approx(3.0)


def test_run_operation_error_not_recorded_in_history(capsys):
    calc = Calculator()
    with patch("builtins.input", side_effect=["10", "0"]):
        run_operation(calc, "divide")
    assert calc.history == []


def test_run_operation_multiple_ops_accumulate_in_history(capsys):
    calc = Calculator()
    with patch("builtins.input", side_effect=["2", "3"]):
        run_operation(calc, "add")
    with patch("builtins.input", return_value="4"):
        run_operation(calc, "square")
    assert len(calc.history) == 2
    assert calc.history[0]["op"] == "add"
    assert calc.history[1]["op"] == "square"


def test_show_history_empty(capsys):
    calc = Calculator()
    _show_history(calc)
    out = capsys.readouterr().out
    assert "No history yet" in out


def test_show_history_with_entries(capsys):
    calc = Calculator()
    calc.history.append({"op": "add", "operands": (3.0, 4.0), "result": 7.0})
    calc.history.append({"op": "square", "operands": (5.0,), "result": 25.0})
    _show_history(calc)
    out = capsys.readouterr().out
    assert "add(3, 4) = 7" in out
    assert "square(5) = 25" in out


def test_main_history_choice_shows_empty(capsys):
    with patch("sys.argv", ["prog"]), patch("builtins.input", side_effect=["h", "q"]):
        main()
    out = capsys.readouterr().out
    assert "No history yet" in out


def test_main_history_shows_after_operation(capsys):
    with patch("sys.argv", ["prog"]), patch("builtins.input", side_effect=["1", "3", "4", "h", "q"]):
        main()
    out = capsys.readouterr().out
    assert "add(3, 4) = 7" in out
