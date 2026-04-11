import logging
import math
import pytest
from unittest.mock import patch
from src.user_input import (
    interactive_mode,
    _get_float,
    _get_int,
    _print_history,
    MAX_RETRIES,
    NORMAL_OPERATIONS,
    SCIENTIFIC_OPERATIONS,
)


class TestInteractiveMode:
    def test_quit_immediately(self, capsys):
        with patch("builtins.input", return_value="q"):
            interactive_mode()
        captured = capsys.readouterr()
        assert "Goodbye!" in captured.out

    def test_menu_is_printed(self, capsys):
        with patch("builtins.input", return_value="q"):
            interactive_mode()
        captured = capsys.readouterr()
        assert "Calculator - Interactive Mode" in captured.out
        assert "Operations:" in captured.out

    def test_add_two_numbers(self, capsys):
        inputs = iter(["1", "3", "5", "q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        assert "Result: 8.0" in captured.out

    def test_subtract_two_numbers(self, capsys):
        inputs = iter(["2", "10", "3", "q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        assert "Result: 7.0" in captured.out

    def test_multiply_two_numbers(self, capsys):
        inputs = iter(["3", "4", "5", "q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        assert "Result: 20.0" in captured.out

    def test_divide_two_numbers(self, capsys):
        inputs = iter(["4", "10", "2", "q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        assert "Result: 5.0" in captured.out

    def test_factorial_integer(self, capsys):
        inputs = iter(["5", "5", "q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        assert "Result: 120" in captured.out

    def test_square_number(self, capsys):
        inputs = iter(["6", "4", "q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        assert "Result: 16.0" in captured.out

    def test_cube_number(self, capsys):
        inputs = iter(["7", "3", "q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        assert "Result: 27.0" in captured.out

    def test_square_root(self, capsys):
        inputs = iter(["8", "9", "q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        assert "Result: 3.0" in captured.out

    def test_power_operation(self, capsys):
        inputs = iter(["10", "2", "3", "q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        assert "Result: 8.0" in captured.out

    def test_invalid_choice_shows_error(self, capsys):
        inputs = iter(["99", "q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        assert "Unknown operation" in captured.out

    def test_divide_by_zero_shows_error(self, capsys):
        inputs = iter(["4", "10", "0", "q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        assert "Error:" in captured.out

    def test_square_root_negative_shows_error(self, capsys):
        inputs = iter(["8", "-1", "q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        assert "Error:" in captured.out

    def test_multiple_operations_in_session(self, capsys):
        inputs = iter(["1", "2", "3", "2", "10", "4", "q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        assert "Result: 5.0" in captured.out
        assert "Result: 6.0" in captured.out


class TestRetryLogicHelpers:
    """Tests for _get_float and _get_int retry helpers."""

    def test_get_float_valid_on_first_attempt(self, capsys):
        with patch("builtins.input", return_value="3.14"):
            result = _get_float("Enter: ")
        assert result == 3.14

    def test_get_float_retries_once_then_succeeds(self, capsys):
        inputs = iter(["abc", "2.5"])
        with patch("builtins.input", side_effect=inputs):
            result = _get_float("Enter: ")
        captured = capsys.readouterr()
        assert result == 2.5
        assert "Invalid input" in captured.out
        assert "attempt(s) remaining" in captured.out

    def test_get_float_exhausts_retries_raises(self, capsys):
        inputs = iter(["x"] * MAX_RETRIES)
        with patch("builtins.input", side_effect=inputs):
            with pytest.raises(ValueError, match="Failed to get a valid number"):
                _get_float("Enter: ")
        captured = capsys.readouterr()
        assert "No more retries" in captured.out

    def test_get_int_valid_on_first_attempt(self, capsys):
        with patch("builtins.input", return_value="7"):
            result = _get_int("Enter: ")
        assert result == 7

    def test_get_int_retries_once_then_succeeds(self, capsys):
        inputs = iter(["not-a-number", "5"])
        with patch("builtins.input", side_effect=inputs):
            result = _get_int("Enter: ")
        captured = capsys.readouterr()
        assert result == 5
        assert "Invalid input" in captured.out
        assert "attempt(s) remaining" in captured.out

    def test_get_int_exhausts_retries_raises(self, capsys):
        inputs = iter(["x"] * MAX_RETRIES)
        with patch("builtins.input", side_effect=inputs):
            with pytest.raises(ValueError, match="Failed to get a valid integer"):
                _get_int("Enter: ")
        captured = capsys.readouterr()
        assert "No more retries" in captured.out


class TestRetryLogicInInteractiveMode:
    """Integration tests for retry logic within interactive_mode."""

    def test_invalid_float_then_valid_computes_result(self, capsys):
        # Select add (op 1), enter bad first number, then good inputs
        inputs = iter(["1", "bad", "3", "4", "q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        assert "Invalid input" in captured.out
        assert "Result: 7.0" in captured.out

    def test_invalid_int_then_valid_computes_factorial(self, capsys):
        # Select factorial (op 5), enter bad integer, then good integer
        inputs = iter(["5", "notint", "4", "q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        assert "Invalid input" in captured.out
        assert "Result: 24" in captured.out

    def test_exhausted_retries_shows_error_and_returns_to_menu(self, capsys):
        # Select square (op 6), exhaust all retries, then quit
        bad_inputs = ["bad"] * MAX_RETRIES
        inputs = iter(["6"] + bad_inputs + ["q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        assert "No more retries" in captured.out
        assert "Error:" in captured.out
        assert "Goodbye!" in captured.out


class TestHistoryInInteractiveMode:
    """Tests for the 'h' history command in interactive_mode."""

    def test_history_option_shown_in_menu(self, capsys):
        with patch("builtins.input", return_value="q"):
            interactive_mode()
        captured = capsys.readouterr()
        assert "history" in captured.out

    def test_history_empty_shows_no_history(self, capsys):
        inputs = iter(["h", "q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        assert "No history" in captured.out

    def test_history_shows_after_operation(self, capsys):
        # add(3, 5) = 8, then show history
        inputs = iter(["1", "3", "5", "h", "q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        assert "add" in captured.out
        assert "8.0" in captured.out

    def test_history_accumulates_multiple_operations(self, capsys):
        # add(1, 2), multiply(3, 4), then show history
        inputs = iter(["1", "1", "2", "3", "3", "4", "h", "q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        assert "add" in captured.out
        assert "multiply" in captured.out

    def test_print_history_empty(self, capsys):
        _print_history([])
        captured = capsys.readouterr()
        assert "No history" in captured.out

    def test_print_history_single_entry(self, capsys):
        _print_history([{"operation": "add", "args": [3, 5], "result": 8}])
        captured = capsys.readouterr()
        assert "add(3, 5) = 8" in captured.out

    def test_print_history_two_arg_entry(self, capsys):
        _print_history([{"operation": "divide", "args": [10.0, 2.0], "result": 5.0}])
        captured = capsys.readouterr()
        assert "divide" in captured.out
        assert "5.0" in captured.out


class TestErrorLoggingInUserInput:
    def test_get_float_exhausted_retries_logs_error(self, caplog):
        with caplog.at_level(logging.ERROR, logger="src.user_input"):
            with patch("builtins.input", return_value="abc"):
                with pytest.raises(ValueError):
                    _get_float("Enter number: ")
        assert len(caplog.records) == 1
        assert "Failed to get a valid number" in caplog.records[0].message

    def test_get_int_exhausted_retries_logs_error(self, caplog):
        with caplog.at_level(logging.ERROR, logger="src.user_input"):
            with patch("builtins.input", return_value="xyz"):
                with pytest.raises(ValueError):
                    _get_int("Enter integer: ")
        assert len(caplog.records) == 1
        assert "Failed to get a valid integer" in caplog.records[0].message

    def test_successful_float_input_does_not_log_error(self, caplog):
        with caplog.at_level(logging.ERROR, logger="src.user_input"):
            with patch("builtins.input", return_value="3.14"):
                result = _get_float("Enter number: ")
        assert result == pytest.approx(3.14)
        assert len(caplog.records) == 0


class TestOperationDicts:
    """Tests for NORMAL_OPERATIONS and SCIENTIFIC_OPERATIONS constants."""

    def test_normal_operations_has_12_entries(self):
        assert len(NORMAL_OPERATIONS) == 12

    def test_scientific_operations_has_15_entries(self):
        assert len(SCIENTIFIC_OPERATIONS) == 15

    def test_scientific_operations_is_superset_of_normal(self):
        for key, op in NORMAL_OPERATIONS.items():
            assert SCIENTIFIC_OPERATIONS[key] == op

    def test_scientific_operations_includes_trig(self):
        trig_ops = set(SCIENTIFIC_OPERATIONS.values())
        assert "sin" in trig_ops
        assert "cos" in trig_ops
        assert "tan" in trig_ops


class TestScientificModeSwitch:
    """Tests for normal/scientific mode switching in interactive_mode."""

    def test_starts_in_normal_mode(self, capsys):
        with patch("builtins.input", return_value="q"):
            interactive_mode()
        captured = capsys.readouterr()
        assert "normal" in captured.out

    def test_switch_to_scientific_mode(self, capsys):
        inputs = iter(["s", "q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        assert "Switched to scientific mode" in captured.out
        assert "scientific" in captured.out

    def test_switch_back_to_normal_mode(self, capsys):
        inputs = iter(["s", "n", "q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        assert "Switched to scientific mode" in captured.out
        assert "Switched to normal mode" in captured.out

    def test_switch_to_scientific_already_in_scientific(self, capsys):
        inputs = iter(["s", "s", "q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        assert "Already in scientific mode" in captured.out

    def test_switch_to_normal_already_in_normal(self, capsys):
        inputs = iter(["n", "q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        assert "Already in normal mode" in captured.out

    def test_scientific_mode_menu_shows_trig_ops(self, capsys):
        inputs = iter(["s", "q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        assert "sin" in captured.out
        assert "cos" in captured.out
        assert "tan" in captured.out

    def test_trig_op_not_available_in_normal_mode(self, capsys):
        # op "13" (sin) is only in scientific mode; in normal mode it's unknown
        inputs = iter(["13", "q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        assert "Unknown operation" in captured.out

    def test_sin_in_scientific_mode(self, capsys):
        # Switch to scientific, select sin (13), enter pi/2 → result ≈ 1.0
        half_pi = str(math.pi / 2)
        inputs = iter(["s", "13", half_pi, "q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        assert "Result:" in captured.out

    def test_cos_in_scientific_mode(self, capsys):
        # Switch to scientific, select cos (14), enter 0 → result = 1.0
        inputs = iter(["s", "14", "0", "q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        assert "Result: 1.0" in captured.out

    def test_tan_in_scientific_mode(self, capsys):
        # Switch to scientific, select tan (15), enter 0 → result = 0.0
        inputs = iter(["s", "15", "0", "q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        assert "Result: 0.0" in captured.out

    def test_history_persists_across_mode_switch(self, capsys):
        # add in normal, switch to scientific, do sin, show history
        inputs = iter(["1", "2", "3", "s", "13", "0", "h", "q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        # Both add and sin should appear in history
        assert "add" in captured.out
        assert "sin" in captured.out

    def test_normal_ops_still_work_after_mode_switch(self, capsys):
        # Switch to scientific and back, then use normal add
        inputs = iter(["s", "n", "1", "4", "6", "q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        assert "Result: 10.0" in captured.out
