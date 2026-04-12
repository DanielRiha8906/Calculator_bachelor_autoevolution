# Codebase Map

## src/__init__.py
- **Purpose:** Package initializer for the `src` module.
- **Exports:** `Calculator`
- **Key invariants:** Re-exports Calculator from `src.calculator` via `__all__`.
- **Last updated:** cycle 0

## src/calculator.py
- **Purpose:** Core arithmetic calculator class with per-instance operation history and error logging.
- **Module-level:** `logger = logging.getLogger(__name__)` — logs errors at ERROR level before re-raising.
- **Public API:**
  - `Calculator.__init__()` → initialises `self.history: list[dict]` to `[]`
  - `Calculator.get_history()` → returns a shallow copy of `self.history`
  - `Calculator.add(a, b)` → `a + b`
  - `Calculator.subtract(a, b)` → `a - b`
  - `Calculator.multiply(a, b)` → `a * b`
  - `Calculator.divide(a, b)` → `a / b` (logs and raises `ZeroDivisionError` if `b == 0`)
  - `Calculator.factorial(n)` → `math.factorial(n)` (logs and raises `ValueError` for negative `n`)
  - `Calculator.square(n)` → `n ** 2`
  - `Calculator.cube(n)` → `n ** 3`
  - `Calculator.square_root(n)` → `math.sqrt(n)` (logs and raises `ValueError` for negative `n`)
  - `Calculator.cube_root(n)` → `math.cbrt(n)` (handles negative inputs; requires Python 3.11+)
  - `Calculator.power(base, exp)` → `base ** exp`
  - `Calculator.log(n)` → `math.log10(n)` (logs and raises `ValueError` for `n <= 0`)
  - `Calculator.ln(n)` → `math.log(n)` (logs and raises `ValueError` for `n <= 0`)
- **Key invariants:** History is appended by `run_operation` (not by Calculator methods themselves). Each history entry is `{"op": str, "operands": tuple, "result": float|int}`. Failed operations are not recorded. `get_history()` returns a copy — callers cannot mutate internal state. Each Calculator instance has its own independent history. Error-logging methods log before re-raising — exceptions still propagate unchanged.
- **Last updated:** cycle 9

## src/__main__.py
- **Purpose:** Dual-mode CLI for the Calculator: bash argv mode and interactive REPL, with error logging.
- **Exports:** `parse_number(prompt, max_attempts)`, `_to_int_if_needed(op, value)`, `run_operation(calc, op)`, `_format_result(value)`, `_show_history(calc)`, `cli_main(args)`, `main()`
- **Module-level constants:** `UNARY_OPS`, `BINARY_OPS`, `INTEGER_OPS`, `MAX_INPUT_ATTEMPTS`, `MENU`, `MENU_MAP`
- **Module-level:** `logger = logging.getLogger(__name__)` — logs caught errors at ERROR level.
- **Key invariants:**
  - `main()` calls `logging.basicConfig(level=ERROR, format=...)` before dispatch so errors surface at runtime.
  - `main()` checks `sys.argv`: if `len(sys.argv) > 1`, calls `cli_main(sys.argv[1:])` and `sys.exit(rc)`; otherwise starts the interactive REPL.
  - `cli_main(args)` parses `[operation, *operands]`, validates arg count, runs the operation, prints `_format_result(result)`, returns 0 on success / 1 on error. Logs errors via `logger.error` before printing.
  - `_format_result(value)` converts whole floats to integer strings (7.0 → "7"); fractional floats and ints pass through as-is.
  - `MENU_MAP` maps strings "1"–"12" to the 12 Calculator method names; "h" shows history; "q" quits.
  - `MENU` string now includes "h. history" option.
  - `parse_number(prompt, max_attempts=MAX_INPUT_ATTEMPTS)` prompts for a valid float up to `max_attempts` times; prints remaining-attempts feedback on each invalid entry; raises `ValueError` after all attempts are exhausted.
  - `MAX_INPUT_ATTEMPTS = 3` is the module-level default for retry limit.
  - `run_operation` catches `ValueError` and `ZeroDivisionError`, logs them via `logger.error`, and prints "Error: …" without crashing the REPL loop. On success, appends `{"op", "operands", "result"}` to `calc.history`.
  - `INTEGER_OPS = {"factorial"}`: inputs for these ops are converted float→int before dispatch; non-whole numbers raise `ValueError`.
  - `_show_history(calc)` prints numbered history entries in `op(operands) = result` format, or "No history yet." if empty.
  - Unknown REPL choice message now mentions 'h' and 'q' as valid non-numeric choices.
- **Last updated:** cycle 9

## tests/test_main.py
- **Purpose:** Test suite for src/__main__.py (both interactive REPL and bash CLI mode).
- **Exports:** 75 test functions covering: parse_number (valid int/float/negative/retry/exhausted retries/remaining-count message), run_operation for all 12 operations + error paths (including too-many-invalid-inputs) + history recording (binary, unary, error-not-recorded, accumulation), MENU_MAP completeness, _format_result (whole float, fractional, int), _show_history (empty, with entries), cli_main for all 12 operations + error paths (unknown op, wrong arg count, invalid number, domain errors), main dispatch (interactive REPL with sys.argv patched to ["prog"], CLI dispatch via sys.argv with 2+ args, 'h' choice shows history), and logging (run_operation logs divide-by-zero and invalid-input errors; cli_main logs divide-by-zero and factorial-negative errors via caplog).
- **Key invariants:** Uses `unittest.mock.patch("builtins.input", ...)` for REPL tests; uses `patch("sys.argv", ...)` for all `main()` tests to control REPL vs. CLI dispatch; uses `capsys` to capture stdout; uses `caplog` fixture to assert log records; imports `MAX_INPUT_ATTEMPTS` and `_show_history` alongside other names.
- **Last updated:** cycle 9

## tests/test_calculator.py
- **Purpose:** Full test suite for Calculator class.
- **Current state:** 67 tests covering all 12 operations, history, and error logging. Tests all previous operations plus 5 new logging tests: `test_divide_by_zero_logs_error`, `test_factorial_negative_logs_error`, `test_square_root_negative_logs_error`, `test_log_non_positive_logs_error`, `test_ln_non_positive_logs_error`. All use `caplog` fixture with `caplog.at_level(logging.ERROR, logger="src.calculator")`.
- **Exports:** `test_add_*` (5), `test_subtract_*` (5), `test_multiply_*` (6), `test_divide_*` (7), `test_factorial_*` (5), `test_square_*` (4), `test_cube_*` (4), `test_square_root_*` (4), `test_cube_root_*` (4), `test_power_*` (4), `test_log_*` (5), `test_ln_*` (5), `test_history_*` (4), logging tests (5)
- **Last updated:** cycle 9
