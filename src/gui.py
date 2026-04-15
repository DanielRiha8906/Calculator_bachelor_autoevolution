"""Tkinter-based GUI for the Calculator application.

Provides a graphical interface that reuses the existing CalculatorSession
for all computation and history management.  Mode-specific operation sets
are encapsulated in CalculatorMode subclasses (see gui_modes.py) so the
GUI loop itself is mode-agnostic.

The window is divided into clearly labelled sections:
  - Mode selection (Simple / Scientific)
  - Operation selection with unary/binary indicator
  - Operand entry (one or two fields depending on operation arity)
  - Result display (prominent output area)
  - Action controls (Calculate, Clear)
  - Session history (scrollable log)

Usage:
    python gui.py
"""
import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk, scrolledtext

from .gui_modes import CalculatorMode, SimpleMode, ScientificMode, parse_number
from .session import CalculatorSession
from .error_logger import log_error

# Re-export mode classes so callers only need to import from src.gui.
__all__ = [
    "CalculatorMode",
    "SimpleMode",
    "ScientificMode",
    "CalculatorGUI",
    "main",
]

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_PAD_OUTER = 12   # outer frame padding (pixels)
_PAD_INNER = 8    # inner section padding
_PAD_WIDGET = 4   # between adjacent widgets


class _OperandSection:
    """Manages the operand entry fields for a single operation.

    Responsible for:
      - Creating and owning the label and entry widgets.
      - Showing/hiding the second operand field when arity changes.
      - Reading and validating the raw text from the entries.
      - Clearing the entries on demand.

    Args:
        parent: The parent tkinter widget that owns this section.
    """

    def __init__(self, parent: tk.Widget) -> None:
        frame = ttk.LabelFrame(parent, text="Operands", padding=_PAD_INNER)
        frame.pack(fill=tk.X, padx=_PAD_OUTER, pady=(_PAD_WIDGET, 0))
        frame.columnconfigure(1, weight=1)

        # First operand row
        ttk.Label(frame, text="First operand:").grid(
            row=0, column=0, sticky="w", pady=_PAD_WIDGET
        )
        self._entry_a = ttk.Entry(frame)
        self._entry_a.grid(row=0, column=1, sticky="ew", padx=(_PAD_WIDGET, 0))

        # Second operand row (shown for binary operations only)
        self._label_b = ttk.Label(frame, text="Second operand:")
        self._entry_b = ttk.Entry(frame)

        self._arity: int = 1
        self._frame = frame

    def set_arity(self, arity: int) -> None:
        """Show or hide the second operand row based on arity."""
        if arity == self._arity:
            return
        self._arity = arity
        if arity == 2:
            self._label_b.grid(
                row=1, column=0, sticky="w", pady=_PAD_WIDGET
            )
            self._entry_b.grid(
                row=1, column=1, sticky="ew", padx=(_PAD_WIDGET, 0)
            )
        else:
            self._label_b.grid_remove()
            self._entry_b.grid_remove()

    def clear(self) -> None:
        """Clear all entry fields."""
        self._entry_a.delete(0, tk.END)
        self._entry_b.delete(0, tk.END)

    def read_a(self) -> str:
        """Return the raw text from the first entry field."""
        return self._entry_a.get().strip()

    def read_b(self) -> str:
        """Return the raw text from the second entry field."""
        return self._entry_b.get().strip()

    def focus_a(self) -> None:
        """Move keyboard focus to the first entry field."""
        self._entry_a.focus_set()


class CalculatorGUI:
    """Tkinter GUI controller for the Calculator application.

    All computation is delegated to a CalculatorSession instance so that
    the GUI layer contains no arithmetic logic.  Mode switching updates the
    operation selector and operand section; the session and its history
    persist across mode changes within the same window lifetime.

    Args:
        root: The Tk root window (or any Toplevel container).
    """

    def __init__(self, root: tk.Tk) -> None:
        self._root = root
        self._session = CalculatorSession()
        self._modes: list[CalculatorMode] = [SimpleMode(), ScientificMode()]
        self._current_mode: CalculatorMode = self._modes[0]
        self._setup_ui()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _setup_ui(self) -> None:
        """Build and layout all widgets."""
        self._root.title("Calculator")
        self._root.resizable(True, True)
        self._root.minsize(380, 520)

        # Configure a uniform style via ttk for consistency.
        style = ttk.Style(self._root)
        style.configure("Result.TLabel", font=("TkDefaultFont", 20, "bold"))
        style.configure("Arity.TLabel", font=("TkDefaultFont", 9))

        self._build_mode_section()
        self._build_operation_section()
        self._operand_section = _OperandSection(self._root)
        self._build_action_section()
        self._build_result_section()
        self._build_history_section()

        # Populate the operation selector for the initial mode.
        self._refresh_operations()

    def _build_mode_section(self) -> None:
        frame = ttk.LabelFrame(self._root, text="Mode", padding=_PAD_INNER)
        frame.pack(fill=tk.X, padx=_PAD_OUTER, pady=(_PAD_OUTER, _PAD_WIDGET))

        self._mode_var = tk.StringVar(value=self._current_mode.name)
        for mode in self._modes:
            ttk.Radiobutton(
                frame,
                text=mode.name,
                variable=self._mode_var,
                value=mode.name,
                command=self._on_mode_change,
            ).pack(side=tk.LEFT, padx=(_PAD_WIDGET, _PAD_WIDGET * 2))

    def _build_operation_section(self) -> None:
        frame = ttk.LabelFrame(self._root, text="Operation", padding=_PAD_INNER)
        frame.pack(fill=tk.X, padx=_PAD_OUTER, pady=_PAD_WIDGET)
        frame.columnconfigure(0, weight=1)

        inner = ttk.Frame(frame)
        inner.pack(fill=tk.X)
        inner.columnconfigure(0, weight=1)

        self._op_var = tk.StringVar()
        self._op_combo = ttk.Combobox(
            inner,
            textvariable=self._op_var,
            state="readonly",
        )
        self._op_combo.grid(row=0, column=0, sticky="ew")
        self._op_combo.bind("<<ComboboxSelected>>", self._on_op_selected)

        self._arity_label_var = tk.StringVar()
        ttk.Label(
            inner,
            textvariable=self._arity_label_var,
            style="Arity.TLabel",
            foreground="gray",
        ).grid(row=0, column=1, padx=(_PAD_WIDGET, 0))

    def _build_action_section(self) -> None:
        frame = ttk.Frame(self._root)
        frame.pack(pady=_PAD_INNER)

        ttk.Button(
            frame,
            text="Calculate",
            command=self._on_calculate,
            width=12,
        ).pack(side=tk.LEFT, padx=(_PAD_WIDGET, _PAD_WIDGET * 2))

        ttk.Button(
            frame,
            text="Clear",
            command=self._on_clear,
            width=8,
        ).pack(side=tk.LEFT, padx=_PAD_WIDGET)

    def _build_result_section(self) -> None:
        frame = ttk.LabelFrame(self._root, text="Result", padding=_PAD_INNER)
        frame.pack(fill=tk.X, padx=_PAD_OUTER, pady=_PAD_WIDGET)

        self._result_var = tk.StringVar(value="—")
        ttk.Label(
            frame,
            textvariable=self._result_var,
            style="Result.TLabel",
            anchor="center",
        ).pack(fill=tk.X, pady=_PAD_WIDGET)

    def _build_history_section(self) -> None:
        frame = ttk.LabelFrame(
            self._root, text="Session History", padding=_PAD_INNER
        )
        frame.pack(
            fill=tk.BOTH, expand=True,
            padx=_PAD_OUTER, pady=(_PAD_WIDGET, _PAD_OUTER)
        )

        self._history_box = scrolledtext.ScrolledText(
            frame,
            height=8,
            state=tk.DISABLED,
            wrap=tk.WORD,
        )
        self._history_box.pack(fill=tk.BOTH, expand=True)

    # ------------------------------------------------------------------
    # State management helpers
    # ------------------------------------------------------------------

    def _refresh_operations(self) -> None:
        """Populate the operation combobox from the current mode."""
        labels = list(self._current_mode.operations.keys())
        self._op_combo["values"] = labels
        if labels:
            self._op_combo.set(labels[0])
            self._apply_operation(labels[0])

    def _apply_operation(self, display_name: str) -> None:
        """Update arity label and operand section for the selected operation."""
        ops = self._current_mode.operations
        if not display_name or display_name not in ops:
            return
        _, arity = ops[display_name]
        self._arity_label_var.set("Binary" if arity == 2 else "Unary")
        self._operand_section.set_arity(arity)
        self._operand_section.focus_a()

    def _refresh_history_display(self) -> None:
        """Overwrite the history widget content with the current session history."""
        entries = self._session.history()
        self._history_box.config(state=tk.NORMAL)
        self._history_box.delete("1.0", tk.END)
        for entry in entries:
            self._history_box.insert(tk.END, entry + "\n")
        self._history_box.config(state=tk.DISABLED)
        self._history_box.see(tk.END)

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _on_mode_change(self) -> None:
        """Handle mode radio button selection."""
        chosen_name = self._mode_var.get()
        for mode in self._modes:
            if mode.name == chosen_name:
                self._current_mode = mode
                break
        self._refresh_operations()

    def _on_op_selected(self, _event=None) -> None:
        """Handle combobox selection change."""
        self._apply_operation(self._op_var.get())

    def _on_clear(self) -> None:
        """Clear all input fields and the result display."""
        self._operand_section.clear()
        self._result_var.set("—")

    def _on_calculate(self) -> None:
        """Read inputs, delegate to the session, display the result."""
        display_name = self._op_var.get()
        if not display_name:
            self._result_var.set("Please select an operation.")
            return

        op_name, arity = self._current_mode.operations[display_name]
        a_raw = self._operand_section.read_a()
        if not a_raw:
            self._result_var.set("Please enter a value.")
            return

        try:
            require_int = op_name == "factorial"
            a = int(a_raw) if require_int else parse_number(a_raw)

            if arity == 2:
                b_raw = self._operand_section.read_b()
                if not b_raw:
                    self._result_var.set("Please enter the second operand.")
                    return
                b = parse_number(b_raw)
                result = self._session.execute(op_name, a, b)
            else:
                result = self._session.execute(op_name, a)

            self._result_var.set(str(result))
            self._refresh_history_display()

        except (ValueError, TypeError) as exc:
            log_error("gui", str(exc))
            self._result_var.set(f"Error: {exc}")
        except ZeroDivisionError:
            log_error("gui", f"division by zero in {op_name}")
            self._result_var.set("Error: division by zero")


def main() -> None:
    """Launch the Calculator GUI application."""
    root = tk.Tk()
    CalculatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
