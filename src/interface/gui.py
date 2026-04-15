"""Graphical user interface for the calculator, built with tkinter.

Exports
-------
CalculatorApp : tkinter application class encapsulating all GUI logic.
launch_gui    : convenience entry-point that creates the root window and runs
                the event loop (blocks until the window is closed).

Design note
-----------
tkinter is imported lazily inside :func:`launch_gui` and injected into
:class:`CalculatorApp` via constructor parameters.  This means the module
can be imported without tkinter being installed, and tests can pass in
MagicMock objects for all three tkinter dependencies without patching
``sys.modules``.
"""
from ..calculator import Calculator
from .history import clear_history, append_to_history
from .interactive import (
    NORMAL_MODE_OPERATIONS,
    SCIENTIFIC_MODE_OPERATIONS,
    _ONE_ARG_OPS,
    _INT_ARG_OPS,
)


class CalculatorApp:
    """Calculator GUI built with tkinter.

    Supports normal mode (four basic operations) and scientific mode
    (all twelve operations).  Session history is accumulated in memory and
    also written to the shared history file used by the other interface modes.

    The layout is divided into clearly separated sections:
    - Mode selection (top)
    - Operation list (left column)
    - Inputs, result, and session history (right column, stacked vertically)
    - Action buttons (bottom)

    Parameters
    ----------
    root : tk.Tk
        The root window.  The caller owns the event loop; this class only
        builds widgets and wires event handlers.
    _tk : module
        The ``tkinter`` module (or a compatible mock for testing).
    _ttk : module
        The ``tkinter.ttk`` module (or a compatible mock for testing).
    _messagebox : module
        The ``tkinter.messagebox`` module (or a compatible mock for testing).
    """

    def __init__(self, root, _tk, _ttk, _messagebox) -> None:
        self._root = root
        self._tk = _tk
        self._ttk = _ttk
        self._messagebox = _messagebox

        self._calc = Calculator()
        self._mode: str = "normal"
        self._history: list[str] = []

        # Clear history file at session start (same behaviour as interactive mode).
        clear_history()

        self._build_ui()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        """Build and lay out all widgets in clearly separated sections."""
        tk = self._tk
        ttk = self._ttk

        self._root.title("Calculator")

        # Outer container provides uniform padding around the whole interface.
        main = ttk.Frame(self._root, padding="10 10 10 10")
        main.grid(row=0, column=0, sticky="nsew")
        self._root.columnconfigure(0, weight=1)
        self._root.rowconfigure(0, weight=1)

        # --- Mode selector (full width, top) ---
        mode_frame = ttk.LabelFrame(main, text="Mode", padding="6 4 6 4")
        mode_frame.grid(row=0, column=0, columnspan=2, pady=(0, 8), sticky="ew")

        self._mode_var = tk.StringVar(value="normal")
        ttk.Radiobutton(
            mode_frame, text="Normal", variable=self._mode_var,
            value="normal", command=self._on_mode_change,
        ).pack(side="left", padx=12, pady=2)
        ttk.Radiobutton(
            mode_frame, text="Scientific", variable=self._mode_var,
            value="scientific", command=self._on_mode_change,
        ).pack(side="left", padx=12, pady=2)

        # --- Operation listbox (left column) ---
        op_frame = ttk.LabelFrame(main, text="Operation", padding="4 4 4 4")
        op_frame.grid(row=1, column=0, padx=(0, 8), pady=(0, 8), sticky="ns")

        self._op_listbox = tk.Listbox(
            op_frame, height=12, width=16, selectmode="single",
            exportselection=False, activestyle="none",
        )
        self._op_listbox.grid(row=0, column=0, sticky="ns")
        self._op_listbox.bind("<<ListboxSelect>>", self._on_operation_select)

        op_scroll = ttk.Scrollbar(
            op_frame, orient="vertical", command=self._op_listbox.yview,
        )
        op_scroll.grid(row=0, column=1, sticky="ns")
        self._op_listbox.config(yscrollcommand=op_scroll.set)

        # --- Right column: inputs, result, history (stacked) ---
        right = ttk.Frame(main)
        right.grid(row=1, column=1, sticky="nsew", pady=(0, 8))
        right.columnconfigure(0, weight=1)

        # --- Input fields ---
        input_frame = ttk.LabelFrame(right, text="Inputs", padding="8 6 8 6")
        input_frame.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        input_frame.columnconfigure(1, weight=1)

        self._label_a = ttk.Label(input_frame, text="Value:", width=12, anchor="w")
        self._label_a.grid(row=0, column=0, padx=(0, 4), pady=3, sticky="w")
        self._entry_a = ttk.Entry(input_frame, width=20)
        self._entry_a.grid(row=0, column=1, pady=3, sticky="ew")

        self._label_b = ttk.Label(input_frame, text="Value 2:", width=12, anchor="w")
        self._label_b.grid(row=1, column=0, padx=(0, 4), pady=3, sticky="w")
        self._entry_b = ttk.Entry(input_frame, width=20)
        self._entry_b.grid(row=1, column=1, pady=3, sticky="ew")

        ttk.Button(
            input_frame, text="Calculate", command=self._on_calculate,
        ).grid(row=2, column=0, columnspan=2, pady=(8, 0), sticky="ew")

        # --- Result display ---
        result_frame = ttk.LabelFrame(right, text="Result", padding="8 4 8 4")
        result_frame.grid(row=1, column=0, sticky="ew", pady=(0, 6))
        result_frame.columnconfigure(0, weight=1)

        self._result_var = tk.StringVar(value="\u2014")
        ttk.Label(
            result_frame, textvariable=self._result_var,
            font=("TkFixedFont", 14), anchor="center",
        ).grid(row=0, column=0, pady=6, sticky="ew")

        # --- Session history panel ---
        hist_frame = ttk.LabelFrame(right, text="Session History", padding="4 4 4 4")
        hist_frame.grid(row=2, column=0, sticky="ew")
        hist_frame.columnconfigure(0, weight=1)

        hist_scroll = ttk.Scrollbar(hist_frame, orient="vertical")
        self._history_listbox = tk.Listbox(
            hist_frame, height=4, width=36, selectmode="browse",
            exportselection=False, yscrollcommand=hist_scroll.set,
            activestyle="none",
        )
        hist_scroll.config(command=self._history_listbox.yview)
        self._history_listbox.grid(row=0, column=0, sticky="ew")
        hist_scroll.grid(row=0, column=1, sticky="ns")

        # --- Action buttons (full width, bottom) ---
        btn_frame = ttk.Frame(main)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=(6, 0), sticky="ew")

        ttk.Button(
            btn_frame, text="Show Full History", command=self._on_show_history,
        ).pack(side="left")
        ttk.Button(
            btn_frame, text="Quit", command=self._root.destroy,
        ).pack(side="right")

        self._refresh_operations()

    def _refresh_operations(self) -> None:
        """Repopulate the operation listbox for the current mode."""
        ops = (
            NORMAL_MODE_OPERATIONS if self._mode == "normal"
            else SCIENTIFIC_MODE_OPERATIONS
        )
        self._op_listbox.delete(0, "end")
        self._operations: list[str] = list(ops.values())
        for name in self._operations:
            self._op_listbox.insert("end", name)
        if self._operations:
            self._op_listbox.selection_set(0)
            self._on_operation_select(None)

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _on_mode_change(self) -> None:
        """Handle mode radio-button change: refresh ops and clear inputs."""
        self._mode = self._mode_var.get()
        self._result_var.set("\u2014")
        self._entry_a.delete(0, "end")
        self._entry_b.delete(0, "end")
        self._refresh_operations()

    def _on_operation_select(self, _event) -> None:
        """Adjust label text and show/hide the second input based on arity."""
        sel = self._op_listbox.curselection()
        if not sel:
            return
        operation = self._operations[sel[0]]

        if operation == "divide":
            self._label_a.config(text="Dividend:")
            self._label_b.config(text="Divisor:")
        elif operation == "log":
            self._label_a.config(text="Number:")
            self._label_b.config(text="Base:")
        elif operation == "power":
            self._label_a.config(text="Base:")
            self._label_b.config(text="Exponent:")
        elif operation in _INT_ARG_OPS:
            self._label_a.config(text="Integer:")
        elif operation in _ONE_ARG_OPS:
            self._label_a.config(text="Number:")
        else:
            self._label_a.config(text="First number:")
            self._label_b.config(text="Second number:")

        if operation in _ONE_ARG_OPS or operation in _INT_ARG_OPS:
            self._label_b.grid_remove()
            self._entry_b.grid_remove()
        else:
            self._label_b.grid()
            self._entry_b.grid()

    def _on_calculate(self) -> None:
        """Read inputs, compute the result, update the display, and save history."""
        sel = self._op_listbox.curselection()
        if not sel:
            self._messagebox.showwarning("No Operation", "Please select an operation.")
            return
        operation = self._operations[sel[0]]

        try:
            result, entry = self._compute(
                operation,
                self._entry_a.get(),
                self._entry_b.get(),
            )
            self._result_var.set(str(result))
            self._history.append(entry)
            self._history_listbox.insert("end", entry)
            self._history_listbox.see("end")
            append_to_history(entry)
        except ValueError as exc:
            self._messagebox.showerror("Calculation Error", str(exc))
            self._result_var.set("Error")

    def _on_show_history(self) -> None:
        """Open a read-only window listing the current session history."""
        tk = self._tk
        ttk = self._ttk

        win = tk.Toplevel(self._root)
        win.title("Session History")
        win.resizable(False, False)

        text = tk.Text(win, width=50, height=20)
        text.pack(padx=8, pady=8)
        scrollbar = ttk.Scrollbar(win, command=text.yview)
        text.config(yscrollcommand=scrollbar.set)

        if self._history:
            for i, entry in enumerate(self._history, start=1):
                text.insert("end", f"{i}. {entry}\n")
        else:
            text.insert("end", "No history yet.")

        text.config(state="disabled")
        ttk.Button(win, text="Close", command=win.destroy).pack(pady=(0, 8))

    # ------------------------------------------------------------------
    # Pure-logic helper (testable without tkinter)
    # ------------------------------------------------------------------

    def _compute(
        self, operation: str, value_a: str, value_b: str,
    ) -> "tuple[float | int, str]":
        """Parse *value_a* and *value_b*, execute *operation*, return (result, history_entry).

        Raises ``ValueError`` on parse failures or calculator errors (e.g.
        division by zero, square root of a negative number).
        """
        if operation in _INT_ARG_OPS:
            n = int(value_a.strip())
            result = self._calc.execute(operation, n)
            entry = f"{operation}({n}) = {result}"
        elif operation in _ONE_ARG_OPS:
            a = float(value_a.strip())
            result = self._calc.execute(operation, a)
            entry = f"{operation}({a}) = {result}"
        else:  # two-arg operation
            a = float(value_a.strip())
            b = float(value_b.strip())
            result = self._calc.execute(operation, a, b)
            entry = f"{operation}({a}, {b}) = {result}"
        return result, entry


def launch_gui() -> None:
    """Create the root Tk window, build the app, and enter the event loop.

    Imports tkinter on demand so the module can be loaded without tkinter
    being installed (tests inject mock objects instead).

    Blocks until the window is closed.
    """
    import tkinter as tk
    from tkinter import ttk, messagebox
    root = tk.Tk()
    CalculatorApp(root, _tk=tk, _ttk=ttk, _messagebox=messagebox)
    root.mainloop()
