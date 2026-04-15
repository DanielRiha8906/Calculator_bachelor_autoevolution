"""Tkinter-based graphical user interface for the Calculator.

Presents all current calculator functionality through a clean, structured
interface organized into six sections:

  - Mode selection (Normal / Scientific)
  - Operation selection (binary and unary operations clearly separated)
  - Operand entry (adapts dynamically to the selected operation's arity)
  - Result display (prominent primary output region)
  - Action controls (Calculate, Clear)
  - Session history (scrollable log of every successful calculation)

The GUI is built from discrete section classes so that layout management,
widget configuration, and mode-specific logic stay within clearly named
responsibility boundaries rather than one monolithic handler.
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from .session import CalculatorSession, BINARY_OPS
from .error_logger import log_error

# ---------------------------------------------------------------------------
# Operation catalogue
# ---------------------------------------------------------------------------

_NORMAL_BINARY: list[str] = ["add", "subtract", "multiply", "divide"]
_NORMAL_UNARY: list[str] = ["square", "square_root"]

_SCIENTIFIC_BINARY: list[str] = ["add", "subtract", "multiply", "divide", "power"]
_SCIENTIFIC_UNARY: list[str] = [
    "square", "square_root",
    "factorial", "cube", "cube_root",
    "log", "ln",
    "sin", "cos", "tan", "cot", "asin", "acos",
]

_MODE_BINARY: dict[str, list[str]] = {
    "Normal": _NORMAL_BINARY,
    "Scientific": _SCIENTIFIC_BINARY,
}
_MODE_UNARY: dict[str, list[str]] = {
    "Normal": _NORMAL_UNARY,
    "Scientific": _SCIENTIFIC_UNARY,
}

# ---------------------------------------------------------------------------
# Visual constants
# ---------------------------------------------------------------------------

_PAD = 8          # standard outer padding
_PAD_INNER = 4    # tighter inner padding

_FONT_LABEL = ("Helvetica", 10)
_FONT_ENTRY = ("Helvetica", 11)
_FONT_RESULT = ("Helvetica", 18, "bold")
_FONT_HISTORY = ("Courier", 9)
_FONT_SECTION = ("Helvetica", 10, "bold")

_COLOR_BG = "#F4F4F4"
_COLOR_SECTION_BG = "#FFFFFF"
_COLOR_RESULT_BG = "#E3F2FD"
_COLOR_RESULT_FG = "#0D47A1"
_COLOR_ERROR_FG = "#C62828"
_COLOR_HISTORY_BG = "#FAFAFA"
_COLOR_BTN_CALC = "#1565C0"
_COLOR_BTN_CALC_FG = "#FFFFFF"
_COLOR_BTN_CLEAR = "#455A64"
_COLOR_BTN_CLEAR_FG = "#FFFFFF"


# ---------------------------------------------------------------------------
# Section classes
# ---------------------------------------------------------------------------

class _SectionFrame(ttk.LabelFrame):
    """Labeled frame that visually groups a set of related widgets."""

    def __init__(self, parent: tk.Widget, title: str, **kwargs) -> None:
        super().__init__(
            parent,
            text=title,
            padding=(_PAD, _PAD_INNER, _PAD, _PAD),
            **kwargs,
        )


class ModeSelector:
    """Builds and owns the mode-selection section.

    Exposes the selected mode via a shared ``tk.StringVar``.  An external
    ``on_change`` callback (if provided) is called whenever the mode changes.
    """

    def __init__(
        self,
        parent: tk.Widget,
        mode_var: tk.StringVar,
        on_change,
    ) -> None:
        self._var = mode_var
        self._on_change = on_change
        self._frame = _SectionFrame(parent, "Mode")
        self._build()

    @property
    def frame(self) -> _SectionFrame:
        return self._frame

    def _build(self) -> None:
        for col, mode in enumerate(("Normal", "Scientific")):
            ttk.Radiobutton(
                self._frame,
                text=mode,
                variable=self._var,
                value=mode,
                command=self._on_change,
            ).grid(row=0, column=col, padx=(_PAD, _PAD * 2), sticky="w")


class OperationSelector:
    """Builds and owns the operation-selection section.

    Operations are split into Binary and Unary groups.  The active group is
    chosen with radio buttons; the operation dropdown updates to show only
    the operations that belong to the current mode and group.

    Exposes the selected operation name via a shared ``tk.StringVar``.
    """

    def __init__(
        self,
        parent: tk.Widget,
        mode_var: tk.StringVar,
        op_type_var: tk.StringVar,
        op_name_var: tk.StringVar,
        on_arity_change,
    ) -> None:
        self._mode_var = mode_var
        self._op_type_var = op_type_var
        self._op_name_var = op_name_var
        self._on_arity_change = on_arity_change
        self._frame = _SectionFrame(parent, "Operation")
        self._combo: ttk.Combobox | None = None
        self._build()

    @property
    def frame(self) -> _SectionFrame:
        return self._frame

    def _build(self) -> None:
        frame = self._frame

        # -- arity type row --
        type_row = ttk.Frame(frame)
        type_row.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, _PAD_INNER))

        ttk.Label(type_row, text="Type:", font=_FONT_LABEL).pack(side="left")
        for op_type in ("Binary", "Unary"):
            ttk.Radiobutton(
                type_row,
                text=op_type,
                variable=self._op_type_var,
                value=op_type,
                command=self._refresh,
            ).pack(side="left", padx=(_PAD, _PAD * 2))

        # -- operation dropdown row --
        op_row = ttk.Frame(frame)
        op_row.grid(row=1, column=0, columnspan=2, sticky="ew")
        op_row.columnconfigure(1, weight=1)

        ttk.Label(op_row, text="Select:", font=_FONT_LABEL).grid(
            row=0, column=0, sticky="w", padx=(0, _PAD)
        )
        self._combo = ttk.Combobox(
            op_row,
            textvariable=self._op_name_var,
            state="readonly",
            font=_FONT_ENTRY,
        )
        self._combo.grid(row=0, column=1, sticky="ew")
        self._combo.bind("<<ComboboxSelected>>", lambda _e: self._on_arity_change())

        self._refresh()

    def _refresh(self) -> None:
        """Rebuild the dropdown to match the current mode and operation type."""
        mode = self._mode_var.get()
        op_type = self._op_type_var.get()
        ops = (
            _MODE_BINARY[mode] if op_type == "Binary" else _MODE_UNARY[mode]
        )
        if self._combo is not None:
            self._combo["values"] = ops
            if self._op_name_var.get() not in ops:
                self._op_name_var.set(ops[0] if ops else "")
        self._on_arity_change()

    def refresh_for_mode(self) -> None:
        """Called by the parent when the mode changes."""
        self._refresh()


class OperandSection:
    """Builds and owns the operand-entry section.

    Operand B is shown for binary operations and hidden for unary ones.
    The ``factorial`` operation additionally restricts input to integers.
    """

    def __init__(
        self,
        parent: tk.Widget,
        operand_a_var: tk.StringVar,
        operand_b_var: tk.StringVar,
    ) -> None:
        self._a_var = operand_a_var
        self._b_var = operand_b_var
        self._frame = _SectionFrame(parent, "Operands")
        self._b_label: ttk.Label | None = None
        self._b_entry: ttk.Entry | None = None
        self._a_label: ttk.Label | None = None
        self._build()

    @property
    def frame(self) -> _SectionFrame:
        return self._frame

    def _build(self) -> None:
        frame = self._frame
        frame.columnconfigure(1, weight=1)

        self._a_label = ttk.Label(frame, text="Operand A:", font=_FONT_LABEL)
        self._a_label.grid(row=0, column=0, sticky="w", padx=(0, _PAD))
        ttk.Entry(
            frame,
            textvariable=self._a_var,
            font=_FONT_ENTRY,
        ).grid(row=0, column=1, sticky="ew", pady=_PAD_INNER)

        self._b_label = ttk.Label(frame, text="Operand B:", font=_FONT_LABEL)
        self._b_label.grid(row=1, column=0, sticky="w", padx=(0, _PAD))
        self._b_entry = ttk.Entry(
            frame,
            textvariable=self._b_var,
            font=_FONT_ENTRY,
        )
        self._b_entry.grid(row=1, column=1, sticky="ew", pady=_PAD_INNER)

    def set_binary_mode(self, is_binary: bool, op_name: str = "") -> None:
        """Show Operand B for binary operations; hide it for unary ones.

        Also updates the Operand A label to reflect integer-only input when
        the ``factorial`` operation is selected.
        """
        if self._b_label is None or self._b_entry is None or self._a_label is None:
            return
        if is_binary:
            self._b_label.grid()
            self._b_entry.grid()
            self._a_label.configure(text="Operand A:")
        else:
            self._b_label.grid_remove()
            self._b_entry.grid_remove()
            hint = " (integer)" if op_name == "factorial" else ""
            self._a_label.configure(text=f"Operand A{hint}:")

    def get_operands(self, op_name: str) -> tuple:
        """Parse and return operands appropriate for *op_name*.

        Returns:
            A 1-tuple ``(a,)`` for unary ops or a 2-tuple ``(a, b)`` for
            binary ones.

        Raises:
            ValueError: if an entry field cannot be parsed as a number.
        """
        raw_a = self._a_var.get().strip()
        if op_name == "factorial":
            a = int(raw_a)
        else:
            a = _parse_number(raw_a)
        if op_name in BINARY_OPS:
            raw_b = self._b_var.get().strip()
            b = _parse_number(raw_b)
            return (a, b)
        return (a,)


class ResultDisplay:
    """Builds and owns the result-display section.

    The result area uses a large, prominent font so it is visually distinct
    from every other region of the interface.
    """

    def __init__(self, parent: tk.Widget) -> None:
        self._frame = _SectionFrame(parent, "Result")
        self._label: tk.Label | None = None
        self._build()

    @property
    def frame(self) -> _SectionFrame:
        return self._frame

    def _build(self) -> None:
        self._label = tk.Label(
            self._frame,
            text="—",
            font=_FONT_RESULT,
            bg=_COLOR_RESULT_BG,
            fg=_COLOR_RESULT_FG,
            anchor="center",
            relief="flat",
            padx=_PAD * 2,
            pady=_PAD,
        )
        self._label.pack(fill="both", expand=True, ipady=_PAD)

    def show_result(self, value) -> None:
        """Display *value* as the current result."""
        if self._label is not None:
            self._label.configure(
                text=str(value),
                fg=_COLOR_RESULT_FG,
            )

    def show_error(self, message: str) -> None:
        """Display an error message in place of the result."""
        if self._label is not None:
            self._label.configure(
                text=f"Error: {message}",
                fg=_COLOR_ERROR_FG,
            )

    def clear(self) -> None:
        """Reset the display to its initial state."""
        if self._label is not None:
            self._label.configure(text="—", fg=_COLOR_RESULT_FG)


class HistoryPanel:
    """Builds and owns the session-history panel.

    Displays each successful calculation as a function-style entry
    (e.g. ``add(2, 3) = 5``) in a monospaced, scrollable text area.
    """

    def __init__(self, parent: tk.Widget) -> None:
        self._frame = _SectionFrame(parent, "Session History")
        self._text: tk.Text | None = None
        self._build()

    @property
    def frame(self) -> _SectionFrame:
        return self._frame

    def _build(self) -> None:
        frame = self._frame
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        scrollbar = ttk.Scrollbar(frame, orient="vertical")
        scrollbar.grid(row=0, column=1, sticky="ns")

        self._text = tk.Text(
            frame,
            font=_FONT_HISTORY,
            bg=_COLOR_HISTORY_BG,
            state="disabled",
            height=8,
            yscrollcommand=scrollbar.set,
            relief="flat",
            wrap="none",
            padx=_PAD_INNER,
            pady=_PAD_INNER,
        )
        self._text.grid(row=0, column=0, sticky="nsew")
        scrollbar.configure(command=self._text.yview)

    def refresh(self, entries: list[str]) -> None:
        """Repopulate the history widget with *entries*."""
        if self._text is None:
            return
        self._text.configure(state="normal")
        self._text.delete("1.0", "end")
        for entry in entries:
            self._text.insert("end", entry + "\n")
        self._text.configure(state="disabled")
        self._text.see("end")

    def clear(self) -> None:
        """Erase all displayed history entries."""
        self.refresh([])


# ---------------------------------------------------------------------------
# Main application
# ---------------------------------------------------------------------------

class CalculatorGUI:
    """Main application window.

    Coordinates all section widgets and owns the single ``CalculatorSession``
    that performs the actual computations.

    Usage::

        root = tk.Tk()
        app = CalculatorGUI(root)
        root.mainloop()
    """

    def __init__(self, root: tk.Tk) -> None:
        self._root = root
        self._session = CalculatorSession()

        # -- shared tkinter variables --
        self._mode_var = tk.StringVar(value="Normal")
        self._op_type_var = tk.StringVar(value="Binary")
        self._op_name_var = tk.StringVar(value="add")
        self._operand_a_var = tk.StringVar()
        self._operand_b_var = tk.StringVar()

        self._root.title("Calculator")
        self._root.resizable(True, True)
        self._root.configure(bg=_COLOR_BG)
        self._root.minsize(380, 560)

        self._setup_styles()
        self._build_ui()

    def _setup_styles(self) -> None:
        style = ttk.Style(self._root)
        style.theme_use("clam")
        style.configure("TLabelframe.Label", font=_FONT_SECTION)
        style.configure("TRadiobutton", font=_FONT_LABEL)
        style.configure("TLabel", font=_FONT_LABEL)
        style.configure(
            "Calc.TButton",
            font=("Helvetica", 11, "bold"),
            padding=(_PAD * 2, _PAD),
        )
        style.configure(
            "Clear.TButton",
            font=("Helvetica", 10),
            padding=(_PAD * 2, _PAD),
        )

    def _build_ui(self) -> None:
        """Assemble all six sections inside a single scrollable main frame."""
        outer = ttk.Frame(self._root, padding=_PAD)
        outer.pack(fill="both", expand=True)
        outer.columnconfigure(0, weight=1)

        # 1 — mode selection
        self._mode_section = ModeSelector(
            outer,
            self._mode_var,
            on_change=self._on_mode_change,
        )
        self._mode_section.frame.grid(
            row=0, column=0, sticky="ew", pady=(0, _PAD_INNER)
        )

        # 2 — operation selection
        self._op_section = OperationSelector(
            outer,
            self._mode_var,
            self._op_type_var,
            self._op_name_var,
            on_arity_change=self._on_arity_change,
        )
        self._op_section.frame.grid(
            row=1, column=0, sticky="ew", pady=(0, _PAD_INNER)
        )

        # 3 — operand entry
        self._operand_section = OperandSection(
            outer,
            self._operand_a_var,
            self._operand_b_var,
        )
        self._operand_section.frame.grid(
            row=2, column=0, sticky="ew", pady=(0, _PAD_INNER)
        )

        # 4 — action buttons
        btn_frame = ttk.Frame(outer)
        btn_frame.grid(row=3, column=0, sticky="ew", pady=(0, _PAD_INNER))
        btn_frame.columnconfigure((0, 1), weight=1)

        self._calc_btn = ttk.Button(
            btn_frame,
            text="Calculate",
            style="Calc.TButton",
            command=self._on_calculate,
        )
        self._calc_btn.grid(row=0, column=0, sticky="ew", padx=(0, _PAD_INNER))

        self._clear_btn = ttk.Button(
            btn_frame,
            text="Clear",
            style="Clear.TButton",
            command=self._on_clear,
        )
        self._clear_btn.grid(row=0, column=1, sticky="ew")

        # 5 — result display
        self._result_section = ResultDisplay(outer)
        self._result_section.frame.grid(
            row=4, column=0, sticky="ew", pady=(0, _PAD_INNER)
        )

        # 6 — session history
        self._history_section = HistoryPanel(outer)
        self._history_section.frame.grid(
            row=5, column=0, sticky="nsew"
        )
        outer.rowconfigure(5, weight=1)

        # initialise the operand section arity state
        self._on_arity_change()

        # bind Enter key to Calculate
        self._root.bind("<Return>", lambda _e: self._on_calculate())

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _on_mode_change(self) -> None:
        """Handle a mode switch: refresh the operation list."""
        self._op_section.refresh_for_mode()

    def _on_arity_change(self) -> None:
        """Handle an operation-type or operation-name change.

        Updates the operand section to show or hide Operand B.
        """
        op_name = self._op_name_var.get()
        is_binary = op_name in BINARY_OPS
        self._operand_section.set_binary_mode(is_binary, op_name)

    def _on_calculate(self) -> None:
        """Read operands, execute the selected operation, update result and history."""
        op_name = self._op_name_var.get()
        if not op_name:
            self._result_section.show_error("No operation selected.")
            return
        try:
            operands = self._operand_section.get_operands(op_name)
            result = self._session.execute(op_name, *operands)
        except (ValueError, TypeError, ZeroDivisionError) as exc:
            log_error("gui", f"calculation error in {op_name}: {exc}")
            self._result_section.show_error(str(exc))
            return
        self._result_section.show_result(result)
        self._history_section.refresh(self._session.history())

    def _on_clear(self) -> None:
        """Clear the operand fields and result display."""
        self._operand_a_var.set("")
        self._operand_b_var.set("")
        self._result_section.clear()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _parse_number(raw: str) -> int | float:
    """Convert *raw* to ``int`` if possible, otherwise to ``float``.

    Args:
        raw: The string read from an entry widget.

    Raises:
        ValueError: if *raw* cannot be parsed as a number.
    """
    try:
        return int(raw)
    except ValueError:
        return float(raw)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Launch the calculator GUI application."""
    root = tk.Tk()
    CalculatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
