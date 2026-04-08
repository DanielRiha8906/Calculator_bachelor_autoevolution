import pytest
import math
from src.calculator import Calculator


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
