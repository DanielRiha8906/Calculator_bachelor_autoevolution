import pytest
import math
from src.calculator import Calculator


# --- add ---

def test_add_positive_numbers():
    calc = Calculator()
    assert calc.add(2, 3) == 5


def test_add_negative_numbers():
    calc = Calculator()
    assert calc.add(-4, -6) == -10


def test_add_mixed_sign():
    calc = Calculator()
    assert calc.add(-3, 7) == 4


def test_add_zeros():
    calc = Calculator()
    assert calc.add(0, 0) == 0


def test_add_floats():
    calc = Calculator()
    assert calc.add(0.1, 0.2) == pytest.approx(0.3)


# --- subtract ---

def test_subtract_positive_numbers():
    calc = Calculator()
    assert calc.subtract(10, 4) == 6


def test_subtract_negative_numbers():
    calc = Calculator()
    assert calc.subtract(-3, -5) == 2


def test_subtract_mixed_sign():
    calc = Calculator()
    assert calc.subtract(5, -3) == 8


def test_subtract_same_values():
    calc = Calculator()
    assert calc.subtract(7, 7) == 0


def test_subtract_floats():
    calc = Calculator()
    assert calc.subtract(1.5, 0.5) == pytest.approx(1.0)


# --- multiply ---

def test_multiply_positive_numbers():
    calc = Calculator()
    assert calc.multiply(3, 4) == 12


def test_multiply_negative_numbers():
    calc = Calculator()
    assert calc.multiply(-3, -4) == 12


def test_multiply_mixed_sign():
    calc = Calculator()
    assert calc.multiply(3, -4) == -12


def test_multiply_by_zero():
    calc = Calculator()
    assert calc.multiply(99, 0) == 0


def test_multiply_by_one():
    calc = Calculator()
    assert calc.multiply(7, 1) == 7


def test_multiply_floats():
    calc = Calculator()
    assert calc.multiply(2.5, 4.0) == pytest.approx(10.0)


# --- divide ---

def test_divide_by_zero_raises():
    calc = Calculator()
    with pytest.raises(ZeroDivisionError):
        calc.divide(10, 0)


def test_divide_positive_numbers():
    calc = Calculator()
    assert calc.divide(10, 2) == 5.0


def test_divide_negative_numbers():
    calc = Calculator()
    assert calc.divide(-12, -4) == 3.0


def test_divide_mixed_sign():
    calc = Calculator()
    assert calc.divide(9, -3) == -3.0


def test_divide_by_one():
    calc = Calculator()
    assert calc.divide(42, 1) == 42.0


def test_divide_floats():
    calc = Calculator()
    assert calc.divide(7.5, 2.5) == pytest.approx(3.0)


def test_divide_results_in_fraction():
    calc = Calculator()
    assert calc.divide(1, 3) == pytest.approx(1 / 3)


# --- factorial ---

def test_factorial_zero():
    calc = Calculator()
    assert calc.factorial(0) == 1


def test_factorial_one():
    calc = Calculator()
    assert calc.factorial(1) == 1


def test_factorial_positive():
    calc = Calculator()
    assert calc.factorial(5) == 120


def test_factorial_large():
    calc = Calculator()
    assert calc.factorial(10) == 3628800


def test_factorial_negative_raises():
    calc = Calculator()
    with pytest.raises(ValueError):
        calc.factorial(-1)
