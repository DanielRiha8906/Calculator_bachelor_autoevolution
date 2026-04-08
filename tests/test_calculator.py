import pytest
import math
from src.calculator import Calculator


@pytest.fixture
def calc():
    return Calculator()


# --- Addition ---

def test_add_positive_numbers(calc):
    assert calc.add(2, 3) == 5

def test_add_negative_numbers(calc):
    assert calc.add(-4, -6) == -10

def test_add_positive_and_negative(calc):
    assert calc.add(10, -3) == 7

def test_add_zero(calc):
    assert calc.add(0, 0) == 0

def test_add_floats(calc):
    assert math.isclose(calc.add(1.1, 2.2), 3.3)


# --- Subtraction ---

def test_subtract_positive_numbers(calc):
    assert calc.subtract(10, 4) == 6

def test_subtract_negative_numbers(calc):
    assert calc.subtract(-3, -7) == 4

def test_subtract_resulting_in_negative(calc):
    assert calc.subtract(2, 9) == -7

def test_subtract_same_number(calc):
    assert calc.subtract(5, 5) == 0

def test_subtract_floats(calc):
    assert math.isclose(calc.subtract(5.5, 2.2), 3.3)


# --- Multiplication ---

def test_multiply_positive_numbers(calc):
    assert calc.multiply(3, 4) == 12

def test_multiply_negative_numbers(calc):
    assert calc.multiply(-3, -4) == 12

def test_multiply_positive_and_negative(calc):
    assert calc.multiply(5, -3) == -15

def test_multiply_by_zero(calc):
    assert calc.multiply(99, 0) == 0

def test_multiply_floats(calc):
    assert math.isclose(calc.multiply(2.5, 4.0), 10.0)


# --- Division ---

def test_divide_positive_numbers(calc):
    assert calc.divide(10, 2) == 5

def test_divide_negative_numbers(calc):
    assert calc.divide(-12, -4) == 3

def test_divide_positive_by_negative(calc):
    assert calc.divide(9, -3) == -3

def test_divide_resulting_in_float(calc):
    assert math.isclose(calc.divide(7, 2), 3.5)

def test_divide_by_zero_raises_value_error():
    calc = Calculator()
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calc.divide(10, 0)
