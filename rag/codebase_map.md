# Codebase Map

## src/__init__.py
- **Purpose:** Package initializer for the `src` module; re-exports Calculator.
- **Exports:** `Calculator`
- **Key invariants:** Re-exports Calculator from `src.calculator` via `__all__`. Has a module-level docstring describing the package purpose.
- **Last updated:** cycle 12

## src/calculator.py
- **Purpose:** Core calculator facade: per-instance history, error logging, and operation dispatch; delegates operation implementations to the `src.operations` sub-package.
- **Imports:** `from .operations import arithmetic, advanced`
- **Module-level docstring:** Present — describes module role and cross-cutting concerns.
- **Module-level constants:** `UNARY_OPS`, `BINARY_OPS`, `INTEGER_OPS` — sets classifying all 12 operations by arity and type requirements.
- **Module-level helpers:** `_to_int_if_needed(op, value)` — coerces value to int for INTEGER_OPS, raises ValueError for non-whole numbers.
- **Module-level:** `logger = logging.getLogger(__name__)` — logs errors at ERROR level before re-raising.
- **Public API:**
  - `Calculator.__init__()` → initialises `self.history: list[dict]` to `[]`; has docstring
  - `Calculator.get_history()` → returns a shallow copy of `self.history`
  - `Calculator.add(a, b)` → delegates to `arithmetic.add`; has docstring
  - `Calculator.subtract(a, b)` → delegates to `arithmetic.subtract`; has docstring
  - `Calculator.multiply(a, b)` → delegates to `arithmetic.multiply`; has docstring
  - `Calculator.divide(a, b)` → delegates to `arithmetic.divide` (logs and raises `ZeroDivisionError` if `b == 0`); has docstring
  - `Calculator.factorial(n)` → delegates to `advanced.factorial` (logs and raises `ValueError` for negative `n`); has docstring
  - `Calculator.square(n)` → delegates to `advanced.square`; has docstring
  - `Calculator.cube(n)` → delegates to `advanced.cube`; has docstring
  - `Calculator.square_root(n)` → delegates to `advanced.square_root` (logs and raises `ValueError` for negative `n`); has docstring
  - `Calculator.cube_root(n)` → delegates to `advanced.cube_root` (handles negative inputs; requires Python 3.11+); has docstring
  - `Calculator.power(base, exp)` → delegates to `advanced.power`; has docstring
  - `Calculator.log(n)` → delegates to `advanced.log` (logs and raises `ValueError` for `n <= 0`); has docstring
  - `Calculator.ln(n)` → delegates to `advanced.ln` (logs and raises `ValueError` for `n <= 0`); has docstring
  - `Calculator.execute(op, *operands)` → dispatches by op name, applies _to_int_if_needed for INTEGER_OPS, records history on success, propagates exceptions unchanged; raises ValueError for unknown ops.
- **Key invariants:** History is recorded by `execute()`, not by individual Calculator methods. Each history entry is `{"op": str, "operands": tuple, "result": float|int}`. Failed operations are not recorded. `get_history()` returns a copy — callers cannot mutate internal state. Each Calculator instance has its own independent history. Error-logging methods log before re-raising — exceptions still propagate unchanged. Operation functions in sub-modules are pure (no logging/history side effects).
- **Last updated:** cycle 12

## src/operations/__init__.py
- **Purpose:** Operations sub-package initializer; re-exports all arithmetic and advanced operation functions for convenience.
- **Exports:** `add`, `subtract`, `multiply`, `divide`, `factorial`, `square`, `cube`, `square_root`, `cube_root`, `power`, `log`, `ln`
- **Last updated:** cycle 11

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
- **Purpose:** Placeholder stub module for future scientific calculator mode operations (trigonometric, hyperbolic, etc.). Currently empty.
- **Public API:** None yet.
- **Last updated:** cycle 11

## src/__main__.py
- **Purpose:** Pure interface layer for the Calculator: bash argv mode and interactive REPL, with error logging. Operation classification and dispatch logic now live in calculator.py.
- **Module-level docstring:** Present — documents both CLI and REPL usage modes with examples.
- **Imports from calculator:** `Calculator`, `BINARY_OPS`, `UNARY_OPS`
- **Exports:** `parse_number(prompt, max_attempts)`, `run_operation(calc, op)`, `_format_result(value)`, `_show_history(calc)`, `cli_main(args)`, `main()`
- **Module-level constants:** `MAX_INPUT_ATTEMPTS`, `MENU`, `MENU_MAP`
- **Module-level:** `logger = logging.getLogger(__name__)` — logs caught errors at ERROR level.
- **Key invariants:**
  - `main()` calls `logging.basicConfig(level=ERROR, format=...)` before dispatch so errors surface at runtime. Has docstring.
  - `main()` checks `sys.argv`: if `len(sys.argv) > 1`, calls `cli_main(sys.argv[1:])` and `sys.exit(rc)`; otherwise starts the interactive REPL.
  - `cli_main(args)` parses `[operation, *operands]`, validates arg count, calls `calc.execute(op, ...)`, prints `_format_result(result)`, returns 0 on success / 1 on error. Logs errors via `logger.error` before printing.
  - `_format_result(value)` converts whole floats to integer strings (7.0 → "7"); fractional floats and ints pass through as-is.
  - `MENU_MAP` maps strings "1"–"12" to the 12 Calculator method names; "h" shows history; "q" quits.
  - `MENU` string includes "h. history" option.
  - `parse_number(prompt, max_attempts=MAX_INPUT_ATTEMPTS)` prompts for a valid float up to `max_attempts` times; prints remaining-attempts feedback on each invalid entry; raises `ValueError` after all attempts are exhausted.
  - `MAX_INPUT_ATTEMPTS = 3` is the module-level default for retry limit.
  - `run_operation` calls `calc.execute(op, ...)` (which handles type coercion and history recording); catches `ValueError` and `ZeroDivisionError`, logs them via `logger.error`, and prints "Error: …" without crashing the REPL loop.
  - `_show_history(calc)` prints numbered history entries in `op(operands) = result` format, or "No history yet." if empty.
  - Unknown REPL choice message mentions 'h' and 'q' as valid non-numeric choices.
- **Last updated:** cycle 12

## tests/test_main.py
- **Purpose:** Test suite for src/__main__.py (both interactive REPL and bash CLI mode).
- **Exports:** 75 test functions covering: parse_number (valid int/float/negative/retry/exhausted retries/remaining-count message), run_operation for all 12 operations + error paths (including too-many-invalid-inputs) + history recording (binary, unary, error-not-recorded, accumulation), MENU_MAP completeness, _format_result (whole float, fractional, int), _show_history (empty, with entries), cli_main for all 12 operations + error paths (unknown op, wrong arg count, invalid number, domain errors), main dispatch (interactive REPL with sys.argv patched to ["prog"], CLI dispatch via sys.argv with 2+ args, 'h' choice shows history), and logging (run_operation logs divide-by-zero and invalid-input errors; cli_main logs divide-by-zero and factorial-negative errors via caplog).
- **Key invariants:** Uses `unittest.mock.patch("builtins.input", ...)` for REPL tests; uses `patch("sys.argv", ...)` for all `main()` tests to control REPL vs. CLI dispatch; uses `capsys` to capture stdout; uses `caplog` fixture to assert log records; imports `MAX_INPUT_ATTEMPTS` and `_show_history` alongside other names.
- **Last updated:** cycle 9

## tests/test_calculator.py
- **Purpose:** Full test suite for Calculator class, including execute() dispatch and module-level constants.
- **Current state:** 82 tests covering all 12 operations, history, error logging, execute() dispatch, and module-level constants/helpers. Imports: `Calculator, BINARY_OPS, UNARY_OPS, INTEGER_OPS, _to_int_if_needed`.
- **Exports:** `test_add_*` (5), `test_subtract_*` (5), `test_multiply_*` (6), `test_divide_*` (7), `test_factorial_*` (5), `test_square_*` (4), `test_cube_*` (4), `test_square_root_*` (4), `test_cube_root_*` (4), `test_power_*` (4), `test_log_*` (5), `test_ln_*` (5), `test_history_*` (4), logging tests (5), `test_execute_*` (9), constants/helper tests (6)
- **Last updated:** cycle 10
