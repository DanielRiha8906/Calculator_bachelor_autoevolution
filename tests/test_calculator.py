import pytest
import math
from src.calculator import Calculator


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