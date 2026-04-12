import pytest
import math
from src.calculator import Calculator


class TestAdd:
    def setup_method(self):
        self.calc = Calculator()

    def test_add_positive_integers(self):
        assert self.calc.add(3, 5) == 8

    def test_add_negative_integers(self):
        assert self.calc.add(-3, -5) == -8

    def test_add_mixed_sign(self):
        assert self.calc.add(-3, 5) == 2

    def test_add_zero(self):
        assert self.calc.add(0, 5) == 5

    def test_add_floats(self):
        assert math.isclose(self.calc.add(1.1, 2.2), 3.3)

    def test_add_invalid_type_raises(self):
        with pytest.raises(TypeError):
            self.calc.add("a", 1)


class TestSubtract:
    def setup_method(self):
        self.calc = Calculator()

    def test_subtract_positive_integers(self):
        assert self.calc.subtract(10, 5) == 5

    def test_subtract_result_negative(self):
        assert self.calc.subtract(3, 8) == -5

    def test_subtract_zero(self):
        assert self.calc.subtract(5, 0) == 5

    def test_subtract_floats(self):
        assert math.isclose(self.calc.subtract(5.5, 2.2), 3.3)

    def test_subtract_invalid_type_raises(self):
        with pytest.raises(TypeError):
            self.calc.subtract("a", 1)


class TestMultiply:
    def setup_method(self):
        self.calc = Calculator()

    def test_multiply_positive_integers(self):
        assert self.calc.multiply(3, 4) == 12

    def test_multiply_by_zero(self):
        assert self.calc.multiply(5, 0) == 0

    def test_multiply_negative_numbers(self):
        assert self.calc.multiply(-3, -4) == 12

    def test_multiply_mixed_sign(self):
        assert self.calc.multiply(-3, 4) == -12

    def test_multiply_floats(self):
        assert math.isclose(self.calc.multiply(2.5, 4.0), 10.0)

    def test_multiply_invalid_type_raises(self):
        with pytest.raises(TypeError):
            self.calc.multiply(None, 5)


class TestDivide:
    def setup_method(self):
        self.calc = Calculator()

    def test_divide_positive_integers(self):
        assert self.calc.divide(10, 2) == 5

    def test_divide_result_float(self):
        assert math.isclose(self.calc.divide(7, 2), 3.5)

    def test_divide_by_zero_raises(self):
        with pytest.raises(ZeroDivisionError):
            self.calc.divide(1, 0)

    def test_divide_negative_by_positive(self):
        assert self.calc.divide(-10, 2) == -5

    def test_divide_floats(self):
        assert math.isclose(self.calc.divide(7.5, 2.5), 3.0)

    def test_divide_zero_numerator(self):
        assert self.calc.divide(0, 5) == 0

    def test_divide_invalid_type_raises(self):
        with pytest.raises(TypeError):
            self.calc.divide("a", 2)
