import pytest
import math
from src.calculator import Calculator


class TestDivideInvalidInputs:
    def setup_method(self):
        self.calc = Calculator()

    def test_divide_by_zero_raises(self):
        with pytest.raises(ZeroDivisionError):
            self.calc.divide(10, 0)

    def test_divide_by_zero_float_raises(self):
        with pytest.raises(ZeroDivisionError):
            self.calc.divide(5.0, 0)

    def test_divide_string_numerator_raises(self):
        with pytest.raises(TypeError):
            self.calc.divide("10", 2)

    def test_divide_string_denominator_raises(self):
        with pytest.raises(TypeError):
            self.calc.divide(10, "2")

    def test_divide_none_numerator_raises(self):
        with pytest.raises(TypeError):
            self.calc.divide(None, 2)

    def test_divide_none_denominator_raises(self):
        with pytest.raises(TypeError):
            self.calc.divide(10, None)
