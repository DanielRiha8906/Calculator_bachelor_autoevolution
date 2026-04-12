import pytest
import math
from src.calculator import Calculator


@pytest.fixture
def calc():
    return Calculator()


# ---------------------------------------------------------------------------
# add
# ---------------------------------------------------------------------------

def test_add_positive_numbers(calc):
    assert calc.add(2, 3) == 5


def test_add_negative_numbers(calc):
    assert calc.add(-4, -6) == -10


def test_add_mixed_sign(calc):
    assert calc.add(-3, 7) == 4


def test_add_zero(calc):
    assert calc.add(0, 5) == 5
    assert calc.add(5, 0) == 5


def test_add_floats(calc):
    assert math.isclose(calc.add(1.1, 2.2), 3.3)


# ---------------------------------------------------------------------------
# subtract
# ---------------------------------------------------------------------------

def test_subtract_positive_numbers(calc):
    assert calc.subtract(10, 4) == 6


def test_subtract_negative_numbers(calc):
    assert calc.subtract(-5, -3) == -2


def test_subtract_mixed_sign(calc):
    assert calc.subtract(3, -7) == 10


def test_subtract_zero(calc):
    assert calc.subtract(9, 0) == 9
    assert calc.subtract(0, 9) == -9


def test_subtract_floats(calc):
    assert math.isclose(calc.subtract(5.5, 2.2), 3.3)


def test_subtract_same_number_gives_zero(calc):
    assert calc.subtract(42, 42) == 0


# ---------------------------------------------------------------------------
# multiply
# ---------------------------------------------------------------------------

def test_multiply_positive_numbers(calc):
    assert calc.multiply(3, 4) == 12


def test_multiply_negative_numbers(calc):
    assert calc.multiply(-3, -4) == 12


def test_multiply_mixed_sign(calc):
    assert calc.multiply(-3, 4) == -12


def test_multiply_by_zero(calc):
    assert calc.multiply(99, 0) == 0
    assert calc.multiply(0, 99) == 0


def test_multiply_by_one(calc):
    assert calc.multiply(7, 1) == 7
    assert calc.multiply(1, 7) == 7


def test_multiply_floats(calc):
    assert math.isclose(calc.multiply(2.5, 4.0), 10.0)


# ---------------------------------------------------------------------------
# divide
# ---------------------------------------------------------------------------

def test_divide_by_zero_raises(calc):
    with pytest.raises(ValueError, match="Division by zero is not allowed"):
        calc.divide(10, 0)


def test_divide_normal(calc):
    assert calc.divide(10, 2) == 5.0


def test_divide_negative_denominator(calc):
    assert calc.divide(9, -3) == -3.0


def test_divide_negative_numerator(calc):
    assert calc.divide(-8, 4) == -2.0


def test_divide_both_negative(calc):
    assert calc.divide(-12, -4) == 3.0


def test_divide_floats(calc):
    assert math.isclose(calc.divide(7.5, 2.5), 3.0)


def test_divide_result_is_fraction(calc):
    assert math.isclose(calc.divide(1, 3), 1 / 3)


# ---------------------------------------------------------------------------
# factorial
# ---------------------------------------------------------------------------

def test_factorial_zero(calc):
    assert calc.factorial(0) == 1


def test_factorial_one(calc):
    assert calc.factorial(1) == 1


def test_factorial_small(calc):
    assert calc.factorial(5) == 120


def test_factorial_large(calc):
    assert calc.factorial(10) == 3628800


def test_factorial_negative_raises(calc):
    with pytest.raises(ValueError, match="Factorial is not defined for negative integers"):
        calc.factorial(-1)


def test_factorial_float_raises(calc):
    with pytest.raises(ValueError, match="Factorial is only defined for non-negative integers"):
        calc.factorial(3.0)
