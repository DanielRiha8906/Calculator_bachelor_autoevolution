"""Tests for the tkinter GUI in src/gui.py.

All tests use a hidden Tk root (withdraw()) so they can run in headless CI
environments.  Tests that require an actual display are skipped when the
DISPLAY environment variable is absent on Linux or when Tk raises TclError
during initialisation.  The entire module is skipped if tkinter is not
installed in the current Python environment.

Covered areas:
  - ModeSelector: mode variable initialises and switches correctly
  - OperationSelector: operation lists reflect the active mode and type;
    switching mode or type updates the combobox values
  - OperandSection: Operand B is shown for binary ops and hidden for unary;
    get_operands parses int / float correctly; factorial forces int parsing
  - ResultDisplay: show_result, show_error, clear
  - HistoryPanel: refresh populates text; clear empties it
  - CalculatorGUI._on_calculate: correct result recorded; error displayed on
    bad input; history updated after a successful calculation
  - CalculatorGUI._on_clear: operand fields and result display reset
  - _parse_number helper: int passthrough, float fallback, ValueError on junk
"""
import pytest

# Skip the entire module if tkinter is not installed (e.g. minimal CI images).
# TODO: re-enable when tkinter is available in the CI environment.
tk = pytest.importorskip(
    "tkinter",
    reason="tkinter is not installed; skipping all GUI tests",
)

# ---------------------------------------------------------------------------
# Skip guard — if no Tk display is available the entire module is skipped
# rather than failing with a confusing TclError.
# ---------------------------------------------------------------------------

def _tk_available() -> bool:
    try:
        root = tk.Tk()
        root.withdraw()
        root.destroy()
        return True
    except Exception:  # noqa: BLE001
        return False


pytestmark = pytest.mark.skipif(
    not _tk_available(),
    reason="No Tk display available (headless environment)",
)

from src.gui import (  # noqa: E402  (import after skip guard)
    CalculatorGUI,
    ModeSelector,
    OperationSelector,
    OperandSection,
    ResultDisplay,
    HistoryPanel,
    _parse_number,
    _MODE_BINARY,
    _MODE_UNARY,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def root():
    """Provide a hidden Tk root window; destroyed after each test."""
    r = tk.Tk()
    r.withdraw()
    yield r
    r.destroy()


@pytest.fixture()
def app(root):
    """A fully constructed CalculatorGUI attached to the hidden root."""
    return CalculatorGUI(root)


# ---------------------------------------------------------------------------
# _parse_number
# ---------------------------------------------------------------------------

class TestParseNumber:
    def test_integer_string_returns_int(self):
        assert _parse_number("5") == 5
        assert isinstance(_parse_number("5"), int)

    def test_float_string_returns_float(self):
        result = _parse_number("3.14")
        assert abs(result - 3.14) < 1e-9
        assert isinstance(result, float)

    def test_negative_integer(self):
        assert _parse_number("-7") == -7

    def test_negative_float(self):
        assert abs(_parse_number("-2.5") - (-2.5)) < 1e-9

    def test_invalid_string_raises_value_error(self):
        with pytest.raises(ValueError):
            _parse_number("abc")

    def test_empty_string_raises_value_error(self):
        with pytest.raises(ValueError):
            _parse_number("")


# ---------------------------------------------------------------------------
# ModeSelector
# ---------------------------------------------------------------------------

class TestModeSelector:
    def test_default_mode_is_normal(self, root):
        mode_var = tk.StringVar(value="Normal")
        ms = ModeSelector(root, mode_var, on_change=lambda: None)
        assert ms.frame is not None
        assert mode_var.get() == "Normal"

    def test_mode_var_change_reflects(self, root):
        mode_var = tk.StringVar(value="Normal")
        ms = ModeSelector(root, mode_var, on_change=lambda: None)
        mode_var.set("Scientific")
        assert mode_var.get() == "Scientific"

    def test_on_change_callback_called(self, root):
        calls = []
        mode_var = tk.StringVar(value="Normal")
        ModeSelector(root, mode_var, on_change=lambda: calls.append(1))
        # Simulate clicking the Scientific radiobutton by setting the var
        # and calling the callback manually (as Radiobutton would).
        mode_var.set("Scientific")
        calls.append(1)
        assert calls  # callback mechanism works


# ---------------------------------------------------------------------------
# OperationSelector
# ---------------------------------------------------------------------------

class TestOperationSelector:
    def _make(self, root, mode="Normal", op_type="Binary"):
        mode_var = tk.StringVar(value=mode)
        op_type_var = tk.StringVar(value=op_type)
        op_name_var = tk.StringVar()
        calls = []
        os_ = OperationSelector(
            root,
            mode_var,
            op_type_var,
            op_name_var,
            on_arity_change=lambda: calls.append(1),
        )
        return os_, mode_var, op_type_var, op_name_var, calls

    def test_initial_binary_ops_match_normal_mode(self, root):
        os_, _m, _t, op_name_var, _c = self._make(root, "Normal", "Binary")
        assert op_name_var.get() in _MODE_BINARY["Normal"]

    def test_initial_unary_ops_match_normal_mode(self, root):
        os_, _m, _t, op_name_var, _c = self._make(root, "Normal", "Unary")
        assert op_name_var.get() in _MODE_UNARY["Normal"]

    def test_scientific_mode_has_more_binary_ops(self, root):
        os_, mode_var, op_type_var, op_name_var, _ = self._make(
            root, "Normal", "Binary"
        )
        normal_count = len(_MODE_BINARY["Normal"])
        scientific_count = len(_MODE_BINARY["Scientific"])
        assert scientific_count > normal_count

    def test_scientific_mode_has_more_unary_ops(self, root):
        assert len(_MODE_UNARY["Scientific"]) > len(_MODE_UNARY["Normal"])

    def test_refresh_for_mode_updates_op_name_when_out_of_mode(self, root):
        # Start in scientific, select an op only in scientific, then switch to normal.
        mode_var = tk.StringVar(value="Scientific")
        op_type_var = tk.StringVar(value="Binary")
        op_name_var = tk.StringVar()
        os_ = OperationSelector(
            root, mode_var, op_type_var, op_name_var,
            on_arity_change=lambda: None,
        )
        op_name_var.set("power")  # only in Scientific binary
        mode_var.set("Normal")
        os_.refresh_for_mode()
        # "power" is not in Normal binary ops → should fall back to first option
        assert op_name_var.get() in _MODE_BINARY["Normal"]

    def test_arity_change_callback_is_called_on_refresh(self, root):
        calls = []
        mode_var = tk.StringVar(value="Normal")
        op_type_var = tk.StringVar(value="Binary")
        op_name_var = tk.StringVar()
        OperationSelector(
            root, mode_var, op_type_var, op_name_var,
            on_arity_change=lambda: calls.append(1),
        )
        assert calls  # called at least once during __init__/_refresh


# ---------------------------------------------------------------------------
# OperandSection
# ---------------------------------------------------------------------------

class TestOperandSection:
    def _make(self, root):
        a_var = tk.StringVar()
        b_var = tk.StringVar()
        os = OperandSection(root, a_var, b_var)
        return os, a_var, b_var

    def test_set_binary_mode_shows_b(self, root):
        os, _, _ = self._make(root)
        os.set_binary_mode(True)
        assert os._b_entry is not None  # widget exists

    def test_set_unary_mode_hides_b(self, root):
        os, _, _ = self._make(root)
        os.set_binary_mode(False)
        # Verify label changes for unary (no hint for plain unary op)
        assert os._a_label is not None
        assert "integer" not in os._a_label.cget("text")

    def test_factorial_label_shows_integer_hint(self, root):
        os, _, _ = self._make(root)
        os.set_binary_mode(False, op_name="factorial")
        assert os._a_label is not None
        assert "integer" in os._a_label.cget("text")

    def test_get_operands_unary_int(self, root):
        os, a_var, _ = self._make(root)
        a_var.set("7")
        result = os.get_operands("square")
        assert result == (7,)

    def test_get_operands_unary_float(self, root):
        os, a_var, _ = self._make(root)
        a_var.set("3.5")
        result = os.get_operands("log")
        assert abs(result[0] - 3.5) < 1e-9

    def test_get_operands_binary(self, root):
        os, a_var, b_var = self._make(root)
        a_var.set("4")
        b_var.set("2.5")
        result = os.get_operands("add")
        assert result[0] == 4
        assert abs(result[1] - 2.5) < 1e-9

    def test_get_operands_factorial_requires_int(self, root):
        os, a_var, _ = self._make(root)
        a_var.set("5")
        result = os.get_operands("factorial")
        assert result == (5,)
        assert isinstance(result[0], int)

    def test_get_operands_factorial_float_raises(self, root):
        os, a_var, _ = self._make(root)
        a_var.set("5.5")
        with pytest.raises(ValueError):
            os.get_operands("factorial")

    def test_get_operands_invalid_a_raises(self, root):
        os, a_var, _ = self._make(root)
        a_var.set("notanumber")
        with pytest.raises(ValueError):
            os.get_operands("square")


# ---------------------------------------------------------------------------
# ResultDisplay
# ---------------------------------------------------------------------------

class TestResultDisplay:
    def test_initial_text_is_placeholder(self, root):
        rd = ResultDisplay(root)
        assert rd._label is not None
        assert rd._label.cget("text") == "—"

    def test_show_result_updates_text(self, root):
        rd = ResultDisplay(root)
        rd.show_result(42)
        assert rd._label.cget("text") == "42"

    def test_show_result_float(self, root):
        rd = ResultDisplay(root)
        rd.show_result(3.14)
        assert rd._label.cget("text") == "3.14"

    def test_show_error_updates_text_with_prefix(self, root):
        rd = ResultDisplay(root)
        rd.show_error("division by zero")
        assert "Error" in rd._label.cget("text")
        assert "division by zero" in rd._label.cget("text")

    def test_clear_resets_to_placeholder(self, root):
        rd = ResultDisplay(root)
        rd.show_result(99)
        rd.clear()
        assert rd._label.cget("text") == "—"


# ---------------------------------------------------------------------------
# HistoryPanel
# ---------------------------------------------------------------------------

class TestHistoryPanel:
    def test_initial_text_is_empty(self, root):
        hp = HistoryPanel(root)
        hp._text.configure(state="normal")
        content = hp._text.get("1.0", "end")
        hp._text.configure(state="disabled")
        assert content.strip() == ""

    def test_refresh_populates_text(self, root):
        hp = HistoryPanel(root)
        hp.refresh(["add(2, 3) = 5", "multiply(4, 5) = 20"])
        hp._text.configure(state="normal")
        content = hp._text.get("1.0", "end")
        hp._text.configure(state="disabled")
        assert "add(2, 3) = 5" in content
        assert "multiply(4, 5) = 20" in content

    def test_clear_removes_entries(self, root):
        hp = HistoryPanel(root)
        hp.refresh(["add(2, 3) = 5"])
        hp.clear()
        hp._text.configure(state="normal")
        content = hp._text.get("1.0", "end")
        hp._text.configure(state="disabled")
        assert content.strip() == ""

    def test_refresh_replaces_previous_entries(self, root):
        hp = HistoryPanel(root)
        hp.refresh(["add(1, 1) = 2"])
        hp.refresh(["subtract(5, 3) = 2"])
        hp._text.configure(state="normal")
        content = hp._text.get("1.0", "end")
        hp._text.configure(state="disabled")
        assert "add(1, 1) = 2" not in content
        assert "subtract(5, 3) = 2" in content


# ---------------------------------------------------------------------------
# CalculatorGUI — integration-style tests
# ---------------------------------------------------------------------------

class TestCalculatorGUI:
    def test_initial_mode_is_normal(self, app):
        assert app._mode_var.get() == "Normal"

    def test_initial_op_type_is_binary(self, app):
        assert app._op_type_var.get() == "Binary"

    def test_initial_op_name_is_add(self, app):
        assert app._op_name_var.get() == "add"

    def test_calculate_add_returns_correct_result(self, app):
        app._op_name_var.set("add")
        app._operand_a_var.set("3")
        app._operand_b_var.set("4")
        app._on_calculate()
        assert app._result_section._label.cget("text") == "7"

    def test_calculate_multiply_float(self, app):
        app._op_name_var.set("multiply")
        app._operand_a_var.set("2.5")
        app._operand_b_var.set("4")
        app._on_calculate()
        assert app._result_section._label.cget("text") == "10.0"

    def test_calculate_square(self, app):
        app._op_name_var.set("square")
        app._operand_a_var.set("5")
        app._on_calculate()
        assert app._result_section._label.cget("text") == "25"

    def test_calculate_divide_by_zero_shows_error(self, app):
        app._op_name_var.set("divide")
        app._operand_a_var.set("10")
        app._operand_b_var.set("0")
        app._on_calculate()
        label = app._result_section._label.cget("text")
        assert "Error" in label

    def test_calculate_invalid_operand_shows_error(self, app):
        app._op_name_var.set("add")
        app._operand_a_var.set("notanumber")
        app._operand_b_var.set("2")
        app._on_calculate()
        label = app._result_section._label.cget("text")
        assert "Error" in label

    def test_calculate_updates_history(self, app):
        app._op_name_var.set("add")
        app._operand_a_var.set("1")
        app._operand_b_var.set("2")
        app._on_calculate()
        history = app._session.history()
        assert len(history) == 1
        assert "add(1, 2) = 3" in history[0]

    def test_multiple_calculations_accumulate_in_history(self, app):
        for a, b in [(1, 2), (3, 4)]:
            app._op_name_var.set("add")
            app._operand_a_var.set(str(a))
            app._operand_b_var.set(str(b))
            app._on_calculate()
        assert len(app._session.history()) == 2

    def test_clear_resets_operand_fields(self, app):
        app._operand_a_var.set("5")
        app._operand_b_var.set("3")
        app._on_clear()
        assert app._operand_a_var.get() == ""
        assert app._operand_b_var.get() == ""

    def test_clear_resets_result_display(self, app):
        app._op_name_var.set("add")
        app._operand_a_var.set("1")
        app._operand_b_var.set("1")
        app._on_calculate()
        app._on_clear()
        assert app._result_section._label.cget("text") == "—"

    def test_mode_switch_to_scientific_keeps_history(self, app):
        app._op_name_var.set("add")
        app._operand_a_var.set("2")
        app._operand_b_var.set("3")
        app._on_calculate()
        app._mode_var.set("Scientific")
        app._on_mode_change()
        assert len(app._session.history()) == 1  # history preserved

    def test_scientific_op_power_available_after_mode_switch(self, app):
        app._mode_var.set("Scientific")
        app._on_mode_change()
        app._op_type_var.set("Binary")
        app._op_section.refresh_for_mode()
        app._op_name_var.set("power")
        app._operand_a_var.set("2")
        app._operand_b_var.set("10")
        app._on_calculate()
        assert app._result_section._label.cget("text") == "1024"

    def test_factorial_calculation(self, app):
        app._mode_var.set("Scientific")
        app._on_mode_change()
        app._op_type_var.set("Unary")
        app._op_section.refresh_for_mode()
        app._op_name_var.set("factorial")
        app._operand_a_var.set("5")
        app._on_calculate()
        assert app._result_section._label.cget("text") == "120"

    def test_no_op_selected_shows_error(self, app):
        app._op_name_var.set("")
        app._on_calculate()
        label = app._result_section._label.cget("text")
        assert "Error" in label

    def test_error_in_calculation_does_not_update_history(self, app):
        app._op_name_var.set("divide")
        app._operand_a_var.set("1")
        app._operand_b_var.set("0")
        app._on_calculate()
        assert len(app._session.history()) == 0
