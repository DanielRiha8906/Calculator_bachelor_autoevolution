## Run: Diagram update — PlantUML artifacts (task/issue-109-add-factorial)

**Date:** 2026-04-11
**Branch:** task/issue-109-add-factorial
**Target:** exp2/expert-generic

### Files changed

- `artifacts/class_diagram.puml` — added `factorial(n: int) : int` to Calculator class and explanatory note
- `artifacts/activity_diagram.puml` — added factorial execution path with TypeError/ValueError branches
- `artifacts/sequence_diagram.puml` — added factorial interaction with TypeError/ValueError/success alt blocks

### Purpose

Updated all three PlantUML diagrams to reflect the addition of `Calculator.factorial()` introduced
in issue #109. Previous diagrams only covered add/subtract/multiply/divide.

### Risks

None. No source or test files were modified.

### Test results

N/A — diagram-only run.

### PR target

exp2/expert-generic (never main)

Duration: PENDING | Cost: PENDING | Turns: PENDING

---

## Run: Issue #109 — Add factorial operation (task/issue-109-add-factorial)

**Date:** 2026-04-11
**Branch:** task/issue-109-add-factorial
**Target:** exp2/expert-generic

### Files changed

- `src/calculator.py` — added `factorial(n)` method using `math.factorial`; added `import math`
- `tests/test_calculator.py` — added 9 tests covering boundary cases (0, 1), positive integers,
  negative input (ValueError), floats/strings/None/bool (TypeError)

### Purpose

Implemented factorial as a new calculator operation per issue #109. The method:
- Accepts only `int` values (booleans explicitly rejected despite being int subclasses)
- Raises `TypeError` for non-integer inputs (float, str, None, bool)
- Raises `ValueError` for negative integers
- Delegates computation to `math.factorial` for correctness and efficiency

### Risks

Minimal. The change is additive — no existing methods or tests were modified. The only
new import (`math`) is from the Python standard library.

### Test results

38 tests collected, 38 passed. No regressions.

### PR target

exp2/expert-generic (never main)

Duration: 100.4s | Cost: $0.303693 USD | Turns: 16

---

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

Duration: 33.2s | Cost: $0.158576 USD | Turns: 15

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
