"""Tests for CalculatorSession and shared operation metadata in src/session.py."""
import pytest

from src.session import (
    CalculatorSession,
    BINARY_OPS,
    UNARY_OPS,
    ALL_OPS,
)


# ---------------------------------------------------------------------------
# Operation metadata sets
# ---------------------------------------------------------------------------

def test_binary_ops_contains_expected():
    assert BINARY_OPS == {"add", "subtract", "multiply", "divide", "power"}


def test_unary_ops_contains_expected():
    assert UNARY_OPS == {
        "factorial", "square", "cube", "square_root", "cube_root", "log", "ln",
        "sin", "cos", "tan", "cot", "asin", "acos",
    }


def test_all_ops_is_union_of_binary_and_unary():
    assert ALL_OPS == BINARY_OPS | UNARY_OPS


def test_binary_and_unary_are_disjoint():
    assert BINARY_OPS.isdisjoint(UNARY_OPS)


def test_all_ops_contains_eighteen_operations():
    assert len(ALL_OPS) == 18


# ---------------------------------------------------------------------------
# CalculatorSession.format_entry (static)
# ---------------------------------------------------------------------------

def test_format_entry_binary():
    assert CalculatorSession.format_entry("add", (2, 3), 5) == "add(2, 3) = 5"


def test_format_entry_unary():
    assert CalculatorSession.format_entry("factorial", (5,), 120) == "factorial(5) = 120"


def test_format_entry_float_result():
    assert CalculatorSession.format_entry("square_root", (9,), 3.0) == "square_root(9) = 3.0"


# ---------------------------------------------------------------------------
# CalculatorSession.execute — all twelve operations
# ---------------------------------------------------------------------------

@pytest.fixture
def session():
    return CalculatorSession()


def test_execute_add(session):
    assert session.execute("add", 2, 3) == 5


def test_execute_subtract(session):
    assert session.execute("subtract", 10, 4) == 6


def test_execute_multiply(session):
    assert session.execute("multiply", 6, 7) == 42


def test_execute_divide(session):
    assert session.execute("divide", 10, 2) == pytest.approx(5.0)


def test_execute_divide_by_zero_raises(session):
    with pytest.raises(ZeroDivisionError):
        session.execute("divide", 5, 0)


def test_execute_power(session):
    assert session.execute("power", 2, 10) == 1024


def test_execute_factorial(session):
    assert session.execute("factorial", 5) == 120


def test_execute_factorial_zero(session):
    assert session.execute("factorial", 0) == 1


def test_execute_factorial_negative_raises(session):
    with pytest.raises(ValueError):
        session.execute("factorial", -1)


def test_execute_factorial_float_raises(session):
    with pytest.raises(TypeError):
        session.execute("factorial", 3.5)


def test_execute_square(session):
    assert session.execute("square", 4) == 16


def test_execute_cube(session):
    assert session.execute("cube", 3) == 27


def test_execute_square_root(session):
    assert session.execute("square_root", 9) == pytest.approx(3.0)


def test_execute_square_root_negative_raises(session):
    with pytest.raises(ValueError):
        session.execute("square_root", -1)


def test_execute_cube_root(session):
    assert session.execute("cube_root", 27) == pytest.approx(3.0)


def test_execute_cube_root_negative(session):
    assert session.execute("cube_root", -8) == pytest.approx(-2.0)


def test_execute_log(session):
    assert session.execute("log", 100) == pytest.approx(2.0)


def test_execute_log_non_positive_raises(session):
    with pytest.raises(ValueError):
        session.execute("log", 0)


def test_execute_ln(session):
    assert session.execute("ln", 1) == pytest.approx(0.0)


def test_execute_ln_negative_raises(session):
    with pytest.raises(ValueError):
        session.execute("ln", -5)


def test_execute_sin(session):
    import math
    assert session.execute("sin", 90) == pytest.approx(1.0)


def test_execute_cos(session):
    assert session.execute("cos", 0) == pytest.approx(1.0)


def test_execute_tan(session):
    assert session.execute("tan", 45) == pytest.approx(1.0)


def test_execute_tan_undefined_raises(session):
    with pytest.raises(ValueError):
        session.execute("tan", 90)


def test_execute_cot(session):
    assert session.execute("cot", 45) == pytest.approx(1.0)


def test_execute_cot_undefined_raises(session):
    with pytest.raises(ValueError):
        session.execute("cot", 0)


def test_execute_asin(session):
    assert session.execute("asin", 1) == pytest.approx(90.0)


def test_execute_asin_out_of_domain_raises(session):
    with pytest.raises(ValueError):
        session.execute("asin", 2)


def test_execute_acos(session):
    assert session.execute("acos", 0) == pytest.approx(90.0)


def test_execute_acos_out_of_domain_raises(session):
    with pytest.raises(ValueError):
        session.execute("acos", -2)


# ---------------------------------------------------------------------------
# History management
# ---------------------------------------------------------------------------

def test_history_empty_on_new_session(session):
    assert session.history() == []


def test_history_records_successful_execution(session):
    session.execute("add", 2, 3)
    assert session.history() == ["add(2, 3) = 5"]


def test_history_accumulates_multiple_entries(session):
    session.execute("add", 2, 3)
    session.execute("factorial", 5)
    assert session.history() == ["add(2, 3) = 5", "factorial(5) = 120"]


def test_history_not_updated_on_error(session):
    with pytest.raises(ZeroDivisionError):
        session.execute("divide", 5, 0)
    assert session.history() == []


def test_history_returns_copy(session):
    session.execute("add", 1, 2)
    h = session.history()
    h.append("fake")
    assert len(session.history()) == 1


# ---------------------------------------------------------------------------
# save()
# ---------------------------------------------------------------------------

def test_save_writes_history_entries(session, tmp_path):
    session.execute("add", 2, 3)
    session.execute("factorial", 5)
    path = str(tmp_path / "history.txt")
    session.save(path)
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    assert lines == ["add(2, 3) = 5", "factorial(5) = 120"]


def test_save_empty_session_writes_empty_file(session, tmp_path):
    path = str(tmp_path / "history.txt")
    session.save(path)
    with open(path, encoding="utf-8") as fh:
        content = fh.read()
    assert content == ""


def test_save_overwrites_previous_content(session, tmp_path):
    path = str(tmp_path / "history.txt")
    # First session writes one entry
    session.execute("add", 1, 1)
    session.save(path)
    # New session overwrites with different content
    session2 = CalculatorSession()
    session2.execute("multiply", 3, 4)
    session2.save(path)
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    assert lines == ["multiply(3, 4) = 12"]
