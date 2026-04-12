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
- **Key invariants:**
  - Division delegates directly to Python `/` operator; no explicit zero-check.
  - `ZeroDivisionError` is raised by Python runtime when dividing by zero.
- **Last updated:** cycle 0

---

## `tests/test_calculator.py`
- **Purpose:** Comprehensive unit test suite for `Calculator`.
- **Current state:** 30 tests across all four operations — add (7 tests), subtract (6 tests), multiply (7 tests), divide (10 tests).
  - Normal inputs (positive, negative, zero, floats)
  - Edge cases: division by zero (`ZeroDivisionError`), float precision via `math.isclose`, zero dividend/multiplier
  - Invalid type inputs (`TypeError`) for all four operations
- **Exports:** None (pytest-discovered)
- **Last updated:** cycle 2 (issue-213)
