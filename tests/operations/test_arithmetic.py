"""Unit tests for src.operations.arithmetic — pure arithmetic functions."""
import pytest

from src.operations.arithmetic import add, subtract, multiply, divide


# --- add ---

def test_add_positive():
    assert add(2, 3) == 5


def test_add_negative():
    assert add(-5, -3) == -8


def test_add_mixed_sign():
    assert add(-1, 1) == 0


def test_add_zeros():
    assert add(0, 0) == 0


def test_add_floats():
    assert add(1.5, 2.5) == 4.0


# --- subtract ---

def test_subtract_positive():
    assert subtract(5, 3) == 2


def test_subtract_negative():
    assert subtract(-3, -5) == 2


def test_subtract_to_negative():
    assert subtract(0, 5) == -5


def test_subtract_zeros():
    assert subtract(0, 0) == 0


def test_subtract_floats():
    assert subtract(3.5, 1.5) == 2.0


# --- multiply ---

def test_multiply_positive():
    assert multiply(3, 4) == 12


def test_multiply_by_zero():
    assert multiply(5, 0) == 0


def test_multiply_negative_and_positive():
    assert multiply(-2, 3) == -6


def test_multiply_two_negatives():
    assert multiply(-2, -3) == 6


def test_multiply_floats():
    assert multiply(2.5, 4) == 10.0


# --- divide ---

def test_divide_even():
    assert divide(10, 2) == 5.0


def test_divide_zero_numerator():
    assert divide(0, 5) == 0.0


def test_divide_negative_numerator():
    assert divide(-10, 2) == -5.0


def test_divide_negative_denominator():
    assert divide(10, -2) == -5.0


def test_divide_returns_float():
    assert divide(7, 2) == 3.5


def test_divide_by_zero_raises():
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        divide(10, 0)
