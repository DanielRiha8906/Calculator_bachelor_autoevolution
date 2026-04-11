"""Tkinter-based graphical interface for the calculator.

Provides :class:`CalculatorGUI` (the main Tk window) and :func:`gui_main`
(the entry point used by ``python -m src --gui``).

The GUI reuses :class:`~src.controller.CalculatorController` for all
computation and :mod:`src.history` for session history, keeping behaviour
consistent with the existing interactive and CLI modes.

tkinter is imported lazily so that ``import src.gui`` succeeds even in
environments where tkinter is not installed.  Only :func:`gui_main` (and
:class:`CalculatorGUI`) require a working tkinter installation.
"""
from __future__ import annotations

try:
    import tkinter as tk
    from tkinter import messagebox, scrolledtext
    _TKINTER_AVAILABLE: bool = True
except ImportError:  # pragma: no cover
    tk = None  # type: ignore[assignment]
    messagebox = None  # type: ignore[assignment]
    scrolledtext = None  # type: ignore[assignment]
    _TKINTER_AVAILABLE = False

from .controller import CalculatorController
from .error_logger import get_error_logger
from .history import clear_history, load_history, record_entry

# Operations available per mode
NORMAL_OPERATIONS: list[str] = ["add", "subtract", "multiply", "divide"]
SCIENTIFIC_OPERATIONS: list[str] = [
    "add", "subtract", "multiply", "divide",
    "factorial", "square", "cube", "square_root", "cube_root",
    "power", "log", "ln",
]

# Human-readable label for each operation
OPERATION_LABELS: dict[str, str] = {
    "add": "Add",
    "subtract": "Subtract",
    "multiply": "Multiply",
    "divide": "Divide",
    "factorial": "Factorial",
    "square": "Square",
    "cube": "Cube",
    "square_root": "Square Root",
    "cube_root": "Cube Root",
    "power": "Power",
    "log": "Log",
    "ln": "Natural Log",
}

# Operations that require a second operand (b)
BINARY_OPERATIONS: frozenset[str] = frozenset(
    {"add", "subtract", "multiply", "divide", "power"}
)

# Operations that require an integer input
INTEGER_OPERATIONS: frozenset[str] = frozenset({"factorial"})

# Operations that expose a log-base input field
LOG_OPERATIONS: frozenset[str] = frozenset({"log"})


def parse_operand(raw: str, *, integer: bool = False) -> float | int:
    """Parse a raw string from a GUI entry field to a numeric value.

    Args:
        raw: The raw string typed by the user.
        integer: When ``True``, parse as :class:`int`; otherwise as
            :class:`float`.

    Returns:
        The parsed numeric value.

    Raises:
        ValueError: If *raw* is empty or cannot be converted.
    """
    cleaned = raw.strip()
    if not cleaned:
        raise ValueError("Input must not be empty.")
    if integer:
        try:
            return int(cleaned)
        except ValueError:
            raise ValueError(
                f"Invalid integer {cleaned!r}: please enter a whole number."
            )
    try:
        return float(cleaned)
    except ValueError:
        raise ValueError(
            f"Invalid number {cleaned!r}: please enter a valid number."
        )


class CalculatorGUI:
    """Main GUI window for the calculator.

    Supports both normal mode (arithmetic only) and scientific mode
    (all twelve operations).  History is managed via :mod:`src.history`
    and cleared at window startup so behaviour mirrors the interactive
    session mode.

    Requires tkinter to be installed.  Instantiating this class without
    tkinter raises :class:`ImportError`.
    """

    def __init__(self, root: tk.Tk) -> None:  # type: ignore[name-defined]
        if not _TKINTER_AVAILABLE:
            raise ImportError(
                "tkinter is not installed. "
                "Install 'python3-tk' to use the GUI."
            )
        self._root = root
        self._controller = CalculatorController()
        self._mode: str = "normal"
        self._selected_op: str | None = None
        self._build_ui()
        clear_history()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        """Build and lay out all tkinter widgets."""
        self._root.title("Calculator")
        self._root.resizable(False, False)

        # -- Mode controls --
        self._mode_label = tk.Label(
            self._root,
            text="Mode: Normal",
            font=("TkDefaultFont", 10, "bold"),
        )
        self._mode_label.grid(
            row=0, column=0, columnspan=4, padx=8, pady=(8, 2)
        )

        self._mode_btn = tk.Button(
            self._root,
            text="Switch to Scientific Mode",
            command=self._toggle_mode,
            width=30,
        )
        self._mode_btn.grid(
            row=1, column=0, columnspan=4, padx=8, pady=(2, 6), sticky="ew"
        )

        # -- Operation buttons frame --
        ops_frame = tk.LabelFrame(self._root, text="Operations", padx=4, pady=4)
        ops_frame.grid(
            row=2, column=0, columnspan=4, padx=8, pady=4, sticky="ew"
        )

        self._op_buttons: dict[str, tk.Button] = {}

        # Row 0: normal operations
        for col, op in enumerate(["add", "subtract", "multiply", "divide"]):
            btn = tk.Button(
                ops_frame,
                text=OPERATION_LABELS[op],
                width=10,
                command=lambda o=op: self._select_operation(o),
            )
            btn.grid(row=0, column=col, padx=2, pady=2)
            self._op_buttons[op] = btn

        # Rows 1-2: scientific-only operations
        sci_layout = [
            ["factorial", "square", "cube", "square_root"],
            ["cube_root", "power", "log", "ln"],
        ]
        self._sci_buttons: list[tk.Button] = []
        for row_idx, ops_row in enumerate(sci_layout, start=1):
            for col, op in enumerate(ops_row):
                btn = tk.Button(
                    ops_frame,
                    text=OPERATION_LABELS[op],
                    width=10,
                    command=lambda o=op: self._select_operation(o),
                )
                btn.grid(row=row_idx, column=col, padx=2, pady=2)
                self._op_buttons[op] = btn
                self._sci_buttons.append(btn)

        # Hide scientific buttons on startup
        self._set_sci_buttons_visible(False)

        # -- Inputs frame --
        input_frame = tk.LabelFrame(self._root, text="Inputs", padx=4, pady=4)
        input_frame.grid(
            row=3, column=0, columnspan=4, padx=8, pady=4, sticky="ew"
        )

        tk.Label(input_frame, text="Operation:").grid(
            row=0, column=0, sticky="e", padx=4, pady=2
        )
        self._op_display = tk.Label(
            input_frame, text="(none selected)", width=22, anchor="w"
        )
        self._op_display.grid(row=0, column=1, columnspan=2, sticky="w", padx=4)

        self._label_a = tk.Label(input_frame, text="Value a:")
        self._label_a.grid(row=1, column=0, sticky="e", padx=4, pady=2)
        self._entry_a = tk.Entry(input_frame, width=22)
        self._entry_a.grid(row=1, column=1, columnspan=2, sticky="ew", padx=4, pady=2)

        self._label_b = tk.Label(input_frame, text="Value b:")
        self._label_b.grid(row=2, column=0, sticky="e", padx=4, pady=2)
        self._entry_b = tk.Entry(input_frame, width=22)
        self._entry_b.grid(row=2, column=1, columnspan=2, sticky="ew", padx=4, pady=2)

        self._label_base = tk.Label(input_frame, text="Log base:")
        self._label_base.grid(row=3, column=0, sticky="e", padx=4, pady=2)
        self._entry_base = tk.Entry(input_frame, width=22)
        self._entry_base.grid(
            row=3, column=1, columnspan=2, sticky="ew", padx=4, pady=2
        )
        self._entry_base.insert(0, "10")

        # b and base rows start hidden
        self._label_b.grid_remove()
        self._entry_b.grid_remove()
        self._label_base.grid_remove()
        self._entry_base.grid_remove()

        # -- Calculate button --
        self._calc_btn = tk.Button(
            self._root,
            text="Calculate",
            command=self._calculate,
            width=20,
            state=tk.DISABLED,
        )
        self._calc_btn.grid(
            row=4, column=0, columnspan=4, padx=8, pady=(4, 2)
        )

        # -- Result display --
        result_frame = tk.LabelFrame(self._root, text="Result", padx=4, pady=4)
        result_frame.grid(
            row=5, column=0, columnspan=4, padx=8, pady=4, sticky="ew"
        )
        self._result_label = tk.Label(
            result_frame,
            text="",
            font=("TkDefaultFont", 12),
            anchor="w",
            width=30,
        )
        self._result_label.grid(row=0, column=0, padx=4)

        # -- History button --
        self._history_btn = tk.Button(
            self._root,
            text="Show History",
            command=self._show_history,
            width=20,
        )
        self._history_btn.grid(
            row=6, column=0, columnspan=4, padx=8, pady=(2, 10)
        )

        # Pressing Enter triggers Calculate
        self._root.bind("<Return>", lambda _event: self._calculate())

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _select_operation(self, operation: str) -> None:
        """React to an operation button click.

        Updates the displayed operation name and shows or hides the
        input fields that the chosen operation requires.
        """
        self._selected_op = operation
        self._op_display.config(text=OPERATION_LABELS[operation])
        self._calc_btn.config(state=tk.NORMAL)
        self._result_label.config(text="")

        # Clear stale input values
        self._entry_a.delete(0, tk.END)
        self._entry_b.delete(0, tk.END)

        # Label for operand a
        if operation == "factorial":
            self._label_a.config(text="Integer n:")
        elif operation == "power":
            self._label_a.config(text="Base:")
        else:
            self._label_a.config(text="Value a:")

        # Show / hide operand b
        if operation in BINARY_OPERATIONS:
            self._label_b.config(
                text="Exponent:" if operation == "power" else "Value b:"
            )
            self._label_b.grid()
            self._entry_b.grid()
        else:
            self._label_b.grid_remove()
            self._entry_b.grid_remove()

        # Show / hide log-base field
        if operation in LOG_OPERATIONS:
            self._label_base.grid()
            self._entry_base.grid()
        else:
            self._label_base.grid_remove()
            self._entry_base.grid_remove()

    def _calculate(self) -> None:
        """Read the input fields, execute the selected operation, and show the result."""
        if self._selected_op is None:
            messagebox.showwarning(
                "No Operation", "Please select an operation first."
            )
            return

        op = self._selected_op

        # --- Parse operand a ---
        try:
            a = parse_operand(
                self._entry_a.get(), integer=(op in INTEGER_OPERATIONS)
            )
        except ValueError as exc:
            messagebox.showerror("Input Error", str(exc))
            return

        # --- Parse operand b (binary ops only) ---
        b: float | None = None
        if op in BINARY_OPERATIONS:
            try:
                b = float(parse_operand(self._entry_b.get()))
            except ValueError as exc:
                messagebox.showerror("Input Error", str(exc))
                return

        # --- Parse log base ---
        log_base: float = 10.0
        if op in LOG_OPERATIONS:
            raw_base = self._entry_base.get().strip()
            if raw_base:
                try:
                    log_base = float(parse_operand(raw_base))
                except ValueError as exc:
                    messagebox.showerror("Input Error", str(exc))
                    return

        # --- Dispatch ---
        try:
            result = self._controller.execute(op, a=a, b=b, base=log_base)
        except (ValueError, ZeroDivisionError) as exc:
            get_error_logger().error("[gui] %s: %s", OPERATION_LABELS[op], exc)
            messagebox.showerror("Calculation Error", str(exc))
            return

        # --- Show result and record in session history ---
        self._result_label.config(text=result)
        record_entry(f"{OPERATION_LABELS[op]}: {result}")

    def _toggle_mode(self) -> None:
        """Toggle between normal and scientific modes."""
        if self._mode == "normal":
            self._mode = "scientific"
            self._mode_label.config(text="Mode: Scientific")
            self._mode_btn.config(text="Switch to Normal Mode")
            self._set_sci_buttons_visible(True)
        else:
            self._mode = "normal"
            self._mode_label.config(text="Mode: Normal")
            self._mode_btn.config(text="Switch to Scientific Mode")
            self._set_sci_buttons_visible(False)
            # Deselect any scientific operation that is no longer available
            if self._selected_op not in NORMAL_OPERATIONS:
                self._selected_op = None
                self._op_display.config(text="(none selected)")
                self._calc_btn.config(state=tk.DISABLED)
                self._result_label.config(text="")

    def _show_history(self) -> None:
        """Open a popup window listing the current session history."""
        entries = load_history()

        popup = tk.Toplevel(self._root)
        popup.title("Session History")
        popup.resizable(False, False)

        if not entries:
            tk.Label(popup, text="No history yet.", padx=20, pady=10).pack()
        else:
            text_widget = scrolledtext.ScrolledText(
                popup, width=40, height=15, state=tk.NORMAL
            )
            text_widget.pack(padx=8, pady=8)
            for i, entry in enumerate(entries, 1):
                text_widget.insert(tk.END, f"{i}. {entry}\n")
            text_widget.config(state=tk.DISABLED)

        tk.Button(popup, text="Close", command=popup.destroy).pack(
            pady=(0, 8)
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _set_sci_buttons_visible(self, visible: bool) -> None:
        """Show or hide all scientific-only operation buttons."""
        for btn in self._sci_buttons:
            if visible:
                btn.grid()
            else:
                btn.grid_remove()


def gui_main() -> None:
    """Launch the calculator GUI.

    Creates the root Tk window, instantiates :class:`CalculatorGUI`, and
    enters the tkinter main loop.  This function blocks until the window
    is closed.

    Raises:
        ImportError: If tkinter is not installed.
    """
    if not _TKINTER_AVAILABLE:
        raise ImportError(
            "tkinter is not installed. "
            "Install 'python3-tk' (e.g. 'sudo apt install python3-tk') "
            "to use the GUI."
        )
    root = tk.Tk()
    _app = CalculatorGUI(root)
    root.mainloop()
