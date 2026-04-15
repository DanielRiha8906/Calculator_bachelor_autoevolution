"""Tkinter-based graphical interface for the Calculator application.

Provides a window-based GUI that reuses CalculatorSession for all operation
dispatch and history management.  Normal and Scientific modes are represented
as concrete subclasses of a shared CalculatorMode abstraction so the GUI loop
is mode-agnostic.
"""

from abc import ABC, abstractmethod

try:
    import tkinter as tk
    from tkinter import messagebox, scrolledtext
    _TKINTER_AVAILABLE = True
except ImportError:  # pragma: no cover — tkinter absent in some headless environments
    _TKINTER_AVAILABLE = False

from .session import CalculatorSession


# ---------------------------------------------------------------------------
# Mode abstractions
# ---------------------------------------------------------------------------

class CalculatorMode(ABC):
    """Abstract base class for calculator operating modes.

    Subclasses define the human-readable mode name and the mapping of
    display labels to (session_operation_name, arity) pairs that
    the GUI uses to build its operation list and determine how many
    operand inputs to show.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable mode name shown in the UI."""

    @property
    @abstractmethod
    def operations(self) -> dict[str, tuple[str, int]]:
        """Available operations for this mode.

        Returns:
            A dict mapping display label (str) to a ``(op_name, arity)``
            tuple where *op_name* is the method name on ``Calculator``
            and *arity* is 1 (unary) or 2 (binary).
        """


class NormalMode(CalculatorMode):
    """Standard calculator mode: basic arithmetic, square, and square root."""

    name = "Normal"

    operations = {
        "Add":         ("add",         2),
        "Subtract":    ("subtract",    2),
        "Multiply":    ("multiply",    2),
        "Divide":      ("divide",      2),
        "Square":      ("square",      1),
        "Square Root": ("square_root", 1),
    }


class ScientificMode(CalculatorMode):
    """Scientific calculator mode: all normal operations plus advanced functions.

    Trig functions (sin, cos, tan, cot) expect input in degrees.
    Inverse trig functions (asin, acos) return values in degrees.
    """

    name = "Scientific"

    operations = {
        "Add":              ("add",         2),
        "Subtract":         ("subtract",    2),
        "Multiply":         ("multiply",    2),
        "Divide":           ("divide",      2),
        "Square":           ("square",      1),
        "Square Root":      ("square_root", 1),
        "Factorial":        ("factorial",   1),
        "Cube":             ("cube",        1),
        "Cube Root":        ("cube_root",   1),
        "Power":            ("power",       2),
        "Log (base 10)":    ("log",         1),
        "Natural Log":      ("ln",          1),
        "Sin (deg)":        ("sin",         1),
        "Cos (deg)":        ("cos",         1),
        "Tan (deg)":        ("tan",         1),
        "Cot (deg)":        ("cot",         1),
        "Arcsin":           ("asin",        1),
        "Arccos":           ("acos",        1),
    }


# ---------------------------------------------------------------------------
# GUI
# ---------------------------------------------------------------------------

class CalculatorGUI:
    """Main window for the tkinter-based calculator.

    Manages mode selection, operation input, result display, and history
    view.  All computation is delegated to a ``CalculatorSession`` instance
    so no calculator logic is duplicated here.

    Args:
        root: The Tk root window (or any Tk/Toplevel container).
    """

    def __init__(self, root) -> None:
        self._root = root
        self._session = CalculatorSession()
        self._mode: CalculatorMode = NormalMode()

        root.title("Calculator")
        root.resizable(False, False)
        self._build_ui()
        self._refresh_operations()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        """Construct and arrange all tkinter widgets."""
        pad = {"padx": 8, "pady": 4}

        # ---- Mode selector ----
        mode_frame = tk.LabelFrame(self._root, text="Mode", **pad)
        mode_frame.grid(row=0, column=0, columnspan=2, sticky="ew", **pad)

        self._mode_var = tk.StringVar(value=NormalMode.name)
        for mode_cls in (NormalMode, ScientificMode):
            tk.Radiobutton(
                mode_frame,
                text=mode_cls.name,
                variable=self._mode_var,
                value=mode_cls.name,
                command=self._on_mode_change,
            ).pack(side=tk.LEFT, padx=6)

        # ---- Operation selector ----
        ops_frame = tk.LabelFrame(self._root, text="Operation", **pad)
        ops_frame.grid(row=1, column=0, rowspan=3, sticky="ns", **pad)

        scrollbar = tk.Scrollbar(ops_frame, orient=tk.VERTICAL)
        self._op_listbox = tk.Listbox(
            ops_frame,
            yscrollcommand=scrollbar.set,
            selectmode=tk.SINGLE,
            width=20,
            height=10,
            exportselection=False,
        )
        scrollbar.config(command=self._op_listbox.yview)
        self._op_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self._op_listbox.bind("<<ListboxSelect>>", self._on_op_selected)

        # ---- Input area ----
        input_frame = tk.LabelFrame(self._root, text="Inputs", **pad)
        input_frame.grid(row=1, column=1, sticky="ew", **pad)

        self._label_a = tk.Label(input_frame, text="Operand A:")
        self._label_a.grid(row=0, column=0, sticky="e", **pad)
        self._input_a_var = tk.StringVar()
        self._entry_a = tk.Entry(input_frame, textvariable=self._input_a_var, width=18)
        self._entry_a.grid(row=0, column=1, **pad)

        self._label_b = tk.Label(input_frame, text="Operand B:")
        self._label_b.grid(row=1, column=0, sticky="e", **pad)
        self._input_b_var = tk.StringVar()
        self._entry_b = tk.Entry(input_frame, textvariable=self._input_b_var, width=18)
        self._entry_b.grid(row=1, column=1, **pad)

        # ---- Calculate button ----
        tk.Button(
            self._root,
            text="Calculate",
            command=self._on_calculate,
            width=16,
        ).grid(row=2, column=1, **pad)

        # ---- Result display ----
        result_frame = tk.LabelFrame(self._root, text="Result", **pad)
        result_frame.grid(row=3, column=1, sticky="ew", **pad)
        self._result_var = tk.StringVar(value="—")
        tk.Label(result_frame, textvariable=self._result_var, font=("Courier", 12)).pack(
            fill=tk.X, **pad
        )

        # ---- History panel ----
        hist_frame = tk.LabelFrame(self._root, text="Session History", **pad)
        hist_frame.grid(row=4, column=0, columnspan=2, sticky="ew", **pad)

        self._history_text = scrolledtext.ScrolledText(
            hist_frame,
            state=tk.DISABLED,
            height=6,
            width=50,
            font=("Courier", 10),
        )
        self._history_text.pack(fill=tk.BOTH, **pad)

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _on_mode_change(self) -> None:
        """Switch the active mode and rebuild the operation list."""
        mode_name = self._mode_var.get()
        if mode_name == NormalMode.name:
            self._mode = NormalMode()
        else:
            self._mode = ScientificMode()
        self._refresh_operations()

    def _refresh_operations(self) -> None:
        """Repopulate the operation listbox from the current mode."""
        self._op_listbox.delete(0, tk.END)
        for label in self._mode.operations:
            self._op_listbox.insert(tk.END, label)
        if self._mode.operations:
            self._op_listbox.selection_set(0)
            self._on_op_selected(None)

    def _on_op_selected(self, _event) -> None:
        """Show or hide the second operand field based on selected arity."""
        selection = self._op_listbox.curselection()
        if not selection:
            return
        label = self._op_listbox.get(selection[0])
        _, arity = self._mode.operations[label]
        if arity == 1:
            self._label_b.grid_remove()
            self._entry_b.grid_remove()
        else:
            self._label_b.grid()
            self._entry_b.grid()

    def _on_calculate(self) -> None:
        """Parse inputs, execute the selected operation, and update the UI."""
        selection = self._op_listbox.curselection()
        if not selection:
            messagebox.showwarning(
                "No operation selected", "Please select an operation from the list."
            )
            return

        label = self._op_listbox.get(selection[0])
        op_name, arity = self._mode.operations[label]

        a_str = self._input_a_var.get().strip()
        if not a_str:
            messagebox.showerror("Missing input", "Please enter a value for Operand A.")
            return

        try:
            a = self._parse_operand(a_str, require_int=(op_name == "factorial"))
        except ValueError as exc:
            messagebox.showerror("Invalid input", f"Operand A: {exc}")
            return

        if arity == 2:
            b_str = self._input_b_var.get().strip()
            if not b_str:
                messagebox.showerror("Missing input", "Please enter a value for Operand B.")
                return
            try:
                b = self._parse_operand(b_str)
            except ValueError as exc:
                messagebox.showerror("Invalid input", f"Operand B: {exc}")
                return
            args = (a, b)
        else:
            args = (a,)

        try:
            result = self._session.execute(op_name, *args)
        except (ValueError, TypeError, ZeroDivisionError) as exc:
            messagebox.showerror("Calculation error", str(exc))
            return

        self._result_var.set(str(result))
        self._refresh_history()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_operand(value: str, require_int: bool = False) -> int | float:
        """Convert a string operand to int or float.

        Args:
            value: Raw string from an entry widget.
            require_int: When True, reject non-integer input.

        Returns:
            Parsed numeric value.

        Raises:
            ValueError: if the string cannot be converted.
        """
        if require_int:
            return int(value)
        try:
            return int(value)
        except ValueError:
            return float(value)

    def _refresh_history(self) -> None:
        """Overwrite the history text widget with the current session history."""
        self._history_text.configure(state=tk.NORMAL)
        self._history_text.delete("1.0", tk.END)
        for entry in self._session.history():
            self._history_text.insert(tk.END, entry + "\n")
        self._history_text.configure(state=tk.DISABLED)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def run_gui() -> None:
    """Launch the calculator GUI.  Blocks until the window is closed.

    Raises:
        RuntimeError: if tkinter is not installed in the current environment.
    """
    if not _TKINTER_AVAILABLE:
        raise RuntimeError(
            "tkinter is required to run the GUI but is not installed. "
            "Install the python3-tk package for your operating system."
        )
    root = tk.Tk()
    CalculatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui()
