"""Tests for the calculator GUI modes, operation specs, and application logic.

Mode and OperationSpec tests run without a display (no tkinter required).
CalculatorApp tests require a live Tk root and are skipped in headless
environments.

TODO: enable the display-dependent tests in CI by provisioning a virtual
display (e.g. Xvfb) in the GitHub Actions workflow.
"""
from __future__ import annotations

import pytest

from src.gui_modes import (
    CalculatorMode,
    OperationSpec,
    ScientificMode,
    SimpleMode,
    parse_number,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _tk_available() -> bool:
    """Return True if a Tk display is reachable."""
    try:
        import tkinter as tk
        root = tk.Tk()
        root.destroy()
        return True
    except Exception:
        return False


TK_AVAILABLE = _tk_available()
requires_display = pytest.mark.skipif(
    not TK_AVAILABLE,
    reason=(
        "No display available — skipping tkinter GUI tests. "
        "TODO: enable with Xvfb in CI."
    ),
)


# ---------------------------------------------------------------------------
# OperationSpec tests (no display required)
# ---------------------------------------------------------------------------

class TestOperationSpec:
    def test_binary_operation_fields(self):
        op = OperationSpec("Add", "add", 2, "a", "b")
        assert op.name == "Add"
        assert op.method == "add"
        assert op.arity == 2
        assert op.label_a == "a"
        assert op.label_b == "b"
        assert op.require_int is False

    def test_unary_default_labels(self):
        op = OperationSpec("Square", "square", 1)
        assert op.arity == 1
        assert op.label_a == "Value"
        assert op.label_b == ""
        assert op.require_int is False

    def test_require_int_flag(self):
        op = OperationSpec("Factorial", "factorial", 1, "n", require_int=True)
        assert op.require_int is True


# ---------------------------------------------------------------------------
# SimpleMode tests (no display required)
# ---------------------------------------------------------------------------

class TestSimpleMode:
    def setup_method(self):
        self.mode = SimpleMode()

    def test_name(self):
        assert self.mode.name == "Simple"

    def test_is_calculator_mode(self):
        assert isinstance(self.mode, CalculatorMode)

    def test_operation_count(self):
        assert len(self.mode.operations) == 6

    def test_all_operation_names_present(self):
        names = [op.name for op in self.mode.operations]
        for expected in ("Add", "Subtract", "Multiply", "Divide", "Square", "Square Root"):
            assert expected in names

    def test_binary_operations_count(self):
        binary = [op for op in self.mode.operations if op.arity == 2]
        assert len(binary) == 4

    def test_unary_operations_count(self):
        unary = [op for op in self.mode.operations if op.arity == 1]
        assert len(unary) == 2

    def test_methods_map_to_calculator(self):
        methods = [op.method for op in self.mode.operations]
        for expected in ("add", "subtract", "multiply", "divide", "square", "sqrt"):
            assert expected in methods

    def test_no_require_int_in_simple_mode(self):
        for op in self.mode.operations:
            assert op.require_int is False


# ---------------------------------------------------------------------------
# ScientificMode tests (no display required)
# ---------------------------------------------------------------------------

class TestScientificMode:
    def setup_method(self):
        self.mode = ScientificMode()

    def test_name(self):
        assert self.mode.name == "Scientific"

    def test_is_calculator_mode(self):
        assert isinstance(self.mode, CalculatorMode)

    def test_operation_count(self):
        assert len(self.mode.operations) == 12

    def test_binary_operations_count(self):
        binary = [op for op in self.mode.operations if op.arity == 2]
        assert len(binary) == 1
        assert binary[0].method == "power"

    def test_unary_operations_count(self):
        unary = [op for op in self.mode.operations if op.arity == 1]
        assert len(unary) == 11

    def test_all_methods_present(self):
        methods = {op.method for op in self.mode.operations}
        expected = {
            "power", "cube", "cbrt", "factorial",
            "log10", "ln",
            "sin", "cos", "tan", "cot", "asin", "acos",
        }
        assert expected == methods

    def test_factorial_requires_int(self):
        factorial_op = next(op for op in self.mode.operations if op.method == "factorial")
        assert factorial_op.require_int is True

    def test_only_factorial_requires_int(self):
        for op in self.mode.operations:
            if op.method != "factorial":
                assert op.require_int is False, f"{op.name} should not require int"

    def test_trig_operations_label_degrees(self):
        direct_trig = {"sin", "cos", "tan", "cot"}
        for op in self.mode.operations:
            if op.method in direct_trig:
                assert "degree" in op.label_a.lower(), (
                    f"{op.name} label_a should mention degrees"
                )

    def test_inverse_trig_has_range_label(self):
        inverse_trig = {"asin", "acos"}
        for op in self.mode.operations:
            if op.method in inverse_trig:
                assert op.label_a, f"{op.name} should have a non-empty label_a"


# ---------------------------------------------------------------------------
# parse_number tests (no display required)
# ---------------------------------------------------------------------------


class TestParseNumber:
    def test_integer_string(self):
        assert parse_number("5") == 5
        assert isinstance(parse_number("5"), int)

    def test_float_string(self):
        val = parse_number("3.14")
        assert val == pytest.approx(3.14)
        assert isinstance(val, float)

    def test_negative_float(self):
        val = parse_number("-2.5")
        assert val == pytest.approx(-2.5)

    def test_empty_string_raises(self):
        with pytest.raises(ValueError, match="empty"):
            parse_number("")

    def test_whitespace_only_raises(self):
        with pytest.raises(ValueError, match="empty"):
            parse_number("   ")

    def test_non_numeric_raises(self):
        with pytest.raises(ValueError):
            parse_number("abc")

    def test_require_int_accepts_integer(self):
        val = parse_number("7", require_int=True)
        assert val == 7
        assert isinstance(val, int)

    def test_require_int_accepts_whole_float_string(self):
        val = parse_number("5.0", require_int=True)
        assert val == 5
        assert isinstance(val, int)

    def test_require_int_rejects_fractional_float(self):
        with pytest.raises(ValueError, match="whole number"):
            parse_number("3.5", require_int=True)

    def test_leading_trailing_whitespace_stripped(self):
        assert parse_number("  42  ") == 42


# ---------------------------------------------------------------------------
# CalculatorApp tests (require a live display)
# ---------------------------------------------------------------------------

@requires_display
class TestCalculatorApp:
    """Integration tests for CalculatorApp — skipped in headless environments."""

    def setup_method(self):
        from src.gui import CalculatorApp
        self.app = CalculatorApp()

    def teardown_method(self):
        self.app.destroy()

    # --- initial state ---

    def test_default_mode_is_simple(self):
        assert self.app.current_mode.name == "Simple"

    def test_history_starts_empty(self):
        assert self.app.history == []

    def test_result_starts_with_dash(self):
        assert self.app.result_var.get() == "\u2014"

    # --- mode switching ---

    def test_switch_to_scientific(self):
        self.app.mode_var.set("Scientific")
        self.app._on_mode_change()
        assert self.app.current_mode.name == "Scientific"

    def test_switch_back_to_simple(self):
        self.app.mode_var.set("Scientific")
        self.app._on_mode_change()
        self.app.mode_var.set("Simple")
        self.app._on_mode_change()
        assert self.app.current_mode.name == "Simple"

    def test_mode_switch_resets_result(self):
        self.app.result_var.set("42")
        self.app.mode_var.set("Scientific")
        self.app._on_mode_change()
        assert self.app.result_var.get() == "\u2014"

    # --- calculation: simple mode ---

    def test_add(self):
        self.app.op_combo.set("Add")
        self.app._on_operation_change()
        self.app.entry_a.insert(0, "3")
        self.app.entry_b.insert(0, "4")
        self.app._calculate()
        assert self.app.result_var.get() == "7"
        assert len(self.app.history) == 1

    def test_subtract(self):
        self.app.op_combo.set("Subtract")
        self.app._on_operation_change()
        self.app.entry_a.insert(0, "10")
        self.app.entry_b.insert(0, "3")
        self.app._calculate()
        assert self.app.result_var.get() == "7"

    def test_multiply(self):
        self.app.op_combo.set("Multiply")
        self.app._on_operation_change()
        self.app.entry_a.insert(0, "6")
        self.app.entry_b.insert(0, "7")
        self.app._calculate()
        assert self.app.result_var.get() == "42"

    def test_divide(self):
        self.app.op_combo.set("Divide")
        self.app._on_operation_change()
        self.app.entry_a.insert(0, "15")
        self.app.entry_b.insert(0, "3")
        self.app._calculate()
        assert self.app.result_var.get() == "5"

    def test_square(self):
        self.app.op_combo.set("Square")
        self.app._on_operation_change()
        self.app.entry_a.insert(0, "5")
        self.app._calculate()
        assert self.app.result_var.get() == "25"

    def test_sqrt(self):
        self.app.op_combo.set("Square Root")
        self.app._on_operation_change()
        self.app.entry_a.insert(0, "9")
        self.app._calculate()
        assert self.app.result_var.get() == "3"

    # --- calculation: scientific mode ---

    def test_factorial(self):
        self.app.mode_var.set("Scientific")
        self.app._on_mode_change()
        self.app.op_combo.set("Factorial")
        self.app._on_operation_change()
        self.app.entry_a.insert(0, "5")
        self.app._calculate()
        assert self.app.result_var.get() == "120"

    def test_power(self):
        self.app.mode_var.set("Scientific")
        self.app._on_mode_change()
        self.app.op_combo.set("Power")
        self.app._on_operation_change()
        self.app.entry_a.insert(0, "2")
        self.app.entry_b.insert(0, "10")
        self.app._calculate()
        assert self.app.result_var.get() == "1024"

    def test_sin_90(self):
        self.app.mode_var.set("Scientific")
        self.app._on_mode_change()
        self.app.op_combo.set("Sin")
        self.app._on_operation_change()
        self.app.entry_a.insert(0, "90")
        self.app._calculate()
        assert self.app.result_var.get() == "1"

    # --- error cases ---

    def test_divide_by_zero_shows_error(self):
        from unittest.mock import patch
        self.app.op_combo.set("Divide")
        self.app._on_operation_change()
        self.app.entry_a.insert(0, "5")
        self.app.entry_b.insert(0, "0")
        with patch("tkinter.messagebox.showerror"):
            self.app._calculate()
        assert self.app.result_var.get() == "Error"

    def test_invalid_first_input_shows_error(self):
        from unittest.mock import patch
        self.app.op_combo.set("Square")
        self.app._on_operation_change()
        self.app.entry_a.insert(0, "abc")
        with patch("tkinter.messagebox.showerror") as mock_err:
            self.app._calculate()
        mock_err.assert_called_once()
        assert "Input Error" in mock_err.call_args[0]

    def test_empty_first_input_shows_error(self):
        from unittest.mock import patch
        self.app.op_combo.set("Square")
        self.app._on_operation_change()
        with patch("tkinter.messagebox.showerror") as mock_err:
            self.app._calculate()
        mock_err.assert_called_once()

    # --- clear ---

    def test_clear_empties_entry_a(self):
        self.app.entry_a.insert(0, "42")
        self.app._clear()
        assert self.app.entry_a.get() == ""

    def test_clear_resets_result(self):
        self.app.result_var.set("99")
        self.app._clear()
        assert self.app.result_var.get() == "\u2014"

    # --- history ---

    def test_successful_calc_appended_to_history(self):
        self.app.op_combo.set("Add")
        self.app._on_operation_change()
        self.app.entry_a.insert(0, "1")
        self.app.entry_b.insert(0, "1")
        self.app._calculate()
        assert len(self.app.history) == 1
        assert "Add(1, 1) = 2" in self.app.history[0]

    def test_error_calc_not_appended_to_history(self):
        from unittest.mock import patch
        self.app.op_combo.set("Divide")
        self.app._on_operation_change()
        self.app.entry_a.insert(0, "1")
        self.app.entry_b.insert(0, "0")
        with patch("tkinter.messagebox.showerror"):
            self.app._calculate()
        assert len(self.app.history) == 0

    def test_multiple_calcs_all_in_history(self):
        for val in ("1", "2", "3"):
            self.app.op_combo.set("Square")
            self.app._on_operation_change()
            self.app.entry_a.delete(0, tk.END)
            self.app.entry_a.insert(0, val)
            self.app._calculate()
        assert len(self.app.history) == 3


# need tk for the last test
try:
    import tkinter as tk
except ImportError:
    pass
