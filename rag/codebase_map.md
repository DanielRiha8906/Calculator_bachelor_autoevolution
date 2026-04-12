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
- **Key invariants:** No input validation; relies on Python's native arithmetic behavior. `divide` will raise `ZeroDivisionError` on zero divisor.
- **Last updated:** cycle 0

## src/__main__.py
- **Purpose:** CLI entry point; demonstrates basic Calculator usage.
- **Exports:** `main()` function
- **Key invariants:** Calls all four operations with hardcoded values (10, 5).
- **Last updated:** cycle 0

## tests/test_calculator.py
- **Purpose:** Test suite for Calculator class.
- **Current state:** Contains `test_divide_by_zero_raises` — asserts that `Calculator.divide(10, 0)` raises `ZeroDivisionError`.
- **Exports:** `test_divide_by_zero_raises`
- **Last updated:** cycle 1
