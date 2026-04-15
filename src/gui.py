"""Tkinter-based GUI for the Calculator application.

Provides a graphical interface that reuses the existing CalculatorSession
for all computation and history management.  Mode-specific operation sets
are encapsulated in CalculatorMode subclasses (see gui_modes.py) so the
GUI loop itself is mode-agnostic.

Usage:
    python gui.py
"""
import tkinter as tk
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


class CalculatorGUI:
    """Tkinter GUI controller for the Calculator application.

    All computation is delegated to a CalculatorSession instance so that
    the GUI layer contains no arithmetic logic.  Mode switching updates the
    operation selector; the session and its history persist across mode
    changes within the same window lifetime.

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

        self._build_mode_frame()
        self._build_operation_frame()
        self._build_input_frame()
        self._build_calculate_button()
        self._build_result_frame()
        self._build_history_frame()

        # Populate the operation selector for the initial mode.
        self._refresh_operations()

    def _build_mode_frame(self) -> None:
        frame = tk.Frame(self._root, pady=4)
        frame.pack(fill=tk.X, padx=10)

        tk.Label(frame, text="Mode:", width=9, anchor="w").pack(side=tk.LEFT)

        self._mode_var = tk.StringVar(value=self._current_mode.name)
        for mode in self._modes:
            tk.Radiobutton(
                frame,
                text=mode.name,
                variable=self._mode_var,
                value=mode.name,
                command=self._on_mode_change,
            ).pack(side=tk.LEFT, padx=4)

    def _build_operation_frame(self) -> None:
        frame = tk.Frame(self._root, pady=4)
        frame.pack(fill=tk.X, padx=10)

        tk.Label(frame, text="Operation:", width=9, anchor="w").pack(side=tk.LEFT)

        self._op_var = tk.StringVar()
        self._op_combo = ttk.Combobox(
            frame,
            textvariable=self._op_var,
            state="readonly",
            width=18,
        )
        self._op_combo.pack(side=tk.LEFT, padx=4)
        self._op_combo.bind("<<ComboboxSelected>>", self._on_op_selected)

    def _build_input_frame(self) -> None:
        self._input_frame = tk.Frame(self._root, pady=4)
        self._input_frame.pack(fill=tk.X, padx=10)

        self._label_a = tk.Label(self._input_frame, text="Value A:", width=9, anchor="w")
        self._entry_a = tk.Entry(self._input_frame, width=14)

        self._label_b = tk.Label(self._input_frame, text="Value B:", width=9, anchor="w")
        self._entry_b = tk.Entry(self._input_frame, width=14)

    def _build_calculate_button(self) -> None:
        tk.Button(
            self._root,
            text="Calculate",
            command=self._on_calculate,
            width=12,
        ).pack(pady=6)

    def _build_result_frame(self) -> None:
        frame = tk.Frame(self._root, pady=4)
        frame.pack(fill=tk.X, padx=10)

        tk.Label(frame, text="Result:", width=9, anchor="w").pack(side=tk.LEFT)
        self._result_var = tk.StringVar()
        tk.Label(
            frame,
            textvariable=self._result_var,
            fg="blue",
            anchor="w",
            width=30,
        ).pack(side=tk.LEFT, padx=4)

    def _build_history_frame(self) -> None:
        frame = tk.LabelFrame(self._root, text="Session History", pady=4)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(4, 10))

        self._history_box = scrolledtext.ScrolledText(
            frame,
            height=8,
            state=tk.DISABLED,
            wrap=tk.WORD,
        )
        self._history_box.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

    # ------------------------------------------------------------------
    # State management helpers
    # ------------------------------------------------------------------

    def _refresh_operations(self) -> None:
        """Populate the operation combobox from the current mode."""
        labels = list(self._current_mode.operations.keys())
        self._op_combo["values"] = labels
        if labels:
            self._op_combo.set(labels[0])
            self._show_inputs_for(labels[0])

    def _show_inputs_for(self, display_name: str) -> None:
        """Show the correct number of input fields for the selected operation."""
        if not display_name or display_name not in self._current_mode.operations:
            return
        _, arity = self._current_mode.operations[display_name]

        # Remove all children from the input frame then re-add as needed.
        for widget in self._input_frame.winfo_children():
            widget.pack_forget()

        self._label_a.pack(side=tk.LEFT)
        self._entry_a.pack(side=tk.LEFT, padx=4)

        if arity == 2:
            self._label_b.pack(side=tk.LEFT)
            self._entry_b.pack(side=tk.LEFT, padx=4)

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
        self._show_inputs_for(self._op_var.get())

    def _on_calculate(self) -> None:
        """Read inputs, delegate to the session, display the result."""
        display_name = self._op_var.get()
        if not display_name:
            self._result_var.set("Please select an operation.")
            return

        op_name, arity = self._current_mode.operations[display_name]
        a_raw = self._entry_a.get().strip()
        if not a_raw:
            self._result_var.set("Please enter a value.")
            return

        try:
            require_int = op_name == "factorial"
            a = int(a_raw) if require_int else parse_number(a_raw)

            if arity == 2:
                b_raw = self._entry_b.get().strip()
                if not b_raw:
                    self._result_var.set("Please enter Value B.")
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
