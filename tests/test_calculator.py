import pytest
import math
from src.calculator import Calculator


@pytest.fixture
def calc():
    return Calculator()


# ---------------------------------------------------------------------------
# add
# ---------------------------------------------------------------------------

class TestAdd:
    def test_two_positive_integers(self, calc):
        assert calc.add(3, 4) == 7

    def test_positive_and_negative(self, calc):
        assert calc.add(10, -3) == 7

    def test_two_negatives(self, calc):
        assert calc.add(-5, -7) == -12

    def test_add_zero(self, calc):
        assert calc.add(0, 0) == 0

    def test_identity_with_zero(self, calc):
        assert calc.add(42, 0) == 42

    def test_floats(self, calc):
        assert math.isclose(calc.add(0.1, 0.2), 0.3, rel_tol=1e-9)

    def test_large_numbers(self, calc):
        assert calc.add(10**9, 10**9) == 2 * 10**9


# ---------------------------------------------------------------------------
# subtract
# ---------------------------------------------------------------------------

class TestSubtract:
    def test_positive_result(self, calc):
        assert calc.subtract(10, 3) == 7

    def test_zero_result(self, calc):
        assert calc.subtract(5, 5) == 0

    def test_negative_result(self, calc):
        assert calc.subtract(3, 10) == -7

    def test_subtract_negative(self, calc):
        assert calc.subtract(5, -3) == 8

    def test_both_negative(self, calc):
        assert calc.subtract(-4, -4) == 0

    def test_floats(self, calc):
        assert math.isclose(calc.subtract(1.5, 0.5), 1.0, rel_tol=1e-9)

    def test_subtract_from_zero(self, calc):
        assert calc.subtract(0, 7) == -7


# ---------------------------------------------------------------------------
# multiply
# ---------------------------------------------------------------------------

class TestMultiply:
    def test_two_positives(self, calc):
        assert calc.multiply(3, 4) == 12

    def test_two_negatives(self, calc):
        assert calc.multiply(-3, -4) == 12

    def test_positive_and_negative(self, calc):
        assert calc.multiply(3, -4) == -12

    def test_multiply_by_zero(self, calc):
        assert calc.multiply(999, 0) == 0

    def test_multiply_by_one(self, calc):
        assert calc.multiply(7, 1) == 7

    def test_floats(self, calc):
        assert math.isclose(calc.multiply(0.1, 0.2), 0.02, rel_tol=1e-9)

    def test_float_times_integer(self, calc):
        assert math.isclose(calc.multiply(2.5, 4), 10.0, rel_tol=1e-9)

    def test_large_numbers(self, calc):
        assert calc.multiply(10**6, 10**6) == 10**12


# ---------------------------------------------------------------------------
# divide
# ---------------------------------------------------------------------------

class TestDivide:
    def test_exact_division(self, calc):
        assert calc.divide(10, 2) == 5.0

    def test_fractional_result(self, calc):
        assert math.isclose(calc.divide(1, 3), 1 / 3, rel_tol=1e-9)

    def test_divide_negative_by_positive(self, calc):
        assert calc.divide(-9, 3) == -3.0

    def test_divide_negative_by_negative(self, calc):
        assert calc.divide(-9, -3) == 3.0

    def test_divide_zero_by_nonzero(self, calc):
        assert calc.divide(0, 5) == 0.0

    def test_float_dividend(self, calc):
        assert math.isclose(calc.divide(5.5, 2), 2.75, rel_tol=1e-9)

    def test_float_divisor(self, calc):
        assert math.isclose(calc.divide(1, 0.5), 2.0, rel_tol=1e-9)

    def test_both_floats(self, calc):
        assert math.isclose(calc.divide(0.3, 0.1), 3.0, rel_tol=1e-9)

    def test_divide_by_zero_raises(self, calc):
        with pytest.raises(ZeroDivisionError):
            calc.divide(1, 0)

    def test_divide_zero_by_zero_raises(self, calc):
        with pytest.raises(ZeroDivisionError):
            calc.divide(0, 0)


# ---------------------------------------------------------------------------
# factorial
# ---------------------------------------------------------------------------

class TestFactorial:
    def test_zero(self, calc):
        assert calc.factorial(0) == 1

    def test_one(self, calc):
        assert calc.factorial(1) == 1

    def test_small_positive(self, calc):
        assert calc.factorial(5) == 120

    def test_larger_positive(self, calc):
        assert calc.factorial(10) == 3628800

    def test_negative_raises(self, calc):
        with pytest.raises(ValueError):
            calc.factorial(-1)

    def test_float_raises(self, calc):
        with pytest.raises(TypeError):
            calc.factorial(3.0)

    def test_string_raises(self, calc):
        with pytest.raises(TypeError):
            calc.factorial("5")

    def test_bool_raises(self, calc):
        with pytest.raises(TypeError):
            calc.factorial(True)


# ---------------------------------------------------------------------------
# square
# ---------------------------------------------------------------------------

class TestSquare:
    def test_positive_integer(self, calc):
        assert calc.square(4) == 16

    def test_zero(self, calc):
        assert calc.square(0) == 0

    def test_negative(self, calc):
        assert calc.square(-3) == 9

    def test_float(self, calc):
        assert math.isclose(calc.square(2.5), 6.25, rel_tol=1e-9)


# ---------------------------------------------------------------------------
# cube
# ---------------------------------------------------------------------------

class TestCube:
    def test_positive_integer(self, calc):
        assert calc.cube(3) == 27

    def test_zero(self, calc):
        assert calc.cube(0) == 0

    def test_negative(self, calc):
        assert calc.cube(-2) == -8

    def test_float(self, calc):
        assert math.isclose(calc.cube(1.5), 3.375, rel_tol=1e-9)


# ---------------------------------------------------------------------------
# square_root
# ---------------------------------------------------------------------------

class TestSquareRoot:
    def test_perfect_square(self, calc):
        assert calc.square_root(9) == 3.0

    def test_zero(self, calc):
        assert calc.square_root(0) == 0.0

    def test_non_perfect_square(self, calc):
        assert math.isclose(calc.square_root(2), math.sqrt(2), rel_tol=1e-9)

    def test_float_input(self, calc):
        assert math.isclose(calc.square_root(0.25), 0.5, rel_tol=1e-9)

    def test_negative_raises(self, calc):
        with pytest.raises(ValueError):
            calc.square_root(-1)


# ---------------------------------------------------------------------------
# cube_root
# ---------------------------------------------------------------------------

class TestCubeRoot:
    def test_perfect_cube(self, calc):
        assert math.isclose(calc.cube_root(27), 3.0, rel_tol=1e-9)

    def test_zero(self, calc):
        assert calc.cube_root(0) == 0.0

    def test_negative(self, calc):
        assert math.isclose(calc.cube_root(-8), -2.0, rel_tol=1e-9)

    def test_float_input(self, calc):
        assert math.isclose(calc.cube_root(0.125), 0.5, rel_tol=1e-9)


# ---------------------------------------------------------------------------
# power
# ---------------------------------------------------------------------------

class TestPower:
    def test_positive_integer_exponent(self, calc):
        assert calc.power(2, 10) == 1024

    def test_zero_exponent(self, calc):
        assert calc.power(5, 0) == 1

    def test_one_exponent(self, calc):
        assert calc.power(7, 1) == 7

    def test_negative_base(self, calc):
        assert calc.power(-2, 3) == -8

    def test_fractional_exponent(self, calc):
        assert math.isclose(calc.power(4, 0.5), 2.0, rel_tol=1e-9)

    def test_zero_base(self, calc):
        assert calc.power(0, 5) == 0

    def test_float_base(self, calc):
        assert math.isclose(calc.power(2.5, 2), 6.25, rel_tol=1e-9)


# ---------------------------------------------------------------------------
# log (base-10)
# ---------------------------------------------------------------------------

class TestLog:
    def test_one(self, calc):
        assert calc.log(1) == 0.0

    def test_ten(self, calc):
        assert math.isclose(calc.log(10), 1.0, rel_tol=1e-9)

    def test_hundred(self, calc):
        assert math.isclose(calc.log(100), 2.0, rel_tol=1e-9)

    def test_fraction(self, calc):
        assert math.isclose(calc.log(0.1), -1.0, rel_tol=1e-9)

    def test_zero_raises(self, calc):
        with pytest.raises(ValueError):
            calc.log(0)

    def test_negative_raises(self, calc):
        with pytest.raises(ValueError):
            calc.log(-5)


# ---------------------------------------------------------------------------
# ln (natural logarithm)
# ---------------------------------------------------------------------------

class TestLn:
    def test_one(self, calc):
        assert calc.ln(1) == 0.0

    def test_e(self, calc):
        assert math.isclose(calc.ln(math.e), 1.0, rel_tol=1e-9)

    def test_e_squared(self, calc):
        assert math.isclose(calc.ln(math.e ** 2), 2.0, rel_tol=1e-9)

    def test_fraction(self, calc):
        assert math.isclose(calc.ln(1 / math.e), -1.0, rel_tol=1e-9)

    def test_zero_raises(self, calc):
        with pytest.raises(ValueError):
            calc.ln(0)

    def test_negative_raises(self, calc):
        with pytest.raises(ValueError):
            calc.ln(-1)
