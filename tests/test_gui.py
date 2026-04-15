"""Tests for the tkinter-based calculator GUI (src/gui.py).

Tests are split into two groups:

1. Mode class tests — pure Python; no tkinter dependency.
2. CalculatorGUI logic tests — tkinter widgets are replaced with MagicMocks
   so tests can run in headless CI environments (no DISPLAY required).

When tkinter is not installed a MagicMock stub is injected into sys.modules
before src.gui is imported, allowing all tests to run regardless of whether
a graphical environment is present.
"""

import sys
import pytest
from unittest.mock import MagicMock, patch

# ---------------------------------------------------------------------------
# Ensure tkinter (and its sub-modules) are importable before loading src.gui.
# In headless CI environments tkinter may not be installed; injecting a mock
# lets the module-level import succeed without skipping any tests.
# ---------------------------------------------------------------------------
try:
    import tkinter as _real_tk  # noqa: F401 — existence check only
except ImportError:
    _tk_mock = MagicMock()
    sys.modules.setdefault("tkinter", _tk_mock)
    sys.modules.setdefault("tkinter.messagebox", _tk_mock)
    sys.modules.setdefault("tkinter.scrolledtext", _tk_mock)

import tkinter as tk  # noqa: E402 — after potential mock injection

from src.gui import (  # noqa: E402
    CalculatorMode,
    NormalMode,
    ScientificMode,
    CalculatorGUI,
)
from src.session import ALL_OPS, BINARY_OPS, UNARY_OPS


# ===========================================================================
# Mode class tests — no tkinter
# ===========================================================================


class TestCalculatorModeAbstraction:
    """Verify that CalculatorMode is a proper ABC."""

    def test_cannot_instantiate_directly(self):
        with pytest.raises(TypeError):
            CalculatorMode()  # abstract methods prevent direct construction


class TestNormalMode:
    def test_name(self):
        assert NormalMode.name == "Normal"

    def test_is_calculator_mode_subclass(self):
        assert issubclass(NormalMode, CalculatorMode)

    def test_is_instantiable(self):
        assert isinstance(NormalMode(), CalculatorMode)

    def test_operation_count(self):
        assert len(NormalMode.operations) == 6

    def test_all_op_names_are_valid_session_ops(self):
        for label, (op_name, arity) in NormalMode.operations.items():
            assert op_name in ALL_OPS, f"'{op_name}' (from label '{label}') not in ALL_OPS"

    def test_arities_are_1_or_2(self):
        for label, (op_name, arity) in NormalMode.operations.items():
            assert arity in (1, 2), f"Unexpected arity {arity} for '{label}'"

    def test_contains_basic_arithmetic(self):
        op_names = {v[0] for v in NormalMode.operations.values()}
        for op in ("add", "subtract", "multiply", "divide"):
            assert op in op_names

    def test_contains_square_and_square_root(self):
        op_names = {v[0] for v in NormalMode.operations.values()}
        assert "square" in op_names
        assert "square_root" in op_names

    def test_binary_ops_have_arity_2(self):
        for label, (op_name, arity) in NormalMode.operations.items():
            if op_name in BINARY_OPS:
                assert arity == 2, f"Binary op '{op_name}' should have arity 2"

    def test_unary_ops_have_arity_1(self):
        for label, (op_name, arity) in NormalMode.operations.items():
            if op_name in UNARY_OPS:
                assert arity == 1, f"Unary op '{op_name}' should have arity 1"

    def test_labels_are_unique(self):
        labels = list(NormalMode.operations.keys())
        assert len(labels) == len(set(labels))


class TestScientificMode:
    def test_name(self):
        assert ScientificMode.name == "Scientific"

    def test_is_calculator_mode_subclass(self):
        assert issubclass(ScientificMode, CalculatorMode)

    def test_is_instantiable(self):
        assert isinstance(ScientificMode(), CalculatorMode)

    def test_operation_count(self):
        assert len(ScientificMode.operations) == 18

    def test_all_op_names_are_valid_session_ops(self):
        for label, (op_name, arity) in ScientificMode.operations.items():
            assert op_name in ALL_OPS, f"'{op_name}' (from label '{label}') not in ALL_OPS"

    def test_arities_are_1_or_2(self):
        for label, (op_name, arity) in ScientificMode.operations.items():
            assert arity in (1, 2), f"Unexpected arity {arity} for '{label}'"

    def test_normal_ops_are_a_subset(self):
        normal_names = {v[0] for v in NormalMode.operations.values()}
        scientific_names = {v[0] for v in ScientificMode.operations.values()}
        assert normal_names.issubset(scientific_names)

    def test_contains_all_18_ops(self):
        scientific_names = {v[0] for v in ScientificMode.operations.values()}
        assert scientific_names == ALL_OPS

    def test_contains_trig_ops(self):
        op_names = {v[0] for v in ScientificMode.operations.values()}
        for op in ("sin", "cos", "tan", "cot", "asin", "acos"):
            assert op in op_names

    def test_contains_power_log_factorial(self):
        op_names = {v[0] for v in ScientificMode.operations.values()}
        for op in ("power", "log", "ln", "factorial", "cube", "cube_root"):
            assert op in op_names

    def test_binary_ops_have_arity_2(self):
        for label, (op_name, arity) in ScientificMode.operations.items():
            if op_name in BINARY_OPS:
                assert arity == 2

    def test_unary_ops_have_arity_1(self):
        for label, (op_name, arity) in ScientificMode.operations.items():
            if op_name in UNARY_OPS:
                assert arity == 1

    def test_labels_are_unique(self):
        labels = list(ScientificMode.operations.keys())
        assert len(labels) == len(set(labels))


# ===========================================================================
# CalculatorGUI._parse_operand — static method; no tkinter
# ===========================================================================


class TestParseOperand:
    def test_integer_string(self):
        assert CalculatorGUI._parse_operand("5") == 5
        assert isinstance(CalculatorGUI._parse_operand("5"), int)

    def test_float_string(self):
        result = CalculatorGUI._parse_operand("3.14")
        assert isinstance(result, float)
        assert result == pytest.approx(3.14)

    def test_negative_integer(self):
        assert CalculatorGUI._parse_operand("-7") == -7

    def test_negative_float(self):
        result = CalculatorGUI._parse_operand("-2.5")
        assert result == pytest.approx(-2.5)

    def test_require_int_accepts_integer_string(self):
        assert CalculatorGUI._parse_operand("10", require_int=True) == 10

    def test_require_int_rejects_float_string(self):
        with pytest.raises(ValueError):
            CalculatorGUI._parse_operand("3.14", require_int=True)

    def test_invalid_string_raises_value_error(self):
        with pytest.raises(ValueError):
            CalculatorGUI._parse_operand("abc")

    def test_empty_string_raises_value_error(self):
        with pytest.raises(ValueError):
            CalculatorGUI._parse_operand("")


# ===========================================================================
# CalculatorGUI logic tests — tkinter widgets are mocked
# ===========================================================================


@pytest.fixture
def gui():
    """Return a CalculatorGUI with _build_ui and _refresh_operations replaced
    by no-ops so no real tkinter widgets are created.  Tests then inject
    MagicMock attributes to stand in for each widget the logic reads or writes.
    """
    with (
        patch.object(CalculatorGUI, "_build_ui", lambda self: None),
        patch.object(CalculatorGUI, "_refresh_operations", lambda self: None),
    ):
        root = MagicMock()
        instance = CalculatorGUI(root)

    # Inject mock widgets that the logic methods interact with
    instance._op_listbox = MagicMock()
    instance._input_a_var = MagicMock()
    instance._input_b_var = MagicMock()
    instance._result_var = MagicMock()
    instance._history_text = MagicMock()
    instance._mode_var = MagicMock()
    instance._label_b = MagicMock()
    instance._entry_b = MagicMock()
    return instance


class TestCalculatorGUIInit:
    def test_initial_mode_is_normal(self, gui):
        assert isinstance(gui._mode, NormalMode)

    def test_session_is_calculator_session(self, gui):
        from src.session import CalculatorSession
        assert isinstance(gui._session, CalculatorSession)

    def test_history_is_empty_on_start(self, gui):
        assert gui._session.history() == []


class TestModeSwitch:
    def test_switch_to_scientific(self, gui):
        gui._mode_var.get.return_value = "Scientific"
        with patch.object(gui, "_refresh_operations") as mock_refresh:
            gui._on_mode_change()
        assert isinstance(gui._mode, ScientificMode)
        mock_refresh.assert_called_once()

    def test_switch_to_normal(self, gui):
        gui._mode = ScientificMode()
        gui._mode_var.get.return_value = "Normal"
        with patch.object(gui, "_refresh_operations") as mock_refresh:
            gui._on_mode_change()
        assert isinstance(gui._mode, NormalMode)
        mock_refresh.assert_called_once()

    def test_switch_to_scientific_and_back(self, gui):
        # _refresh_operations calls _on_op_selected, which reads from
        # _op_listbox; keep the listbox returning an empty selection so
        # _on_op_selected exits early and doesn't hit the operations dict.
        gui._op_listbox.curselection.return_value = ()

        gui._mode_var.get.return_value = "Scientific"
        gui._on_mode_change()
        assert isinstance(gui._mode, ScientificMode)

        gui._mode_var.get.return_value = "Normal"
        gui._on_mode_change()
        assert isinstance(gui._mode, NormalMode)


class TestOpSelected:
    def test_unary_hides_second_input(self, gui):
        gui._mode = NormalMode()
        # "Square" is unary (arity=1)
        gui._op_listbox.curselection.return_value = (4,)  # index of "Square"
        gui._op_listbox.get.return_value = "Square"
        gui._on_op_selected(None)
        gui._label_b.grid_remove.assert_called()
        gui._entry_b.grid_remove.assert_called()

    def test_binary_shows_second_input(self, gui):
        gui._mode = NormalMode()
        # "Add" is binary (arity=2)
        gui._op_listbox.curselection.return_value = (0,)
        gui._op_listbox.get.return_value = "Add"
        gui._on_op_selected(None)
        gui._label_b.grid.assert_called()
        gui._entry_b.grid.assert_called()

    def test_empty_selection_is_ignored(self, gui):
        gui._op_listbox.curselection.return_value = ()
        # Should not raise
        gui._on_op_selected(None)


class TestCalculate:
    def test_binary_operation_add(self, gui):
        gui._mode = NormalMode()
        gui._op_listbox.curselection.return_value = (0,)
        gui._op_listbox.get.return_value = "Add"
        gui._input_a_var.get.return_value = "3"
        gui._input_b_var.get.return_value = "4"

        with patch.object(gui, "_refresh_history") as mock_refresh:
            gui._on_calculate()

        gui._result_var.set.assert_called_once_with("7")
        mock_refresh.assert_called_once()
        assert gui._session.history() == ["add(3, 4) = 7"]

    def test_unary_operation_square(self, gui):
        gui._mode = NormalMode()
        gui._op_listbox.curselection.return_value = (4,)
        gui._op_listbox.get.return_value = "Square"
        gui._input_a_var.get.return_value = "5"

        with patch.object(gui, "_refresh_history") as mock_refresh:
            gui._on_calculate()

        gui._result_var.set.assert_called_once_with("25")
        mock_refresh.assert_called_once()

    def test_factorial_uses_integer_operand(self, gui):
        gui._mode = ScientificMode()
        gui._op_listbox.curselection.return_value = (6,)
        gui._op_listbox.get.return_value = "Factorial"
        gui._input_a_var.get.return_value = "5"

        with patch.object(gui, "_refresh_history"):
            gui._on_calculate()

        gui._result_var.set.assert_called_once_with("120")

    def test_factorial_float_input_shows_error(self, gui):
        gui._mode = ScientificMode()
        gui._op_listbox.curselection.return_value = (6,)
        gui._op_listbox.get.return_value = "Factorial"
        gui._input_a_var.get.return_value = "5.5"

        with patch("src.gui.messagebox") as mock_mb:
            gui._on_calculate()

        mock_mb.showerror.assert_called_once()
        gui._result_var.set.assert_not_called()

    def test_division_by_zero_shows_error(self, gui):
        gui._mode = NormalMode()
        gui._op_listbox.curselection.return_value = (3,)
        gui._op_listbox.get.return_value = "Divide"
        gui._input_a_var.get.return_value = "5"
        gui._input_b_var.get.return_value = "0"

        with patch("src.gui.messagebox") as mock_mb:
            gui._on_calculate()

        mock_mb.showerror.assert_called_once()
        gui._result_var.set.assert_not_called()

    def test_sqrt_negative_shows_error(self, gui):
        gui._mode = NormalMode()
        gui._op_listbox.curselection.return_value = (5,)
        gui._op_listbox.get.return_value = "Square Root"
        gui._input_a_var.get.return_value = "-4"

        with patch("src.gui.messagebox") as mock_mb:
            gui._on_calculate()

        mock_mb.showerror.assert_called_once()

    def test_missing_operand_a_shows_error(self, gui):
        gui._mode = NormalMode()
        gui._op_listbox.curselection.return_value = (0,)
        gui._op_listbox.get.return_value = "Add"
        gui._input_a_var.get.return_value = ""

        with patch("src.gui.messagebox") as mock_mb:
            gui._on_calculate()

        mock_mb.showerror.assert_called_once()
        gui._result_var.set.assert_not_called()

    def test_missing_operand_b_shows_error(self, gui):
        gui._mode = NormalMode()
        gui._op_listbox.curselection.return_value = (0,)
        gui._op_listbox.get.return_value = "Add"
        gui._input_a_var.get.return_value = "3"
        gui._input_b_var.get.return_value = ""

        with patch("src.gui.messagebox") as mock_mb:
            gui._on_calculate()

        mock_mb.showerror.assert_called_once()
        gui._result_var.set.assert_not_called()

    def test_invalid_non_numeric_a_shows_error(self, gui):
        gui._mode = NormalMode()
        gui._op_listbox.curselection.return_value = (0,)
        gui._op_listbox.get.return_value = "Add"
        gui._input_a_var.get.return_value = "abc"

        with patch("src.gui.messagebox") as mock_mb:
            gui._on_calculate()

        mock_mb.showerror.assert_called_once()

    def test_no_selection_shows_warning(self, gui):
        gui._op_listbox.curselection.return_value = ()

        with patch("src.gui.messagebox") as mock_mb:
            gui._on_calculate()

        mock_mb.showwarning.assert_called_once()
        gui._result_var.set.assert_not_called()

    def test_history_grows_with_calculations(self, gui):
        gui._mode = NormalMode()

        for operands, expected in [
            (("Add", "1", "2"), "add(1, 2) = 3"),
            (("Multiply", "3", "4"), "multiply(3, 4) = 12"),
        ]:
            op_label, a, b = operands
            gui._op_listbox.curselection.return_value = (0,)
            gui._op_listbox.get.return_value = op_label
            gui._input_a_var.get.return_value = a
            gui._input_b_var.get.return_value = b
            with patch.object(gui, "_refresh_history"):
                gui._on_calculate()

        hist = gui._session.history()
        assert len(hist) == 2
        assert hist[0] == "add(1, 2) = 3"
        assert hist[1] == "multiply(3, 4) = 12"

    def test_failed_calculation_does_not_add_to_history(self, gui):
        gui._mode = NormalMode()
        gui._op_listbox.curselection.return_value = (3,)
        gui._op_listbox.get.return_value = "Divide"
        gui._input_a_var.get.return_value = "1"
        gui._input_b_var.get.return_value = "0"

        with patch("src.gui.messagebox"):
            gui._on_calculate()

        assert gui._session.history() == []


class TestRefreshHistory:
    def test_refresh_history_writes_entries(self, gui):
        # Pre-populate history via a successful calculation
        gui._mode = NormalMode()
        gui._op_listbox.curselection.return_value = (0,)
        gui._op_listbox.get.return_value = "Add"
        gui._input_a_var.get.return_value = "2"
        gui._input_b_var.get.return_value = "3"
        with patch.object(gui, "_refresh_history"):
            gui._on_calculate()

        # Now call _refresh_history for real
        gui._refresh_history()

        gui._history_text.configure.assert_called()
        gui._history_text.delete.assert_called()
        gui._history_text.insert.assert_called()

    def test_refresh_history_empty_session(self, gui):
        # No calculations yet — should still work without error
        gui._refresh_history()
        gui._history_text.configure.assert_called()
        gui._history_text.delete.assert_called()


class TestScientificModeCalculations:
    """Spot-check scientific mode ops through the GUI calculate path."""

    def _setup_unary(self, gui, label, value):
        gui._mode = ScientificMode()
        gui._op_listbox.curselection.return_value = (0,)
        gui._op_listbox.get.return_value = label
        gui._input_a_var.get.return_value = value

    def test_sin_90(self, gui):
        self._setup_unary(gui, "Sin (deg)", "90")
        with patch.object(gui, "_refresh_history"):
            gui._on_calculate()
        gui._result_var.set.assert_called_once_with("1.0")

    def test_natural_log(self, gui):
        import math
        self._setup_unary(gui, "Natural Log", "1")
        with patch.object(gui, "_refresh_history"):
            gui._on_calculate()
        gui._result_var.set.assert_called_once_with("0.0")

    def test_power_operation(self, gui):
        gui._mode = ScientificMode()
        gui._op_listbox.curselection.return_value = (0,)
        gui._op_listbox.get.return_value = "Power"
        gui._input_a_var.get.return_value = "2"
        gui._input_b_var.get.return_value = "8"
        with patch.object(gui, "_refresh_history"):
            gui._on_calculate()
        gui._result_var.set.assert_called_once_with("256")
