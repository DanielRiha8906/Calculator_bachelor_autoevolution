"""Tkinter GUI for the Calculator application.

Provides a graphical interface that exposes all Calculator operations
(arithmetic, advanced, and scientific) through a point-and-click interface.
All computation is delegated to :class:`src.calculator.Calculator` so the
CLI/REPL interfaces remain fully functional alongside the GUI.

Launch via::

    python -m src --gui

Or programmatically::

    from src.gui import launch_gui
    launch_gui()
"""
import logging
import tkinter as tk
from tkinter import messagebox

from .calculator import Calculator, BINARY_OPS

logger = logging.getLogger(__name__)


class CalculatorGUI:
    """Tkinter-based graphical calculator backed by :class:`~src.calculator.Calculator`.

    The GUI is divided into three areas:

    * **Display** — shows the current expression and the running result.
    * **Main panel** — digit keys, basic binary operators (+−×÷), the
      equals key, common unary operations, and control buttons.
    * **Scientific panel** — ten scientific operations (sin, cos, …, exp);
      toggled by the *Sci* button.

    All operations are executed through :meth:`~src.calculator.Calculator.execute`
    so history is recorded automatically.
    """

    def __init__(self, root: tk.Tk) -> None:
        """Attach the calculator UI to *root* and initialise internal state."""
        self.root = root
        self.calc = Calculator()
        self.mode: str = "normal"
        self._pending_op: str | None = None
        self._first_operand: float | None = None
        self._current_input: str = ""
        self._build_ui()

    # ------------------------------------------------------------------ build

    def _build_ui(self) -> None:
        """Construct all tkinter widgets and lay them out with grid."""
        self.root.title("Calculator")
        self.root.configure(bg="#1a1a2e")
        self.root.resizable(False, False)

        # --- Display area (row 0) ---
        display_frame = tk.Frame(self.root, bg="#1a1a2e", padx=6, pady=6)
        display_frame.grid(row=0, column=0, columnspan=4, sticky="ew")

        self.expression_var = tk.StringVar(value="")
        tk.Label(
            display_frame,
            textvariable=self.expression_var,
            bg="#1a1a2e",
            fg="#888888",
            anchor="e",
            font=("Arial", 11),
        ).pack(fill="x")

        self.display_var = tk.StringVar(value="0")
        tk.Label(
            display_frame,
            textvariable=self.display_var,
            bg="#1a1a2e",
            fg="white",
            anchor="e",
            font=("Arial", 28, "bold"),
        ).pack(fill="x")

        # --- Digit and basic binary-op buttons (rows 1-4) ---
        _DIG = "#34495e"   # digit button colour
        _BOP = "#e74c3c"   # binary op colour
        _EQL = "#e67e22"   # equals colour

        btn_grid = [
            ("7", 1, 0, lambda: self.press_digit("7"), _DIG),
            ("8", 1, 1, lambda: self.press_digit("8"), _DIG),
            ("9", 1, 2, lambda: self.press_digit("9"), _DIG),
            ("÷", 1, 3, lambda: self.set_binary_op("divide"),   _BOP),
            ("4", 2, 0, lambda: self.press_digit("4"), _DIG),
            ("5", 2, 1, lambda: self.press_digit("5"), _DIG),
            ("6", 2, 2, lambda: self.press_digit("6"), _DIG),
            ("×", 2, 3, lambda: self.set_binary_op("multiply"), _BOP),
            ("1", 3, 0, lambda: self.press_digit("1"), _DIG),
            ("2", 3, 1, lambda: self.press_digit("2"), _DIG),
            ("3", 3, 2, lambda: self.press_digit("3"), _DIG),
            ("−", 3, 3, lambda: self.set_binary_op("subtract"), _BOP),
            ("0", 4, 0, lambda: self.press_digit("0"), _DIG),
            (".", 4, 1, lambda: self.press_digit("."), _DIG),
            ("=", 4, 2, self.equals,                             _EQL),
            ("+", 4, 3, lambda: self.set_binary_op("add"),      _BOP),
        ]
        for label, row, col, cmd, bg in btn_grid:
            tk.Button(
                self.root,
                text=label,
                font=("Arial", 16),
                bg=bg,
                fg="white",
                activebackground=bg,
                command=cmd,
            ).grid(row=row, column=col, sticky="nsew", padx=2, pady=2)

        # --- Utility buttons: clear + common unary ops (row 5) ---
        _UOP = "#3498db"   # unary op colour
        utility = [
            ("C",  "#e74c3c", self.clear,                              5, 0),
            ("x²", _UOP,     lambda: self.execute_unary("square"),     5, 1),
            ("√",  _UOP,     lambda: self.execute_unary("square_root"),5, 2),
            ("n!", _UOP,     lambda: self.execute_unary("factorial"),  5, 3),
        ]
        for label, bg, cmd, row, col in utility:
            tk.Button(
                self.root, text=label, font=("Arial", 14),
                bg=bg, fg="white", activebackground=bg, command=cmd,
            ).grid(row=row, column=col, sticky="nsew", padx=2, pady=2)

        # --- More unary ops (row 6) ---
        unary_row = [
            ("x³", "cube"),
            ("∛",  "cube_root"),
            ("log","log"),
            ("ln", "ln"),
        ]
        for col, (label, op) in enumerate(unary_row):
            tk.Button(
                self.root, text=label, font=("Arial", 14),
                bg=_UOP, fg="white", activebackground=_UOP,
                command=lambda o=op: self.execute_unary(o),
            ).grid(row=6, column=col, sticky="nsew", padx=2, pady=2)

        # --- Control row (row 7): power, sci toggle, history ---
        controls = [
            ("xʸ",  "#3498db", lambda: self.set_binary_op("power"), 7, 0),
            ("Sci", "#9b59b6", self.toggle_mode,                    7, 1),
            ("Hist","#27ae60", self.show_history,                   7, 2),
        ]
        for label, bg, cmd, row, col in controls:
            tk.Button(
                self.root, text=label, font=("Arial", 14),
                bg=bg, fg="white", activebackground=bg, command=cmd,
            ).grid(row=row, column=col, sticky="nsew", padx=2, pady=2)

        # --- Scientific panel (row 8, hidden until toggled) ---
        self.sci_frame = tk.Frame(self.root, bg="#2c3e50")
        self.sci_frame.grid(row=8, column=0, columnspan=4, sticky="ew")

        sci_ops = [
            "sin", "cos", "tan", "asin", "acos",
            "atan", "sinh", "cosh", "tanh", "exp",
        ]
        for i, op in enumerate(sci_ops):
            tk.Button(
                self.sci_frame, text=op, font=("Arial", 12),
                bg="#2c3e50", fg="white", activebackground="#2c3e50",
                command=lambda o=op: self.execute_unary(o),
            ).grid(row=i // 5, column=i % 5, sticky="nsew", padx=1, pady=1)

        self.sci_frame.grid_remove()

    # ------------------------------------------------------------------ logic

    def press_digit(self, digit: str) -> None:
        """Append *digit* or a decimal point to the current input string.

        A second decimal point in the same number is silently ignored.
        Leading zeros are suppressed (e.g. pressing 0 then 5 gives "5").
        """
        if digit == "." and "." in self._current_input:
            return
        if self._current_input == "0" and digit != ".":
            self._current_input = digit
        else:
            self._current_input += digit
        self.display_var.set(self._current_input or "0")

    def clear(self) -> None:
        """Reset the display, pending operation, and all internal state."""
        self._current_input = ""
        self._pending_op = None
        self._first_operand = None
        self.display_var.set("0")
        self.expression_var.set("")

    def set_binary_op(self, op: str) -> None:
        """Register *op* as the pending binary operation.

        The current input is stored as the first operand and the input
        buffer is cleared so the user can type the second operand.
        Does nothing if the input buffer is empty.
        """
        if not self._current_input:
            return
        self._first_operand = float(self._current_input)
        self._pending_op = op
        self.expression_var.set(f"{self._format(self._first_operand)} {op}")
        self._current_input = ""

    def equals(self) -> None:
        """Execute the pending binary operation using the current input as the second operand.

        On success the result replaces the current input so it can be chained
        into the next operation.  On error the display shows ``"Error"`` and
        the expression line shows the error message.
        Does nothing if there is no pending operation or no second operand.
        """
        if self._pending_op is None or not self._current_input:
            return
        try:
            b = float(self._current_input)
            result = self.calc.execute(self._pending_op, self._first_operand, b)
            self.expression_var.set(
                f"{self._format(self._first_operand)} {self._pending_op}"
                f" {self._format(b)} ="
            )
            self.display_var.set(self._format(result))
            self._current_input = self._format(result)
            self._pending_op = None
            self._first_operand = None
        except (ValueError, ZeroDivisionError) as exc:
            logger.error("GUI equals failed (%s): %s", self._pending_op, exc)
            self.display_var.set("Error")
            self.expression_var.set(str(exc))
            self._current_input = ""

    def execute_unary(self, op: str) -> None:
        """Execute unary operation *op* on the current input and display the result.

        On error the display shows ``"Error"`` and the expression line shows
        the error message.  Does nothing if the input buffer is empty.
        """
        if not self._current_input:
            return
        try:
            a = float(self._current_input)
            result = self.calc.execute(op, a)
            self.expression_var.set(f"{op}({self._format(a)}) =")
            self.display_var.set(self._format(result))
            self._current_input = self._format(result)
        except (ValueError, ZeroDivisionError) as exc:
            logger.error("GUI execute_unary failed (%s): %s", op, exc)
            self.display_var.set("Error")
            self.expression_var.set(str(exc))
            self._current_input = ""

    def toggle_mode(self) -> None:
        """Show or hide the scientific operation panel."""
        if self.mode == "normal":
            self.mode = "scientific"
            self.sci_frame.grid()
        else:
            self.mode = "normal"
            self.sci_frame.grid_remove()

    def show_history(self) -> None:
        """Display the full operation history in an info dialog."""
        history = self.calc.get_history()
        if not history:
            messagebox.showinfo("History", "No history yet.")
            return
        lines = [
            f"{i}. {e['op']}({', '.join(self._format(o) for o in e['operands'])})"
            f" = {self._format(e['result'])}"
            for i, e in enumerate(history, 1)
        ]
        messagebox.showinfo("History", "\n".join(lines))

    @staticmethod
    def _format(value: "int | float") -> str:
        """Return a human-readable string: whole floats are shown without decimals."""
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        return str(value)


def launch_gui() -> None:
    """Create the Tk root window, attach the CalculatorGUI, and enter the event loop."""
    root = tk.Tk()
    CalculatorGUI(root)
    root.mainloop()
