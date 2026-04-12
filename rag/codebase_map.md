# Codebase Map

Per-file summaries: purpose, public API surface, key invariants.

---

## `src/__init__.py`
- **Purpose:** Package initializer for the `src` package.
- **Exports:** `Calculator`
- **Invariants:** Re-exports `Calculator` from `calculator.py`; no logic of its own.
- **Last updated:** cycle 0

---

## `src/__main__.py`
- **Purpose:** Interactive CLI entry point for the Calculator.
- **Exports:** `main()`, `display_menu()`, `get_number()`, `OPERATIONS`
- **Public API:**
  - `OPERATIONS: dict[str, tuple[str, int]]` — maps menu key to `(operation_name, arity)`; covers all 12 operations
  - `display_menu() -> None` — prints the numbered operation menu
  - `get_number(prompt, require_int=False) -> int | float` — reads one number from stdin; raises `ValueError` for non-numeric or (when `require_int=True`) non-integer input
  - `main() -> None` — runs the interactive session loop until the user enters 'q'
- **Invariants:**
  - Unary operations (factorial, square, cube, square_root, cube_root, log, ln) prompt for one operand; factorial uses `require_int=True`.
  - Binary operations (add, subtract, multiply, divide, power) prompt for two operands.
  - `ValueError`, `TypeError`, and `ZeroDivisionError` from operations or input parsing are caught and printed as "Error: <msg>"; the session continues.
  - Unknown menu keys print a warning; the loop continues without consuming extra input.
- **Last updated:** cycle 5 (issue-222)

---

## `src/calculator.py`
- **Purpose:** Core arithmetic calculator implementation.
- **Public API:**
  - `Calculator.add(a, b) -> float/int` — returns `a + b`
  - `Calculator.subtract(a, b) -> float/int` — returns `a - b`
  - `Calculator.multiply(a, b) -> float/int` — returns `a * b`
  - `Calculator.divide(a, b) -> float/int` — returns `a / b`; raises `ZeroDivisionError` naturally when `b == 0`
  - `Calculator.factorial(n: int) -> int` — returns `n!`; raises `TypeError` for non-integers (including bool/float), raises `ValueError` for negative integers
  - `Calculator.square(x) -> float` — returns `x * x`
  - `Calculator.cube(x) -> float` — returns `x * x * x`
  - `Calculator.square_root(x) -> float` — returns `math.sqrt(x)`; raises `ValueError` for `x < 0`
  - `Calculator.cube_root(x) -> float` — returns real cube root (negative for negative x); uses `-(abs(x)**(1/3))` for negatives
  - `Calculator.power(base, exp) -> float` — returns `base ** exp`
  - `Calculator.log(x) -> float` — returns `math.log10(x)`; raises `ValueError` for `x <= 0`
  - `Calculator.ln(x) -> float` — returns `math.log(x)`; raises `ValueError` for `x <= 0`
- **Key invariants:**
  - Division delegates directly to Python `/` operator; no explicit zero-check.
  - `ZeroDivisionError` is raised by Python runtime when dividing by zero.
  - Factorial validates input type explicitly: booleans are rejected (`isinstance(n, bool)` checked before `isinstance(n, int)` since `bool` is a subclass of `int`).
  - Factorial is computed iteratively; `factorial(0)` and `factorial(1)` both return 1.
  - `square_root` raises `ValueError` for negative inputs (not `math.sqrt`'s `ValueError`; explicit guard for clear messaging).
  - `cube_root` handles negative inputs by computing `-(abs(x)**(1/3))` to stay in real domain.
  - `log` and `ln` raise `ValueError` for `x <= 0` with explicit guard before delegating to `math`.
  - Module imports `math` at the top.
- **Last updated:** cycle 4 (issue-219)

---

## `tests/test_calculator.py`
- **Purpose:** Comprehensive unit test suite for `Calculator`.
- **Current state:** 76 tests covering all twelve operations. Includes normal inputs, edge cases (zero operands, negative values, large numbers), floating-point precision via `pytest.approx`, `ZeroDivisionError` for divide, factorial boundary/rejection, `ValueError` for square_root (negative), log/ln (non-positive), and cube_root negative-input correctness. Uses a `calc` pytest fixture.
- **Exports:** None
- **Last updated:** cycle 4 (issue-219)

---

## `tests/test_main.py`
- **Purpose:** Unit tests for the interactive CLI in `src/__main__.py`.
- **Current state:** 32 tests covering: OPERATIONS mapping invariants (all 12 ops present, correct arities), `get_number` parsing (int, float, require_int, invalid input), quit behaviour (immediate and case-insensitive), all 12 operations end-to-end through mocked stdin/stdout, error paths (divide-by-zero, sqrt negative, log/ln non-positive, factorial negative/float, non-numeric input), unknown operation key, multi-calculation sessions.
- **Test strategy:** `unittest.mock.patch` on `builtins.input` (side_effect list) and `builtins.print` (capture). Helper `run_main_with_inputs` flattens all printed args into a list of strings.
- **Exports:** None
- **Last updated:** cycle 5 (issue-222)
