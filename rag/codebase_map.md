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
- **Last updated:** cycle 3
- **Public API:**
  - `Calculator.add(a, b)` → `a + b`
  - `Calculator.subtract(a, b)` → `a - b`
  - `Calculator.multiply(a, b)` → `a * b`
  - `Calculator.divide(a, b)` → `a / b`; raises `ValueError("Division by zero is not allowed")` when `b == 0`
  - `Calculator.factorial(n: int) -> int` → `n!`; raises `ValueError` for negative `n` or non-integer `n`
- **Invariants:** No state — all methods are pure functions of their arguments. Imports `math` at module level for `math.factorial`.

---

## src/__main__.py
- **Purpose:** CLI entry point for manual smoke-testing the calculator.
- **Exports:** `main()` function; executed when `python -m src` is run.
- **Invariants:** Only calls `Calculator` methods; no side effects beyond stdout.

---

## tests/test_calculator.py
- **Purpose:** Unit test suite for `Calculator` — full coverage of all five arithmetic operations.
- **Last updated:** cycle 3
- **Tests (30 total):**
  - **add (5):** positive numbers, negative numbers, mixed sign, zero identity, floats
  - **subtract (6):** positive numbers, negative numbers, mixed sign, zero, floats, same-number-gives-zero
  - **multiply (6):** positive numbers, negative numbers, mixed sign, zero, identity (×1), floats
  - **divide (7):** divide-by-zero `ValueError`, normal, negative denominator, negative numerator, both negative, floats, fractional result
  - **factorial (6):** zero (0! = 1), one (1! = 1), small (5! = 120), large (10! = 3628800), negative raises `ValueError`, float raises `ValueError`
- **Invariants:** Must import from `src.calculator`, not from the package root; uses `math.isclose` for float comparisons.
