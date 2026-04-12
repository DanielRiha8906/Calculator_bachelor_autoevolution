# Codebase Map

## src/__init__.py
- **Purpose:** Package initializer for the `src` module.
- **Exports:** `Calculator`
- **Key invariants:** Re-exports Calculator from `src.calculator` via `__all__`.
- **Last updated:** cycle 0

## src/calculator.py
- **Purpose:** Core arithmetic calculator class.
- **Public API:**
  - `Calculator.add(a, b)` → `a + b`
  - `Calculator.subtract(a, b)` → `a - b`
  - `Calculator.multiply(a, b)` → `a * b`
  - `Calculator.divide(a, b)` → `a / b` (raises `ZeroDivisionError` if `b == 0`, Python built-in behavior)
  - `Calculator.factorial(n)` → `math.factorial(n)` (raises `ValueError` for negative `n`)
  - `Calculator.square(n)` → `n ** 2`
  - `Calculator.cube(n)` → `n ** 3`
  - `Calculator.square_root(n)` → `math.sqrt(n)` (raises `ValueError` for negative `n`)
  - `Calculator.cube_root(n)` → `math.cbrt(n)` (handles negative inputs; requires Python 3.11+)
  - `Calculator.power(base, exp)` → `base ** exp`
  - `Calculator.log(n)` → `math.log10(n)` (raises `ValueError` for `n <= 0`)
  - `Calculator.ln(n)` → `math.log(n)` (raises `ValueError` for `n <= 0`)
- **Key invariants:** No input validation except where delegated to stdlib. `divide` raises `ZeroDivisionError` on zero divisor; `factorial` raises `ValueError` for negative inputs; `square_root`, `log`, `ln` raise `ValueError` for invalid domain inputs.
- **Last updated:** cycle 4

## src/__main__.py
- **Purpose:** Dual-mode CLI for the Calculator: bash argv mode and interactive REPL.
- **Exports:** `parse_number(prompt)`, `_to_int_if_needed(op, value)`, `run_operation(calc, op)`, `_format_result(value)`, `cli_main(args)`, `main()`
- **Module-level constants:** `UNARY_OPS`, `BINARY_OPS`, `INTEGER_OPS`, `MENU`, `MENU_MAP`
- **Key invariants:**
  - `main()` checks `sys.argv`: if `len(sys.argv) > 1`, calls `cli_main(sys.argv[1:])` and `sys.exit(rc)`; otherwise starts the interactive REPL.
  - `cli_main(args)` parses `[operation, *operands]`, validates arg count, runs the operation, prints `_format_result(result)`, returns 0 on success / 1 on error.
  - `_format_result(value)` converts whole floats to integer strings (7.0 → "7"); fractional floats and ints pass through as-is.
  - `MENU_MAP` maps strings "1"–"12" to the 12 Calculator method names; "q" quits.
  - `parse_number` loops until the user enters a valid float; never raises.
  - `run_operation` catches `ValueError` and `ZeroDivisionError` and prints "Error: …" without crashing the REPL loop.
  - `INTEGER_OPS = {"factorial"}`: inputs for these ops are converted float→int before dispatch; non-whole numbers raise `ValueError`.
- **Last updated:** cycle 6

## tests/test_main.py
- **Purpose:** Test suite for src/__main__.py (both interactive REPL and bash CLI mode).
- **Exports:** 52 test functions covering: parse_number (valid int/float/negative/retry), MENU_MAP completeness, run_operation for all 12 operations + error paths, _format_result (whole float, fractional, int), cli_main for all 12 operations + error paths (unknown op, wrong arg count, invalid number, domain errors), and main dispatch (interactive REPL with sys.argv patched to ["prog"], CLI dispatch via sys.argv with 2+ args).
- **Key invariants:** Uses `unittest.mock.patch("builtins.input", ...)` for REPL tests; uses `patch("sys.argv", ...)` for all `main()` tests to control REPL vs. CLI dispatch; uses `capsys` to capture stdout.
- **Last updated:** cycle 6

## tests/test_calculator.py
- **Purpose:** Full test suite for Calculator class.
- **Current state:** 58 tests covering all 12 operations — add, subtract, multiply, divide, factorial, square, cube, square_root, cube_root, power, log, ln — with positive, negative, mixed-sign, zero, float, and boundary inputs. Includes `test_divide_by_zero_raises` (ZeroDivisionError), `test_factorial_negative_raises` (ValueError), `test_square_root_negative_raises` (ValueError), `test_log_non_positive_raises`, `test_log_negative_raises`, `test_ln_non_positive_raises`, `test_ln_negative_raises` (all ValueError).
- **Exports:** `test_add_*` (5), `test_subtract_*` (5), `test_multiply_*` (6), `test_divide_*` (7), `test_factorial_*` (5), `test_square_*` (4), `test_cube_*` (4), `test_square_root_*` (4), `test_cube_root_*` (4), `test_power_*` (4), `test_log_*` (5), `test_ln_*` (5)
- **Last updated:** cycle 4
