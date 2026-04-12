# Codebase Map

Per-file summaries: purpose, public API surface, key invariants.

---

## src/__init__.py
- **Purpose:** Python package initializer for `src/`.
- **Exports:** `Calculator` (re-exported from `src.calculator`)
- **Invariants:** Must always export `Calculator` so external imports work.

---

## src/calculator.py
- **Purpose:** Defines the `Calculator` class — the core computation unit.
- **Last updated:** cycle 4
- **Public API:**
  - `Calculator.add(a, b)` → `a + b`
  - `Calculator.subtract(a, b)` → `a - b`
  - `Calculator.multiply(a, b)` → `a * b`
  - `Calculator.divide(a, b)` → `a / b`; raises `ValueError("Division by zero is not allowed")` when `b == 0`
  - `Calculator.factorial(n: int) -> int` → `n!`; raises `ValueError` for negative `n` or non-integer `n`
  - `Calculator.square(a)` → `a ** 2`
  - `Calculator.cube(a)` → `a ** 3`
  - `Calculator.square_root(a)` → `math.sqrt(a)`; raises `ValueError` for `a < 0`
  - `Calculator.cube_root(a)` → real cube root; supports negative input via sign-preserving `(-abs(a))**(1/3)` trick
  - `Calculator.power(a, b)` → `a ** b`
  - `Calculator.log(a, base)` → `math.log(a, base)`; raises `ValueError` for `a <= 0` or `base <= 0` or `base == 1`
  - `Calculator.ln(a)` → `math.log(a)`; raises `ValueError` for `a <= 0`
- **Invariants:** No state — all methods are pure functions of their arguments. Imports `math` at module level.

---

## src/__main__.py
- **Purpose:** CLI entry point — supports both interactive menu-driven mode and non-interactive single-operation mode (via command-line arguments).
- **Last updated:** cycle 6
- **Exports:** `main(args=None)`, `cli_mode(args)`, `show_menu()`, `parse_number(prompt)`, `parse_int(prompt)`, `run_operation(calc, operation)`, `OPERATIONS` dict, `_ONE_ARG_OPS`, `_INT_ARG_OPS`, `_TWO_ARG_OPS`, `_ALL_OPS`.
- **Key constants:**
  - `OPERATIONS` maps menu keys `"1"`–`"12"` to operation names.
  - `_ONE_ARG_OPS` — `{square, cube, square_root, cube_root, ln}` (one float arg).
  - `_INT_ARG_OPS` — `{factorial}` (one int arg).
  - `_TWO_ARG_OPS` — `{add, subtract, multiply, divide, power, log}` (two float args).
- **CLI mode usage:** `python -m src <operation> <value> [<value2>]` — parses via `argparse`, prints result to stdout, returns 0 on success / 1 on error (errors go to stderr).
- **Interactive mode:** `python -m src` (no args) — presents a numbered menu, loops until user enters `"q"`.
- **Dispatch:** `main(args=None)` — if `args` is `None`, uses `sys.argv[1:]`; if non-empty, delegates to `cli_mode(args)` and exits. Passing `args=[]` forces interactive mode (used by tests).
- **Invariants:** `cli_mode` validates argument count per operation and catches `ValueError` from Calculator. `run_operation` catches `ValueError` and prints to stdout (interactive error display).

---

## tests/test_main.py
- **Purpose:** Unit tests for the interactive CLI and cli_mode in `src/__main__.py` using mocked `input()` and `capsys`.
- **Last updated:** cycle 6
- **Tests (48 total):**
  - **show_menu (1):** verifies all operation names and "q" appear in output.
  - **parse_number (4):** valid int, valid float, negative, retry-on-invalid-then-accept.
  - **parse_int (2):** valid int, retry-on-float-string-then-accept.
  - **run_operation (16):** one test per operation (add, subtract, multiply, divide, power, log, factorial, square, cube, square_root, cube_root, ln); plus error tests for divide-by-zero, factorial-negative, square_root-negative, and unknown-operation.
  - **main interactive (5):** quit immediately, invalid-choice-then-quit, add-then-quit, two-operations-then-quit, error-then-continue. All call `main([])` to force interactive mode.
  - **cli_mode (20):** happy-path test for all 12 operations; error tests for divide-by-zero, factorial-negative, square_root-negative; wrong-arg-count tests for two-arg and one-arg ops; unknown-operation SystemExit; main() dispatch integration test.
- **Invariants:** Interactive tests call `main([])` to bypass sys.argv; cli_mode tests call `cli_mode([...])` directly. Errors in cli_mode go to stderr; result goes to stdout.

---

## tests/test_calculator.py
- **Purpose:** Unit test suite for `Calculator` — full coverage of all twelve operations.
- **Last updated:** cycle 4
- **Tests (63 total):**
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
- **Invariants:** Must import from `src.calculator`, not from the package root; uses `math.isclose` for float comparisons.
