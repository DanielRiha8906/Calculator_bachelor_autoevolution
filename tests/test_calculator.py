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


# ---------------------------------------------------------------------------
# factorial
# ---------------------------------------------------------------------------

def test_factorial_zero(calc):
    assert calc.factorial(0) == 1


def test_factorial_one(calc):
    assert calc.factorial(1) == 1


def test_factorial_positive_integer(calc):
    assert calc.factorial(5) == 120


def test_factorial_larger_integer(calc):
    assert calc.factorial(10) == 3628800


def test_factorial_negative_raises(calc):
    with pytest.raises(ValueError):
        calc.factorial(-1)


def test_factorial_negative_large_raises(calc):
    with pytest.raises(ValueError):
        calc.factorial(-10)


def test_factorial_float_raises(calc):
    with pytest.raises(TypeError):
        calc.factorial(3.0)


def test_factorial_non_integer_raises(calc):
    with pytest.raises(TypeError):
        calc.factorial(1.5)


def test_factorial_bool_raises(calc):
    with pytest.raises(TypeError):
        calc.factorial(True)


def test_factorial_string_raises(calc):
    with pytest.raises(TypeError):
        calc.factorial("5")


# ---------------------------------------------------------------------------
# square
# ---------------------------------------------------------------------------

def test_square_positive(calc):
    assert calc.square(4) == 16


def test_square_zero(calc):
    assert calc.square(0) == 0


def test_square_negative(calc):
    assert calc.square(-3) == 9


def test_square_float(calc):
    assert calc.square(2.5) == pytest.approx(6.25)


# ---------------------------------------------------------------------------
# cube
# ---------------------------------------------------------------------------

def test_cube_positive(calc):
    assert calc.cube(3) == 27


def test_cube_zero(calc):
    assert calc.cube(0) == 0


def test_cube_negative(calc):
    assert calc.cube(-2) == -8


def test_cube_float(calc):
    assert calc.cube(1.5) == pytest.approx(3.375)


# ---------------------------------------------------------------------------
# square_root
# ---------------------------------------------------------------------------

def test_square_root_positive(calc):
    assert calc.square_root(9) == pytest.approx(3.0)


def test_square_root_zero(calc):
    assert calc.square_root(0) == pytest.approx(0.0)


def test_square_root_non_perfect(calc):
    assert calc.square_root(2) == pytest.approx(math.sqrt(2))


def test_square_root_float(calc):
    assert calc.square_root(0.25) == pytest.approx(0.5)


def test_square_root_negative_raises(calc):
    with pytest.raises(ValueError):
        calc.square_root(-1)


def test_square_root_large_negative_raises(calc):
    with pytest.raises(ValueError):
        calc.square_root(-100)


# ---------------------------------------------------------------------------
# cube_root
# ---------------------------------------------------------------------------

def test_cube_root_positive(calc):
    assert calc.cube_root(27) == pytest.approx(3.0)


def test_cube_root_zero(calc):
    assert calc.cube_root(0) == pytest.approx(0.0)


def test_cube_root_negative(calc):
    assert calc.cube_root(-8) == pytest.approx(-2.0)


def test_cube_root_float(calc):
    assert calc.cube_root(0.125) == pytest.approx(0.5)


def test_cube_root_large_negative(calc):
    assert calc.cube_root(-27) == pytest.approx(-3.0)


# ---------------------------------------------------------------------------
# power
# ---------------------------------------------------------------------------

def test_power_positive_exponent(calc):
    assert calc.power(2, 10) == pytest.approx(1024)


def test_power_zero_exponent(calc):
    assert calc.power(5, 0) == pytest.approx(1)


def test_power_one_exponent(calc):
    assert calc.power(7, 1) == pytest.approx(7)


def test_power_negative_exponent(calc):
    assert calc.power(2, -1) == pytest.approx(0.5)


def test_power_fractional_exponent(calc):
    assert calc.power(4, 0.5) == pytest.approx(2.0)


def test_power_zero_base(calc):
    assert calc.power(0, 5) == pytest.approx(0)


def test_power_negative_base(calc):
    assert calc.power(-2, 3) == pytest.approx(-8)


# ---------------------------------------------------------------------------
# log (base-10)
# ---------------------------------------------------------------------------

def test_log_one(calc):
    assert calc.log(1) == pytest.approx(0.0)


def test_log_ten(calc):
    assert calc.log(10) == pytest.approx(1.0)


def test_log_hundred(calc):
    assert calc.log(100) == pytest.approx(2.0)


def test_log_fraction(calc):
    assert calc.log(0.1) == pytest.approx(-1.0)


def test_log_zero_raises(calc):
    with pytest.raises(ValueError):
        calc.log(0)


def test_log_negative_raises(calc):
    with pytest.raises(ValueError):
        calc.log(-5)


# ---------------------------------------------------------------------------
# ln (natural logarithm)
# ---------------------------------------------------------------------------

def test_ln_one(calc):
    assert calc.ln(1) == pytest.approx(0.0)


def test_ln_e(calc):
    assert calc.ln(math.e) == pytest.approx(1.0)


def test_ln_positive(calc):
    assert calc.ln(math.e ** 3) == pytest.approx(3.0)


def test_ln_fraction(calc):
    assert calc.ln(0.5) == pytest.approx(math.log(0.5))


def test_ln_zero_raises(calc):
    with pytest.raises(ValueError):
        calc.ln(0)


def test_ln_negative_raises(calc):
    with pytest.raises(ValueError):
        calc.ln(-1)
