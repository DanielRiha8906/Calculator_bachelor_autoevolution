## Run: issue-101 — Add tests for incorrect inputs in division

- **Branch:** task/issue-101-add-division-input-tests
- **Target PR branch:** exp2/naive-generic
- **Date:** 2026-04-11

### Files changed
- `tests/test_calculator.py` — added `TestDivisionIncorrectInputs` class with 6 test cases

### Purpose
Implements Issue #101 (V2 Task 1 - Naive/generic): add tests that cover incorrect inputs to the `divide` method. Tests assert the expected Python exceptions are raised for division by zero (`ZeroDivisionError`) and non-numeric inputs such as strings and `None` (`TypeError`).

### Risks
- None. Tests only add new test cases; no production code was modified.

### Test results
All 6 tests passed:
- `test_divide_by_zero` — PASSED
- `test_divide_by_zero_float` — PASSED
- `test_divide_string_numerator` — PASSED
- `test_divide_string_denominator` — PASSED
- `test_divide_none_numerator` — PASSED
- `test_divide_none_denominator` — PASSED

Duration: PENDING | Cost: PENDING | Turns: PENDING
