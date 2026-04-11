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