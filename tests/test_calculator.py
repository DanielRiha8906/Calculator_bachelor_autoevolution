import logging
import pytest
import math
from src.calculator import Calculator


class TestAddition:
    def setup_method(self):
        self.calc = Calculator()

    def test_add_two_positive_integers(self):
        assert self.calc.add(3, 5) == 8

    def test_add_two_negative_integers(self):
        assert self.calc.add(-3, -5) == -8

    def test_add_positive_and_negative(self):
        assert self.calc.add(10, -3) == 7

    def test_add_zero(self):
        assert self.calc.add(5, 0) == 5

    def test_add_floats(self):
        assert self.calc.add(1.5, 2.5) == 4.0

    def test_add_float_and_integer(self):
        assert self.calc.add(1.5, 2) == 3.5


class TestSubtraction:
    def setup_method(self):
        self.calc = Calculator()

    def test_subtract_two_positive_integers(self):
        assert self.calc.subtract(10, 3) == 7

    def test_subtract_results_in_negative(self):
        assert self.calc.subtract(3, 10) == -7

    def test_subtract_negative_number(self):
        assert self.calc.subtract(5, -3) == 8

    def test_subtract_zero(self):
        assert self.calc.subtract(5, 0) == 5

    def test_subtract_floats(self):
        assert self.calc.subtract(2.5, 1.5) == pytest.approx(1.0)

    def test_subtract_same_values(self):
        assert self.calc.subtract(5, 5) == 0


class TestMultiplication:
    def setup_method(self):
        self.calc = Calculator()

    def test_multiply_two_positive_integers(self):
        assert self.calc.multiply(3, 4) == 12

    def test_multiply_by_zero(self):
        assert self.calc.multiply(5, 0) == 0

    def test_multiply_negative(self):
        assert self.calc.multiply(-3, 4) == -12

    def test_multiply_two_negatives(self):
        assert self.calc.multiply(-3, -4) == 12

    def test_multiply_floats(self):
        assert self.calc.multiply(2.5, 2.0) == pytest.approx(5.0)

    def test_multiply_by_one(self):
        assert self.calc.multiply(7, 1) == 7


class TestDivision:
    def setup_method(self):
        self.calc = Calculator()

    def test_divide_two_integers(self):
        assert self.calc.divide(10, 2) == 5.0

    def test_divide_result_float(self):
        assert self.calc.divide(5, 2) == pytest.approx(2.5)

    def test_divide_negative_by_positive(self):
        assert self.calc.divide(-10, 2) == -5.0

    def test_divide_negative_by_negative(self):
        assert self.calc.divide(-10, -2) == 5.0

    def test_divide_floats(self):
        assert self.calc.divide(5.0, 2.0) == pytest.approx(2.5)

    def test_divide_by_one(self):
        assert self.calc.divide(7, 1) == 7.0


class TestDivisionIncorrectInputs:
    def setup_method(self):
        self.calc = Calculator()

    def test_divide_by_zero(self):
        with pytest.raises(ZeroDivisionError):
            self.calc.divide(10, 0)

    def test_divide_by_zero_float(self):
        with pytest.raises(ZeroDivisionError):
            self.calc.divide(5.0, 0)

    def test_divide_string_numerator(self):
        with pytest.raises(TypeError):
            self.calc.divide("ten", 2)

    def test_divide_string_denominator(self):
        with pytest.raises(TypeError):
            self.calc.divide(10, "two")

    def test_divide_none_numerator(self):
        with pytest.raises(TypeError):
            self.calc.divide(None, 2)

    def test_divide_none_denominator(self):
        with pytest.raises(TypeError):
            self.calc.divide(10, None)


class TestFactorial:
    def setup_method(self):
        self.calc = Calculator()

    def test_factorial_zero(self):
        assert self.calc.factorial(0) == 1

    def test_factorial_one(self):
        assert self.calc.factorial(1) == 1

    def test_factorial_small_positive(self):
        assert self.calc.factorial(5) == 120

    def test_factorial_larger_positive(self):
        assert self.calc.factorial(10) == 3628800


class TestFactorialIncorrectInputs:
    def setup_method(self):
        self.calc = Calculator()

    def test_factorial_negative(self):
        with pytest.raises(ValueError):
            self.calc.factorial(-1)

    def test_factorial_float(self):
        with pytest.raises(TypeError):
            self.calc.factorial(2.5)

    def test_factorial_string(self):
        with pytest.raises(TypeError):
            self.calc.factorial("five")

    def test_factorial_none(self):
        with pytest.raises(TypeError):
            self.calc.factorial(None)


class TestSquare:
    def setup_method(self):
        self.calc = Calculator()

    def test_square_positive_integer(self):
        assert self.calc.square(4) == 16

    def test_square_negative_integer(self):
        assert self.calc.square(-3) == 9

    def test_square_zero(self):
        assert self.calc.square(0) == 0

    def test_square_float(self):
        assert self.calc.square(2.5) == pytest.approx(6.25)

    def test_square_one(self):
        assert self.calc.square(1) == 1


class TestCube:
    def setup_method(self):
        self.calc = Calculator()

    def test_cube_positive_integer(self):
        assert self.calc.cube(3) == 27

    def test_cube_negative_integer(self):
        assert self.calc.cube(-2) == -8

    def test_cube_zero(self):
        assert self.calc.cube(0) == 0

    def test_cube_float(self):
        assert self.calc.cube(2.0) == pytest.approx(8.0)

    def test_cube_one(self):
        assert self.calc.cube(1) == 1


class TestSquareRoot:
    def setup_method(self):
        self.calc = Calculator()

    def test_square_root_perfect_square(self):
        assert self.calc.square_root(9) == pytest.approx(3.0)

    def test_square_root_non_perfect_square(self):
        assert self.calc.square_root(2) == pytest.approx(math.sqrt(2))

    def test_square_root_zero(self):
        assert self.calc.square_root(0) == pytest.approx(0.0)

    def test_square_root_float_input(self):
        assert self.calc.square_root(6.25) == pytest.approx(2.5)


class TestSquareRootIncorrectInputs:
    def setup_method(self):
        self.calc = Calculator()

    def test_square_root_negative(self):
        with pytest.raises(ValueError):
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

    def test_cube_root_float_input(self):
        assert self.calc.cube_root(8.0) == pytest.approx(2.0)


class TestPower:
    def setup_method(self):
        self.calc = Calculator()

    def test_power_positive_base_integer_exp(self):
        assert self.calc.power(2, 3) == pytest.approx(8.0)

    def test_power_base_to_zero(self):
        assert self.calc.power(5, 0) == pytest.approx(1.0)

    def test_power_base_to_one(self):
        assert self.calc.power(7, 1) == pytest.approx(7.0)

    def test_power_float_exponent(self):
        assert self.calc.power(4, 0.5) == pytest.approx(2.0)

    def test_power_fractional_base(self):
        assert self.calc.power(0.5, 2) == pytest.approx(0.25)


class TestLog:
    def setup_method(self):
        self.calc = Calculator()

    def test_log_of_one(self):
        assert self.calc.log(1) == pytest.approx(0.0)

    def test_log_of_ten(self):
        assert self.calc.log(10) == pytest.approx(1.0)

    def test_log_of_hundred(self):
        assert self.calc.log(100) == pytest.approx(2.0)

    def test_log_of_float(self):
        assert self.calc.log(0.1) == pytest.approx(-1.0)


class TestLogIncorrectInputs:
    def setup_method(self):
        self.calc = Calculator()

    def test_log_of_zero(self):
        with pytest.raises(ValueError):
            self.calc.log(0)

    def test_log_of_negative(self):
        with pytest.raises(ValueError):
            self.calc.log(-1)


class TestLn:
    def setup_method(self):
        self.calc = Calculator()

    def test_ln_of_one(self):
        assert self.calc.ln(1) == pytest.approx(0.0)

    def test_ln_of_e(self):
        assert self.calc.ln(math.e) == pytest.approx(1.0)

    def test_ln_of_e_squared(self):
        assert self.calc.ln(math.e ** 2) == pytest.approx(2.0)

    def test_ln_of_float(self):
        assert self.calc.ln(0.5) == pytest.approx(math.log(0.5))


class TestLnIncorrectInputs:
    def setup_method(self):
        self.calc = Calculator()

    def test_ln_of_zero(self):
        with pytest.raises(ValueError):
            self.calc.ln(0)

    def test_ln_of_negative(self):
        with pytest.raises(ValueError):
            self.calc.ln(-1)


class TestHistory:
    def setup_method(self):
        self.calc = Calculator()

    def test_history_starts_empty(self):
        assert self.calc.get_history() == []

    def test_history_records_successful_operation(self):
        self.calc.add(3, 5)
        history = self.calc.get_history()
        assert len(history) == 1
        assert history[0]["operation"] == "add"
        assert history[0]["args"] == [3, 5]
        assert history[0]["result"] == 8

    def test_history_records_multiple_operations(self):
        self.calc.add(1, 2)
        self.calc.multiply(3, 4)
        history = self.calc.get_history()
        assert len(history) == 2
        assert history[0]["operation"] == "add"
        assert history[1]["operation"] == "multiply"

    def test_history_not_recorded_on_error(self):
        with pytest.raises(ZeroDivisionError):
            self.calc.divide(1, 0)
        assert self.calc.get_history() == []

    def test_clear_history_empties_list(self):
        self.calc.add(1, 2)
        self.calc.clear_history()
        assert self.calc.get_history() == []

    def test_get_history_returns_copy(self):
        self.calc.add(1, 2)
        returned = self.calc.get_history()
        returned.clear()
        assert len(self.calc.get_history()) == 1

    def test_history_records_single_arg_operation(self):
        self.calc.square(4)
        history = self.calc.get_history()
        assert len(history) == 1
        assert history[0]["operation"] == "square"
        assert history[0]["args"] == [4]
        assert history[0]["result"] == 16

    def test_history_records_factorial(self):
        self.calc.factorial(5)
        history = self.calc.get_history()
        assert history[0]["operation"] == "factorial"
        assert history[0]["result"] == 120


class TestCalculatorErrorLogging:
    def setup_method(self):
        self.calc = Calculator()

    def test_divide_by_zero_is_logged(self, caplog):
        with caplog.at_level(logging.ERROR, logger="src.calculator"):
            with pytest.raises(ZeroDivisionError):
                self.calc.divide(10, 0)
        assert len(caplog.records) == 1
        assert "divide" in caplog.records[0].message

    def test_square_root_negative_is_logged(self, caplog):
        with caplog.at_level(logging.ERROR, logger="src.calculator"):
            with pytest.raises(ValueError):
                self.calc.square_root(-1)
        assert len(caplog.records) == 1
        assert "square_root" in caplog.records[0].message

    def test_log_zero_is_logged(self, caplog):
        with caplog.at_level(logging.ERROR, logger="src.calculator"):
            with pytest.raises(ValueError):
                self.calc.log(0)
        assert len(caplog.records) == 1
        assert "log" in caplog.records[0].message

    def test_ln_negative_is_logged(self, caplog):
        with caplog.at_level(logging.ERROR, logger="src.calculator"):
            with pytest.raises(ValueError):
                self.calc.ln(-1)
        assert len(caplog.records) == 1
        assert "ln" in caplog.records[0].message

    def test_factorial_negative_is_logged(self, caplog):
        with caplog.at_level(logging.ERROR, logger="src.calculator"):
            with pytest.raises(ValueError):
                self.calc.factorial(-1)
        assert len(caplog.records) == 1
        assert "factorial" in caplog.records[0].message

    def test_successful_operation_does_not_log_error(self, caplog):
        with caplog.at_level(logging.ERROR, logger="src.calculator"):
            self.calc.add(3, 5)
        assert len(caplog.records) == 0