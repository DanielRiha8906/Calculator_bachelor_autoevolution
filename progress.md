## Run: Issue #103 — Add ZeroDivisionError test coverage (exp2/expert-generic)

**Date:** 2026-04-11
**Branch:** task/issue-103-add-zero-division-error
**Target:** exp2/expert-generic

### Files changed

- `tests/test_calculator.py` — added `test_divide_by_zero_raises_error`

### Purpose

Added a focused test to assert that `Calculator.divide()` raises `ZeroDivisionError`
when the divisor is zero. This documents and verifies the existing Python behavior
without modifying the implementation (Python's `/` operator already raises
`ZeroDivisionError` for zero divisors, so no implementation change was required).

### Risks

None. The change is additive (new test only) and does not touch the implementation.

### Test results

1 test collected, 1 passed. No regressions.

### PR target

exp2/expert-generic (never main)

Duration: PENDING | Cost: PENDING | Turns: PENDING
