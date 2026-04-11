import pytest
import math
from src.calculator import Calculator


@pytest.fixture
def calc():
    return Calculator()


# --- add ---

def test_add_positive_numbers(calc):
    assert calc.add(2, 3) == 5


def test_add_negative_numbers(calc):
    assert calc.add(-5, -3) == -8


def test_add_mixed_sign(calc):
    assert calc.add(-1, 1) == 0


def test_add_zeros(calc):
    assert calc.add(0, 0) == 0


def test_add_floats(calc):
    assert calc.add(1.5, 2.5) == 4.0


# --- subtract ---

def test_subtract_positive_numbers(calc):
    assert calc.subtract(5, 3) == 2


def test_subtract_negative_numbers(calc):
    assert calc.subtract(-3, -5) == 2


def test_subtract_to_negative(calc):
    assert calc.subtract(0, 5) == -5


def test_subtract_zeros(calc):
    assert calc.subtract(0, 0) == 0


def test_subtract_floats(calc):
    assert calc.subtract(3.5, 1.5) == 2.0


# --- multiply ---

def test_multiply_positive_numbers(calc):
    assert calc.multiply(3, 4) == 12


def test_multiply_by_zero(calc):
    assert calc.multiply(5, 0) == 0


def test_multiply_negative_and_positive(calc):
    assert calc.multiply(-2, 3) == -6


def test_multiply_negative_numbers(calc):
    assert calc.multiply(-2, -3) == 6


def test_multiply_floats(calc):
    assert calc.multiply(2.5, 4) == 10.0


# --- divide ---

def test_divide_even(calc):
    assert calc.divide(10, 2) == 5.0


def test_divide_zero_numerator(calc):
    assert calc.divide(0, 5) == 0.0


def test_divide_negative_numerator(calc):
    assert calc.divide(-10, 2) == -5.0


def test_divide_negative_denominator(calc):
    assert calc.divide(10, -2) == -5.0


def test_divide_returns_float(calc):
    assert calc.divide(7, 2) == 3.5


def test_divide_by_zero_raises():
    calc = Calculator()
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        calc.divide(10, 0)


# --- factorial ---

def test_factorial_zero(calc):
    assert calc.factorial(0) == 1


def test_factorial_one(calc):
    assert calc.factorial(1) == 1


def test_factorial_positive(calc):
    assert calc.factorial(5) == 120


def test_factorial_large(calc):
    assert calc.factorial(10) == 3628800


def test_factorial_negative_raises(calc):
    with pytest.raises(ValueError, match="not defined for negative"):
        calc.factorial(-1)


def test_factorial_non_integer_raises(calc):
    with pytest.raises(ValueError, match="non-negative integer"):
        calc.factorial(2.5)
