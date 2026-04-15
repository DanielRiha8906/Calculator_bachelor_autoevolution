# Codebase Map

Per-file summaries: purpose, public API surface, key invariants.

---

## src/__init__.py
- **Purpose:** Python package initializer for `src/`. Has module docstring describing the package and CLI usage.
- **Last updated:** cycle 12
- **Exports:** `Calculator` (re-exported from `src.calculator`)
- **Invariants:** Must always export `Calculator` so external imports work.

---

## src/calculator.py
- **Purpose:** Defines the `Calculator` class — the core computation unit. Delegates to `src.operations.basic` and `src.operations.scientific` for all computation logic.
- **Last updated:** cycle 12
- **Public API:**
  - `Calculator.add(a, b)` → delegates to `operations.basic.add`
  - `Calculator.subtract(a, b)` → delegates to `operations.basic.subtract`
  - `Calculator.multiply(a, b)` → delegates to `operations.basic.multiply`
  - `Calculator.divide(a, b)` → delegates to `operations.basic.divide`; raises `ValueError("Division by zero is not allowed")` when `b == 0`
  - `Calculator.factorial(n: int) -> int` → delegates to `operations.scientific.factorial`; raises `ValueError` for negative `n` or non-integer `n`
  - `Calculator.square(a)` → delegates to `operations.scientific.square`
  - `Calculator.cube(a)` → delegates to `operations.scientific.cube`
  - `Calculator.square_root(a)` → delegates to `operations.scientific.square_root`; raises `ValueError` for `a < 0`
  - `Calculator.cube_root(a)` → delegates to `operations.scientific.cube_root`; supports negative input
  - `Calculator.power(a, b)` → delegates to `operations.scientific.power`
  - `Calculator.log(a, base)` → delegates to `operations.scientific.log`; raises `ValueError` for `a <= 0` or `base <= 0` or `base == 1`
  - `Calculator.ln(a)` → delegates to `operations.scientific.ln`; raises `ValueError` for `a <= 0`
  - `Calculator.execute(operation: str, *args)` → dispatches to the named method by `getattr`; raises `ValueError` for unknown or non-callable names.
- **Invariants:** No state — all methods are pure delegates. Imports from `src.operations.basic` and `src.operations.scientific`.

---

## src/operations/__init__.py
- **Purpose:** Package init for the operations sub-package.
- **Last updated:** cycle 11
- **Exports:** Nothing (docstring only, modules are imported directly).

---

## src/operations/basic.py
- **Purpose:** Pure arithmetic operation functions: add, subtract, multiply, divide.
- **Last updated:** cycle 11
- **Public API:**
  - `add(a, b)` → `a + b`
  - `subtract(a, b)` → `a - b`
  - `multiply(a, b)` → `a * b`
  - `divide(a, b)` → `a / b`; raises `ValueError("Division by zero is not allowed")` when `b == 0`
- **Invariants:** No state, no imports except built-ins. All functions are pure.

---

## src/operations/scientific.py
- **Purpose:** Pure scientific operation functions: factorial, square, cube, square_root, cube_root, power, log, ln.
- **Last updated:** cycle 11
- **Public API:**
  - `factorial(n: int) -> int` → `n!`; raises `ValueError` for non-integer `n` or negative `n`
  - `square(a)` → `a ** 2`
  - `cube(a)` → `a ** 3`
  - `square_root(a)` → `math.sqrt(a)`; raises `ValueError` for `a < 0`
  - `cube_root(a)` → real cube root; supports negative input via sign-preserving idiom
  - `power(a, b)` → `a ** b`
  - `log(a, base)` → `math.log(a, base)`; raises `ValueError` for `a <= 0` or `base <= 0` or `base == 1`
  - `ln(a)` → `math.log(a)`; raises `ValueError` for `a <= 0`
- **Invariants:** Imports `math` at module level. All functions are pure and stateless.

---

## src/interface/__init__.py
- **Purpose:** Package init for the interface sub-package.
- **Last updated:** cycle 11
- **Exports:** Nothing (docstring only).

---

## src/interface/history.py
- **Purpose:** Session history and error-log file helpers. Owns all file-I/O for history and error logging.
- **Last updated:** cycle 11
- **Public API:**
  - `HISTORY_FILE = "history.txt"` — default history path (patchable in tests via None-sentinel pattern)
  - `ERROR_LOG_FILE = "error.log"` — default error log path (patchable in tests)
  - `clear_history(filepath=None)` — truncate/create history file
  - `append_to_history(entry, filepath=None)` — append one line to history
  - `show_history(filepath=None)` — print all history entries to stdout
  - `append_to_error_log(message, filepath=None)` — append timestamped line to error log
- **Invariants:** All functions use the None-sentinel pattern for the `filepath` parameter so tests can monkeypatch `HISTORY_FILE` and `ERROR_LOG_FILE`. Tests must patch `src.interface.history.HISTORY_FILE` and `src.interface.history.ERROR_LOG_FILE` (not `src.__main__`).

---

## src/interface/interactive.py
- **Purpose:** Interactive menu-driven mode components. Owns all user-facing input and output for the interactive loop.
- **Last updated:** cycle 11
- **Public API / Exports:**
  - `TooManyAttemptsError` — custom exception raised after MAX_ATTEMPTS invalid inputs
  - `MAX_ATTEMPTS = 3`
  - `OPERATIONS` — dict mapping menu keys `"1"`–`"12"` to operation names
  - `_ONE_ARG_OPS`, `_INT_ARG_OPS`, `_TWO_ARG_OPS`, `_ALL_OPS` — arity grouping sets
  - `_OP_PROMPTS` — dict mapping operation name → tuple of prompt strings
  - `show_menu()` — print the numbered operation menu
  - `parse_number(prompt, max_attempts)` — prompt for float with retry; raises `TooManyAttemptsError`
  - `parse_int(prompt, max_attempts)` — prompt for int with retry; raises `TooManyAttemptsError`
  - `run_operation(calc, operation)` — collect inputs, delegate to `calc.execute`, return history entry or None
- **Invariants:** Imports `append_to_error_log` from `.history` (not from `__main__`). `parse_number`/`parse_int` log invalid inputs via `append_to_error_log`.

---

## src/interface/cli.py
- **Purpose:** Non-interactive CLI mode. Parses command-line arguments and executes a single operation.
- **Last updated:** cycle 11
- **Public API:**
  - `cli_mode(args: list[str]) -> int` — parses args, validates arity/types, calls `Calculator.execute`, prints result; returns 0 on success, 1 on error
- **Invariants:** Uses arity sets from `src.interface.interactive`. Errors go to stderr; result goes to stdout. Imports `append_to_error_log` from `.history`.

---

## src/__main__.py
- **Purpose:** CLI entry point — `main()` function + re-exports from sub-modules for backward compatibility.
- **Last updated:** cycle 11
- **Exports (re-exported from sub-modules):**
  - `HISTORY_FILE`, `ERROR_LOG_FILE` from `src.interface.history`
  - `clear_history`, `append_to_history`, `show_history`, `append_to_error_log` from `src.interface.history`
  - `MAX_ATTEMPTS`, `OPERATIONS`, `TooManyAttemptsError` from `src.interface.interactive`
  - `show_menu`, `parse_number`, `parse_int`, `run_operation` from `src.interface.interactive`
  - `cli_mode` from `src.interface.cli`
- **Defined here:** `main(args=None)` — dispatches to CLI mode or starts the interactive loop.
- **Invariants:** Re-exports allow old `from src.__main__ import X` statements to continue working. However, monkeypatching `HISTORY_FILE`/`ERROR_LOG_FILE` must target `src.interface.history`, not `src.__main__`.
- **CLI mode usage:** `python -m src <operation> <value> [<value2>]`
- **Interactive mode:** `python -m src` (no args)

---

## tests/test_calculator.py
- **Purpose:** Unit test suite for `Calculator` — full coverage of all twelve operations plus the execute dispatch method.
- **Last updated:** cycle 10
- **Tests (68 total):**
  - **add (5):** positive numbers, negative numbers, mixed sign, zero identity, floats
  - **subtract (6):** positive numbers, negative numbers, mixed sign, zero, floats, same-number-gives-zero
  - **multiply (6):** positive numbers, negative numbers, mixed sign, zero, identity (×1), floats
  - **divide (7):** divide-by-zero `ValueError`, normal, negative denominator, negative numerator, both negative, floats, fractional result
  - **factorial (6):** zero, one, small (5!), large (10!), negative raises `ValueError`, float raises `ValueError`
  - **square (4):** positive, negative, zero, float
  - **cube (4):** positive, negative, zero, float
  - **square_root (4):** positive, zero, float, negative raises `ValueError`
  - **cube_root (4):** positive, negative, zero, float
  - **power (5):** positive exponent, zero exponent, one exponent, negative exponent, float base
  - **log (7):** base 10, base 2, base e, non-positive `a` raises, negative `a` raises, base==1 raises, base==0 raises
  - **ln (5):** ln(e)==1, ln(1)==0, ln(e³)==3, zero raises `ValueError`, negative raises `ValueError`
  - **execute (5):** two-arg dispatch, one-arg dispatch, int-arg dispatch, ValueError propagation, unknown-op raises ValueError
- **Invariants:** Must import from `src.calculator`, not from the package root; uses `math.isclose` for float comparisons.

---

## tests/test_main.py
- **Purpose:** Unit tests for the interactive CLI and cli_mode — 84 tests with mocked input.
- **Last updated:** cycle 11
- **Key change from cycle 10:** `autouse` fixture `isolate_files` now monkeypatches `src.interface.history.HISTORY_FILE` and `src.interface.history.ERROR_LOG_FILE` (not `src.__main__`). All inline monkeypatching in individual tests also targets `src.interface.history`.
- **Tests (84 total):** Same test count and coverage as cycle 10. No tests added or removed.
- **Invariants:** Tests import `src.interface.history as _history_mod` for monkeypatching. All other imports remain via `src.__main__` re-exports. Interactive tests call `main([])` to bypass sys.argv; cli_mode tests call `cli_mode([...])` directly.
