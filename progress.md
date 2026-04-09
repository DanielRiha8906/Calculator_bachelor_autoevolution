## Run: 2026-04-09 — Issue #102 (task/102-zero-division-error)

**Branch:** task/102-zero-division-error
**PR target:** exp2/structured-generic

### Files changed
- `src/calculator.py` — added zero-divisor guard in `divide()`, raises `ValueError`
- `tests/test_calculator.py` — added `test_divide_by_zero_raises_value_error`

### Purpose
Handle division by zero explicitly so callers receive a clear `ValueError` instead of Python's bare `ZeroDivisionError`. Matches Issue #102 requirement.

### Risks
None — minimal change, no existing tests affected.

### Test results
All tests passed (1 collected, 1 passed).

Duration: PENDING | Cost: PENDING | Turns: PENDING
