"""Unit tests for src.operations.algebraic — power, root, and factorial functions."""
import pytest

from src.operations.algebraic import power, square, cube, square_root, cube_root, factorial


# --- power ---

def test_power_positive_exponent():
    assert power(2, 10) == 1024


def test_power_zero_exponent():
    assert power(5, 0) == 1


def test_power_negative_exponent():
    assert power(2, -1) == pytest.approx(0.5)


def test_power_float_base():
    assert power(2.0, 3) == pytest.approx(8.0)


# --- square ---

def test_square_positive():
    assert square(4) == 16


def test_square_zero():
    assert square(0) == 0


def test_square_negative():
    assert square(-3) == 9


def test_square_float():
    assert square(2.5) == 6.25


# --- cube ---

def test_cube_positive():
    assert cube(3) == 27


def test_cube_zero():
    assert cube(0) == 0


def test_cube_negative():
    assert cube(-2) == -8


def test_cube_float():
    assert cube(2.0) == 8.0


# --- square_root ---

def test_square_root_perfect_square():
    assert square_root(9) == 3.0


def test_square_root_zero():
    assert square_root(0) == 0.0


def test_square_root_float():
    import math
    assert square_root(2.0) == pytest.approx(math.sqrt(2.0))


def test_square_root_negative_raises():
    with pytest.raises(ValueError, match="not defined for negative"):
        square_root(-1)


# --- cube_root ---

def test_cube_root_positive():
    assert cube_root(27) == pytest.approx(3.0)


def test_cube_root_zero():
    assert cube_root(0) == pytest.approx(0.0)


def test_cube_root_negative():
    assert cube_root(-8) == pytest.approx(-2.0)


def test_cube_root_float():
    assert cube_root(8.0) == pytest.approx(2.0)


# --- factorial ---

def test_factorial_zero():
    assert factorial(0) == 1


def test_factorial_one():
    assert factorial(1) == 1


def test_factorial_positive():
    assert factorial(5) == 120


def test_factorial_large():
    assert factorial(10) == 3628800


def test_factorial_negative_raises():
    with pytest.raises(ValueError, match="not defined for negative"):
        factorial(-1)


def test_factorial_non_integer_raises():
    with pytest.raises(ValueError, match="non-negative integer"):
        factorial(2.5)
