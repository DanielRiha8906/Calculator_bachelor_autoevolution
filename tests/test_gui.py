"""Tests for src/gui.py.

Pure-function tests (parse_operand, constants) run in all environments.
Widget tests require a live Tk display and are skipped automatically when
no display is available (e.g. headless CI without Xvfb).
"""
import pytest
from unittest.mock import patch

import src.history as history_module
from src.gui import (
    parse_operand,
    NORMAL_OPERATIONS,
    SCIENTIFIC_OPERATIONS,
    OPERATION_LABELS,
    BINARY_OPERATIONS,
    INTEGER_OPERATIONS,
    LOG_OPERATIONS,
    gui_main,
    _TKINTER_AVAILABLE,
)


# ---------------------------------------------------------------------------
# Detect whether a Tk display is available for widget tests
# ---------------------------------------------------------------------------

def _has_display() -> bool:
    """Return True only if tkinter is installed and a display is reachable."""
    try:
        import tkinter as tk
        root = tk.Tk()
        root.destroy()
        return True
    except Exception:
        return False


HAS_DISPLAY = _has_display()
needs_display = pytest.mark.skipif(
    not HAS_DISPLAY,
    reason="No Tk display available (headless environment or tkinter not installed)",
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def tmp_history_file(tmp_path, monkeypatch):
    """Redirect HISTORY_FILE so tests never write to the project root."""
    tmp_file = tmp_path / "history.txt"
    monkeypatch.setattr(history_module, "HISTORY_FILE", tmp_file)
    return tmp_file


# ---------------------------------------------------------------------------
# parse_operand — pure function, no display required
# ---------------------------------------------------------------------------

class TestParseOperand:
    def test_valid_float(self):
        assert parse_operand("3.14") == pytest.approx(3.14)

    def test_valid_integer_string_as_float(self):
        assert parse_operand("5") == 5.0

    def test_negative_float(self):
        assert parse_operand("-2.5") == pytest.approx(-2.5)

    def test_strips_whitespace(self):
        assert parse_operand("  7  ") == 7.0

    def test_integer_mode_valid(self):
        result = parse_operand("4", integer=True)
        assert result == 4
        assert isinstance(result, int)

    def test_integer_mode_negative(self):
        result = parse_operand("-3", integer=True)
        assert result == -3

    def test_empty_string_raises(self):
        with pytest.raises(ValueError, match="must not be empty"):
            parse_operand("")

    def test_whitespace_only_raises(self):
        with pytest.raises(ValueError, match="must not be empty"):
            parse_operand("   ")

    def test_non_numeric_raises(self):
        with pytest.raises(ValueError):
            parse_operand("abc")

    def test_integer_mode_float_string_raises(self):
        with pytest.raises(ValueError, match="whole number"):
            parse_operand("3.5", integer=True)

    def test_integer_mode_non_numeric_raises(self):
        with pytest.raises(ValueError):
            parse_operand("xyz", integer=True)


# ---------------------------------------------------------------------------
# Module-level constants
# ---------------------------------------------------------------------------

class TestConstants:
    def test_normal_operations_are_arithmetic(self):
        assert set(NORMAL_OPERATIONS) == {"add", "subtract", "multiply", "divide"}

    def test_scientific_operations_include_normal(self):
        for op in NORMAL_OPERATIONS:
            assert op in SCIENTIFIC_OPERATIONS

    def test_scientific_operations_include_advanced(self):
        for op in [
            "factorial", "square", "cube", "square_root", "cube_root",
            "power", "log", "ln",
        ]:
            assert op in SCIENTIFIC_OPERATIONS

    def test_all_operations_have_labels(self):
        for op in SCIENTIFIC_OPERATIONS:
            assert op in OPERATION_LABELS, f"Missing label for {op!r}"

    def test_labels_are_non_empty_strings(self):
        for op, label in OPERATION_LABELS.items():
            assert isinstance(label, str) and label.strip(), (
                f"Label for {op!r} is empty"
            )

    def test_binary_operations_subset_of_scientific(self):
        for op in BINARY_OPERATIONS:
            assert op in SCIENTIFIC_OPERATIONS

    def test_integer_operations_subset_of_scientific(self):
        for op in INTEGER_OPERATIONS:
            assert op in SCIENTIFIC_OPERATIONS

    def test_log_operations_subset_of_scientific(self):
        for op in LOG_OPERATIONS:
            assert op in SCIENTIFIC_OPERATIONS


# ---------------------------------------------------------------------------
# gui_main — import and availability checks (no display required)
# ---------------------------------------------------------------------------

def test_gui_main_is_callable():
    """gui_main must be importable and callable."""
    assert callable(gui_main)


def test_gui_main_raises_when_tkinter_unavailable(monkeypatch):
    """gui_main must raise ImportError when _TKINTER_AVAILABLE is False."""
    monkeypatch.setattr("src.gui._TKINTER_AVAILABLE", False)
    with pytest.raises(ImportError, match="tkinter"):
        gui_main()


# ---------------------------------------------------------------------------
# CalculatorGUI widget tests (skipped when no display)
# ---------------------------------------------------------------------------

@needs_display
class TestCalculatorGUIWidget:
    """Integration tests that create a real Tk window.

    These tests are skipped automatically in headless CI environments or
    when tkinter is not installed.  They verify GUI state transitions
    without pumping the Tk event loop.
    """

    @pytest.fixture
    def app(self):
        import tkinter as tk
        from src.gui import CalculatorGUI

        root = tk.Tk()
        root.withdraw()  # Keep window off-screen during tests
        gui = CalculatorGUI(root)
        yield gui
        root.destroy()

    def test_initial_mode_is_normal(self, app):
        assert app._mode == "normal"

    def test_initial_no_operation_selected(self, app):
        assert app._selected_op is None

    def test_select_operation_updates_selected_op(self, app):
        app._select_operation("add")
        assert app._selected_op == "add"

    def test_select_binary_operation_shows_b_field(self, app):
        app._select_operation("add")
        assert app._entry_b.winfo_manager() != ""

    def test_select_unary_operation_hides_b_field(self, app):
        app._select_operation("square")
        assert app._entry_b.winfo_manager() == ""

    def test_select_log_shows_base_field(self, app):
        app._select_operation("log")
        assert app._entry_base.winfo_manager() != ""

    def test_select_non_log_hides_base_field(self, app):
        app._select_operation("add")
        assert app._entry_base.winfo_manager() == ""

    def test_toggle_mode_switches_to_scientific(self, app):
        app._toggle_mode()
        assert app._mode == "scientific"

    def test_toggle_mode_switches_back_to_normal(self, app):
        app._toggle_mode()
        app._toggle_mode()
        assert app._mode == "normal"

    def test_toggle_to_normal_deselects_scientific_op(self, app):
        app._toggle_mode()  # → scientific
        app._select_operation("factorial")
        app._toggle_mode()  # → normal: factorial must be deselected
        assert app._selected_op is None

    def test_toggle_to_normal_retains_normal_op(self, app):
        app._toggle_mode()  # → scientific
        app._select_operation("add")
        app._toggle_mode()  # → normal: add must remain selected
        assert app._selected_op == "add"

    def test_calculate_add_result(self, app):
        app._select_operation("add")
        app._entry_a.insert(0, "3")
        app._entry_b.insert(0, "4")
        app._calculate()
        assert app._result_label.cget("text") == "7.0"

    def test_calculate_records_history(self, app):
        from src.history import load_history
        app._select_operation("multiply")
        app._entry_a.insert(0, "6")
        app._entry_b.insert(0, "7")
        app._calculate()
        entries = load_history()
        assert any("Multiply" in e for e in entries)

    def test_calculate_with_empty_a_shows_error(self, app):
        from src.history import load_history
        app._select_operation("square")
        with patch("src.gui.messagebox.showerror") as mock_err:
            app._calculate()
        mock_err.assert_called_once()
        assert load_history() == []

    def test_calculate_invalid_a_shows_error(self, app):
        app._select_operation("add")
        app._entry_a.insert(0, "not_a_number")
        app._entry_b.insert(0, "5")
        with patch("src.gui.messagebox.showerror") as mock_err:
            app._calculate()
        mock_err.assert_called_once()

    def test_calculate_divide_by_zero_shows_error(self, app):
        app._select_operation("divide")
        app._entry_a.insert(0, "10")
        app._entry_b.insert(0, "0")
        with patch("src.gui.messagebox.showerror") as mock_err:
            app._calculate()
        mock_err.assert_called_once()

    def test_calculate_sqrt_negative_shows_error(self, app):
        app._toggle_mode()  # → scientific
        app._select_operation("square_root")
        app._entry_a.insert(0, "-4")
        with patch("src.gui.messagebox.showerror") as mock_err:
            app._calculate()
        mock_err.assert_called_once()

    def test_calculate_factorial_integer_input(self, app):
        app._toggle_mode()  # → scientific
        app._select_operation("factorial")
        app._entry_a.insert(0, "5")
        app._calculate()
        assert app._result_label.cget("text") == "120"

    def test_calculate_log_default_base(self, app):
        app._toggle_mode()  # → scientific
        app._select_operation("log")
        app._entry_a.insert(0, "100")
        app._calculate()
        assert float(app._result_label.cget("text")) == pytest.approx(2.0)

    def test_calculate_power(self, app):
        app._toggle_mode()  # → scientific
        app._select_operation("power")
        app._entry_a.insert(0, "2")
        app._entry_b.insert(0, "10")
        app._calculate()
        assert app._result_label.cget("text") == "1024.0"

    def test_show_history_with_no_entries(self, app):
        import tkinter as tk
        app._show_history()
        children = app._root.winfo_children()
        toplevels = [w for w in children if isinstance(w, tk.Toplevel)]
        assert len(toplevels) == 1
        toplevels[0].destroy()

    def test_show_history_with_entries(self, app):
        import tkinter as tk
        from src.history import record_entry
        record_entry("Add: 5.0")
        record_entry("Subtract: 3.0")
        app._show_history()
        children = app._root.winfo_children()
        toplevels = [w for w in children if isinstance(w, tk.Toplevel)]
        assert len(toplevels) == 1
        toplevels[0].destroy()
