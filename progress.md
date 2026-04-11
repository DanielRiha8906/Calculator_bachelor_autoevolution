## Run: Diagram update — PlantUML artifacts (task/issue-106-unit-test-suite)

**Date:** 2026-04-11
**Branch:** task/issue-106-unit-test-suite
**Target:** exp2/expert-generic

### Files changed

- `artifacts/class_diagram.puml` — verified accurate; no changes needed
- `artifacts/activity_diagram.puml` — verified accurate; no changes needed
- `artifacts/sequence_diagram.puml` — verified accurate; no changes needed

### Purpose

Reviewed all three PlantUML diagrams against the current state of `src/`. The source code
(Calculator class with add/subtract/multiply/divide, `__main__.py` entry point, and `__init__.py`
export module) is unchanged, so all diagrams remain correct and required no updates.

### Risks

None. No source or test files were modified.

### Test results

N/A — diagram-only run.

### PR target

exp2/expert-generic (never main)

Duration: PENDING | Cost: PENDING | Turns: PENDING

---

## Run: Issue #106 — Unit test suite for all calculator operations (exp2/expert-generic)

**Date:** 2026-04-11
**Branch:** task/issue-106-unit-test-suite
**Target:** exp2/expert-generic

### Files changed

- `tests/test_calculator.py` — replaced single divide-by-zero test with a full 29-test suite
  covering add, subtract, multiply, and divide across normal inputs, edge cases, and invalid inputs

### Purpose

Created a comprehensive unit test suite for the four calculator operations as required by
issue #106 (V2 Task 2 - TestSuite - Expert/generic). Tests cover:
- Normal positive, negative, and mixed-sign integer inputs
- Float inputs using `pytest.approx` where IEEE 754 precision applies
- Edge cases: zero operands, divide-by-zero (ZeroDivisionError)
- Invalid inputs: `None` or non-numeric strings that raise TypeError

One correctness fix was applied during authoring: the original draft tested `multiply("x", 2)`
expecting TypeError, but Python's `*` operator performs string repetition without raising —
the test was corrected to use `None` instead.

### Risks

Minimal. The change is additive (tests only). The existing `test_divide_by_zero_raises_error`
was preserved (now part of the unified suite).

### Test results

29 tests collected, 29 passed. No regressions.

### PR target

exp2/expert-generic (never main)

Duration: 108.7s | Cost: $0.293650 USD | Turns: 18

---

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

Duration: 87.3s | Cost: $0.236692 USD | Turns: 17
