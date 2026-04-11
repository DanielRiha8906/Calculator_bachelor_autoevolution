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


# --- square ---

def test_square_positive(calc):
    assert calc.square(4) == 16


def test_square_zero(calc):
    assert calc.square(0) == 0


def test_square_negative(calc):
    assert calc.square(-3) == 9


def test_square_float(calc):
    assert calc.square(2.5) == 6.25


# --- cube ---

def test_cube_positive(calc):
    assert calc.cube(3) == 27


def test_cube_zero(calc):
    assert calc.cube(0) == 0


def test_cube_negative(calc):
    assert calc.cube(-2) == -8


def test_cube_float(calc):
    assert calc.cube(2.0) == 8.0


# --- square_root ---

def test_square_root_perfect_square(calc):
    assert calc.square_root(9) == 3.0


def test_square_root_zero(calc):
    assert calc.square_root(0) == 0.0


def test_square_root_float(calc):
    assert calc.square_root(2.0) == pytest.approx(math.sqrt(2.0))


def test_square_root_negative_raises(calc):
    with pytest.raises(ValueError, match="not defined for negative"):
        calc.square_root(-1)


# --- cube_root ---

def test_cube_root_positive(calc):
    assert calc.cube_root(27) == pytest.approx(3.0)


def test_cube_root_zero(calc):
    assert calc.cube_root(0) == pytest.approx(0.0)


def test_cube_root_negative(calc):
    assert calc.cube_root(-8) == pytest.approx(-2.0)


def test_cube_root_float(calc):
    assert calc.cube_root(8.0) == pytest.approx(2.0)


# --- power ---

def test_power_positive_exponent(calc):
    assert calc.power(2, 10) == 1024


def test_power_zero_exponent(calc):
    assert calc.power(5, 0) == 1


def test_power_negative_exponent(calc):
    assert calc.power(2, -1) == pytest.approx(0.5)


def test_power_float_base(calc):
    assert calc.power(2.0, 3) == pytest.approx(8.0)


# --- log ---

def test_log_base10(calc):
    assert calc.log(100) == pytest.approx(2.0)


def test_log_base2(calc):
    assert calc.log(8, 2) == pytest.approx(3.0)


def test_log_one(calc):
    assert calc.log(1) == pytest.approx(0.0)


def test_log_non_positive_raises(calc):
    with pytest.raises(ValueError, match="not defined for non-positive"):
        calc.log(0)


def test_log_negative_raises(calc):
    with pytest.raises(ValueError, match="not defined for non-positive"):
        calc.log(-5)


# --- ln ---

def test_ln_e(calc):
    assert calc.ln(math.e) == pytest.approx(1.0)


def test_ln_one(calc):
    assert calc.ln(1) == pytest.approx(0.0)


def test_ln_float(calc):
    assert calc.ln(math.e ** 2) == pytest.approx(2.0)


def test_ln_non_positive_raises(calc):
    with pytest.raises(ValueError, match="not defined for non-positive"):
        calc.ln(0)


def test_ln_negative_raises(calc):
    with pytest.raises(ValueError, match="not defined for non-positive"):
        calc.ln(-1)
