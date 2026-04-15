# Codebase Map

## src/__init__.py
- **Purpose:** Package initializer for the `src` module; re-exports Calculator.
- **Exports:** `Calculator`
- **Key invariants:** Re-exports Calculator from `src.calculator` via `__all__`. Has a module-level docstring describing the package purpose.
- **Last updated:** cycle 12

## src/calculator.py
- **Purpose:** Core calculator facade: per-instance history, error logging, and operation dispatch; delegates operation implementations to the `src.operations` sub-package.
- **Imports:** `from .operations import arithmetic, advanced, scientific`
- **Module-level docstring:** Present — describes module role and cross-cutting concerns.
- **Module-level constants:** `UNARY_OPS`, `BINARY_OPS`, `INTEGER_OPS`, `SCIENTIFIC_UNARY_OPS` — sets classifying all operations by arity and type requirements.
- **Module-level helpers:** `_to_int_if_needed(op, value)` — coerces value to int for INTEGER_OPS, raises ValueError for non-whole numbers.
- **Module-level:** `logger = logging.getLogger(__name__)` — logs errors at ERROR level before re-raising.
- **Public API:**
  - `Calculator.__init__()` → initialises `self.history: list[dict]` to `[]`; has docstring
  - `Calculator.get_history()` → returns a shallow copy of `self.history`
  - `Calculator.add(a, b)`, `subtract`, `multiply`, `divide` → arithmetic ops; divide logs ZeroDivisionError
  - `Calculator.factorial(n)`, `square`, `cube`, `square_root`, `cube_root`, `power`, `log`, `ln` → advanced ops; factorial/square_root/log/ln log ValueError
  - `Calculator.sin(x)`, `cos(x)`, `tan(x)` → trigonometric (radians); no error logging needed
  - `Calculator.asin(x)`, `acos(x)` → inverse trig; logs and raises `ValueError` for `|x| > 1`
  - `Calculator.atan(x)`, `sinh(x)`, `cosh(x)`, `tanh(x)`, `exp(x)` → hyperbolic/exponential; no domain errors
  - `Calculator.execute(op, *operands)` → dispatches by op name across BINARY_OPS, UNARY_OPS, SCIENTIFIC_UNARY_OPS; applies _to_int_if_needed for INTEGER_OPS; records history on success; propagates exceptions unchanged; raises ValueError for unknown ops.
- **Key invariants:** History is recorded by `execute()`, not by individual Calculator methods. Each history entry is `{"op": str, "operands": tuple, "result": float|int}`. Failed operations are not recorded. `get_history()` returns a copy — callers cannot mutate internal state. SCIENTIFIC_UNARY_OPS are not in UNARY_OPS (separate set). All scientific ops are unary.
- **Last updated:** cycle 13

## src/operations/__init__.py
- **Purpose:** Operations sub-package initializer; re-exports all arithmetic, advanced, and scientific operation functions for convenience.
- **Exports:** `add`, `subtract`, `multiply`, `divide`, `factorial`, `square`, `cube`, `square_root`, `cube_root`, `power`, `log`, `ln`, `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `sinh`, `cosh`, `tanh`, `exp`
- **Last updated:** cycle 13

## src/operations/arithmetic.py
- **Purpose:** Pure arithmetic operation functions with no side effects.
- **Public API:**
  - `add(a, b)` → `a + b`
  - `subtract(a, b)` → `a - b`
  - `multiply(a, b)` → `a * b`
  - `divide(a, b)` → `a / b` (raises `ZeroDivisionError` natively if `b == 0`)
- **Key invariants:** No logging, no state. All functions are pure.
- **Last updated:** cycle 11

## src/operations/advanced.py
- **Purpose:** Pure advanced mathematical operation functions (power, roots, factorial, logarithms) with no side effects.
- **Imports:** `math`
- **Public API:**
  - `factorial(n)` → `math.factorial(n)` (raises `ValueError` for negative `n`)
  - `square(n)` → `n ** 2`
  - `cube(n)` → `n ** 3`
  - `square_root(n)` → `math.sqrt(n)` (raises `ValueError` for negative `n`)
  - `cube_root(n)` → `math.cbrt(n)` (handles negative inputs; requires Python 3.11+)
  - `power(base, exp)` → `base ** exp`
  - `log(n)` → `math.log10(n)` (raises `ValueError` for `n <= 0`)
  - `ln(n)` → `math.log(n)` (raises `ValueError` for `n <= 0`)
- **Key invariants:** No logging, no state. All functions are pure.
- **Last updated:** cycle 11

## src/operations/scientific.py
- **Purpose:** Pure scientific math operation functions (trigonometric, hyperbolic, exponential) with no side effects. All angle inputs/outputs in radians.
- **Imports:** `math`
- **Public API:**
  - `sin(x)` → `math.sin(x)`
  - `cos(x)` → `math.cos(x)`
  - `tan(x)` → `math.tan(x)`
  - `asin(x)` → `math.asin(x)` (raises `ValueError` for `|x| > 1`)
  - `acos(x)` → `math.acos(x)` (raises `ValueError` for `|x| > 1`)
  - `atan(x)` → `math.atan(x)`
  - `sinh(x)` → `math.sinh(x)`
  - `cosh(x)` → `math.cosh(x)`
  - `tanh(x)` → `math.tanh(x)`
  - `exp(x)` → `math.exp(x)`
- **Key invariants:** No logging, no state. All functions are pure.
- **Last updated:** cycle 13

## src/__main__.py
- **Purpose:** Interface layer for the Calculator: GUI (--gui), bash argv CLI mode, and interactive REPL with normal/scientific mode switching, with error logging.
- **Module-level docstring:** Present — documents GUI, CLI, and REPL usage modes with examples.
- **Imports from calculator:** `Calculator`, `BINARY_OPS`, `UNARY_OPS`, `SCIENTIFIC_UNARY_OPS`
- **Exports:** `parse_number(prompt, max_attempts)`, `run_operation(calc, op)`, `_format_result(value)`, `_show_history(calc)`, `cli_main(args)`, `main()`
- **Module-level constants:** `MAX_INPUT_ATTEMPTS`, `MENU`, `MENU_MAP`, `SCIENTIFIC_MENU`, `SCIENTIFIC_MENU_MAP`
- **Module-level:** `logger = logging.getLogger(__name__)` — logs caught errors at ERROR level.
- **Key invariants:**
  - `main()` checks `sys.argv[1] == "--gui"` first; if matched, lazily imports `src.gui.launch_gui` and calls it, then returns.
  - All other existing argv branches (CLI dispatch, REPL) are unaffected by the new `--gui` check.
  - `main()` tracks `mode` ("normal" or "scientific"). Pressing 'm' toggles mode and prints a confirmation. Normal mode uses MENU/MENU_MAP; scientific mode uses SCIENTIFIC_MENU/SCIENTIFIC_MENU_MAP.
  - `MENU_MAP` maps "1"–"12" to the 12 standard Calculator ops; unchanged.
  - `SCIENTIFIC_MENU_MAP` maps "1"–"10" to 10 scientific ops (sin, cos, tan, asin, acos, atan, sinh, cosh, tanh, exp).
  - Unknown REPL choice message mentions 'h', 'm', and 'q' as valid non-numeric choices (range differs by mode: 1-12 normal, 1-10 scientific).
  - `cli_main` uses `all_ops = UNARY_OPS | BINARY_OPS | SCIENTIFIC_UNARY_OPS` — scientific ops available without mode switching in CLI.
  - History is shared across normal and scientific mode operations within the same REPL session.
  - `run_operation` works for scientific ops (they're unary, so falls through to the single-operand path correctly).
- **Last updated:** cycle 14

## src/gui.py
- **Purpose:** Tkinter graphical interface for the Calculator. Exposes all 22 Calculator operations through a button-based layout. All computation is delegated to `Calculator.execute()` so history is recorded automatically.
- **Module-level docstring:** Present — documents launch methods.
- **Imports:** `import tkinter as tk`, `from tkinter import messagebox`, `from .calculator import Calculator, BINARY_OPS`
- **Module-level:** `logger = logging.getLogger(__name__)`
- **Visual design (cycle 15):** Modern dark iOS-inspired theme. Colour palette defined at top of `_build_ui`: black display (D_BG), charcoal window (BG=#1c1c1e), orange operators (C_OP=#ff9f0a), gray digits (C_DIGIT=#333333), dark-gray unary buttons (C_UNARY), light-gray C button with dark text, green Sci (C_CTL_SCI), blue Hist (C_CTL_HIST). Local `_btn()` helper applies `relief="flat"`, `borderwidth=0`, `cursor="hand2"`, and consistent padding to every button. Display font 36-bold, main button font 20-bold. `root.columnconfigure(weight=1, minsize=78)` distributes columns evenly; `root.minsize(320,560)`.
- **Public API:**
  - `CalculatorGUI(root)` — attaches calculator GUI to a `tk.Tk` root window
  - `CalculatorGUI.press_digit(digit)` — appends digit/decimal to `_current_input`; guards against double decimals and leading zeros
  - `CalculatorGUI.clear()` — resets `_current_input`, `_pending_op`, `_first_operand`; display shows "0"
  - `CalculatorGUI.set_binary_op(op)` — stores current input as `_first_operand`, sets `_pending_op`; no-op if input is empty
  - `CalculatorGUI.equals()` — executes `calc.execute(_pending_op, _first_operand, b)`; on error shows "Error" in display
  - `CalculatorGUI.execute_unary(op)` — executes `calc.execute(op, a)`; on error shows "Error" in display
  - `CalculatorGUI.toggle_mode()` — toggles `self.mode` between "normal" and "scientific"; shows/hides `sci_frame`
  - `CalculatorGUI.show_history()` — shows `messagebox.showinfo` with numbered history entries
  - `CalculatorGUI._format(value)` — static; whole floats shown as integers
  - `launch_gui()` — creates a `tk.Tk` root, attaches `CalculatorGUI`, calls `mainloop()`
- **Key invariants:**
  - `_current_input` stores the raw string being typed; `display_var` mirrors it for the label.
  - `_pending_op` and `_first_operand` are None when no binary op is in progress.
  - After `equals()` or `execute_unary()` succeeds, the result becomes the new `_current_input`.
  - On any error, display shows "Error", `_current_input` is cleared, but `_pending_op`/`_first_operand` may remain set.
  - Scientific panel (`sci_frame`) is hidden by default; `toggle_mode()` calls `grid()` or `grid_remove()` to show/hide it.
  - GUI and CLI/REPL interfaces share no state — each has its own `Calculator` instance.
- **Last updated:** cycle 15

## tests/test_main.py
- **Purpose:** Test suite for src/__main__.py (both interactive REPL and bash CLI mode), including scientific mode and the --gui flag.
- **Exports:** 96 test functions. Adds: `test_main_gui_flag_calls_launch_gui` — patches sys.argv=["prog","--gui"] and sys.modules["src.gui"] to verify launch_gui() is called.
- **Key invariants:** Imports `SCIENTIFIC_MENU_MAP` alongside other names. Scientific REPL tests patch sys.argv to ["prog"] and use 'm' as the first input to enter scientific mode.
- **Last updated:** cycle 14

## tests/test_gui.py
- **Purpose:** Test suite for src/gui.py (CalculatorGUI logic methods). tkinter is mocked via sys.modules injection so tests run headless without a display.
- **Exports:** 46 test functions covering: `_format` (4), `press_digit` (6), `clear` (4), `set_binary_op` (4), `equals` (8), `execute_unary` (10), `toggle_mode` (4), `show_history` (3), `main() --gui flag` (1).
- **Key invariants:**
  - `_FakeStringVar` substitute stores values in memory; `side_effect=_FakeStringVar` on mock StringVar gives independent instances per call.
  - `Frame.side_effect = lambda: MagicMock()` ensures display_frame and sci_frame are distinct mocks.
  - `monkeypatch.setitem(sys.modules, "tkinter", fake_tk)` before import prevents display errors.
  - toggle_mode tests compare `call_count` before/after to handle calls made during `_build_ui`.
- **Last updated:** cycle 14

## tests/test_calculator.py
- **Purpose:** Full test suite for Calculator class, including execute() dispatch, module-level constants, and scientific mode operations.
- **Current state:** 109 tests. Imports: `Calculator, BINARY_OPS, UNARY_OPS, INTEGER_OPS, SCIENTIFIC_UNARY_OPS, _to_int_if_needed`.
- **Exports:** existing 82 tests + `test_scientific_unary_ops_set` (1), scientific method tests: sin(2), cos(2), tan(2), asin(4), acos(4), atan(2), sinh(1), cosh(1), tanh(1), exp(2), execute scientific (3)
- **Last updated:** cycle 13
