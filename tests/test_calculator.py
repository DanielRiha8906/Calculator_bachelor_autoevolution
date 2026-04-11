import pytest
import math
from src.calculator import Calculator


def test_divide_by_zero_raises_error():
    calc = Calculator()
    with pytest.raises(ZeroDivisionError):
        calc.divide(10, 0)