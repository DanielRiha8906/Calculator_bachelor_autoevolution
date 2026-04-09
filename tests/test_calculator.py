import pytest
import math
from src.calculator import Calculator
from src.__main__ import run_interactive, run_cli


class TestAdd:
    def setup_method(self):
        self.calc = Calculator()

    def test_add_positive_numbers(self):
        assert self.calc.add(3, 5) == 8

    def test_add_negative_numbers(self):
        assert self.calc.add(-3, -5) == -8

    def test_add_positive_and_negative(self):
        assert self.calc.add(10, -4) == 6

    def test_add_zero(self):
        assert self.calc.add(7, 0) == 7

    def test_add_both_zero(self):
        assert self.calc.add(0, 0) == 0


class TestSubtract:
    def setup_method(self):
        self.calc = Calculator()

    def test_subtract_positive_numbers(self):
        assert self.calc.subtract(10, 4) == 6

    def test_subtract_negative_numbers(self):
        assert self.calc.subtract(-3, -5) == 2

    def test_subtract_positive_and_negative(self):
        assert self.calc.subtract(5, -3) == 8

    def test_subtract_zero(self):
        assert self.calc.subtract(9, 0) == 9

    def test_subtract_to_zero(self):
        assert self.calc.subtract(5, 5) == 0


class TestMultiply:
    def setup_method(self):
        self.calc = Calculator()

    def test_multiply_positive_numbers(self):
        assert self.calc.multiply(3, 4) == 12

    def test_multiply_negative_numbers(self):
        assert self.calc.multiply(-3, -4) == 12

    def test_multiply_positive_and_negative(self):
        assert self.calc.multiply(3, -4) == -12

    def test_multiply_by_zero(self):
        assert self.calc.multiply(5, 0) == 0

    def test_multiply_by_one(self):
        assert self.calc.multiply(7, 1) == 7


class TestDivide:
    def setup_method(self):
        self.calc = Calculator()

    def test_divide_normal(self):
        assert self.calc.divide(10, 2) == 5

    def test_divide_by_zero_raises_value_error(self):
        with pytest.raises(ValueError, match="Division by zero is not allowed"):
            self.calc.divide(10, 0)

    def test_divide_negative_by_zero_raises_value_error(self):
        with pytest.raises(ValueError):
            self.calc.divide(-5, 0)

    def test_divide_zero_by_zero_raises_value_error(self):
        with pytest.raises(ValueError):
            self.calc.divide(0, 0)

    def test_divide_string_numerator_raises_type_error(self):
        with pytest.raises(TypeError):
            self.calc.divide("hello", 2)

    def test_divide_string_denominator_raises_type_error(self):
        with pytest.raises(TypeError):
            self.calc.divide(10, "hello")

    def test_divide_none_numerator_raises_type_error(self):
        with pytest.raises(TypeError):
            self.calc.divide(None, 2)

    def test_divide_none_denominator_raises_type_error(self):
        with pytest.raises(TypeError):
            self.calc.divide(10, None)


class TestFactorial:
    def setup_method(self):
        self.calc = Calculator()

    def test_factorial_of_zero(self):
        assert self.calc.factorial(0) == 1

    def test_factorial_of_one(self):
        assert self.calc.factorial(1) == 1

    def test_factorial_of_positive_number(self):
        assert self.calc.factorial(5) == 120

    def test_factorial_large_number(self):
        assert self.calc.factorial(10) == 3628800

    def test_factorial_negative_raises_value_error(self):
        with pytest.raises(ValueError, match="Factorial is not defined for negative numbers"):
            self.calc.factorial(-1)

    def test_factorial_float_raises_type_error(self):
        with pytest.raises(TypeError, match="Factorial is only defined for integers"):
            self.calc.factorial(3.5)


class TestSquare:
    def setup_method(self):
        self.calc = Calculator()

    def test_square_positive(self):
        assert self.calc.square(4) == 16

    def test_square_negative(self):
        assert self.calc.square(-3) == 9

    def test_square_zero(self):
        assert self.calc.square(0) == 0

    def test_square_float(self):
        assert self.calc.square(2.5) == pytest.approx(6.25)


class TestCube:
    def setup_method(self):
        self.calc = Calculator()

    def test_cube_positive(self):
        assert self.calc.cube(3) == 27

    def test_cube_negative(self):
        assert self.calc.cube(-2) == -8

    def test_cube_zero(self):
        assert self.calc.cube(0) == 0

    def test_cube_float(self):
        assert self.calc.cube(2.0) == pytest.approx(8.0)


class TestSquareRoot:
    def setup_method(self):
        self.calc = Calculator()

    def test_square_root_positive(self):
        assert self.calc.square_root(9) == pytest.approx(3.0)

    def test_square_root_zero(self):
        assert self.calc.square_root(0) == pytest.approx(0.0)

    def test_square_root_float(self):
        assert self.calc.square_root(2.0) == pytest.approx(math.sqrt(2))

    def test_square_root_negative_raises_value_error(self):
        with pytest.raises(ValueError, match="Square root is not defined for negative numbers"):
            self.calc.square_root(-1)


class TestCubeRoot:
    def setup_method(self):
        self.calc = Calculator()

    def test_cube_root_positive(self):
        assert self.calc.cube_root(27) == pytest.approx(3.0)

    def test_cube_root_negative(self):
        assert self.calc.cube_root(-8) == pytest.approx(-2.0)

    def test_cube_root_zero(self):
        assert self.calc.cube_root(0) == pytest.approx(0.0)

    def test_cube_root_float(self):
        assert self.calc.cube_root(1.0) == pytest.approx(1.0)


class TestPower:
    def setup_method(self):
        self.calc = Calculator()

    def test_power_positive_exponent(self):
        assert self.calc.power(2, 10) == 1024

    def test_power_zero_exponent(self):
        assert self.calc.power(5, 0) == 1

    def test_power_negative_exponent(self):
        assert self.calc.power(2, -1) == pytest.approx(0.5)

    def test_power_fractional_exponent(self):
        assert self.calc.power(9, 0.5) == pytest.approx(3.0)

    def test_power_base_zero(self):
        assert self.calc.power(0, 5) == 0


class TestLog:
    def setup_method(self):
        self.calc = Calculator()

    def test_log_of_one(self):
        assert self.calc.log(1) == pytest.approx(0.0)

    def test_log_of_ten(self):
        assert self.calc.log(10) == pytest.approx(1.0)

    def test_log_of_hundred(self):
        assert self.calc.log(100) == pytest.approx(2.0)

    def test_log_zero_raises_value_error(self):
        with pytest.raises(ValueError, match="Logarithm is not defined for non-positive numbers"):
            self.calc.log(0)

    def test_log_negative_raises_value_error(self):
        with pytest.raises(ValueError):
            self.calc.log(-5)


class TestLn:
    def setup_method(self):
        self.calc = Calculator()

    def test_ln_of_one(self):
        assert self.calc.ln(1) == pytest.approx(0.0)

    def test_ln_of_e(self):
        assert self.calc.ln(math.e) == pytest.approx(1.0)

    def test_ln_positive(self):
        assert self.calc.ln(math.e ** 3) == pytest.approx(3.0)

    def test_ln_zero_raises_value_error(self):
        with pytest.raises(ValueError, match="Natural logarithm is not defined for non-positive numbers"):
            self.calc.ln(0)

    def test_ln_negative_raises_value_error(self):
        with pytest.raises(ValueError):
            self.calc.ln(-1)


class TestRunInteractive:
    """Tests for the interactive user-input loop in src/__main__.py."""

    def setup_method(self):
        self.calc = Calculator()

    def _run(self, *responses):
        """Helper: run the interactive loop with pre-canned responses and capture output."""
        responses_iter = iter(responses)

        def fake_input(prompt=""):
            return next(responses_iter)

        outputs = []
        run_interactive(self.calc, input_fn=fake_input, output_fn=outputs.append)
        return outputs

    def test_quit_exits_immediately(self):
        outputs = self._run("quit")
        assert any("quit" in line.lower() or "exit" in line.lower() for line in outputs)

    def test_unknown_operation_shows_error(self):
        outputs = self._run("foobar", "quit")
        assert any("Unknown operation" in line or "foobar" in line for line in outputs)

    def test_binary_add(self):
        outputs = self._run("add", "3", "5", "quit")
        assert any("Result: 8.0" in line for line in outputs)

    def test_binary_subtract(self):
        outputs = self._run("subtract", "10", "4", "quit")
        assert any("Result: 6.0" in line for line in outputs)

    def test_binary_multiply(self):
        outputs = self._run("multiply", "3", "4", "quit")
        assert any("Result: 12.0" in line for line in outputs)

    def test_binary_divide(self):
        outputs = self._run("divide", "10", "2", "quit")
        assert any("Result: 5.0" in line for line in outputs)

    def test_binary_power(self):
        outputs = self._run("power", "2", "8", "quit")
        assert any("Result: 256.0" in line for line in outputs)

    def test_unary_square(self):
        outputs = self._run("square", "4", "quit")
        assert any("Result: 16" in line for line in outputs)

    def test_unary_cube(self):
        outputs = self._run("cube", "3", "quit")
        assert any("Result: 27" in line for line in outputs)

    def test_unary_square_root(self):
        outputs = self._run("square_root", "9", "quit")
        assert any("Result: 3.0" in line for line in outputs)

    def test_unary_log(self):
        outputs = self._run("log", "100", "quit")
        assert any("Result: 2.0" in line for line in outputs)

    def test_unary_ln(self):
        outputs = self._run("ln", "1", "quit")
        assert any("Result: 0.0" in line for line in outputs)

    def test_factorial_valid(self):
        outputs = self._run("factorial", "5", "quit")
        assert any("Result: 120" in line for line in outputs)

    def test_factorial_non_integer_input_shows_error(self):
        # Three bad inputs exhaust all retries (MAX_INPUT_RETRIES=3), then quit
        outputs = self._run("factorial", "3.5", "2.5", "1.5", "quit")
        assert any("Error" in line for line in outputs)

    def test_invalid_number_binary_shows_error(self):
        # Three bad inputs exhaust all retries for first number, then quit
        outputs = self._run("add", "abc", "xyz", "bad", "quit")
        assert any("Error" in line for line in outputs)

    def test_invalid_number_unary_shows_error(self):
        # Three bad inputs exhaust all retries, then quit
        outputs = self._run("square", "abc", "xyz", "bad", "quit")
        assert any("Error" in line for line in outputs)

    def test_retry_succeeds_on_second_attempt_binary(self):
        # First number fails once then succeeds; second number valid; result produced
        outputs = self._run("add", "abc", "3", "5", "quit")
        assert any("Error" in line for line in outputs)
        assert any("Result: 8.0" in line for line in outputs)

    def test_retry_succeeds_on_second_attempt_unary(self):
        # Number fails once then succeeds; result produced
        outputs = self._run("square", "abc", "4", "quit")
        assert any("Error" in line for line in outputs)
        assert any("Result: 16" in line for line in outputs)

    def test_all_retries_exhausted_returns_to_menu(self):
        # Exhaust all retries for first number, then a valid operation succeeds
        outputs = self._run("add", "bad1", "bad2", "bad3", "add", "2", "3", "quit")
        assert any("Error" in line for line in outputs)
        assert any("Result: 5.0" in line for line in outputs)

    def test_divide_by_zero_shows_error(self):
        outputs = self._run("divide", "10", "0", "quit")
        assert any("Error" in line for line in outputs)

    def test_square_root_negative_shows_error(self):
        outputs = self._run("square_root", "-1", "quit")
        assert any("Error" in line for line in outputs)

    def test_multiple_operations_in_sequence(self):
        outputs = self._run("add", "1", "2", "multiply", "3", "4", "quit")
        results = [line for line in outputs if line.startswith("Result:")]
        assert len(results) == 2
        assert "Result: 3.0" in results[0]
        assert "Result: 12.0" in results[1]


class TestRunCLI:
    """Tests for the non-interactive CLI (bash) mode in src/__main__.py."""

    def setup_method(self):
        self.calc = Calculator()

    def _run(self, *argv):
        """Helper: run CLI mode with given argv and capture output and exit code."""
        outputs = []
        code = run_cli(list(argv), self.calc, output_fn=outputs.append)
        return outputs, code

    def test_help_flag_short_exits_zero(self):
        outputs, code = self._run("-h")
        assert code == 0
        assert any("Usage" in line for line in outputs)

    def test_help_flag_long_exits_zero(self):
        outputs, code = self._run("--help")
        assert code == 0
        assert any("Usage" in line for line in outputs)

    def test_empty_argv_shows_usage_exits_zero(self):
        outputs, code = run_cli([], self.calc, output_fn=[].append), 0
        # empty list is the --help path; just ensure no crash
        outputs2 = []
        code2 = run_cli([], self.calc, output_fn=outputs2.append)
        assert code2 == 0

    def test_binary_add(self):
        outputs, code = self._run("add", "3", "5")
        assert code == 0
        assert any("Result: 8.0" in line for line in outputs)

    def test_binary_subtract(self):
        outputs, code = self._run("subtract", "10", "4")
        assert code == 0
        assert any("Result: 6.0" in line for line in outputs)

    def test_binary_multiply(self):
        outputs, code = self._run("multiply", "3", "4")
        assert code == 0
        assert any("Result: 12.0" in line for line in outputs)

    def test_binary_divide(self):
        outputs, code = self._run("divide", "10", "2")
        assert code == 0
        assert any("Result: 5.0" in line for line in outputs)

    def test_binary_power(self):
        outputs, code = self._run("power", "2", "8")
        assert code == 0
        assert any("Result: 256.0" in line for line in outputs)

    def test_unary_square(self):
        outputs, code = self._run("square", "4")
        assert code == 0
        assert any("Result: 16" in line for line in outputs)

    def test_unary_cube(self):
        outputs, code = self._run("cube", "3")
        assert code == 0
        assert any("Result: 27" in line for line in outputs)

    def test_unary_square_root(self):
        outputs, code = self._run("square_root", "9")
        assert code == 0
        assert any("Result: 3.0" in line for line in outputs)

    def test_unary_log(self):
        outputs, code = self._run("log", "100")
        assert code == 0
        assert any("Result: 2.0" in line for line in outputs)

    def test_unary_ln(self):
        outputs, code = self._run("ln", "1")
        assert code == 0
        assert any("Result: 0.0" in line for line in outputs)

    def test_factorial_valid(self):
        outputs, code = self._run("factorial", "5")
        assert code == 0
        assert any("Result: 120" in line for line in outputs)

    def test_unknown_operation_returns_error(self):
        outputs, code = self._run("foobar")
        assert code == 1
        assert any("Error" in line for line in outputs)

    def test_binary_op_missing_second_arg_returns_error(self):
        outputs, code = self._run("add", "5")
        assert code == 1
        assert any("Error" in line for line in outputs)

    def test_binary_op_missing_all_args_returns_error(self):
        outputs, code = self._run("multiply")
        assert code == 1
        assert any("Error" in line for line in outputs)

    def test_unary_op_missing_arg_returns_error(self):
        outputs, code = self._run("square")
        assert code == 1
        assert any("Error" in line for line in outputs)

    def test_invalid_number_binary_returns_error(self):
        outputs, code = self._run("add", "abc", "5")
        assert code == 1
        assert any("Error" in line for line in outputs)

    def test_invalid_number_unary_returns_error(self):
        outputs, code = self._run("square", "abc")
        assert code == 1
        assert any("Error" in line for line in outputs)

    def test_factorial_non_integer_returns_error(self):
        outputs, code = self._run("factorial", "3.5")
        assert code == 1
        assert any("Error" in line for line in outputs)

    def test_divide_by_zero_returns_error(self):
        outputs, code = self._run("divide", "10", "0")
        assert code == 1
        assert any("Error" in line for line in outputs)

    def test_square_root_negative_returns_error(self):
        outputs, code = self._run("square_root", "-1")
        assert code == 1
        assert any("Error" in line for line in outputs)

    def test_operation_case_insensitive(self):
        outputs, code = self._run("ADD", "3", "5")
        assert code == 0
        assert any("Result: 8.0" in line for line in outputs)


class TestCalculatorHistory:
    """Tests for the operation history feature on the Calculator class."""

    def setup_method(self):
        self.calc = Calculator()

    def test_history_starts_empty(self):
        assert self.calc.get_history() == []

    def test_history_records_successful_binary_operation(self):
        self.calc.add(3, 5)
        history = self.calc.get_history()
        assert len(history) == 1
        assert history[0]["operation"] == "add"
        assert history[0]["operands"] == (3, 5)
        assert history[0]["result"] == 8

    def test_history_records_successful_unary_operation(self):
        self.calc.square(4)
        history = self.calc.get_history()
        assert len(history) == 1
        assert history[0]["operation"] == "square"
        assert history[0]["operands"] == (4,)
        assert history[0]["result"] == 16

    def test_history_records_multiple_operations_in_order(self):
        self.calc.add(1, 2)
        self.calc.multiply(3, 4)
        self.calc.factorial(5)
        history = self.calc.get_history()
        assert len(history) == 3
        assert history[0]["operation"] == "add"
        assert history[1]["operation"] == "multiply"
        assert history[2]["operation"] == "factorial"

    def test_history_does_not_record_failed_operation(self):
        with pytest.raises(ValueError):
            self.calc.divide(10, 0)
        assert self.calc.get_history() == []

    def test_history_does_not_record_failed_sqrt(self):
        with pytest.raises(ValueError):
            self.calc.square_root(-1)
        assert self.calc.get_history() == []

    def test_history_does_not_record_failed_factorial(self):
        with pytest.raises(TypeError):
            self.calc.factorial(3.5)
        assert self.calc.get_history() == []

    def test_clear_history_removes_all_entries(self):
        self.calc.add(1, 2)
        self.calc.subtract(5, 3)
        self.calc.clear_history()
        assert self.calc.get_history() == []

    def test_get_history_returns_copy(self):
        self.calc.add(1, 2)
        history = self.calc.get_history()
        history.clear()
        # Internal history must not be affected by mutation of the returned list
        assert len(self.calc.get_history()) == 1

    def test_history_records_all_operations(self):
        self.calc.add(1, 1)
        self.calc.subtract(5, 2)
        self.calc.multiply(3, 3)
        self.calc.divide(8, 2)
        self.calc.power(2, 3)
        self.calc.factorial(4)
        self.calc.square(5)
        self.calc.cube(2)
        self.calc.square_root(9)
        self.calc.cube_root(27)
        self.calc.log(100)
        self.calc.ln(1)
        assert len(self.calc.get_history()) == 12


class TestRunInteractiveHistory:
    """Tests for history commands in the interactive session."""

    def setup_method(self):
        self.calc = Calculator()

    def _run(self, *responses):
        responses_iter = iter(responses)

        def fake_input(prompt=""):
            return next(responses_iter)

        outputs = []
        run_interactive(self.calc, input_fn=fake_input, output_fn=outputs.append)
        return outputs

    def test_welcome_message_mentions_history(self):
        outputs = self._run("quit")
        assert any("history" in line.lower() for line in outputs)

    def test_history_command_empty_shows_no_history(self):
        outputs = self._run("history", "quit")
        assert any("No history yet" in line for line in outputs)

    def test_history_command_shows_previous_operations(self):
        outputs = self._run("add", "3", "5", "history", "quit")
        history_lines = [line for line in outputs if "add" in line and "=" in line]
        assert len(history_lines) == 1
        assert "8" in history_lines[0]

    def test_history_shows_multiple_entries(self):
        outputs = self._run("add", "1", "2", "multiply", "3", "4", "history", "quit")
        history_lines = [line for line in outputs if "=" in line and any(
            op in line for op in ("add", "multiply")
        )]
        assert len(history_lines) == 2

    def test_clear_history_command_empties_history(self):
        outputs = self._run("add", "1", "2", "clear_history", "history", "quit")
        assert any("cleared" in line.lower() for line in outputs)
        assert any("No history yet" in line for line in outputs)

    def test_failed_operation_not_in_history(self):
        outputs = self._run("divide", "10", "0", "history", "quit")
        assert any("Error" in line for line in outputs)
        assert any("No history yet" in line for line in outputs)


class TestCalculatorErrorLogging:
    """Verify that Calculator emits ERROR log records for each invalid-input condition."""

    def setup_method(self):
        self.calc = Calculator()

    def test_divide_by_zero_logs_error(self, caplog):
        import logging
        with caplog.at_level(logging.ERROR, logger="src.calculator"):
            with pytest.raises(ValueError):
                self.calc.divide(10, 0)
        assert any("divide" in r.message and "b=0" in r.message for r in caplog.records)

    def test_factorial_non_integer_logs_error(self, caplog):
        import logging
        with caplog.at_level(logging.ERROR, logger="src.calculator"):
            with pytest.raises(TypeError):
                self.calc.factorial(3.5)
        assert any("factorial" in r.message and "non-integer" in r.message for r in caplog.records)

    def test_factorial_negative_logs_error(self, caplog):
        import logging
        with caplog.at_level(logging.ERROR, logger="src.calculator"):
            with pytest.raises(ValueError):
                self.calc.factorial(-1)
        assert any("factorial" in r.message and "negative" in r.message for r in caplog.records)

    def test_square_root_negative_logs_error(self, caplog):
        import logging
        with caplog.at_level(logging.ERROR, logger="src.calculator"):
            with pytest.raises(ValueError):
                self.calc.square_root(-4)
        assert any("square_root" in r.message and "negative" in r.message for r in caplog.records)

    def test_log_non_positive_logs_error(self, caplog):
        import logging
        with caplog.at_level(logging.ERROR, logger="src.calculator"):
            with pytest.raises(ValueError):
                self.calc.log(0)
        assert any("log" in r.message and "non-positive" in r.message for r in caplog.records)

    def test_ln_non_positive_logs_error(self, caplog):
        import logging
        with caplog.at_level(logging.ERROR, logger="src.calculator"):
            with pytest.raises(ValueError):
                self.calc.ln(-1)
        assert any("ln" in r.message and "non-positive" in r.message for r in caplog.records)

    def test_successful_operations_produce_no_error_logs(self, caplog):
        import logging
        with caplog.at_level(logging.ERROR, logger="src.calculator"):
            self.calc.add(1, 2)
            self.calc.divide(10, 2)
            self.calc.factorial(5)
            self.calc.square_root(9)
            self.calc.log(10)
            self.calc.ln(1)
        assert caplog.records == []

    def test_error_log_level_is_error(self, caplog):
        import logging
        with caplog.at_level(logging.ERROR, logger="src.calculator"):
            with pytest.raises(ValueError):
                self.calc.divide(5, 0)
        assert all(r.levelno == logging.ERROR for r in caplog.records)
