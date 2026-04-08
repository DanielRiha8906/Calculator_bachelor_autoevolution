import pytest
import math
from src.calculator import Calculator


def test_divide_by_zero_raises_value_error():
    calc = Calculator()
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calc.divide(10, 0)