## Run: Issue #115 — Add interactive user input (task/issue-115-user-input)

**Date:** 2026-04-11
**Branch:** task/issue-115-user-input
**Target:** exp2/expert-generic

### Files changed

- `src/__main__.py` — replaced static hardcoded demo with a full interactive session loop
  covering all 11 Calculator operations; added `_parse_number()` helper and `OPERATIONS` table
- `tests/test_main.py` — new file; 28 tests driving the interactive session via mocked input,
  covering all operations, error paths, invalid choices, and multi-calculation sessions

### Purpose

Implemented interactive runtime input per issue #115 (V2 Task 5 - User Input - Expert/generic):
- Menu-driven selection of all 11 operations (add, subtract, multiply, divide, factorial, square,
  cube, sqrt, cbrt, power, log10, ln)
- Prompts for one operand (unary operations) or two operands (binary operations) based on the
  selected operation; factorial enforces integer input at parse time
- Errors (ValueError, TypeError, ZeroDivisionError) are caught and displayed without terminating
  the session, allowing the user to continue
- Session loops until the user enters 'q' to quit

No changes were made to `src/calculator.py` or `tests/test_calculator.py` — the implementation
is strictly scoped to input-driven execution as required by the issue.

### Risks

Minimal. The Calculator class and its test suite are untouched. The new interactive layer depends
only on `builtins.input` and the existing Calculator methods, both of which are straightforwardly
testable via mocking.

### Test results

103 tests collected, 103 passed. No regressions (75 pre-existing + 28 new).

### PR target

exp2/expert-generic (never main)

Duration: PENDING | Cost: PENDING | Turns: PENDING

---

## Run: Diagram update — PlantUML artifacts (task/issue-112-more-functions)

**Date:** 2026-04-11
**Branch:** task/issue-112-more-functions
**Target:** exp2/expert-generic

### Files changed

- `artifacts/class_diagram.puml` — verified accurate; no changes needed
- `artifacts/activity_diagram.puml` — verified accurate; no changes needed
- `artifacts/sequence_diagram.puml` — verified accurate; no changes needed

### Purpose

Reviewed all three PlantUML diagrams against the current state of `src/`. All eleven
Calculator methods (add, subtract, multiply, divide, factorial, square, cube, sqrt, cbrt,
power, log10, ln) are correctly represented in every diagram. No updates were required.

### Risks

None. No source or test files were modified.

### Test results

N/A — diagram-only run.

### PR target

exp2/expert-generic (never main)

Duration: 28.2s | Cost: $0.158094 USD | Turns: 13

---

## Run: Issue #112 — Add more calculator operations (task/issue-112-more-functions)

**Date:** 2026-04-11
**Branch:** task/issue-112-more-functions
**Target:** exp2/expert-generic

### Files changed

- `src/calculator.py` — added `square`, `cube`, `sqrt`, `cbrt`, `power`, `log10`, and `ln` methods
- `tests/test_calculator.py` — added 37 tests covering all new operations including edge cases
- `artifacts/class_diagram.puml` — added all 7 new method signatures with constraint notes
- `artifacts/activity_diagram.puml` — added execution paths and error branches for each new operation
- `artifacts/sequence_diagram.puml` — added interaction sequences with alt blocks for error cases

### Purpose

Implemented seven new calculator operations per issue #112 (V2 Task 4 - More functions):
- `square(n)` — returns n²; defined for all real numbers
- `cube(n)` — returns n³; defined for all real numbers (negative cube is negative)
- `sqrt(n)` — returns √n via `math.sqrt`; raises `ValueError` for n < 0
- `cbrt(n)` — returns ∛n via `math.cbrt`; defined for all real numbers including negatives
- `power(base, exp)` — returns base^exp via `math.pow`; raises `ValueError` for complex results (negative base with non-integer exponent)
- `log10(n)` — returns log₁₀(n) via `math.log10`; raises `ValueError` for n ≤ 0
- `ln(n)` — returns ln(n) via `math.log`; raises `ValueError` for n ≤ 0

Unary operations (square, cube, sqrt, cbrt, log10, ln) and binary operation (power) are integrated consistently with the existing pattern established by `factorial` and the arithmetic methods.

### Risks

Minimal. The change is purely additive — no existing methods or tests were modified. All new methods rely exclusively on Python's standard `math` module (already imported). The `math.cbrt` function requires Python 3.11+; the project targets Python 3.12 per CLAUDE.md.

### Test results

75 tests collected, 75 passed. No regressions.

### PR target

exp2/expert-generic (never main)

Duration: 240.0s | Cost: $0.711373 USD | Turns: 32

---

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

Duration: 48.2s | Cost: $0.175778 USD | Turns: 18

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
