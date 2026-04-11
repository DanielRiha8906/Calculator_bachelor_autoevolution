"""Unit tests for src.operations.transcendental — logarithm functions."""
import math
import pytest

from src.operations.transcendental import log, ln


# --- log ---

def test_log_base10():
    assert log(100) == pytest.approx(2.0)


def test_log_base2():
    assert log(8, 2) == pytest.approx(3.0)


def test_log_one():
    assert log(1) == pytest.approx(0.0)


def test_log_non_positive_raises():
    with pytest.raises(ValueError, match="not defined for non-positive"):
        log(0)


def test_log_negative_raises():
    with pytest.raises(ValueError, match="not defined for non-positive"):
        log(-5)


# --- ln ---

def test_ln_e():
    assert ln(math.e) == pytest.approx(1.0)


def test_ln_one():
    assert ln(1) == pytest.approx(0.0)


def test_ln_float():
    assert ln(math.e ** 2) == pytest.approx(2.0)


def test_ln_non_positive_raises():
    with pytest.raises(ValueError, match="not defined for non-positive"):
        ln(0)


def test_ln_negative_raises():
    with pytest.raises(ValueError, match="not defined for non-positive"):
        ln(-1)
