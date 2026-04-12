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
- **Purpose:** Unit test suite for `Calculator`.
- **Last updated:** cycle 1
- **Tests:**
  - `test_divide_by_zero_raises` — asserts `ValueError` with message "Division by zero is not allowed" when dividing by 0
  - `test_divide_normal` — asserts `divide(10, 2) == 5.0`
  - `test_divide_negative_denominator` — asserts `divide(9, -3) == -3.0`
- **Invariants:** Must import from `src.calculator`, not from the package root.
