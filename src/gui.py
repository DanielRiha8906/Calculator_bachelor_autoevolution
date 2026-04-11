"""Tkinter GUI for the calculator application.

Provides a CalculatorApp window that wraps the Calculator class, supporting
Simple and Scientific modes through the CalculatorMode abstractions defined
in gui_modes.  All calculation logic is delegated to Calculator — nothing is
duplicated here.

Launch via:
    python -m src.gui
"""
from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Optional

from src.calculator import Calculator
from src.gui_modes import (
    CalculatorMode,
    OperationSpec,
    ScientificMode,
    SimpleMode,
    parse_number,
)


class CalculatorApp(tk.Tk):
    """Main calculator window.

    Supports mode switching between Simple and Scientific, dynamic operand
    input fields based on the selected operation, a live result display, and a
    scrollable session-history list.
    """

    def __init__(self) -> None:
        super().__init__()
        self.title("Calculator")
        self.resizable(False, True)
        self.calculator = Calculator()
        self.modes: list[CalculatorMode] = [SimpleMode(), ScientificMode()]
        self.current_mode: CalculatorMode = self.modes[0]
        self.history: list[str] = []
        self._build_ui()
        self._refresh_operations()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        self._build_mode_frame()
        self._build_operation_frame()
        self._build_input_frame()
        self._build_result_frame()
        self._build_buttons()
        self._build_history_frame()

    def _build_mode_frame(self) -> None:
        frame = ttk.LabelFrame(self, text="Mode")
        frame.pack(fill=tk.X, padx=10, pady=(10, 4))

        self.mode_var = tk.StringVar(value=self.current_mode.name)
        for mode in self.modes:
            ttk.Radiobutton(
                frame,
                text=mode.name,
                value=mode.name,
                variable=self.mode_var,
                command=self._on_mode_change,
            ).pack(side=tk.LEFT, padx=8, pady=4)

    def _build_operation_frame(self) -> None:
        frame = ttk.LabelFrame(self, text="Operation")
        frame.pack(fill=tk.X, padx=10, pady=4)

        self.op_var = tk.StringVar()
        self.op_combo = ttk.Combobox(
            frame, textvariable=self.op_var, state="readonly", width=32
        )
        self.op_combo.pack(fill=tk.X, padx=8, pady=6)
        self.op_combo.bind("<<ComboboxSelected>>", self._on_operation_change)

    def _build_input_frame(self) -> None:
        frame = ttk.LabelFrame(self, text="Inputs")
        frame.pack(fill=tk.X, padx=10, pady=4)
        frame.columnconfigure(1, weight=1)

        self.label_a = ttk.Label(frame, text="Value:")
        self.label_a.grid(row=0, column=0, sticky=tk.W, padx=8, pady=4)
        self.entry_a = ttk.Entry(frame, width=30)
        self.entry_a.grid(row=0, column=1, sticky=tk.EW, padx=8, pady=4)

        self.label_b = ttk.Label(frame, text="")
        self.label_b.grid(row=1, column=0, sticky=tk.W, padx=8, pady=4)
        self.entry_b = ttk.Entry(frame, width=30)
        self.entry_b.grid(row=1, column=1, sticky=tk.EW, padx=8, pady=4)

    def _build_result_frame(self) -> None:
        frame = ttk.LabelFrame(self, text="Result")
        frame.pack(fill=tk.X, padx=10, pady=4)

        self.result_var = tk.StringVar(value="\u2014")
        ttk.Label(
            frame, textvariable=self.result_var, font=("TkDefaultFont", 16, "bold")
        ).pack(padx=8, pady=8)

    def _build_buttons(self) -> None:
        frame = ttk.Frame(self)
        frame.pack(padx=10, pady=4)

        ttk.Button(frame, text="Calculate", command=self._calculate).pack(
            side=tk.LEFT, padx=4
        )
        ttk.Button(frame, text="Clear", command=self._clear).pack(side=tk.LEFT, padx=4)

    def _build_history_frame(self) -> None:
        frame = ttk.LabelFrame(self, text="Session History")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(4, 10))

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
        self.history_listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, height=8)
        scrollbar.config(command=self.history_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_listbox.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _on_mode_change(self) -> None:
        mode_name = self.mode_var.get()
        for mode in self.modes:
            if mode.name == mode_name:
                self.current_mode = mode
                break
        self._refresh_operations()

    def _on_operation_change(self, _event: object = None) -> None:
        op = self._selected_operation()
        if op is not None:
            self._update_inputs(op)

    # ------------------------------------------------------------------
    # UI state helpers
    # ------------------------------------------------------------------

    def _refresh_operations(self) -> None:
        """Repopulate the operation combobox for the current mode."""
        ops = self.current_mode.operations
        self.op_combo["values"] = [op.name for op in ops]
        if ops:
            self.op_combo.current(0)
            self._update_inputs(ops[0])
        self.result_var.set("\u2014")

    def _selected_operation(self) -> Optional[OperationSpec]:
        op_name = self.op_var.get()
        for op in self.current_mode.operations:
            if op.name == op_name:
                return op
        return None

    def _update_inputs(self, op: OperationSpec) -> None:
        """Reconfigure input labels and enable/disable the second input field."""
        self.label_a.config(text=f"{op.label_a}:")
        self.entry_a.delete(0, tk.END)

        if op.arity == 2:
            self.label_b.config(text=f"{op.label_b}:")
            self.entry_b.config(state=tk.NORMAL)
            self.entry_b.delete(0, tk.END)
        else:
            self.label_b.config(text="")
            self.entry_b.config(state=tk.DISABLED)
            self.entry_b.delete(0, tk.END)

    # ------------------------------------------------------------------
    # Calculation
    # ------------------------------------------------------------------

    def _calculate(self) -> None:
        """Read inputs, call Calculator, update result and history."""
        op = self._selected_operation()
        if op is None:
            return

        try:
            a = parse_number(self.entry_a.get(), require_int=op.require_int)
        except ValueError as exc:
            messagebox.showerror("Input Error", f"First input \u2014 {exc}")
            return

        b: int | float | None = None
        if op.arity == 2:
            try:
                b = parse_number(self.entry_b.get())
            except ValueError as exc:
                messagebox.showerror("Input Error", f"Second input \u2014 {exc}")
                return

        try:
            method = getattr(self.calculator, op.method)
            result = method(a, b) if op.arity == 2 else method(a)
        except (ValueError, ZeroDivisionError, OverflowError) as exc:
            messagebox.showerror("Calculation Error", str(exc))
            self.result_var.set("Error")
            return

        # Display whole-number floats without a decimal point for readability.
        if isinstance(result, float) and result == int(result) and abs(result) < 1e15:
            display = str(int(result))
        else:
            display = str(result)

        self.result_var.set(display)

        entry = (
            f"{op.name}({a}, {b}) = {display}"
            if op.arity == 2
            else f"{op.name}({a}) = {display}"
        )
        self.history.append(entry)
        self.history_listbox.insert(tk.END, entry)
        self.history_listbox.see(tk.END)

    def _clear(self) -> None:
        """Clear input fields and reset the result display."""
        self.entry_a.delete(0, tk.END)
        if str(self.entry_b.cget("state")) == tk.NORMAL:
            self.entry_b.delete(0, tk.END)
        self.result_var.set("\u2014")


def run() -> None:
    """Launch the calculator GUI."""
    app = CalculatorApp()
    app.mainloop()


if __name__ == "__main__":
    run()
