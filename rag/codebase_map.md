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
- **Purpose:** CLI entry point that demonstrates all four Calculator operations.
- **Exports:** `main()` function
- **Invariants:** Calls `add(10,5)`, `subtract(10,5)`, `multiply(10,5)`, `divide(10,5)` and prints results. Not imported by tests.
- **Last updated:** cycle 0

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
