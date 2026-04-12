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
- **Purpose:** Test suite for `Calculator`.
- **Current state:** Contains `test_divide_by_zero_raises` — asserts `ZeroDivisionError` is raised when calling `divide(1, 0)`.
- **Exports:** None
- **Last updated:** cycle 1 (issue-210)
