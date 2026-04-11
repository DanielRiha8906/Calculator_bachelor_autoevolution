## Run: Issue #102 — Add ZeroDivisionError handling

**Branch:** task/issue-102-zero-division-error
**Target branch:** exp2/structured-generic
**Date:** 2026-04-11

### Files changed
- `src/calculator.py` — Updated `divide()` to raise `ZeroDivisionError` when divisor is zero
- `tests/test_calculator.py` — Added `test_divide_by_zero_raises` unit test

### Purpose
Add explicit ZeroDivisionError handling to the calculator's divide method and a corresponding unit test, as specified in issue #102 (V2 Task 1 - Structured/generic experiment).

### Risks
- Minimal risk: the change is backward-compatible for all valid inputs (non-zero divisors).
- The explicit raise replaces the implicit Python ZeroDivisionError with an identical exception and a descriptive message, so no existing caller behavior is broken.

### Test results
All tests passed: 1 passed in 0.01s

### Intended PR target
exp2/structured-generic

Duration: 83.2s | Cost: $0.243861 USD | Turns: 15
