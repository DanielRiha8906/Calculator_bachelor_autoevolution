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
