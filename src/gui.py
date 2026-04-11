"""Graphical User Interface for the Calculator using tkinter.

Provides a window-based calculator that exposes all operations available
in the :class:`~src.calculator.Calculator` class through a point-and-click
interface.  Supports two modes:

* **Normal mode** — displays only the four basic arithmetic operations
  (add, subtract, multiply, divide) and the power function.
* **Scientific mode** — additionally displays unary scientific operations
  (factorial, square, cube, square_root, cube_root, log, ln).

The GUI wraps the same :class:`~src.calculator.Calculator` backend used
by the CLI and interactive REPL, so operation history is tracked
identically across all interface layers.

Usage::

    python -m src --gui     # launch the GUI window
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext
from typing import Optional

from .calculator import Calculator

# Operations that take two operands (first entered, then second via "=")
TWO_ARG_OPS = {"add", "subtract", "multiply", "divide", "power"}
# Operations that require an integer operand
INT_OPS = {"factorial"}


class CalculatorGUI:
    """Tkinter-based graphical calculator.

    Wraps a :class:`~src.calculator.Calculator` instance and exposes all its
    operations through buttons.  The window starts in **normal mode** (basic
    arithmetic only); clicking *Normal / Scientific* toggles scientific
    operations on or off.

    Binary operations (add, subtract, multiply, divide, power) follow the
    two-step flow: click the operator button to store the first operand, then
    click ``=`` after entering the second operand.  Unary scientific operations
    apply immediately to whatever value is on the display.

    Attributes:
        root: The root ``tk.Tk`` window.
        calc: The :class:`~src.calculator.Calculator` that holds history.
        scientific_mode: Whether scientific operation buttons are currently active.
        _pending_op: Name of the binary operation awaiting its second operand.
        _pending_value: First operand stored for the pending binary operation.
        _should_reset: When ``True`` the next digit press clears the display first.
    """

    def __init__(self, root: tk.Tk) -> None:
        """Initialise the GUI and build all widgets.

        Args:
            root: The root ``tk.Tk`` window to attach all widgets to.
        """
        self.root = root
        self.root.title("Calculator")
        self.root.resizable(False, False)

        self.calc = Calculator()
        self.scientific_mode: bool = False
        self._pending_op: Optional[str] = None
        self._pending_value: Optional[float] = None
        self._should_reset: bool = False

        self._build_ui()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        """Create and lay out all widgets in the root window."""
        # Result / input display
        self._display_var = tk.StringVar(value="0")
        display = tk.Entry(
            self.root,
            textvariable=self._display_var,
            font=("Helvetica", 24),
            justify="right",
            state="readonly",
            width=16,
        )
        display.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky="ew")

        # Mode toggle and history row
        mode_btn = tk.Button(
            self.root,
            text="Normal / Scientific",
            command=self._toggle_mode,
            width=20,
        )
        mode_btn.grid(row=1, column=0, columnspan=3, padx=5, pady=2, sticky="ew")

        history_btn = tk.Button(
            self.root,
            text="History",
            command=self._show_history,
            width=10,
        )
        history_btn.grid(row=1, column=3, columnspan=2, padx=5, pady=2, sticky="ew")

        self._build_scientific_ops()
        self._build_number_pad()
        self._build_basic_ops()

    def _build_number_pad(self) -> None:
        """Create digit buttons (0–9), decimal point, and clear."""
        buttons = [
            ("7", 3, 0), ("8", 3, 1), ("9", 3, 2),
            ("4", 4, 0), ("5", 4, 1), ("6", 4, 2),
            ("1", 5, 0), ("2", 5, 1), ("3", 5, 2),
            ("0", 6, 0), (".", 6, 1), ("C", 6, 2),
        ]
        for label, row, col in buttons:
            if label == "C":
                cmd = self._on_clear
            else:
                cmd = lambda d=label: self._on_digit(d)
            btn = tk.Button(
                self.root,
                text=label,
                font=("Helvetica", 14),
                width=5,
                command=cmd,
            )
            btn.grid(row=row, column=col, padx=3, pady=3)

    def _build_basic_ops(self) -> None:
        """Create buttons for binary arithmetic operations, power, and equals."""
        binary_ops = [
            ("+", "add", 3, 3),
            ("-", "subtract", 4, 3),
            ("×", "multiply", 5, 3),
            ("÷", "divide", 6, 3),
        ]
        for label, op, row, col in binary_ops:
            btn = tk.Button(
                self.root,
                text=label,
                font=("Helvetica", 14),
                width=5,
                command=lambda o=op: self._on_binary_op(o),
            )
            btn.grid(row=row, column=col, padx=3, pady=3)

        # Power is a two-arg op placed in the scientific row area
        power_btn = tk.Button(
            self.root,
            text="x^y",
            font=("Helvetica", 14),
            width=5,
            command=lambda: self._on_binary_op("power"),
        )
        power_btn.grid(row=3, column=4, padx=3, pady=3)

        # Equals spans multiple rows for visual weight
        equals_btn = tk.Button(
            self.root,
            text="=",
            font=("Helvetica", 14),
            width=5,
            command=self._on_equals,
        )
        equals_btn.grid(row=4, column=4, rowspan=3, padx=3, pady=3, sticky="ns")

    def _build_scientific_ops(self) -> None:
        """Create buttons for unary scientific operations (disabled in normal mode)."""
        sci_ops = [
            ("n!", "factorial", 2, 0),
            ("x²", "square", 2, 1),
            ("x³", "cube", 2, 2),
            ("√x", "square_root", 2, 3),
            ("∛x", "cube_root", 2, 4),
            ("log", "log", 7, 0),
            ("ln", "ln", 7, 1),
        ]
        self._sci_buttons: list[tk.Button] = []
        for label, op, row, col in sci_ops:
            btn = tk.Button(
                self.root,
                text=label,
                font=("Helvetica", 14),
                width=5,
                command=lambda o=op: self._on_unary_op(o),
            )
            btn.grid(row=row, column=col, padx=3, pady=3)
            self._sci_buttons.append(btn)

        self._update_sci_buttons_state()

    # ------------------------------------------------------------------
    # Display helpers
    # ------------------------------------------------------------------

    def _get_display(self) -> str:
        """Return the current string shown on the display."""
        return self._display_var.get()

    def _set_display(self, value: str) -> None:
        """Write *value* to the display."""
        self._display_var.set(value)

    def _display_float(self, value: float) -> None:
        """Format *value* and write it to the display.

        Whole-number results are shown without a decimal point
        (e.g. ``7`` rather than ``7.0``).
        """
        if value == int(value):
            self._set_display(str(int(value)))
        else:
            self._set_display(str(value))

    def _update_sci_buttons_state(self) -> None:
        """Enable or disable scientific buttons according to :attr:`scientific_mode`."""
        state = tk.NORMAL if self.scientific_mode else tk.DISABLED
        for btn in self._sci_buttons:
            btn.configure(state=state)

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _on_digit(self, digit: str) -> None:
        """Append *digit* to the current display value.

        If :attr:`_should_reset` is ``True`` the display is cleared first
        (this happens after a binary operator or a completed calculation).
        A leading ``"0"`` is replaced rather than extended unless ``digit``
        is ``"."``.  Duplicate decimal points are ignored.

        Args:
            digit: A single character — one of ``"0"``–``"9"`` or ``"."``.
        """
        current = self._get_display()
        if self._should_reset:
            current = ""
            self._should_reset = False
        if digit == "." and "." in current:
            return
        if current == "0" and digit != ".":
            current = ""
        self._set_display(current + digit)

    def _on_clear(self) -> None:
        """Reset the display to ``"0"`` and clear any pending binary operation."""
        self._set_display("0")
        self._pending_op = None
        self._pending_value = None
        self._should_reset = False

    def _on_binary_op(self, op: str) -> None:
        """Store the current display value and *op* for the next ``=`` press.

        Args:
            op: Operation name (``"add"``, ``"subtract"``, ``"multiply"``,
                ``"divide"``, or ``"power"``).
        """
        try:
            self._pending_value = float(self._get_display())
        except ValueError:
            messagebox.showerror("Input Error", "Invalid number on display.")
            return
        self._pending_op = op
        self._should_reset = True

    def _on_equals(self) -> None:
        """Execute the stored binary operation with the current display as the second operand.

        Does nothing if no binary operator has been selected yet.
        On success, updates the display with the result and sets
        :attr:`_should_reset` so the next digit press starts fresh.
        On error, shows a message box and clears the calculator state.
        """
        if self._pending_op is None or self._pending_value is None:
            return
        try:
            b = float(self._get_display())
        except ValueError:
            messagebox.showerror("Input Error", "Invalid number on display.")
            return
        op_method = getattr(self.calc, self._pending_op)
        try:
            result = op_method(self._pending_value, b)
        except (ValueError, ZeroDivisionError, TypeError) as exc:
            messagebox.showerror("Calculation Error", str(exc))
            self._on_clear()
            return
        self._display_float(result)
        self._pending_op = None
        self._pending_value = None
        self._should_reset = True

    def _on_unary_op(self, op: str) -> None:
        """Apply a single-operand scientific operation to the current display value.

        Args:
            op: Operation name (``"factorial"``, ``"square"``, ``"cube"``,
                ``"square_root"``, ``"cube_root"``, ``"log"``, or ``"ln"``).
        """
        try:
            if op in INT_OPS:
                a = int(float(self._get_display()))
            else:
                a = float(self._get_display())
        except ValueError:
            messagebox.showerror("Input Error", "Invalid number on display.")
            return
        op_method = getattr(self.calc, op)
        try:
            result = op_method(a)
        except (ValueError, ZeroDivisionError, TypeError) as exc:
            messagebox.showerror("Calculation Error", str(exc))
            return
        self._display_float(result)
        self._should_reset = True

    def _toggle_mode(self) -> None:
        """Toggle between normal mode (basic ops) and scientific mode (all ops).

        Updates the window title and enables/disables the scientific buttons.
        """
        self.scientific_mode = not self.scientific_mode
        mode_label = "Scientific" if self.scientific_mode else "Normal"
        self.root.title(f"Calculator [{mode_label}]")
        self._update_sci_buttons_state()

    def _show_history(self) -> None:
        """Open a modal window showing the current session's operation history."""
        history = self.calc.get_history()
        win = tk.Toplevel(self.root)
        win.title("History")
        win.resizable(False, False)

        text = scrolledtext.ScrolledText(win, width=40, height=15, state="normal")
        text.pack(padx=10, pady=10)

        if not history:
            text.insert(tk.END, "No history yet.")
        else:
            for i, entry in enumerate(history, start=1):
                args_str = ", ".join(str(a) for a in entry["args"])
                line = f"{i}. {entry['operation']}({args_str}) = {entry['result']}\n"
                text.insert(tk.END, line)

        text.configure(state="disabled")
        close_btn = tk.Button(win, text="Close", command=win.destroy)
        close_btn.pack(pady=(0, 10))


def launch_gui() -> None:
    """Create the root ``tk.Tk`` window and start the GUI event loop.

    This is the primary entry point for GUI mode, called from
    :mod:`src.__main__` when the ``--gui`` flag is passed.
    """
    root = tk.Tk()
    CalculatorGUI(root)
    root.mainloop()
