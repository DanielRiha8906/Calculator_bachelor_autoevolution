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
- **Public API:**
  - `Calculator.add(a, b)` → `a + b`
  - `Calculator.subtract(a, b)` → `a - b`
  - `Calculator.multiply(a, b)` → `a * b`
  - `Calculator.divide(a, b)` → `a / b` (raises `ZeroDivisionError` if `b == 0` at cycle 0; no guard)
- **Invariants:** No state — all methods are pure functions of their arguments.
- **Known issues (cycle 0):** `divide` does not guard against `b == 0`; raises a raw Python `ZeroDivisionError`.

---

## src/__main__.py
- **Purpose:** CLI entry point for manual smoke-testing the calculator.
- **Exports:** `main()` function; executed when `python -m src` is run.
- **Invariants:** Only calls `Calculator` methods; no side effects beyond stdout.

---

## tests/test_calculator.py
- **Purpose:** Unit test suite for `Calculator`.
- **State at cycle 0:** Only contains imports (`import pytest`, `import math`, `from src.calculator import Calculator`). No test functions defined yet.
- **Invariants:** Must import from `src.calculator`, not from the package root.
