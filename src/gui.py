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

# ---------------------------------------------------------------------------
# Colour palette — modern dark theme
# ---------------------------------------------------------------------------
_BG        = "#0d1117"   # window / main background
_DISPLAY_BG = "#161b22"  # display area
_EXPR_FG   = "#6e7681"   # expression (secondary) text
_MAIN_FG   = "#e6edf3"   # primary text / digits

_DIG       = "#21262d"   # digit / neutral buttons
_DIG_HOV   = "#30363d"
_DIG_ACT   = "#3d444d"

_BOP       = "#1f6feb"   # binary operator (blue)
_BOP_HOV   = "#388bfd"
_BOP_ACT   = "#58a6ff"

_EQL       = "#238636"   # equals (green)
_EQL_HOV   = "#2ea043"
_EQL_ACT   = "#3fb950"

_CLR       = "#da3633"   # clear (red)
_CLR_HOV   = "#f85149"
_CLR_ACT   = "#ff7b72"

_UOP       = "#6e40c9"   # unary ops (purple)
_UOP_HOV   = "#8957e5"
_UOP_ACT   = "#a371f7"

_SCI       = "#0d419d"   # sci-toggle (navy)
_SCI_HOV   = "#1158c7"
_SCI_ACT   = "#388bfd"

_HIST      = "#1b4721"   # history (dark green)
_HIST_HOV  = "#238636"
_HIST_ACT  = "#2ea043"

_SCI_PNL   = "#161b22"   # scientific panel background
_SCI_BTN   = "#21262d"   # scientific panel buttons
_SCI_HOV   = "#2d333b"
_SCI_ACT   = "#3d444d"


def _make_button(
    parent: tk.Widget,
    text: str,
    command,
    bg: str,
    hover_bg: str,
    active_bg: str,
    fg: str = _MAIN_FG,
    font: tuple = ("Segoe UI", 15, "bold"),
    padx: int = 0,
    pady: int = 0,
) -> tk.Button:
    """Create a styled button with hover and active visual feedback."""
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        bg=bg,
        fg=fg,
        font=font,
        relief="flat",
        bd=0,
        activebackground=active_bg,
        activeforeground=fg,
        cursor="hand2",
        padx=padx,
        pady=pady,
    )
    btn.bind("<Enter>", lambda _e: btn.config(bg=hover_bg))
    btn.bind("<Leave>", lambda _e: btn.config(bg=bg))
    return btn


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
        self.root.configure(bg=_BG)
        self.root.resizable(False, False)

        # Configure uniform column / row weights so buttons fill space evenly.
        for col in range(4):
            self.root.columnconfigure(col, weight=1, minsize=72)

        # ── Display area (row 0) ─────────────────────────────────────────────
        display_frame = tk.Frame(self.root, bg=_DISPLAY_BG, padx=12, pady=10)
        display_frame.grid(row=0, column=0, columnspan=4, sticky="ew")
        display_frame.columnconfigure(0, weight=1)

        self.expression_var = tk.StringVar(value="")
        tk.Label(
            display_frame,
            textvariable=self.expression_var,
            bg=_DISPLAY_BG,
            fg=_EXPR_FG,
            anchor="e",
            font=("Segoe UI", 11),
        ).grid(row=0, column=0, sticky="ew")

        self.display_var = tk.StringVar(value="0")
        tk.Label(
            display_frame,
            textvariable=self.display_var,
            bg=_DISPLAY_BG,
            fg=_MAIN_FG,
            anchor="e",
            font=("Segoe UI", 32, "bold"),
        ).grid(row=1, column=0, sticky="ew")

        # Thin separator line between display and buttons
        tk.Frame(self.root, bg="#30363d", height=1).grid(
            row=1, column=0, columnspan=4, sticky="ew"
        )

        # ── Digit and basic binary-op buttons (rows 2-5) ────────────────────
        btn_grid = [
            ("7", 2, 0, lambda: self.press_digit("7"), _DIG, _DIG_HOV, _DIG_ACT),
            ("8", 2, 1, lambda: self.press_digit("8"), _DIG, _DIG_HOV, _DIG_ACT),
            ("9", 2, 2, lambda: self.press_digit("9"), _DIG, _DIG_HOV, _DIG_ACT),
            ("÷", 2, 3, lambda: self.set_binary_op("divide"),   _BOP, _BOP_HOV, _BOP_ACT),
            ("4", 3, 0, lambda: self.press_digit("4"), _DIG, _DIG_HOV, _DIG_ACT),
            ("5", 3, 1, lambda: self.press_digit("5"), _DIG, _DIG_HOV, _DIG_ACT),
            ("6", 3, 2, lambda: self.press_digit("6"), _DIG, _DIG_HOV, _DIG_ACT),
            ("×", 3, 3, lambda: self.set_binary_op("multiply"), _BOP, _BOP_HOV, _BOP_ACT),
            ("1", 4, 0, lambda: self.press_digit("1"), _DIG, _DIG_HOV, _DIG_ACT),
            ("2", 4, 1, lambda: self.press_digit("2"), _DIG, _DIG_HOV, _DIG_ACT),
            ("3", 4, 2, lambda: self.press_digit("3"), _DIG, _DIG_HOV, _DIG_ACT),
            ("−", 4, 3, lambda: self.set_binary_op("subtract"), _BOP, _BOP_HOV, _BOP_ACT),
            ("0", 5, 0, lambda: self.press_digit("0"), _DIG, _DIG_HOV, _DIG_ACT),
            (".", 5, 1, lambda: self.press_digit("."), _DIG, _DIG_HOV, _DIG_ACT),
            ("=", 5, 2, self.equals,                             _EQL, _EQL_HOV, _EQL_ACT),
            ("+", 5, 3, lambda: self.set_binary_op("add"),      _BOP, _BOP_HOV, _BOP_ACT),
        ]
        for label, row, col, cmd, bg, hbg, abg in btn_grid:
            btn = _make_button(self.root, label, cmd, bg, hbg, abg)
            btn.grid(row=row, column=col, sticky="nsew", padx=1, pady=1, ipady=10)

        # ── Utility buttons: clear + common unary ops (row 6) ───────────────
        utility = [
            ("C",   _CLR, _CLR_HOV, _CLR_ACT, self.clear,                              6, 0),
            ("x²",  _UOP, _UOP_HOV, _UOP_ACT, lambda: self.execute_unary("square"),    6, 1),
            ("√",   _UOP, _UOP_HOV, _UOP_ACT, lambda: self.execute_unary("square_root"),6, 2),
            ("n!",  _UOP, _UOP_HOV, _UOP_ACT, lambda: self.execute_unary("factorial"), 6, 3),
        ]
        for label, bg, hbg, abg, cmd, row, col in utility:
            btn = _make_button(self.root, label, cmd, bg, hbg, abg, font=("Segoe UI", 13, "bold"))
            btn.grid(row=row, column=col, sticky="nsew", padx=1, pady=1, ipady=8)

        # ── More unary ops (row 7) ───────────────────────────────────────────
        unary_row = [
            ("x³", "cube"),
            ("∛",  "cube_root"),
            ("log", "log"),
            ("ln",  "ln"),
        ]
        for col, (label, op) in enumerate(unary_row):
            btn = _make_button(
                self.root, label,
                lambda o=op: self.execute_unary(o),
                _UOP, _UOP_HOV, _UOP_ACT,
                font=("Segoe UI", 13, "bold"),
            )
            btn.grid(row=7, column=col, sticky="nsew", padx=1, pady=1, ipady=8)

        # ── Control row (row 8): power, sci toggle, history ─────────────────
        controls = [
            ("xʸ",  _DIG,  _DIG_HOV,  _DIG_ACT,  lambda: self.set_binary_op("power"), 8, 0),
            ("Sci", _SCI,  _SCI_HOV,  _SCI_ACT,  self.toggle_mode,                    8, 1),
            ("Hist",_HIST, _HIST_HOV, _HIST_ACT, self.show_history,                   8, 2),
        ]
        for label, bg, hbg, abg, cmd, row, col in controls:
            btn = _make_button(self.root, label, cmd, bg, hbg, abg, font=("Segoe UI", 13, "bold"))
            btn.grid(row=row, column=col, sticky="nsew", padx=1, pady=1, ipady=8)

        # Spacer in control row col 3
        tk.Frame(self.root, bg=_BG).grid(row=8, column=3, sticky="nsew", padx=1, pady=1)

        # ── Scientific panel (row 9, hidden until toggled) ───────────────────
        self.sci_frame = tk.Frame(self.root, bg=_SCI_PNL, pady=4)
        self.sci_frame.grid(row=9, column=0, columnspan=4, sticky="ew")
        for col in range(5):
            self.sci_frame.columnconfigure(col, weight=1)

        sci_ops = [
            "sin", "cos", "tan", "asin", "acos",
            "atan", "sinh", "cosh", "tanh", "exp",
        ]
        for i, op in enumerate(sci_ops):
            btn = _make_button(
                self.sci_frame, op,
                lambda o=op: self.execute_unary(o),
                _SCI_BTN, _SCI_HOV, _SCI_ACT,
                font=("Segoe UI", 11, "bold"),
            )
            btn.grid(row=i // 5, column=i % 5, sticky="nsew", padx=1, pady=1, ipady=6)

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
