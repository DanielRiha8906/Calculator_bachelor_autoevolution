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
        # -- colour palette (modern dark theme) --
        BG         = "#1c1c1e"   # window background
        D_BG       = "#000000"   # display background
        D_FG       = "#ffffff"   # display main result text
        D_FG2      = "#8e8e93"   # display expression/secondary text
        C_DIGIT    = "#333333"   # digit button
        C_OP       = "#ff9f0a"   # binary-operator button (orange)
        C_CLR      = "#a5a5a5"   # clear button (light gray)
        C_CLR_FG   = "#1c1c1e"   # dark text on clear button for contrast
        C_UNARY    = "#2c2c2e"   # unary-op button (dark gray)
        C_CTL_SCI  = "#30d158"   # sci-toggle button (green)
        C_CTL_HIST = "#0a84ff"   # history button (blue)
        FG         = "#ffffff"   # default button foreground

        # -- fonts --
        F_EXPR   = ("Arial", 12)
        F_DISP   = ("Arial", 36, "bold")
        F_BTN    = ("Arial", 20, "bold")
        F_BTN_SM = ("Arial", 14)
        F_SCI    = ("Arial", 12)

        self.root.title("Calculator")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        self.root.minsize(320, 560)

        # Make all four columns share horizontal space equally
        for col in range(4):
            self.root.columnconfigure(col, weight=1, minsize=78)

        # --- Display area (row 0) ---
        display_frame = tk.Frame(self.root, bg=D_BG, padx=14, pady=10)
        display_frame.grid(row=0, column=0, columnspan=4, sticky="ew")

        self.expression_var = tk.StringVar(value="")
        tk.Label(
            display_frame,
            textvariable=self.expression_var,
            bg=D_BG,
            fg=D_FG2,
            anchor="e",
            font=F_EXPR,
        ).pack(fill="x")

        self.display_var = tk.StringVar(value="0")
        tk.Label(
            display_frame,
            textvariable=self.display_var,
            bg=D_BG,
            fg=D_FG,
            anchor="e",
            font=F_DISP,
        ).pack(fill="x")

        # Helper: create a flat, styled button
        def _btn(parent, text, bg, cmd, fg=FG, font=F_BTN):
            return tk.Button(
                parent,
                text=text,
                font=font,
                bg=bg,
                fg=fg,
                activebackground=bg,
                activeforeground=fg,
                relief="flat",
                borderwidth=0,
                padx=4,
                pady=14,
                cursor="hand2",
                command=cmd,
            )

        _PAD = {"padx": 2, "pady": 2, "sticky": "nsew"}

        # --- Digit and binary-operator buttons (rows 1–4) ---
        btn_grid = [
            ("7", 1, 0, lambda: self.press_digit("7"), C_DIGIT, FG),
            ("8", 1, 1, lambda: self.press_digit("8"), C_DIGIT, FG),
            ("9", 1, 2, lambda: self.press_digit("9"), C_DIGIT, FG),
            ("÷", 1, 3, lambda: self.set_binary_op("divide"),   C_OP,    FG),
            ("4", 2, 0, lambda: self.press_digit("4"), C_DIGIT, FG),
            ("5", 2, 1, lambda: self.press_digit("5"), C_DIGIT, FG),
            ("6", 2, 2, lambda: self.press_digit("6"), C_DIGIT, FG),
            ("×", 2, 3, lambda: self.set_binary_op("multiply"), C_OP,    FG),
            ("1", 3, 0, lambda: self.press_digit("1"), C_DIGIT, FG),
            ("2", 3, 1, lambda: self.press_digit("2"), C_DIGIT, FG),
            ("3", 3, 2, lambda: self.press_digit("3"), C_DIGIT, FG),
            ("−", 3, 3, lambda: self.set_binary_op("subtract"), C_OP,    FG),
            ("0", 4, 0, lambda: self.press_digit("0"), C_DIGIT, FG),
            (".", 4, 1, lambda: self.press_digit("."), C_DIGIT, FG),
            ("=", 4, 2, self.equals,                             C_OP,    FG),
            ("+", 4, 3, lambda: self.set_binary_op("add"),      C_OP,    FG),
        ]
        for label, row, col, cmd, bg, fg in btn_grid:
            _btn(self.root, label, bg, cmd, fg=fg).grid(row=row, column=col, **_PAD)

        # --- Utility row: C, x², √, n! (row 5) ---
        utility = [
            ("C",   C_CLR,   C_CLR_FG, self.clear,                               5, 0),
            ("x²",  C_UNARY, FG,       lambda: self.execute_unary("square"),      5, 1),
            ("√",   C_UNARY, FG,       lambda: self.execute_unary("square_root"), 5, 2),
            ("n!",  C_UNARY, FG,       lambda: self.execute_unary("factorial"),   5, 3),
        ]
        for label, bg, fg, cmd, row, col in utility:
            _btn(self.root, label, bg, cmd, fg=fg, font=F_BTN_SM).grid(
                row=row, column=col, **_PAD
            )

        # --- Second unary row: x³, ∛, log, ln (row 6) ---
        unary_row = [("x³", "cube"), ("∛", "cube_root"), ("log", "log"), ("ln", "ln")]
        for col, (label, op) in enumerate(unary_row):
            _btn(
                self.root, label, C_UNARY,
                lambda o=op: self.execute_unary(o),
                font=F_BTN_SM,
            ).grid(row=6, column=col, **_PAD)

        # --- Control row: xʸ, Sci, Hist (row 7) ---
        controls = [
            ("xʸ",  C_OP,        lambda: self.set_binary_op("power"), 7, 0),
            ("Sci", C_CTL_SCI,  self.toggle_mode,                    7, 1),
            ("Hist",C_CTL_HIST, self.show_history,                   7, 2),
        ]
        for label, bg, cmd, row, col in controls:
            _btn(self.root, label, bg, cmd, font=F_BTN_SM).grid(
                row=row, column=col, **_PAD
            )

        # --- Scientific panel (row 8, hidden until toggled) ---
        self.sci_frame = tk.Frame(self.root, bg=BG)
        self.sci_frame.grid(row=8, column=0, columnspan=4, sticky="ew")

        sci_ops = [
            "sin", "cos", "tan", "asin", "acos",
            "atan", "sinh", "cosh", "tanh", "exp",
        ]
        for i, op in enumerate(sci_ops):
            _btn(
                self.sci_frame, op, C_UNARY,
                lambda o=op: self.execute_unary(o),
                font=F_SCI,
            ).grid(row=i // 5, column=i % 5, padx=1, pady=1, sticky="nsew")

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
