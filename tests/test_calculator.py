import pytest
import math
from src.calculator import Calculator


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def calc():
    return Calculator()


# ---------------------------------------------------------------------------
# add
# ---------------------------------------------------------------------------

def test_add_positive_integers(calc):
    assert calc.add(3, 4) == 7


def test_add_negative_integers(calc):
    assert calc.add(-3, -4) == -7


def test_add_mixed_sign(calc):
    assert calc.add(-3, 4) == 1


def test_add_zeros(calc):
    assert calc.add(0, 0) == 0


def test_add_floats(calc):
    assert calc.add(0.1, 0.2) == pytest.approx(0.3)


def test_add_large_numbers(calc):
    assert calc.add(10**9, 10**9) == 2 * 10**9


# ---------------------------------------------------------------------------
# subtract
# ---------------------------------------------------------------------------

def test_subtract_positive_integers(calc):
    assert calc.subtract(10, 4) == 6


def test_subtract_resulting_negative(calc):
    assert calc.subtract(4, 10) == -6


def test_subtract_zeros(calc):
    assert calc.subtract(0, 0) == 0


def test_subtract_floats(calc):
    assert calc.subtract(1.5, 0.5) == pytest.approx(1.0)


def test_subtract_negative_operand(calc):
    assert calc.subtract(5, -3) == 8


# ---------------------------------------------------------------------------
# multiply
# ---------------------------------------------------------------------------

def test_multiply_positive_integers(calc):
    assert calc.multiply(3, 4) == 12


def test_multiply_by_zero(calc):
    assert calc.multiply(99, 0) == 0


def test_multiply_negative_numbers(calc):
    assert calc.multiply(-3, -4) == 12


def test_multiply_mixed_sign(calc):
    assert calc.multiply(-3, 4) == -12


def test_multiply_floats(calc):
    assert calc.multiply(0.1, 3.0) == pytest.approx(0.3)


def test_multiply_by_one(calc):
    assert calc.multiply(7, 1) == 7


def test_multiply_large_numbers(calc):
    assert calc.multiply(10**6, 10**6) == 10**12


# ---------------------------------------------------------------------------
# divide
# ---------------------------------------------------------------------------

def test_divide_positive_integers(calc):
    assert calc.divide(10, 2) == 5.0


def test_divide_non_even(calc):
    assert calc.divide(10, 3) == pytest.approx(3.3333333)


def test_divide_by_one(calc):
    assert calc.divide(7, 1) == 7.0


def test_divide_negative_dividend(calc):
    assert calc.divide(-10, 2) == -5.0


def test_divide_negative_divisor(calc):
    assert calc.divide(10, -2) == -5.0


def test_divide_both_negative(calc):
    assert calc.divide(-10, -2) == 5.0


def test_divide_floats(calc):
    assert calc.divide(1.0, 3.0) == pytest.approx(0.3333333)


def test_divide_zero_numerator(calc):
    assert calc.divide(0, 5) == 0.0


def test_divide_by_zero_raises(calc):
    with pytest.raises(ZeroDivisionError):
        calc.divide(1, 0)


def test_divide_by_zero_float_raises(calc):
    with pytest.raises(ZeroDivisionError):
        calc.divide(1.0, 0)
