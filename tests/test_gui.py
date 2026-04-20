"""Tests for the tkinter GUI module (src/gui.py).

Tkinter is mocked via ``sys.modules`` patching so these tests run in
headless CI environments without a graphical display.  They verify the
internal business logic of :class:`~src.gui.CalculatorGUI`:

* Default state after initialisation
* Digit entry and display formatting
* Clear (C) button behaviour
* Binary operator flow (store first operand → press = with second)
* Unary scientific operation flow
* Mode toggle (normal ↔ scientific)
* History integration (operations reach the underlying Calculator)
* ``launch_gui`` creates a Tk window and calls ``mainloop``

The ``messagebox`` reference in ``src.gui`` is patched per-test using
``unittest.mock.patch.object`` on the imported module so error-path
assertions remain isolated.
"""

import sys
import unittest
from unittest.mock import MagicMock, patch


# ---------------------------------------------------------------------------
# Tkinter mock — built once, injected into sys.modules for the whole module
# ---------------------------------------------------------------------------

def _build_tk_mock() -> MagicMock:
    """Return a MagicMock that stands in for the ``tkinter`` module."""
    tk = MagicMock()
    # Constants the GUI accesses by name
    tk.NORMAL = "normal"
    tk.DISABLED = "disabled"
    tk.END = "end"
    return tk


_TK_MOCK = _build_tk_mock()
_MESSAGEBOX_MOCK = MagicMock()
_SCROLLEDTEXT_MOCK = MagicMock()
_TK_MOCK.messagebox = _MESSAGEBOX_MOCK
_TK_MOCK.scrolledtext = _SCROLLEDTEXT_MOCK


# ---------------------------------------------------------------------------
# Base test class — patches sys.modules and imports src.gui once
# ---------------------------------------------------------------------------

class _GUITestBase(unittest.TestCase):
    """Patches tkinter in sys.modules, then imports src.gui."""

    @classmethod
    def setUpClass(cls) -> None:
        cls._patcher = patch.dict(
            "sys.modules",
            {
                "tkinter": _TK_MOCK,
                "tkinter.messagebox": _MESSAGEBOX_MOCK,
                "tkinter.scrolledtext": _SCROLLEDTEXT_MOCK,
            },
        )
        cls._patcher.start()

        # Remove any cached import so we get a fresh module with the mocks
        sys.modules.pop("src.gui", None)
        import src.gui as gui_module

        cls._gui_module = gui_module
        cls.CalculatorGUI = gui_module.CalculatorGUI
        cls.launch_gui = gui_module.launch_gui

    @classmethod
    def tearDownClass(cls) -> None:
        cls._patcher.stop()
        sys.modules.pop("src.gui", None)

    # ------------------------------------------------------------------
    # Helper
    # ------------------------------------------------------------------

    def _make_gui(self) -> "src.gui.CalculatorGUI":  # type: ignore[name-defined]
        """Return a CalculatorGUI with a controllable display mock.

        The real ``_display_var`` (a ``tk.StringVar`` mock) is replaced with
        a fresh ``MagicMock`` whose ``get()`` returns ``"0"`` by default.
        Tests override ``get.return_value`` to simulate display content and
        use ``set.assert_called_with(...)`` to verify updates.

        Scientific buttons are replaced with plain MagicMocks so tests can
        assert ``configure`` calls without caring about grid placement.
        """
        mock_root = MagicMock()
        gui = self.CalculatorGUI(mock_root)

        # Controllable display variable
        display_mock = MagicMock()
        display_mock.get.return_value = "0"
        gui._display_var = display_mock

        # Simple button mocks (7 scientific operations)
        gui._sci_buttons = [MagicMock() for _ in range(7)]
        return gui


# ---------------------------------------------------------------------------
# Test classes
# ---------------------------------------------------------------------------

class TestCalculatorGUIInit(_GUITestBase):
    """CalculatorGUI begins with correct default state."""

    def test_scientific_mode_defaults_to_false(self):
        gui = self._make_gui()
        self.assertFalse(gui.scientific_mode)

    def test_pending_op_defaults_to_none(self):
        gui = self._make_gui()
        self.assertIsNone(gui._pending_op)

    def test_pending_value_defaults_to_none(self):
        gui = self._make_gui()
        self.assertIsNone(gui._pending_value)

    def test_should_reset_defaults_to_false(self):
        gui = self._make_gui()
        self.assertFalse(gui._should_reset)

    def test_calculator_instance_created(self):
        from src.calculator import Calculator
        gui = self._make_gui()
        self.assertIsInstance(gui.calc, Calculator)


class TestDigitInput(_GUITestBase):
    """_on_digit correctly builds up the display string."""

    def test_digit_replaces_leading_zero(self):
        gui = self._make_gui()
        gui._display_var.get.return_value = "0"
        gui._on_digit("5")
        gui._display_var.set.assert_called_with("5")

    def test_digit_appends_to_existing_value(self):
        gui = self._make_gui()
        gui._display_var.get.return_value = "4"
        gui._on_digit("2")
        gui._display_var.set.assert_called_with("42")

    def test_decimal_appended_to_zero(self):
        gui = self._make_gui()
        gui._display_var.get.return_value = "0"
        gui._on_digit(".")
        gui._display_var.set.assert_called_with("0.")

    def test_duplicate_decimal_is_ignored(self):
        gui = self._make_gui()
        gui._display_var.get.return_value = "3.1"
        gui._on_digit(".")
        gui._display_var.set.assert_not_called()

    def test_should_reset_clears_display_before_digit(self):
        gui = self._make_gui()
        gui._display_var.get.return_value = "9"
        gui._should_reset = True
        gui._on_digit("7")
        gui._display_var.set.assert_called_with("7")

    def test_should_reset_flag_cleared_after_digit(self):
        gui = self._make_gui()
        gui._display_var.get.return_value = "9"
        gui._should_reset = True
        gui._on_digit("7")
        self.assertFalse(gui._should_reset)


class TestClear(_GUITestBase):
    """_on_clear resets display and clears all pending state."""

    def test_display_set_to_zero(self):
        gui = self._make_gui()
        gui._on_clear()
        gui._display_var.set.assert_called_with("0")

    def test_pending_op_cleared(self):
        gui = self._make_gui()
        gui._pending_op = "add"
        gui._on_clear()
        self.assertIsNone(gui._pending_op)

    def test_pending_value_cleared(self):
        gui = self._make_gui()
        gui._pending_value = 5.0
        gui._on_clear()
        self.assertIsNone(gui._pending_value)

    def test_should_reset_cleared(self):
        gui = self._make_gui()
        gui._should_reset = True
        gui._on_clear()
        self.assertFalse(gui._should_reset)


class TestBinaryOp(_GUITestBase):
    """_on_binary_op stores operand and operator for the pending operation."""

    def test_stores_pending_op_name(self):
        gui = self._make_gui()
        gui._display_var.get.return_value = "3"
        gui._on_binary_op("add")
        self.assertEqual(gui._pending_op, "add")

    def test_stores_pending_value_as_float(self):
        gui = self._make_gui()
        gui._display_var.get.return_value = "7"
        gui._on_binary_op("multiply")
        self.assertEqual(gui._pending_value, 7.0)

    def test_sets_should_reset_flag(self):
        gui = self._make_gui()
        gui._display_var.get.return_value = "4"
        gui._on_binary_op("subtract")
        self.assertTrue(gui._should_reset)

    def test_invalid_display_shows_error_and_leaves_no_pending_op(self):
        gui = self._make_gui()
        gui._display_var.get.return_value = "abc"
        with patch.object(self._gui_module, "messagebox") as mb:
            gui._on_binary_op("add")
            mb.showerror.assert_called_once()
        self.assertIsNone(gui._pending_op)


class TestEquals(_GUITestBase):
    """_on_equals executes the pending binary operation and updates the display."""

    def test_add_two_integers(self):
        gui = self._make_gui()
        gui._pending_op = "add"
        gui._pending_value = 3.0
        gui._display_var.get.return_value = "4"
        gui._on_equals()
        gui._display_var.set.assert_called_with("7")

    def test_subtract_two_integers(self):
        gui = self._make_gui()
        gui._pending_op = "subtract"
        gui._pending_value = 10.0
        gui._display_var.get.return_value = "3"
        gui._on_equals()
        gui._display_var.set.assert_called_with("7")

    def test_multiply_two_integers(self):
        gui = self._make_gui()
        gui._pending_op = "multiply"
        gui._pending_value = 6.0
        gui._display_var.get.return_value = "7"
        gui._on_equals()
        gui._display_var.set.assert_called_with("42")

    def test_divide_two_integers(self):
        gui = self._make_gui()
        gui._pending_op = "divide"
        gui._pending_value = 10.0
        gui._display_var.get.return_value = "2"
        gui._on_equals()
        gui._display_var.set.assert_called_with("5")

    def test_power_operation(self):
        gui = self._make_gui()
        gui._pending_op = "power"
        gui._pending_value = 2.0
        gui._display_var.get.return_value = "10"
        gui._on_equals()
        gui._display_var.set.assert_called_with("1024")

    def test_divide_by_zero_shows_error(self):
        gui = self._make_gui()
        gui._pending_op = "divide"
        gui._pending_value = 5.0
        gui._display_var.get.return_value = "0"
        with patch.object(self._gui_module, "messagebox") as mb:
            gui._on_equals()
            mb.showerror.assert_called_once()

    def test_no_pending_op_does_nothing(self):
        gui = self._make_gui()
        gui._pending_op = None
        gui._display_var.get.return_value = "5"
        gui._on_equals()
        gui._display_var.set.assert_not_called()

    def test_clears_pending_op_after_success(self):
        gui = self._make_gui()
        gui._pending_op = "add"
        gui._pending_value = 1.0
        gui._display_var.get.return_value = "2"
        gui._on_equals()
        self.assertIsNone(gui._pending_op)

    def test_clears_pending_value_after_success(self):
        gui = self._make_gui()
        gui._pending_op = "add"
        gui._pending_value = 1.0
        gui._display_var.get.return_value = "2"
        gui._on_equals()
        self.assertIsNone(gui._pending_value)

    def test_sets_should_reset_after_success(self):
        gui = self._make_gui()
        gui._pending_op = "add"
        gui._pending_value = 1.0
        gui._display_var.get.return_value = "2"
        gui._on_equals()
        self.assertTrue(gui._should_reset)


class TestUnaryOp(_GUITestBase):
    """_on_unary_op applies a single-operand scientific function."""

    def test_square(self):
        gui = self._make_gui()
        gui._display_var.get.return_value = "5"
        gui._on_unary_op("square")
        gui._display_var.set.assert_called_with("25")

    def test_cube(self):
        gui = self._make_gui()
        gui._display_var.get.return_value = "3"
        gui._on_unary_op("cube")
        gui._display_var.set.assert_called_with("27")

    def test_square_root_of_perfect_square(self):
        gui = self._make_gui()
        gui._display_var.get.return_value = "9"
        gui._on_unary_op("square_root")
        gui._display_var.set.assert_called_with("3")

    def test_factorial(self):
        gui = self._make_gui()
        gui._display_var.get.return_value = "5"
        gui._on_unary_op("factorial")
        gui._display_var.set.assert_called_with("120")

    def test_log_base_ten(self):
        gui = self._make_gui()
        gui._display_var.get.return_value = "100"
        gui._on_unary_op("log")
        # log10(100) = 2 exactly
        gui._display_var.set.assert_called_with("2")

    def test_cube_root(self):
        # cube_root(1) = 1.0 exactly; avoids floating-point rounding issues
        # (e.g. cube_root(27) returns 3.0000000000000004 on some platforms)
        gui = self._make_gui()
        gui._display_var.get.return_value = "1"
        gui._on_unary_op("cube_root")
        gui._display_var.set.assert_called_with("1")

    def test_square_root_of_negative_shows_error(self):
        gui = self._make_gui()
        gui._display_var.get.return_value = "-4"
        with patch.object(self._gui_module, "messagebox") as mb:
            gui._on_unary_op("square_root")
            mb.showerror.assert_called_once()

    def test_sets_should_reset_on_success(self):
        gui = self._make_gui()
        gui._display_var.get.return_value = "4"
        gui._on_unary_op("square")
        self.assertTrue(gui._should_reset)

    def test_does_not_set_should_reset_on_error(self):
        gui = self._make_gui()
        gui._display_var.get.return_value = "-1"
        with patch.object(self._gui_module, "messagebox"):
            gui._on_unary_op("square_root")
        self.assertFalse(gui._should_reset)


class TestModeToggle(_GUITestBase):
    """_toggle_mode switches between normal and scientific mode."""

    def test_starts_in_normal_mode(self):
        gui = self._make_gui()
        self.assertFalse(gui.scientific_mode)

    def test_toggle_enables_scientific(self):
        gui = self._make_gui()
        gui._toggle_mode()
        self.assertTrue(gui.scientific_mode)

    def test_toggle_twice_returns_to_normal(self):
        gui = self._make_gui()
        gui._toggle_mode()
        gui._toggle_mode()
        self.assertFalse(gui.scientific_mode)

    def test_scientific_mode_enables_sci_buttons(self):
        gui = self._make_gui()
        gui._toggle_mode()  # → scientific
        for btn in gui._sci_buttons:
            btn.configure.assert_called_with(state="normal")

    def test_normal_mode_disables_sci_buttons(self):
        gui = self._make_gui()
        gui._toggle_mode()  # → scientific
        for btn in gui._sci_buttons:
            btn.configure.reset_mock()
        gui._toggle_mode()  # → normal
        for btn in gui._sci_buttons:
            btn.configure.assert_called_with(state="disabled")

    def test_title_updated_to_scientific(self):
        gui = self._make_gui()
        gui._toggle_mode()
        gui.root.title.assert_called_with("Calculator [Scientific]")

    def test_title_updated_to_normal(self):
        gui = self._make_gui()
        gui._toggle_mode()
        gui._toggle_mode()
        gui.root.title.assert_called_with("Calculator [Normal]")


class TestDisplayFloat(_GUITestBase):
    """_display_float formats numbers for the display."""

    def test_whole_number_shown_without_decimal(self):
        gui = self._make_gui()
        gui._display_float(5.0)
        gui._display_var.set.assert_called_with("5")

    def test_fractional_number_shown_with_decimal(self):
        gui = self._make_gui()
        gui._display_float(3.14)
        gui._display_var.set.assert_called_with("3.14")

    def test_negative_whole_number(self):
        gui = self._make_gui()
        gui._display_float(-7.0)
        gui._display_var.set.assert_called_with("-7")

    def test_zero(self):
        gui = self._make_gui()
        gui._display_float(0.0)
        gui._display_var.set.assert_called_with("0")


class TestHistoryIntegration(_GUITestBase):
    """Operations executed through the GUI are recorded in Calculator history."""

    def test_binary_op_recorded_in_history(self):
        gui = self._make_gui()
        gui._pending_op = "add"
        gui._pending_value = 3.0
        gui._display_var.get.return_value = "4"
        gui._on_equals()
        history = gui.calc.get_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["operation"], "add")
        self.assertEqual(history[0]["result"], 7)

    def test_unary_op_recorded_in_history(self):
        gui = self._make_gui()
        gui._display_var.get.return_value = "4"
        gui._on_unary_op("square")
        history = gui.calc.get_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["operation"], "square")
        self.assertEqual(history[0]["result"], 16)

    def test_multiple_ops_accumulate_in_history(self):
        gui = self._make_gui()
        # First op: 3 + 4 = 7
        gui._pending_op = "add"
        gui._pending_value = 3.0
        gui._display_var.get.return_value = "4"
        gui._on_equals()
        # Second op: square(5) = 25
        gui._display_var.get.return_value = "5"
        gui._on_unary_op("square")
        self.assertEqual(len(gui.calc.get_history()), 2)

    def test_failed_op_not_recorded_in_history(self):
        gui = self._make_gui()
        gui._pending_op = "divide"
        gui._pending_value = 5.0
        gui._display_var.get.return_value = "0"
        with patch.object(self._gui_module, "messagebox"):
            gui._on_equals()
        self.assertEqual(len(gui.calc.get_history()), 0)


class TestLaunchGui(_GUITestBase):
    """launch_gui creates a Tk window and enters the event loop."""

    def test_creates_tk_window_and_calls_mainloop(self):
        mock_root = MagicMock()
        _TK_MOCK.Tk.return_value = mock_root
        # Call via the module reference to avoid Python's method-binding behaviour
        # (accessing a plain function via `self.name` would inject `self` as arg 1)
        self._gui_module.launch_gui()
        _TK_MOCK.Tk.assert_called()
        mock_root.mainloop.assert_called_once()
