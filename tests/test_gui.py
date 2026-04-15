"""Tests for src/gui.py (CalculatorGUI).

tkinter is injected as a fake module into ``sys.modules`` *before*
``src.gui`` is imported, so these tests run in headless CI environments
that have no display and may not even have tkinter installed.

The fixture rebuilds a fresh ``CalculatorGUI`` for every test by
removing ``src.gui`` from ``sys.modules`` and re-importing it against
the fake tkinter.
"""
import importlib
import sys
import pytest
from unittest.mock import MagicMock, patch


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

class _FakeStringVar:
    """Minimal substitute for tkinter.StringVar — stores a string value in memory."""

    def __init__(self, value: str = "") -> None:
        self._val = str(value)

    def set(self, v) -> None:
        self._val = str(v)

    def get(self) -> str:
        return self._val


def _make_fake_tk() -> MagicMock:
    """Return a MagicMock that mimics the tkinter module for GUI construction.

    * ``StringVar`` uses :class:`_FakeStringVar` so callers can read back set values.
    * ``Frame``, ``Label``, and ``Button`` each return a fresh ``MagicMock``
      per call so that different widgets (e.g. *display_frame* vs *sci_frame*)
      are independent and can be asserted on separately.
    """
    fake_tk = MagicMock()
    fake_tk.StringVar.side_effect = _FakeStringVar
    fake_tk.Frame.side_effect = lambda *a, **kw: MagicMock()
    fake_tk.Label.side_effect = lambda *a, **kw: MagicMock()
    fake_tk.Button.side_effect = lambda *a, **kw: MagicMock()
    return fake_tk


# ---------------------------------------------------------------------------
# Fixture
# ---------------------------------------------------------------------------

@pytest.fixture
def gui(monkeypatch):
    """Return a CalculatorGUI instance with tkinter fully replaced by mocks.

    The fixture injects a fake ``tkinter`` into ``sys.modules`` **before**
    importing ``src.gui``, so the module-level ``import tkinter as tk``
    inside ``gui.py`` picks up the mock without ever touching a real display.
    All per-test state is isolated via ``monkeypatch``; cleanup is automatic.
    """
    fake_tk = _make_fake_tk()
    fake_msgbox = MagicMock()
    # Make the attribute lookup in "from tkinter import messagebox" find our mock.
    fake_tk.messagebox = fake_msgbox

    # Inject fake tkinter before src.gui is imported.
    monkeypatch.setitem(sys.modules, "tkinter", fake_tk)
    monkeypatch.setitem(sys.modules, "tkinter.messagebox", fake_msgbox)
    monkeypatch.setitem(sys.modules, "tkinter.ttk", MagicMock())

    # Force re-import of src.gui with the fake tkinter in place.
    monkeypatch.delitem(sys.modules, "src.gui", raising=False)

    import src.gui as gui_module  # noqa: PLC0415

    root = MagicMock()
    g = gui_module.CalculatorGUI(root)
    # Expose the messagebox mock so tests can assert on showinfo calls.
    g._fake_msgbox = gui_module.messagebox
    return g


# ---------------------------------------------------------------------------
# _format static method
# ---------------------------------------------------------------------------

def test_format_whole_float(gui):
    assert gui._format(3.0) == "3"


def test_format_non_whole_float(gui):
    assert gui._format(3.14) == "3.14"


def test_format_integer(gui):
    assert gui._format(5) == "5"


def test_format_negative_whole_float(gui):
    assert gui._format(-2.0) == "-2"


# ---------------------------------------------------------------------------
# press_digit
# ---------------------------------------------------------------------------

def test_press_digit_single(gui):
    gui.press_digit("5")
    assert gui._current_input == "5"
    assert gui.display_var.get() == "5"


def test_press_digit_multiple(gui):
    gui.press_digit("1")
    gui.press_digit("2")
    gui.press_digit("3")
    assert gui._current_input == "123"


def test_press_digit_decimal_once(gui):
    gui.press_digit("3")
    gui.press_digit(".")
    gui.press_digit("1")
    assert gui._current_input == "3.1"


def test_press_digit_decimal_twice_ignored(gui):
    gui.press_digit("3")
    gui.press_digit(".")
    gui.press_digit(".")
    assert gui._current_input.count(".") == 1


def test_press_digit_leading_zero_replaced(gui):
    gui._current_input = "0"
    gui.press_digit("5")
    assert gui._current_input == "5"


def test_press_digit_zero_then_decimal(gui):
    gui._current_input = "0"
    gui.press_digit(".")
    # "0." is a valid in-progress decimal input.
    assert gui._current_input == "0."


# ---------------------------------------------------------------------------
# clear
# ---------------------------------------------------------------------------

def test_clear_resets_input(gui):
    gui.press_digit("7")
    gui.clear()
    assert gui._current_input == ""


def test_clear_resets_display(gui):
    gui.press_digit("7")
    gui.clear()
    assert gui.display_var.get() == "0"


def test_clear_resets_expression(gui):
    gui.press_digit("7")
    gui.set_binary_op("add")
    gui.clear()
    assert gui.expression_var.get() == ""


def test_clear_resets_pending_op_and_operand(gui):
    gui.press_digit("7")
    gui.set_binary_op("add")
    gui.clear()
    assert gui._pending_op is None
    assert gui._first_operand is None


# ---------------------------------------------------------------------------
# set_binary_op
# ---------------------------------------------------------------------------

def test_set_binary_op_stores_operand(gui):
    gui.press_digit("3")
    gui.set_binary_op("add")
    assert gui._first_operand == 3.0
    assert gui._pending_op == "add"


def test_set_binary_op_clears_input(gui):
    gui.press_digit("3")
    gui.set_binary_op("multiply")
    assert gui._current_input == ""


def test_set_binary_op_updates_expression(gui):
    gui.press_digit("4")
    gui.set_binary_op("subtract")
    assert "subtract" in gui.expression_var.get()


def test_set_binary_op_noop_when_empty(gui):
    gui.set_binary_op("add")
    assert gui._pending_op is None


# ---------------------------------------------------------------------------
# equals
# ---------------------------------------------------------------------------

def test_equals_add(gui):
    gui.press_digit("3")
    gui.set_binary_op("add")
    gui.press_digit("4")
    gui.equals()
    assert gui.display_var.get() == "7"


def test_equals_subtract(gui):
    gui.press_digit("1")
    gui.press_digit("0")
    gui.set_binary_op("subtract")
    gui.press_digit("3")
    gui.equals()
    assert gui.display_var.get() == "7"


def test_equals_multiply(gui):
    gui.press_digit("6")
    gui.set_binary_op("multiply")
    gui.press_digit("7")
    gui.equals()
    assert gui.display_var.get() == "42"


def test_equals_divide(gui):
    gui.press_digit("1")
    gui.press_digit("0")
    gui.set_binary_op("divide")
    gui.press_digit("2")
    gui.equals()
    assert gui.display_var.get() == "5"


def test_equals_result_stored_in_input(gui):
    """After equals the result enters _current_input so it can be chained."""
    gui.press_digit("3")
    gui.set_binary_op("add")
    gui.press_digit("4")
    gui.equals()
    assert gui._current_input == "7"


def test_equals_clears_pending_op(gui):
    gui.press_digit("3")
    gui.set_binary_op("add")
    gui.press_digit("4")
    gui.equals()
    assert gui._pending_op is None
    assert gui._first_operand is None


def test_equals_noop_without_pending_op(gui):
    gui.press_digit("5")
    gui.equals()
    assert gui._current_input == "5"


def test_equals_noop_without_second_input(gui):
    gui.press_digit("5")
    gui.set_binary_op("add")
    gui.equals()
    assert gui._pending_op == "add"


def test_equals_divide_by_zero_shows_error(gui):
    gui.press_digit("5")
    gui.set_binary_op("divide")
    gui.press_digit("0")
    gui.equals()
    assert gui.display_var.get() == "Error"
    assert gui._current_input == ""


def test_equals_power(gui):
    gui.press_digit("2")
    gui.set_binary_op("power")
    gui.press_digit("8")
    gui.equals()
    assert gui.display_var.get() == "256"


# ---------------------------------------------------------------------------
# execute_unary
# ---------------------------------------------------------------------------

def test_execute_unary_square(gui):
    gui.press_digit("4")
    gui.execute_unary("square")
    assert gui.display_var.get() == "16"


def test_execute_unary_square_root(gui):
    gui.press_digit("9")
    gui.execute_unary("square_root")
    assert gui.display_var.get() == "3"


def test_execute_unary_cube(gui):
    gui.press_digit("3")
    gui.execute_unary("cube")
    assert gui.display_var.get() == "27"


def test_execute_unary_result_stored_in_input(gui):
    gui.press_digit("5")
    gui.execute_unary("square")
    assert gui._current_input == "25"


def test_execute_unary_updates_expression(gui):
    gui.press_digit("3")
    gui.execute_unary("square")
    assert "square" in gui.expression_var.get()


def test_execute_unary_noop_when_empty(gui):
    gui.execute_unary("square")
    assert gui._current_input == ""
    assert gui.display_var.get() == "0"


def test_execute_unary_square_root_negative_shows_error(gui):
    gui._current_input = "-4"
    gui.execute_unary("square_root")
    assert gui.display_var.get() == "Error"
    assert gui._current_input == ""


def test_execute_unary_factorial(gui):
    gui.press_digit("5")
    gui.execute_unary("factorial")
    assert gui.display_var.get() == "120"


def test_execute_unary_sin(gui):
    gui._current_input = "0"
    gui.execute_unary("sin")
    assert gui.display_var.get() == "0"


def test_execute_unary_exp(gui):
    gui._current_input = "0"
    gui.execute_unary("exp")
    assert gui.display_var.get() == "1"


# ---------------------------------------------------------------------------
# toggle_mode
# ---------------------------------------------------------------------------

def test_toggle_mode_normal_to_scientific(gui):
    assert gui.mode == "normal"
    gui.toggle_mode()
    assert gui.mode == "scientific"


def test_toggle_mode_scientific_to_normal(gui):
    gui.toggle_mode()  # normal → scientific
    gui.toggle_mode()  # scientific → normal
    assert gui.mode == "normal"


def test_toggle_mode_shows_sci_frame(gui):
    """toggle_mode() into scientific mode calls sci_frame.grid()."""
    before = gui.sci_frame.grid.call_count
    gui.toggle_mode()
    assert gui.sci_frame.grid.call_count == before + 1


def test_toggle_mode_hides_sci_frame(gui):
    """toggle_mode() back to normal mode calls sci_frame.grid_remove()."""
    before = gui.sci_frame.grid_remove.call_count
    gui.toggle_mode()  # show
    gui.toggle_mode()  # hide
    assert gui.sci_frame.grid_remove.call_count == before + 1


# ---------------------------------------------------------------------------
# show_history
# ---------------------------------------------------------------------------

def test_show_history_empty(gui):
    gui.show_history()
    gui._fake_msgbox.showinfo.assert_called_once()
    _, message = gui._fake_msgbox.showinfo.call_args[0]
    assert "No history yet" in message


def test_show_history_with_entries(gui):
    gui.press_digit("3")
    gui.set_binary_op("add")
    gui.press_digit("4")
    gui.equals()
    gui.show_history()
    _, message = gui._fake_msgbox.showinfo.call_args[0]
    assert "add" in message
    assert "7" in message


def test_show_history_multiple_entries_numbered(gui):
    for _ in range(3):
        gui.press_digit("2")
        gui.execute_unary("square")
    gui.show_history()
    _, text = gui._fake_msgbox.showinfo.call_args[0]
    assert "1." in text
    assert "2." in text
    assert "3." in text


# ---------------------------------------------------------------------------
# main() --gui flag
# ---------------------------------------------------------------------------

def test_main_gui_flag_calls_launch_gui(monkeypatch):
    """main() with --gui should import src.gui and call launch_gui()."""
    launch_gui_mock = MagicMock()
    fake_gui_mod = MagicMock()
    fake_gui_mod.launch_gui = launch_gui_mock

    monkeypatch.setitem(sys.modules, "src.gui", fake_gui_mod)
    monkeypatch.setattr(sys, "argv", ["prog", "--gui"])

    from src.__main__ import main  # noqa: PLC0415
    main()

    launch_gui_mock.assert_called_once()
