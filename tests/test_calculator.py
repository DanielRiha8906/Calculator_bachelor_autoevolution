import pytest
import math
from src.calculator import Calculator


@pytest.fixture
def calc():
    return Calculator()


def test_divide_by_zero_raises(calc):
    with pytest.raises(ValueError, match="Division by zero is not allowed"):
        calc.divide(10, 0)


def test_divide_normal(calc):
    assert calc.divide(10, 2) == 5.0


def test_divide_negative_denominator(calc):
    assert calc.divide(9, -3) == -3.0
