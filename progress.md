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

Duration: 83.2s | Cost: $0.244124 USD | Turns: 16

---

## Run: issue-104 — Add full test suite for calculator

- **Branch:** task/issue-104-add-calculator-tests
- **Target PR branch:** exp2/naive-generic
- **Date:** 2026-04-11

### Files changed
- `tests/test_calculator.py` — added `TestAddition`, `TestSubtraction`, `TestMultiplication`, and `TestDivision` classes (24 new test cases)
- `artifacts/class_diagram.puml` — updated to reflect the four new test classes

### Purpose
Implements Issue #104 (V2 Task 2 - Test suite - Naive/generic): creates a comprehensive test suite covering all four Calculator operations. Added 6 tests each for `add`, `subtract`, `multiply`, and `divide` (happy paths), complementing the existing 6 division error-case tests.

### Risks
- None. Only test files and diagrams were modified; no production code was changed.

### Test results
All 30 tests passed:
- `TestAddition` (6 tests) — all PASSED
- `TestSubtraction` (6 tests) — all PASSED
- `TestMultiplication` (6 tests) — all PASSED
- `TestDivision` (6 tests) — all PASSED
- `TestDivisionIncorrectInputs` (6 tests) — all PASSED

Duration: 142.9s | Cost: $0.416957 USD | Turns: 19
