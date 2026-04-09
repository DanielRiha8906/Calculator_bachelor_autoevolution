import os
import pytest
import math
from unittest.mock import patch
from src.calculator import Calculator
from src.__main__ import run_session, _format_entry
from main import run_cli
from src.error_logger import ERROR_LOG_FILE


@pytest.fixture
def calc():
    return Calculator()


# ---------------------------------------------------------------------------
# add
# ---------------------------------------------------------------------------

class TestAdd:
    def test_two_positive_integers(self, calc):
        assert calc.add(3, 4) == 7

    def test_positive_and_negative(self, calc):
        assert calc.add(10, -3) == 7

    def test_two_negatives(self, calc):
        assert calc.add(-5, -7) == -12

    def test_add_zero(self, calc):
        assert calc.add(0, 0) == 0

    def test_identity_with_zero(self, calc):
        assert calc.add(42, 0) == 42

    def test_floats(self, calc):
        assert math.isclose(calc.add(0.1, 0.2), 0.3, rel_tol=1e-9)

    def test_large_numbers(self, calc):
        assert calc.add(10**9, 10**9) == 2 * 10**9


# ---------------------------------------------------------------------------
# subtract
# ---------------------------------------------------------------------------

class TestSubtract:
    def test_positive_result(self, calc):
        assert calc.subtract(10, 3) == 7

    def test_zero_result(self, calc):
        assert calc.subtract(5, 5) == 0

    def test_negative_result(self, calc):
        assert calc.subtract(3, 10) == -7

    def test_subtract_negative(self, calc):
        assert calc.subtract(5, -3) == 8

    def test_both_negative(self, calc):
        assert calc.subtract(-4, -4) == 0

    def test_floats(self, calc):
        assert math.isclose(calc.subtract(1.5, 0.5), 1.0, rel_tol=1e-9)

    def test_subtract_from_zero(self, calc):
        assert calc.subtract(0, 7) == -7


# ---------------------------------------------------------------------------
# multiply
# ---------------------------------------------------------------------------

class TestMultiply:
    def test_two_positives(self, calc):
        assert calc.multiply(3, 4) == 12

    def test_two_negatives(self, calc):
        assert calc.multiply(-3, -4) == 12

    def test_positive_and_negative(self, calc):
        assert calc.multiply(3, -4) == -12

    def test_multiply_by_zero(self, calc):
        assert calc.multiply(999, 0) == 0

    def test_multiply_by_one(self, calc):
        assert calc.multiply(7, 1) == 7

    def test_floats(self, calc):
        assert math.isclose(calc.multiply(0.1, 0.2), 0.02, rel_tol=1e-9)

    def test_float_times_integer(self, calc):
        assert math.isclose(calc.multiply(2.5, 4), 10.0, rel_tol=1e-9)

    def test_large_numbers(self, calc):
        assert calc.multiply(10**6, 10**6) == 10**12


# ---------------------------------------------------------------------------
# divide
# ---------------------------------------------------------------------------

class TestDivide:
    def test_exact_division(self, calc):
        assert calc.divide(10, 2) == 5.0

    def test_fractional_result(self, calc):
        assert math.isclose(calc.divide(1, 3), 1 / 3, rel_tol=1e-9)

    def test_divide_negative_by_positive(self, calc):
        assert calc.divide(-9, 3) == -3.0

    def test_divide_negative_by_negative(self, calc):
        assert calc.divide(-9, -3) == 3.0

    def test_divide_zero_by_nonzero(self, calc):
        assert calc.divide(0, 5) == 0.0

    def test_float_dividend(self, calc):
        assert math.isclose(calc.divide(5.5, 2), 2.75, rel_tol=1e-9)

    def test_float_divisor(self, calc):
        assert math.isclose(calc.divide(1, 0.5), 2.0, rel_tol=1e-9)

    def test_both_floats(self, calc):
        assert math.isclose(calc.divide(0.3, 0.1), 3.0, rel_tol=1e-9)

    def test_divide_by_zero_raises(self, calc):
        with pytest.raises(ZeroDivisionError):
            calc.divide(1, 0)

    def test_divide_zero_by_zero_raises(self, calc):
        with pytest.raises(ZeroDivisionError):
            calc.divide(0, 0)


# ---------------------------------------------------------------------------
# division by zero — focused coverage
# ---------------------------------------------------------------------------

class TestDivideByZero:
    """Focused tests asserting that division by zero always raises ZeroDivisionError."""

    def test_negative_dividend_zero_divisor(self, calc):
        with pytest.raises(ZeroDivisionError):
            calc.divide(-5, 0)

    def test_float_dividend_zero_divisor(self, calc):
        with pytest.raises(ZeroDivisionError):
            calc.divide(3.14, 0)

    def test_float_zero_divisor(self, calc):
        with pytest.raises(ZeroDivisionError):
            calc.divide(1, 0.0)

    def test_large_dividend_zero_divisor(self, calc):
        with pytest.raises(ZeroDivisionError):
            calc.divide(1e308, 0)

    def test_exception_type_is_zero_division_error(self, calc):
        with pytest.raises(ZeroDivisionError):
            calc.divide(42, 0)


# ---------------------------------------------------------------------------
# factorial
# ---------------------------------------------------------------------------

class TestFactorial:
    def test_zero(self, calc):
        assert calc.factorial(0) == 1

    def test_one(self, calc):
        assert calc.factorial(1) == 1

    def test_small_positive(self, calc):
        assert calc.factorial(5) == 120

    def test_larger_positive(self, calc):
        assert calc.factorial(10) == 3628800

    def test_negative_raises(self, calc):
        with pytest.raises(ValueError):
            calc.factorial(-1)

    def test_float_raises(self, calc):
        with pytest.raises(TypeError):
            calc.factorial(3.0)

    def test_string_raises(self, calc):
        with pytest.raises(TypeError):
            calc.factorial("5")

    def test_bool_raises(self, calc):
        with pytest.raises(TypeError):
            calc.factorial(True)


# ---------------------------------------------------------------------------
# square
# ---------------------------------------------------------------------------

class TestSquare:
    def test_positive_integer(self, calc):
        assert calc.square(4) == 16

    def test_zero(self, calc):
        assert calc.square(0) == 0

    def test_negative(self, calc):
        assert calc.square(-3) == 9

    def test_float(self, calc):
        assert math.isclose(calc.square(2.5), 6.25, rel_tol=1e-9)


# ---------------------------------------------------------------------------
# cube
# ---------------------------------------------------------------------------

class TestCube:
    def test_positive_integer(self, calc):
        assert calc.cube(3) == 27

    def test_zero(self, calc):
        assert calc.cube(0) == 0

    def test_negative(self, calc):
        assert calc.cube(-2) == -8

    def test_float(self, calc):
        assert math.isclose(calc.cube(1.5), 3.375, rel_tol=1e-9)


# ---------------------------------------------------------------------------
# square_root
# ---------------------------------------------------------------------------

class TestSquareRoot:
    def test_perfect_square(self, calc):
        assert calc.square_root(9) == 3.0

    def test_zero(self, calc):
        assert calc.square_root(0) == 0.0

    def test_non_perfect_square(self, calc):
        assert math.isclose(calc.square_root(2), math.sqrt(2), rel_tol=1e-9)

    def test_float_input(self, calc):
        assert math.isclose(calc.square_root(0.25), 0.5, rel_tol=1e-9)

    def test_negative_raises(self, calc):
        with pytest.raises(ValueError):
            calc.square_root(-1)


# ---------------------------------------------------------------------------
# cube_root
# ---------------------------------------------------------------------------

class TestCubeRoot:
    def test_perfect_cube(self, calc):
        assert math.isclose(calc.cube_root(27), 3.0, rel_tol=1e-9)

    def test_zero(self, calc):
        assert calc.cube_root(0) == 0.0

    def test_negative(self, calc):
        assert math.isclose(calc.cube_root(-8), -2.0, rel_tol=1e-9)

    def test_float_input(self, calc):
        assert math.isclose(calc.cube_root(0.125), 0.5, rel_tol=1e-9)


# ---------------------------------------------------------------------------
# power
# ---------------------------------------------------------------------------

class TestPower:
    def test_positive_integer_exponent(self, calc):
        assert calc.power(2, 10) == 1024

    def test_zero_exponent(self, calc):
        assert calc.power(5, 0) == 1

    def test_one_exponent(self, calc):
        assert calc.power(7, 1) == 7

    def test_negative_base(self, calc):
        assert calc.power(-2, 3) == -8

    def test_fractional_exponent(self, calc):
        assert math.isclose(calc.power(4, 0.5), 2.0, rel_tol=1e-9)

    def test_zero_base(self, calc):
        assert calc.power(0, 5) == 0

    def test_float_base(self, calc):
        assert math.isclose(calc.power(2.5, 2), 6.25, rel_tol=1e-9)


# ---------------------------------------------------------------------------
# log (base-10)
# ---------------------------------------------------------------------------

class TestLog:
    def test_one(self, calc):
        assert calc.log(1) == 0.0

    def test_ten(self, calc):
        assert math.isclose(calc.log(10), 1.0, rel_tol=1e-9)

    def test_hundred(self, calc):
        assert math.isclose(calc.log(100), 2.0, rel_tol=1e-9)

    def test_fraction(self, calc):
        assert math.isclose(calc.log(0.1), -1.0, rel_tol=1e-9)

    def test_zero_raises(self, calc):
        with pytest.raises(ValueError):
            calc.log(0)

    def test_negative_raises(self, calc):
        with pytest.raises(ValueError):
            calc.log(-5)


# ---------------------------------------------------------------------------
# ln (natural logarithm)
# ---------------------------------------------------------------------------

class TestLn:
    def test_one(self, calc):
        assert calc.ln(1) == 0.0

    def test_e(self, calc):
        assert math.isclose(calc.ln(math.e), 1.0, rel_tol=1e-9)

    def test_e_squared(self, calc):
        assert math.isclose(calc.ln(math.e ** 2), 2.0, rel_tol=1e-9)

    def test_fraction(self, calc):
        assert math.isclose(calc.ln(1 / math.e), -1.0, rel_tol=1e-9)

    def test_zero_raises(self, calc):
        with pytest.raises(ValueError):
            calc.ln(0)

    def test_negative_raises(self, calc):
        with pytest.raises(ValueError):
            calc.ln(-1)


# ---------------------------------------------------------------------------
# run_session (interactive loop in __main__)
# ---------------------------------------------------------------------------

class TestMain:
    def test_quit_immediately(self, calc, capsys):
        with patch("builtins.input", side_effect=["0"]):
            run_session(calc)
        assert "Goodbye!" in capsys.readouterr().out

    def test_add(self, calc, capsys):
        with patch("builtins.input", side_effect=["1", "3", "4", "0"]):
            run_session(calc)
        assert "Result: 7.0" in capsys.readouterr().out

    def test_subtract(self, calc, capsys):
        with patch("builtins.input", side_effect=["2", "10", "3", "0"]):
            run_session(calc)
        assert "Result: 7.0" in capsys.readouterr().out

    def test_multiply(self, calc, capsys):
        with patch("builtins.input", side_effect=["3", "6", "7", "0"]):
            run_session(calc)
        assert "Result: 42.0" in capsys.readouterr().out

    def test_divide(self, calc, capsys):
        with patch("builtins.input", side_effect=["4", "10", "2", "0"]):
            run_session(calc)
        assert "Result: 5.0" in capsys.readouterr().out

    def test_power(self, calc, capsys):
        with patch("builtins.input", side_effect=["5", "2", "10", "0"]):
            run_session(calc)
        assert "Result: 1024.0" in capsys.readouterr().out

    def test_factorial(self, calc, capsys):
        with patch("builtins.input", side_effect=["6", "5", "0"]):
            run_session(calc)
        assert "Result: 120" in capsys.readouterr().out

    def test_square(self, calc, capsys):
        with patch("builtins.input", side_effect=["7", "4", "0"]):
            run_session(calc)
        assert "Result: 16.0" in capsys.readouterr().out

    def test_cube(self, calc, capsys):
        with patch("builtins.input", side_effect=["8", "3", "0"]):
            run_session(calc)
        assert "Result: 27.0" in capsys.readouterr().out

    def test_square_root(self, calc, capsys):
        with patch("builtins.input", side_effect=["9", "9", "0"]):
            run_session(calc)
        assert "Result: 3.0" in capsys.readouterr().out

    def test_cube_root(self, calc, capsys):
        with patch("builtins.input", side_effect=["10", "27", "0"]):
            run_session(calc)
        assert "Result:" in capsys.readouterr().out

    def test_log(self, calc, capsys):
        with patch("builtins.input", side_effect=["11", "100", "0"]):
            run_session(calc)
        assert "Result: 2.0" in capsys.readouterr().out

    def test_ln(self, calc, capsys):
        with patch("builtins.input", side_effect=["12", "1", "0"]):
            run_session(calc)
        assert "Result: 0.0" in capsys.readouterr().out

    def test_unknown_choice(self, calc, capsys):
        with patch("builtins.input", side_effect=["99", "0"]):
            run_session(calc)
        assert "Unknown choice" in capsys.readouterr().out

    def test_divide_by_zero_error(self, calc, capsys):
        with patch("builtins.input", side_effect=["4", "1", "0", "0"]):
            run_session(calc)
        assert "Error:" in capsys.readouterr().out

    def test_sqrt_negative_error(self, calc, capsys):
        with patch("builtins.input", side_effect=["9", "-4", "0"]):
            run_session(calc)
        assert "Error:" in capsys.readouterr().out

    def test_factorial_non_integer_error(self, calc, capsys):
        with patch("builtins.input", side_effect=["6", "5.5", "0"]):
            run_session(calc)
        assert "Error" in capsys.readouterr().out

    def test_multiple_calculations(self, calc, capsys):
        with patch("builtins.input", side_effect=["1", "2", "3", "3", "4", "5", "0"]):
            run_session(calc)
        assert capsys.readouterr().out.count("Result:") == 2

    def test_too_many_invalid_choices_ends_session(self, calc, capsys):
        # Five consecutive unknown choices must terminate the session.
        with patch("builtins.input", side_effect=["a", "b", "c", "d", "e"]):
            run_session(calc)
        out = capsys.readouterr().out
        assert "Too many invalid choices" in out
        assert "Goodbye!" not in out

    def test_invalid_choice_lists_available_operations(self, calc, capsys):
        # An unknown choice must print the list of available operations.
        with patch("builtins.input", side_effect=["99", "0"]):
            run_session(calc)
        assert "Available operations" in capsys.readouterr().out

    def test_invalid_choice_retry_succeeds(self, calc, capsys):
        # One invalid choice followed by a valid choice should complete normally.
        with patch("builtins.input", side_effect=["99", "1", "2", "3", "0"]):
            run_session(calc)
        assert "Result: 5.0" in capsys.readouterr().out

    def test_too_many_invalid_numbers_ends_session(self, calc, capsys):
        # Five non-numeric inputs for a single operand must terminate the session.
        with patch("builtins.input", side_effect=["1", "x", "x", "x", "x", "x"]):
            run_session(calc)
        out = capsys.readouterr().out
        assert "Too many invalid inputs" in out

    def test_invalid_number_shows_remaining_attempts(self, calc, capsys):
        # One invalid number should show the remaining-attempts hint.
        with patch("builtins.input", side_effect=["1", "abc", "5", "3", "0"]):
            run_session(calc)
        out = capsys.readouterr().out
        assert "attempt(s) left" in out
        assert "Result: 8.0" in out

    def test_choice_failure_counter_resets_after_valid_choice(self, calc, capsys):
        # Four invalid choices, one valid operation, then four more invalid choices
        # should NOT terminate — each run of bad choices starts fresh.
        with patch(
            "builtins.input",
            side_effect=["a", "b", "c", "d", "1", "3", "4", "a", "b", "c", "d", "0"],
        ):
            run_session(calc)
        out = capsys.readouterr().out
        assert "Result: 7.0" in out
        assert "Goodbye!" in out


# ---------------------------------------------------------------------------
# CLI (bash mode) — main.py:run_cli
# ---------------------------------------------------------------------------

class TestCLI:
    """Tests for the bash CLI interface (main.py:run_cli)."""

    def test_add(self, capsys):
        run_cli(["add", "5", "7"])
        assert "12.0" in capsys.readouterr().out

    def test_subtract(self, capsys):
        run_cli(["subtract", "10", "3"])
        assert "7.0" in capsys.readouterr().out

    def test_multiply(self, capsys):
        run_cli(["multiply", "4", "5"])
        assert "20.0" in capsys.readouterr().out

    def test_divide(self, capsys):
        run_cli(["divide", "10", "2"])
        assert "5.0" in capsys.readouterr().out

    def test_power(self, capsys):
        run_cli(["power", "2", "8"])
        assert "256.0" in capsys.readouterr().out

    def test_factorial(self, capsys):
        run_cli(["factorial", "5"])
        assert "120" in capsys.readouterr().out

    def test_square(self, capsys):
        run_cli(["square", "6"])
        assert "36.0" in capsys.readouterr().out

    def test_cube(self, capsys):
        run_cli(["cube", "3"])
        assert "27.0" in capsys.readouterr().out

    def test_square_root(self, capsys):
        run_cli(["square_root", "9"])
        assert "3.0" in capsys.readouterr().out

    def test_cube_root(self, capsys):
        run_cli(["cube_root", "8"])
        assert "2.0" in capsys.readouterr().out

    def test_log(self, capsys):
        run_cli(["log", "100"])
        assert "2.0" in capsys.readouterr().out

    def test_ln(self, capsys):
        run_cli(["ln", "1"])
        assert "0.0" in capsys.readouterr().out

    def test_unknown_operation_exits(self, capsys):
        with pytest.raises(SystemExit) as exc_info:
            run_cli(["foobar", "5"])
        assert exc_info.value.code == 1

    def test_wrong_operand_count_too_few_exits(self, capsys):
        with pytest.raises(SystemExit) as exc_info:
            run_cli(["add", "5"])
        assert exc_info.value.code == 1

    def test_wrong_operand_count_too_many_exits(self, capsys):
        with pytest.raises(SystemExit) as exc_info:
            run_cli(["square", "5", "6"])
        assert exc_info.value.code == 1

    def test_invalid_number_exits(self, capsys):
        with pytest.raises(SystemExit) as exc_info:
            run_cli(["add", "foo", "7"])
        assert exc_info.value.code == 1

    def test_divide_by_zero_exits(self, capsys):
        with pytest.raises(SystemExit) as exc_info:
            run_cli(["divide", "5", "0"])
        assert exc_info.value.code == 1

    def test_sqrt_negative_exits(self, capsys):
        with pytest.raises(SystemExit) as exc_info:
            run_cli(["square_root", "-4"])
        assert exc_info.value.code == 1

    def test_factorial_non_integer_exits(self, capsys):
        with pytest.raises(SystemExit) as exc_info:
            run_cli(["factorial", "5.5"])
        assert exc_info.value.code == 1


# ---------------------------------------------------------------------------
# History — session tracking, display, and file output
# ---------------------------------------------------------------------------

class TestHistory:
    """Tests for session history tracking, 'h' display, and file output."""

    def test_history_empty_initially(self, calc, capsys, tmp_path):
        history_file = str(tmp_path / "history.txt")
        with patch("builtins.input", side_effect=["h", "0"]):
            run_session(calc, history_file=history_file)
        assert "No history yet." in capsys.readouterr().out

    def test_history_shows_entry_after_two_operand_calc(self, calc, capsys, tmp_path):
        history_file = str(tmp_path / "history.txt")
        with patch("builtins.input", side_effect=["1", "2", "3", "h", "0"]):
            run_session(calc, history_file=history_file)
        assert "add(2, 3) = 5" in capsys.readouterr().out

    def test_history_shows_entry_after_one_operand_calc(self, calc, capsys, tmp_path):
        history_file = str(tmp_path / "history.txt")
        with patch("builtins.input", side_effect=["9", "9", "h", "0"]):
            run_session(calc, history_file=history_file)
        assert "square_root(9) = 3" in capsys.readouterr().out

    def test_history_shows_factorial_entry(self, calc, capsys, tmp_path):
        history_file = str(tmp_path / "history.txt")
        with patch("builtins.input", side_effect=["6", "5", "h", "0"]):
            run_session(calc, history_file=history_file)
        assert "factorial(5) = 120" in capsys.readouterr().out

    def test_history_written_to_file_on_quit(self, calc, tmp_path):
        history_file = str(tmp_path / "history.txt")
        with patch("builtins.input", side_effect=["1", "4", "5", "0"]):
            run_session(calc, history_file=history_file)
        with open(history_file) as f:
            content = f.read()
        assert "add(4, 5) = 9" in content

    def test_history_file_created_even_when_empty(self, calc, tmp_path):
        history_file = str(tmp_path / "history.txt")
        with patch("builtins.input", side_effect=["0"]):
            run_session(calc, history_file=history_file)
        assert os.path.exists(history_file)

    def test_history_accumulates_multiple_entries(self, calc, tmp_path):
        history_file = str(tmp_path / "history.txt")
        with patch("builtins.input", side_effect=["1", "2", "3", "3", "4", "5", "h", "0"]):
            run_session(calc, history_file=history_file)
        with open(history_file) as f:
            content = f.read()
        assert "add(2, 3) = 5" in content
        assert "multiply(4, 5) = 20" in content

    def test_format_entry_two_operands(self):
        assert _format_entry("add", (2.0, 3.0), 5.0) == "add(2, 3) = 5"

    def test_format_entry_one_operand(self):
        assert _format_entry("square_root", (9.0,), 3.0) == "square_root(9) = 3"

    def test_format_entry_factorial(self):
        assert _format_entry("factorial", (5,), 120) == "factorial(5) = 120"

    def test_history_not_recorded_on_math_error(self, calc, capsys, tmp_path):
        history_file = str(tmp_path / "history.txt")
        # divide by zero should not add an entry to history
        with patch("builtins.input", side_effect=["4", "1", "0", "h", "0"]):
            run_session(calc, history_file=history_file)
        out = capsys.readouterr().out
        assert "No history yet." in out


# ---------------------------------------------------------------------------
# Error logging — separate log file for failures and invalid usage
# ---------------------------------------------------------------------------

class TestErrorLogging:
    """Tests for error logging to calculator_errors.log (separate from history)."""

    def _read_log(self, path: str) -> str:
        if not os.path.exists(path):
            return ""
        with open(path, encoding="utf-8") as f:
            return f.read()

    # --- Interactive mode ---

    def test_calculation_error_logged_interactive(self, calc, tmp_path):
        # Division by zero must produce an entry in the error log.
        log_file = str(tmp_path / "errors.log")
        with patch("builtins.input", side_effect=["4", "1", "0", "0"]):
            run_session(calc, error_log_file=log_file)
        assert "divide" in self._read_log(log_file)

    def test_sqrt_negative_logged_interactive(self, calc, tmp_path):
        log_file = str(tmp_path / "errors.log")
        with patch("builtins.input", side_effect=["9", "-4", "0"]):
            run_session(calc, error_log_file=log_file)
        assert "square_root" in self._read_log(log_file)

    def test_invalid_menu_choice_logged_interactive(self, calc, tmp_path):
        log_file = str(tmp_path / "errors.log")
        with patch("builtins.input", side_effect=["99", "0"]):
            run_session(calc, error_log_file=log_file)
        assert "99" in self._read_log(log_file)

    def test_too_many_invalid_choices_logged_interactive(self, calc, tmp_path):
        log_file = str(tmp_path / "errors.log")
        with patch("builtins.input", side_effect=["a", "b", "c", "d", "e"]):
            run_session(calc, error_log_file=log_file)
        content = self._read_log(log_file)
        assert "too many invalid menu choices" in content.lower()

    def test_invalid_number_input_logged_interactive(self, calc, tmp_path):
        # Typing a non-numeric value for an operand must appear in the error log.
        log_file = str(tmp_path / "errors.log")
        with patch("builtins.input", side_effect=["1", "abc", "2", "3", "0"]):
            run_session(calc, error_log_file=log_file)
        assert "abc" in self._read_log(log_file)

    def test_factorial_non_integer_logged_interactive(self, calc, tmp_path):
        log_file = str(tmp_path / "errors.log")
        with patch("builtins.input", side_effect=["6", "5.5", "0"]):
            run_session(calc, error_log_file=log_file)
        assert "factorial" in self._read_log(log_file)

    def test_too_many_invalid_inputs_logged_interactive(self, calc, tmp_path):
        # TooManyAttemptsError must be recorded in the error log.
        log_file = str(tmp_path / "errors.log")
        with patch("builtins.input", side_effect=["1", "x", "x", "x", "x", "x"]):
            run_session(calc, error_log_file=log_file)
        content = self._read_log(log_file)
        assert "Too many invalid inputs" in content

    def test_successful_operation_not_in_error_log_interactive(self, calc, tmp_path):
        # A successful calculation must not generate any error log entry.
        log_file = str(tmp_path / "errors.log")
        with patch("builtins.input", side_effect=["1", "3", "4", "0"]):
            run_session(calc, error_log_file=log_file)
        assert self._read_log(log_file) == ""

    def test_error_log_separate_from_history(self, calc, tmp_path):
        # history.txt and errors.log must be distinct files with distinct content.
        history_file = str(tmp_path / "history.txt")
        log_file = str(tmp_path / "errors.log")
        with patch("builtins.input", side_effect=["4", "1", "0", "0"]):
            run_session(calc, history_file=history_file, error_log_file=log_file)
        assert os.path.exists(history_file)
        assert "divide" in self._read_log(log_file)
        with open(history_file) as f:
            history_content = f.read()
        # The error detail must not appear in the history file.
        assert "ERROR" not in history_content

    # --- CLI mode ---

    def test_unknown_operation_logged_cli(self, tmp_path):
        log_file = str(tmp_path / "errors.log")
        with pytest.raises(SystemExit):
            run_cli(["foobar", "5"], error_log_file=log_file)
        assert "foobar" in self._read_log(log_file)

    def test_wrong_operand_count_logged_cli(self, tmp_path):
        log_file = str(tmp_path / "errors.log")
        with pytest.raises(SystemExit):
            run_cli(["add", "5"], error_log_file=log_file)
        assert "add" in self._read_log(log_file)

    def test_invalid_number_logged_cli(self, tmp_path):
        log_file = str(tmp_path / "errors.log")
        with pytest.raises(SystemExit):
            run_cli(["add", "foo", "7"], error_log_file=log_file)
        assert "foo" in self._read_log(log_file)

    def test_calculation_error_logged_cli(self, tmp_path):
        log_file = str(tmp_path / "errors.log")
        with pytest.raises(SystemExit):
            run_cli(["divide", "5", "0"], error_log_file=log_file)
        assert "divide" in self._read_log(log_file)

    def test_factorial_non_integer_logged_cli(self, tmp_path):
        log_file = str(tmp_path / "errors.log")
        with pytest.raises(SystemExit):
            run_cli(["factorial", "5.5"], error_log_file=log_file)
        assert "factorial" in self._read_log(log_file)

    def test_successful_cli_operation_not_in_error_log(self, tmp_path):
        # A successful CLI operation must not produce any error log entry.
        log_file = str(tmp_path / "errors.log")
        run_cli(["add", "3", "4"], error_log_file=log_file)
        assert self._read_log(log_file) == ""
