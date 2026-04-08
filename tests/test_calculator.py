import pytest
import math
from src.calculator import Calculator


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
