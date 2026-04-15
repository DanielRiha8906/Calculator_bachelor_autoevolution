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


# ---------------------------------------------------------------------------
# square
# ---------------------------------------------------------------------------

def test_square_positive(calc):
    assert calc.square(4) == 16


def test_square_negative(calc):
    assert calc.square(-3) == 9


def test_square_zero(calc):
    assert calc.square(0) == 0


def test_square_float(calc):
    assert math.isclose(calc.square(2.5), 6.25)


# ---------------------------------------------------------------------------
# cube
# ---------------------------------------------------------------------------

def test_cube_positive(calc):
    assert calc.cube(3) == 27


def test_cube_negative(calc):
    assert calc.cube(-2) == -8


def test_cube_zero(calc):
    assert calc.cube(0) == 0


def test_cube_float(calc):
    assert math.isclose(calc.cube(2.0), 8.0)


# ---------------------------------------------------------------------------
# square_root
# ---------------------------------------------------------------------------

def test_square_root_positive(calc):
    assert math.isclose(calc.square_root(9), 3.0)


def test_square_root_zero(calc):
    assert calc.square_root(0) == 0.0


def test_square_root_float(calc):
    assert math.isclose(calc.square_root(2.0), math.sqrt(2))


def test_square_root_negative_raises(calc):
    with pytest.raises(ValueError, match="Square root is not defined for negative numbers"):
        calc.square_root(-1)


# ---------------------------------------------------------------------------
# cube_root
# ---------------------------------------------------------------------------

def test_cube_root_positive(calc):
    assert math.isclose(calc.cube_root(27), 3.0)


def test_cube_root_negative(calc):
    assert math.isclose(calc.cube_root(-8), -2.0)


def test_cube_root_zero(calc):
    assert calc.cube_root(0) == 0.0


def test_cube_root_float(calc):
    assert math.isclose(calc.cube_root(8.0), 2.0)


# ---------------------------------------------------------------------------
# power
# ---------------------------------------------------------------------------

def test_power_positive_exponent(calc):
    assert calc.power(2, 10) == 1024


def test_power_zero_exponent(calc):
    assert calc.power(5, 0) == 1


def test_power_one_exponent(calc):
    assert calc.power(7, 1) == 7


def test_power_negative_exponent(calc):
    assert math.isclose(calc.power(2, -1), 0.5)


def test_power_float_base(calc):
    assert math.isclose(calc.power(2.0, 3), 8.0)


# ---------------------------------------------------------------------------
# log
# ---------------------------------------------------------------------------

def test_log_base_10(calc):
    assert math.isclose(calc.log(100, 10), 2.0)


def test_log_base_2(calc):
    assert math.isclose(calc.log(8, 2), 3.0)


def test_log_base_e(calc):
    assert math.isclose(calc.log(math.e, math.e), 1.0)


def test_log_non_positive_raises(calc):
    with pytest.raises(ValueError, match="Logarithm is not defined for non-positive numbers"):
        calc.log(0, 10)


def test_log_negative_raises(calc):
    with pytest.raises(ValueError, match="Logarithm is not defined for non-positive numbers"):
        calc.log(-5, 10)


def test_log_invalid_base_raises(calc):
    with pytest.raises(ValueError, match="Logarithm base must be positive and not equal to 1"):
        calc.log(10, 1)


def test_log_zero_base_raises(calc):
    with pytest.raises(ValueError, match="Logarithm base must be positive and not equal to 1"):
        calc.log(10, 0)


# ---------------------------------------------------------------------------
# ln
# ---------------------------------------------------------------------------

def test_ln_e(calc):
    assert math.isclose(calc.ln(math.e), 1.0)


def test_ln_one(calc):
    assert math.isclose(calc.ln(1), 0.0)


def test_ln_positive(calc):
    assert math.isclose(calc.ln(math.e ** 3), 3.0)


def test_ln_non_positive_raises(calc):
    with pytest.raises(ValueError, match="Natural logarithm is not defined for non-positive numbers"):
        calc.ln(0)


def test_ln_negative_raises(calc):
    with pytest.raises(ValueError, match="Natural logarithm is not defined for non-positive numbers"):
        calc.ln(-1)


# ---------------------------------------------------------------------------
# execute (unified dispatch)
# ---------------------------------------------------------------------------

def test_execute_two_arg_op(calc):
    """execute routes two-argument operations correctly."""
    assert calc.execute("add", 3, 4) == 7


def test_execute_one_arg_op(calc):
    """execute routes single-argument operations correctly."""
    assert calc.execute("square", 5) == 25


def test_execute_int_arg_op(calc):
    """execute routes integer-argument operations correctly."""
    assert calc.execute("factorial", 5) == 120


def test_execute_preserves_value_error(calc):
    """execute lets ValueError from the underlying method propagate."""
    with pytest.raises(ValueError, match="Division by zero is not allowed"):
        calc.execute("divide", 10, 0)


def test_execute_unknown_operation_raises(calc):
    """execute raises ValueError for an unrecognised operation name."""
    with pytest.raises(ValueError, match="Unknown operation"):
        calc.execute("nonexistent")
