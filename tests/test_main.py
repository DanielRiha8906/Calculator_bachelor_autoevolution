import math
import pytest
from unittest.mock import patch

import src.history as history_module
from src.__main__ import (
    display_menu, get_number, get_integer, perform_operation, main,
    TooManyAttemptsError, MAX_INPUT_ATTEMPTS,
)
from src.controller import CalculatorController


@pytest.fixture(autouse=True)
def tmp_history_file(tmp_path, monkeypatch):
    """Redirect HISTORY_FILE to a temporary path so tests never write to the project root."""
    tmp_file = tmp_path / "history.txt"
    monkeypatch.setattr(history_module, "HISTORY_FILE", tmp_file)
    return tmp_file


@pytest.fixture
def calc():
    return CalculatorController()


# --- display_menu ---

def test_display_menu_contains_all_operations(capsys):
    display_menu()
    captured = capsys.readouterr()
    for label in [
        "Add", "Subtract", "Multiply", "Divide", "Factorial",
        "Square", "Cube", "Square Root", "Cube Root", "Power",
        "Log", "Natural Log", "History", "Exit",
    ]:
        assert label in captured.out


# --- get_number ---

def test_get_number_integer_input():
    with patch("builtins.input", return_value="42"):
        assert get_number("prompt: ") == 42.0


def test_get_number_float_input():
    with patch("builtins.input", return_value="3.14"):
        assert get_number("prompt: ") == pytest.approx(3.14)


def test_get_number_negative_input():
    with patch("builtins.input", return_value="-7"):
        assert get_number("prompt: ") == -7.0


def test_get_number_retries_on_invalid(capsys):
    with patch("builtins.input", side_effect=["abc", "5"]):
        result = get_number("prompt: ")
    assert result == 5.0
    assert "Invalid input" in capsys.readouterr().out


def test_get_number_raises_after_max_attempts():
    invalid_inputs = ["abc"] * MAX_INPUT_ATTEMPTS
    with patch("builtins.input", side_effect=invalid_inputs):
        with pytest.raises(TooManyAttemptsError):
            get_number("prompt: ")


def test_get_number_succeeds_on_last_attempt():
    inputs = ["bad"] * (MAX_INPUT_ATTEMPTS - 1) + ["42"]
    with patch("builtins.input", side_effect=inputs):
        assert get_number("prompt: ") == 42.0


def test_get_number_remaining_attempts_shown(capsys):
    with patch("builtins.input", side_effect=["abc", "5"]):
        get_number("prompt: ", max_attempts=3)
    out = capsys.readouterr().out
    assert "2 attempt(s) remaining" in out


# --- get_integer ---

def test_get_integer_valid():
    with patch("builtins.input", return_value="7"):
        assert get_integer("prompt: ") == 7


def test_get_integer_retries_on_float(capsys):
    with patch("builtins.input", side_effect=["2.5", "4"]):
        result = get_integer("prompt: ")
    assert result == 4
    assert "Invalid input" in capsys.readouterr().out


def test_get_integer_retries_on_text(capsys):
    with patch("builtins.input", side_effect=["hello", "3"]):
        result = get_integer("prompt: ")
    assert result == 3
    assert "Invalid input" in capsys.readouterr().out


def test_get_integer_raises_after_max_attempts():
    invalid_inputs = ["abc"] * MAX_INPUT_ATTEMPTS
    with patch("builtins.input", side_effect=invalid_inputs):
        with pytest.raises(TooManyAttemptsError):
            get_integer("prompt: ")


def test_get_integer_succeeds_on_last_attempt():
    inputs = ["bad"] * (MAX_INPUT_ATTEMPTS - 1) + ["7"]
    with patch("builtins.input", side_effect=inputs):
        assert get_integer("prompt: ") == 7


def test_get_integer_remaining_attempts_shown(capsys):
    with patch("builtins.input", side_effect=["abc", "5"]):
        get_integer("prompt: ", max_attempts=3)
    out = capsys.readouterr().out
    assert "2 attempt(s) remaining" in out


# --- perform_operation ---

def test_perform_add(calc):
    with patch("builtins.input", side_effect=["3", "4"]):
        assert perform_operation(calc, "1") == "7.0"


def test_perform_subtract(calc):
    with patch("builtins.input", side_effect=["10", "3"]):
        assert perform_operation(calc, "2") == "7.0"


def test_perform_multiply(calc):
    with patch("builtins.input", side_effect=["3", "4"]):
        assert perform_operation(calc, "3") == "12.0"


def test_perform_divide(calc):
    with patch("builtins.input", side_effect=["10", "2"]):
        assert perform_operation(calc, "4") == "5.0"


def test_perform_divide_by_zero_raises(calc):
    with patch("builtins.input", side_effect=["10", "0"]):
        with pytest.raises(ZeroDivisionError):
            perform_operation(calc, "4")


def test_perform_factorial(calc):
    with patch("builtins.input", return_value="5"):
        assert perform_operation(calc, "5") == "120"


def test_perform_factorial_negative_raises(calc):
    with patch("builtins.input", return_value="-1"):
        with pytest.raises(ValueError):
            perform_operation(calc, "5")


def test_perform_square(calc):
    with patch("builtins.input", return_value="4"):
        assert perform_operation(calc, "6") == "16.0"


def test_perform_cube(calc):
    with patch("builtins.input", return_value="3"):
        assert perform_operation(calc, "7") == "27.0"


def test_perform_square_root(calc):
    with patch("builtins.input", return_value="9"):
        assert perform_operation(calc, "8") == "3.0"


def test_perform_square_root_negative_raises(calc):
    with patch("builtins.input", return_value="-4"):
        with pytest.raises(ValueError):
            perform_operation(calc, "8")


def test_perform_cube_root(calc):
    with patch("builtins.input", return_value="27"):
        result = perform_operation(calc, "9")
        assert float(result) == pytest.approx(3.0)


def test_perform_power(calc):
    with patch("builtins.input", side_effect=["2", "10"]):
        assert perform_operation(calc, "10") == "1024.0"


def test_perform_log_default_base(calc):
    with patch("builtins.input", side_effect=["100", ""]):
        result = perform_operation(calc, "11")
        assert float(result) == pytest.approx(2.0)


def test_perform_log_custom_base(calc):
    with patch("builtins.input", side_effect=["8", "2"]):
        result = perform_operation(calc, "11")
        assert float(result) == pytest.approx(3.0)


def test_perform_log_invalid_base_defaults_to_10(calc, capsys):
    with patch("builtins.input", side_effect=["100", "abc"]):
        result = perform_operation(calc, "11")
    assert float(result) == pytest.approx(2.0)
    assert "Invalid base" in capsys.readouterr().out


def test_perform_ln(calc):
    with patch("builtins.input", return_value=str(math.e)):
        result = perform_operation(calc, "12")
        assert float(result) == pytest.approx(1.0)


def test_perform_unknown_operation_returns_none(calc):
    assert perform_operation(calc, "99") is None


def test_perform_exit_choice_returns_none(calc):
    # "0" is the exit sentinel handled by main(); perform_operation returns None for it
    assert perform_operation(calc, "0") is None


# --- main ---

def test_main_shows_welcome_message(capsys):
    with patch("builtins.input", return_value="0"):
        main()
    assert "Welcome" in capsys.readouterr().out


def test_main_exits_on_zero(capsys):
    with patch("builtins.input", return_value="0"):
        main()
    assert "Goodbye!" in capsys.readouterr().out


def test_main_add_then_exit(capsys):
    with patch("builtins.input", side_effect=["1", "3", "4", "0"]):
        main()
    captured = capsys.readouterr()
    assert "Result: 7.0" in captured.out
    assert "Goodbye!" in captured.out


def test_main_unknown_choice_then_exit(capsys):
    with patch("builtins.input", side_effect=["99", "0"]):
        main()
    captured = capsys.readouterr()
    assert "Unknown operation" in captured.out
    assert "Goodbye!" in captured.out


def test_main_error_caught_loop_continues(capsys):
    # Divide by zero should print error then allow exit on next iteration
    with patch("builtins.input", side_effect=["4", "10", "0", "0"]):
        main()
    captured = capsys.readouterr()
    assert "Error:" in captured.out
    assert "Goodbye!" in captured.out


def test_main_multiple_operations(capsys):
    # Factorial then square root then exit
    with patch("builtins.input", side_effect=["5", "4", "8", "9", "0"]):
        main()
    captured = capsys.readouterr()
    assert "Result: 24" in captured.out   # factorial(4) = 24
    assert "Result: 3.0" in captured.out  # sqrt(9) = 3.0
    assert "Goodbye!" in captured.out


def test_main_exits_after_max_invalid_choices(capsys):
    # MAX_INPUT_ATTEMPTS consecutive invalid choices should end the session
    invalid_sequence = ["99"] * MAX_INPUT_ATTEMPTS
    with patch("builtins.input", side_effect=invalid_sequence):
        main()
    captured = capsys.readouterr()
    assert "Unknown operation" in captured.out
    assert "Too many invalid choices" in captured.out


def test_main_invalid_choice_counter_resets_after_valid(capsys):
    # Two invalid choices, then a valid operation, then exit — should not terminate early
    with patch("builtins.input", side_effect=["99", "99", "1", "3", "4", "0"]):
        main()
    captured = capsys.readouterr()
    assert "Result: 7.0" in captured.out
    assert "Goodbye!" in captured.out


def test_main_exits_after_too_many_invalid_operands(capsys):
    # Valid operation choice followed by MAX_INPUT_ATTEMPTS invalid numeric inputs
    invalid_operands = ["abc"] * MAX_INPUT_ATTEMPTS
    with patch("builtins.input", side_effect=["1"] + invalid_operands):
        main()
    captured = capsys.readouterr()
    assert "Maximum input attempts" in captured.out


# --- history integration ---

def test_main_clears_history_at_session_start(tmp_history_file, capsys):
    # Pre-populate the history file; main() should wipe it at the start.
    tmp_history_file.write_text("stale entry\n", encoding="utf-8")
    with patch("builtins.input", return_value="0"):
        main()
    assert tmp_history_file.read_text(encoding="utf-8") == ""


def test_main_records_history_after_successful_operation(tmp_history_file, capsys):
    with patch("builtins.input", side_effect=["1", "3", "4", "0"]):
        main()
    entries = tmp_history_file.read_text(encoding="utf-8").splitlines()
    assert len(entries) == 1
    assert "Add" in entries[0]
    assert "7.0" in entries[0]


def test_main_show_history_displays_entries(tmp_history_file, capsys):
    # Perform add, then show history, then exit.
    with patch("builtins.input", side_effect=["1", "5", "3", "13", "0"]):
        main()
    out = capsys.readouterr().out
    assert "Session history" in out
    assert "Add" in out
