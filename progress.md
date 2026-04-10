## Run: Issue #101 — Add test for incorrect inputs in division

**Branch:** task/issue-101-division-invalid-inputs
**Target:** exp2/naive-generic
**Date:** 2026-04-09

### Files changed
- `tests/test_calculator.py` — added `TestDivideInvalidInputs` with 6 tests covering division by zero and non-numeric inputs

### Purpose
Add tests that verify `Calculator.divide()` raises the appropriate Python exceptions (`ZeroDivisionError`, `TypeError`) when given invalid inputs such as zero divisors, string arguments, and `None` values.

### Risks
- None: tests only assert existing Python behaviour; no source code was modified.

### Test results
All 6 tests passed (pytest 9.0.3, Python 3.12.3).

### Duration / Cost / Turns
Duration: PENDING | Cost: PENDING | Turns: PENDING
