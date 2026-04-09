import pytest
import math
from src.calculator import Calculator


class TestDivideByZero:
    def test_divide_by_zero_raises(self):
        calc = Calculator()
        with pytest.raises(ZeroDivisionError):
            calc.divide(1, 0)

    def test_divide_by_zero_float_raises(self):
        calc = Calculator()
        with pytest.raises(ZeroDivisionError):
            calc.divide(5.0, 0)

    def test_divide_by_zero_negative_raises(self):
        calc = Calculator()
        with pytest.raises(ZeroDivisionError):
            calc.divide(-3, 0)
