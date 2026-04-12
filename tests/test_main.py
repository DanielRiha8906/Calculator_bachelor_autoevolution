"""Tests for the interactive CLI loop and CLI mode in src/__main__.py."""
import math
import sys
from unittest.mock import patch
import pytest

import src.__main__ as _main_mod
from src.__main__ import (
    show_menu,
    parse_number,
    parse_int,
    run_operation,
    main,
    cli_mode,
    clear_history,
    append_to_history,
    show_history,
    OPERATIONS,
    TooManyAttemptsError,
    MAX_ATTEMPTS,
    HISTORY_FILE,
)
from src.calculator import Calculator


@pytest.fixture
def calc():
    return Calculator()


@pytest.fixture(autouse=True)
def isolate_history(tmp_path, monkeypatch):
    """Redirect all history file operations to a temp directory.

    This prevents tests from writing to or reading from a real ``history.txt``
    in the working directory, keeping test runs clean and independent.
    """
    monkeypatch.setattr(_main_mod, "HISTORY_FILE", str(tmp_path / "history.txt"))


# ---------------------------------------------------------------------------
# show_menu
# ---------------------------------------------------------------------------

def test_show_menu_prints_all_operations(capsys):
    show_menu()
    captured = capsys.readouterr().out
    for key, name in OPERATIONS.items():
        assert name in captured
    assert "q" in captured


def test_show_menu_includes_history_option(capsys):
    show_menu()
    assert "h" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# clear_history / append_to_history / show_history
# ---------------------------------------------------------------------------

def test_clear_history_creates_empty_file(tmp_path):
    filepath = str(tmp_path / "h.txt")
    clear_history(filepath)
    assert open(filepath).read() == ""


def test_clear_history_overwrites_existing_content(tmp_path):
    filepath = str(tmp_path / "h.txt")
    open(filepath, "w").write("old data\n")
    clear_history(filepath)
    assert open(filepath).read() == ""


def test_append_to_history_adds_entry(tmp_path):
    filepath = str(tmp_path / "h.txt")
    clear_history(filepath)
    append_to_history("add(1.0, 2.0) = 3.0", filepath)
    lines = open(filepath).read().splitlines()
    assert lines == ["add(1.0, 2.0) = 3.0"]


def test_append_to_history_multiple_entries(tmp_path):
    filepath = str(tmp_path / "h.txt")
    clear_history(filepath)
    append_to_history("add(1.0, 2.0) = 3.0", filepath)
    append_to_history("square(4.0) = 16.0", filepath)
    lines = open(filepath).read().splitlines()
    assert lines == ["add(1.0, 2.0) = 3.0", "square(4.0) = 16.0"]


def test_show_history_empty(tmp_path, capsys):
    filepath = str(tmp_path / "h.txt")
    clear_history(filepath)
    show_history(filepath)
    assert "No history" in capsys.readouterr().out


def test_show_history_no_file(tmp_path, capsys):
    """show_history handles a missing file gracefully."""
    filepath = str(tmp_path / "does_not_exist.txt")
    show_history(filepath)
    assert "No history" in capsys.readouterr().out


def test_show_history_with_entries(tmp_path, capsys):
    filepath = str(tmp_path / "h.txt")
    clear_history(filepath)
    append_to_history("add(1.0, 2.0) = 3.0", filepath)
    append_to_history("factorial(5) = 120", filepath)
    show_history(filepath)
    captured = capsys.readouterr().out
    assert "add(1.0, 2.0) = 3.0" in captured
    assert "factorial(5) = 120" in captured


# ---------------------------------------------------------------------------
# run_operation — return value (history entry)
# ---------------------------------------------------------------------------

def test_run_operation_add_returns_history_entry(calc):
    with patch("builtins.input", side_effect=["3", "4"]):
        entry = run_operation(calc, "add")
    assert entry == "add(3.0, 4.0) = 7.0"


def test_run_operation_returns_none_on_error(calc):
    """ValueError from Calculator (e.g. divide by zero) returns None."""
    with patch("builtins.input", side_effect=["10", "0"]):
        entry = run_operation(calc, "divide")
    assert entry is None


def test_run_operation_returns_none_for_unknown_op(calc):
    entry = run_operation(calc, "nonexistent")
    assert entry is None


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


def test_parse_number_raises_after_max_attempts():
    """TooManyAttemptsError is raised after MAX_ATTEMPTS consecutive invalid inputs."""
    bad_inputs = ["abc"] * MAX_ATTEMPTS
    with patch("builtins.input", side_effect=bad_inputs):
        with pytest.raises(TooManyAttemptsError):
            parse_number("Enter: ")


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


def test_parse_int_raises_after_max_attempts():
    """TooManyAttemptsError is raised after MAX_ATTEMPTS consecutive invalid inputs."""
    bad_inputs = ["abc"] * MAX_ATTEMPTS
    with patch("builtins.input", side_effect=bad_inputs):
        with pytest.raises(TooManyAttemptsError):
            parse_int("Enter: ")


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
# Pass args=[] explicitly so main() uses interactive mode regardless of
# what pytest puts in sys.argv.
# ---------------------------------------------------------------------------

def test_main_quit_immediately(capsys):
    """User selects 'q' on first prompt — loop exits cleanly."""
    with patch("builtins.input", return_value="q"):
        main([])
    assert "Goodbye" in capsys.readouterr().out


def test_main_invalid_choice_then_quit(capsys):
    """Invalid menu choice shows error; 'q' exits cleanly."""
    with patch("builtins.input", side_effect=["99", "q"]):
        main([])
    captured = capsys.readouterr().out
    assert "Invalid choice" in captured
    assert "Goodbye" in captured


def test_main_add_then_quit(capsys):
    """User picks add, enters two numbers, sees result, then quits."""
    with patch("builtins.input", side_effect=["1", "3", "4", "q"]):
        main([])
    captured = capsys.readouterr().out
    assert "7" in captured
    assert "Goodbye" in captured


def test_main_two_operations_then_quit(capsys):
    """User performs two operations in sequence before quitting."""
    # op 1 = add (inputs: 2 and 3)
    # op 2 = square (input: 4)
    with patch("builtins.input", side_effect=["1", "2", "3", "6", "4", "q"]):
        main([])
    captured = capsys.readouterr().out
    assert "5" in captured   # 2 + 3
    assert "16" in captured  # 4^2
    assert "Goodbye" in captured


def test_main_error_then_continue(capsys):
    """Division-by-zero error is reported but the loop continues."""
    # op: divide 10 by 0 → error, then quit
    with patch("builtins.input", side_effect=["4", "10", "0", "q"]):
        main([])
    captured = capsys.readouterr().out
    assert "Error" in captured
    assert "Goodbye" in captured


def test_main_too_many_invalid_choices_ends_session(capsys):
    """Session ends after MAX_ATTEMPTS consecutive invalid menu choices."""
    bad_choices = ["99"] * MAX_ATTEMPTS
    with patch("builtins.input", side_effect=bad_choices):
        main([])
    captured = capsys.readouterr().out
    assert "Too many invalid choices" in captured
    assert "Goodbye" not in captured


def test_main_too_many_invalid_operands_ends_session(capsys):
    """Session ends when operand input exceeds the retry limit."""
    # Select add ("1"), then provide MAX_ATTEMPTS invalid numbers
    bad_operands = ["abc"] * MAX_ATTEMPTS
    with patch("builtins.input", side_effect=["1"] + bad_operands):
        main([])
    captured = capsys.readouterr().out
    assert "Too many" in captured
    assert "Goodbye" not in captured


def test_main_show_history_option(capsys):
    """Pressing 'h' displays the (empty) history without exiting the loop."""
    with patch("builtins.input", side_effect=["h", "q"]):
        main([])
    captured = capsys.readouterr().out
    assert "No history" in captured
    assert "Goodbye" in captured


def test_main_history_recorded_after_operation(tmp_path, monkeypatch):
    """A successful operation is persisted to the history file."""
    hist_path = str(tmp_path / "history.txt")
    monkeypatch.setattr(_main_mod, "HISTORY_FILE", hist_path)
    with patch("builtins.input", side_effect=["1", "3", "4", "q"]):
        main([])
    lines = open(hist_path).read().splitlines()
    assert len(lines) == 1
    assert "add" in lines[0]
    assert "7" in lines[0]


def test_main_error_operation_not_recorded(tmp_path, monkeypatch):
    """A failed operation (e.g. divide by zero) is not written to history."""
    hist_path = str(tmp_path / "history.txt")
    monkeypatch.setattr(_main_mod, "HISTORY_FILE", hist_path)
    with patch("builtins.input", side_effect=["4", "10", "0", "q"]):
        main([])
    lines = open(hist_path).read().splitlines()
    assert lines == []


def test_main_history_cleared_on_new_session(tmp_path, monkeypatch):
    """Starting a new session wipes the history from the previous session."""
    hist_path = str(tmp_path / "history.txt")
    monkeypatch.setattr(_main_mod, "HISTORY_FILE", hist_path)
    # First session: perform add
    with patch("builtins.input", side_effect=["1", "2", "3", "q"]):
        main([])
    lines_after_first = open(hist_path).read().splitlines()
    assert len(lines_after_first) == 1
    # Second session: quit immediately — history should be cleared
    with patch("builtins.input", side_effect=["q"]):
        main([])
    lines_after_second = open(hist_path).read().splitlines()
    assert lines_after_second == []


def test_main_show_history_with_previous_operations(capsys):
    """After performing an operation, 'h' shows it in the history display."""
    # add 3+4=7, then show history, then quit
    with patch("builtins.input", side_effect=["1", "3", "4", "h", "q"]):
        main([])
    captured = capsys.readouterr().out
    assert "add" in captured
    assert "7" in captured


# ---------------------------------------------------------------------------
# cli_mode — non-interactive single-operation execution
# ---------------------------------------------------------------------------

def test_cli_mode_add(capsys):
    rc = cli_mode(["add", "3", "4"])
    assert rc == 0
    assert "7" in capsys.readouterr().out


def test_cli_mode_subtract(capsys):
    rc = cli_mode(["subtract", "10", "3"])
    assert rc == 0
    assert "7" in capsys.readouterr().out


def test_cli_mode_multiply(capsys):
    rc = cli_mode(["multiply", "6", "7"])
    assert rc == 0
    assert "42" in capsys.readouterr().out


def test_cli_mode_divide(capsys):
    rc = cli_mode(["divide", "10", "2"])
    assert rc == 0
    assert "5" in capsys.readouterr().out


def test_cli_mode_power(capsys):
    rc = cli_mode(["power", "2", "10"])
    assert rc == 0
    assert "1024" in capsys.readouterr().out


def test_cli_mode_log(capsys):
    rc = cli_mode(["log", "100", "10"])
    assert rc == 0
    out = capsys.readouterr().out
    assert math.isclose(float(out.strip()), 2.0)


def test_cli_mode_factorial(capsys):
    rc = cli_mode(["factorial", "5"])
    assert rc == 0
    assert "120" in capsys.readouterr().out


def test_cli_mode_square(capsys):
    rc = cli_mode(["square", "4"])
    assert rc == 0
    assert "16" in capsys.readouterr().out


def test_cli_mode_cube(capsys):
    rc = cli_mode(["cube", "3"])
    assert rc == 0
    assert "27" in capsys.readouterr().out


def test_cli_mode_square_root(capsys):
    rc = cli_mode(["square_root", "9"])
    assert rc == 0
    out = capsys.readouterr().out
    assert math.isclose(float(out.strip()), 3.0)


def test_cli_mode_cube_root(capsys):
    rc = cli_mode(["cube_root", "27"])
    assert rc == 0
    out = capsys.readouterr().out
    assert math.isclose(float(out.strip()), 3.0)


def test_cli_mode_ln(capsys):
    import math as _math
    rc = cli_mode(["ln", str(_math.e)])
    assert rc == 0
    out = capsys.readouterr().out
    assert math.isclose(float(out.strip()), 1.0)


def test_cli_mode_divide_by_zero_returns_error(capsys):
    rc = cli_mode(["divide", "10", "0"])
    assert rc == 1
    assert "Error" in capsys.readouterr().err


def test_cli_mode_factorial_negative_returns_error(capsys):
    rc = cli_mode(["factorial", "-1"])
    assert rc == 1
    assert "Error" in capsys.readouterr().err


def test_cli_mode_square_root_negative_returns_error(capsys):
    rc = cli_mode(["square_root", "-4"])
    assert rc == 1
    assert "Error" in capsys.readouterr().err


def test_cli_mode_wrong_arg_count_two_arg_op(capsys):
    """Passing only one value to a two-argument operation returns error."""
    rc = cli_mode(["add", "3"])
    assert rc == 1
    assert "Error" in capsys.readouterr().err


def test_cli_mode_wrong_arg_count_one_arg_op(capsys):
    """Passing two values to a one-argument operation returns error."""
    rc = cli_mode(["square", "4", "5"])
    assert rc == 1
    assert "Error" in capsys.readouterr().err


def test_cli_mode_unknown_operation_exits():
    """argparse raises SystemExit for an unrecognised operation name."""
    with pytest.raises(SystemExit):
        cli_mode(["unknown_op", "3"])


def test_cli_mode_non_numeric_two_arg_returns_error(capsys):
    """Non-numeric value for a two-argument op prints a clear error and returns 1."""
    rc = cli_mode(["add", "abc", "3"])
    assert rc == 1
    captured = capsys.readouterr()
    assert "Error" in captured.err
    assert "abc" in captured.err


def test_cli_mode_non_numeric_one_arg_returns_error(capsys):
    """Non-numeric value for a one-argument op prints a clear error and returns 1."""
    rc = cli_mode(["square", "xyz"])
    assert rc == 1
    captured = capsys.readouterr()
    assert "Error" in captured.err
    assert "xyz" in captured.err


def test_cli_mode_non_integer_factorial_returns_error(capsys):
    """Non-integer value for factorial prints a clear error and returns 1."""
    rc = cli_mode(["factorial", "abc"])
    assert rc == 1
    captured = capsys.readouterr()
    assert "Error" in captured.err
    assert "abc" in captured.err


def test_main_dispatches_to_cli_mode(capsys):
    """main() with CLI args calls cli_mode and exits with code 0."""
    with pytest.raises(SystemExit) as exc_info:
        main(["add", "2", "3"])
    assert exc_info.value.code == 0
    assert "5" in capsys.readouterr().out
