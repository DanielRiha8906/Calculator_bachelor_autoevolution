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
- **Last updated:** cycle 1
- **Public API:**
  - `Calculator.add(a, b)` → `a + b`
  - `Calculator.subtract(a, b)` → `a - b`
  - `Calculator.multiply(a, b)` → `a * b`
  - `Calculator.divide(a, b)` → `a / b`; raises `ValueError("Division by zero is not allowed")` when `b == 0`
- **Invariants:** No state — all methods are pure functions of their arguments.

---

## src/__main__.py
- **Purpose:** CLI entry point for manual smoke-testing the calculator.
- **Exports:** `main()` function; executed when `python -m src` is run.
- **Invariants:** Only calls `Calculator` methods; no side effects beyond stdout.

---

## tests/test_calculator.py
- **Purpose:** Unit test suite for `Calculator` — full coverage of all four arithmetic operations.
- **Last updated:** cycle 2
- **Tests (24 total):**
  - **add (5):** positive numbers, negative numbers, mixed sign, zero identity, floats
  - **subtract (6):** positive numbers, negative numbers, mixed sign, zero, floats, same-number-gives-zero
  - **multiply (6):** positive numbers, negative numbers, mixed sign, zero, identity (×1), floats
  - **divide (7):** divide-by-zero `ValueError`, normal, negative denominator, negative numerator, both negative, floats, fractional result
- **Invariants:** Must import from `src.calculator`, not from the package root; uses `math.isclose` for float comparisons.
