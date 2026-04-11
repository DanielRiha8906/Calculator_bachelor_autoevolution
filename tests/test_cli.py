"""Tests for the bash CLI in main.py.

Each test invokes main() directly with a pre-built argument list and asserts
on captured stdout, stderr, and exit code.  The CLI writes results to stdout
and errors to stderr, exiting with code 1 on any failure.
"""

import io
import math
from unittest.mock import patch

import pytest

from main import main


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _run(args: list[str]) -> tuple[str, str, int]:
    """Run main(args), return (stdout, stderr, exit_code).

    Exit code 0 means main() returned normally; 1 (or any non-zero value)
    means sys.exit() was called.

    setup_error_logging is patched to a no-op so tests produce no file
    side-effects; use test_error_logging.py for logging-specific assertions.
    """
    captured_out = io.StringIO()
    captured_err = io.StringIO()
    exit_code = 0
    try:
        with patch("sys.stdout", captured_out), patch("sys.stderr", captured_err):
            with patch("main.setup_error_logging"):
                main(args)
    except SystemExit as exc:
        exit_code = exc.code if exc.code is not None else 0
    return captured_out.getvalue(), captured_err.getvalue(), exit_code


# ---------------------------------------------------------------------------
# Argument validation
# ---------------------------------------------------------------------------

def test_no_args_exits_nonzero():
    _, err, code = _run([])
    assert code != 0
    assert "Usage" in err


def test_unknown_operation_exits_nonzero():
    _, err, code = _run(["modulo", "10", "3"])
    assert code != 0
    assert "unknown operation" in err


def test_unary_operation_with_too_many_args_exits_nonzero():
    _, err, code = _run(["factorial", "5", "3"])
    assert code != 0
    assert "requires 1 operand" in err


def test_binary_operation_with_too_few_args_exits_nonzero():
    _, err, code = _run(["add", "5"])
    assert code != 0
    assert "requires 2 operands" in err


def test_binary_operation_with_no_operands_exits_nonzero():
    _, err, code = _run(["add"])
    assert code != 0
    assert "requires 2 operands" in err


def test_invalid_number_format_exits_nonzero():
    _, err, code = _run(["add", "abc", "5"])
    assert code != 0
    assert "Error" in err


# ---------------------------------------------------------------------------
# Two-operand operations — happy path
# ---------------------------------------------------------------------------

def test_add():
    out, _, code = _run(["add", "5", "7"])
    assert code == 0
    assert out.strip() == "12"


def test_subtract():
    out, _, code = _run(["subtract", "10", "3"])
    assert code == 0
    assert out.strip() == "7"


def test_multiply():
    out, _, code = _run(["multiply", "4", "5"])
    assert code == 0
    assert out.strip() == "20"


def test_divide():
    out, _, code = _run(["divide", "10", "2"])
    assert code == 0
    assert float(out.strip()) == pytest.approx(5.0)


def test_power():
    out, _, code = _run(["power", "2", "3"])
    assert code == 0
    assert float(out.strip()) == pytest.approx(8.0)


def test_add_floats():
    out, _, code = _run(["add", "1.5", "2.5"])
    assert code == 0
    assert float(out.strip()) == pytest.approx(4.0)


# ---------------------------------------------------------------------------
# Two-operand operations — error cases
# ---------------------------------------------------------------------------

def test_divide_by_zero_exits_nonzero():
    _, err, code = _run(["divide", "5", "0"])
    assert code != 0
    assert "Error" in err


def test_power_negative_base_fractional_exponent_exits_nonzero():
    _, err, code = _run(["power", "-2", "0.5"])
    assert code != 0
    assert "Error" in err


# ---------------------------------------------------------------------------
# One-operand operations — happy path
# ---------------------------------------------------------------------------

def test_factorial():
    out, _, code = _run(["factorial", "5"])
    assert code == 0
    assert out.strip() == "120"


def test_factorial_zero():
    out, _, code = _run(["factorial", "0"])
    assert code == 0
    assert out.strip() == "1"


def test_square():
    out, _, code = _run(["square", "4"])
    assert code == 0
    assert out.strip() == "16"


def test_square_negative():
    out, _, code = _run(["square", "-3"])
    assert code == 0
    assert out.strip() == "9"


def test_cube():
    out, _, code = _run(["cube", "3"])
    assert code == 0
    assert out.strip() == "27"


def test_sqrt():
    out, _, code = _run(["sqrt", "9"])
    assert code == 0
    assert float(out.strip()) == pytest.approx(3.0)


def test_cbrt():
    out, _, code = _run(["cbrt", "27"])
    assert code == 0
    assert float(out.strip()) == pytest.approx(3.0)


def test_cbrt_negative():
    out, _, code = _run(["cbrt", "-27"])
    assert code == 0
    assert float(out.strip()) == pytest.approx(-3.0)


def test_log10():
    out, _, code = _run(["log10", "100"])
    assert code == 0
    assert float(out.strip()) == pytest.approx(2.0)


def test_ln():
    out, _, code = _run(["ln", "1"])
    assert code == 0
    assert float(out.strip()) == pytest.approx(0.0)


def test_ln_e():
    out, _, code = _run(["ln", str(math.e)])
    assert code == 0
    assert float(out.strip()) == pytest.approx(1.0)


# ---------------------------------------------------------------------------
# One-operand operations — error cases
# ---------------------------------------------------------------------------

def test_factorial_negative_exits_nonzero():
    _, err, code = _run(["factorial", "-1"])
    assert code != 0
    assert "Error" in err


def test_factorial_float_input_exits_nonzero():
    _, err, code = _run(["factorial", "3.5"])
    assert code != 0
    assert "Error" in err


def test_sqrt_negative_exits_nonzero():
    _, err, code = _run(["sqrt", "-1"])
    assert code != 0
    assert "Error" in err


def test_log10_non_positive_exits_nonzero():
    _, err, code = _run(["log10", "0"])
    assert code != 0
    assert "Error" in err


def test_ln_non_positive_exits_nonzero():
    _, err, code = _run(["ln", "-1"])
    assert code != 0
    assert "Error" in err
