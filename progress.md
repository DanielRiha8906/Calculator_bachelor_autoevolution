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

---

## Run: diagram-update — Update PlantUML diagrams

- **Branch:** task/issue-104-add-calculator-tests
- **Date:** 2026-04-11

### Files changed
- `artifacts/class_diagram.puml` — verified accurate; no changes needed
- `artifacts/activity_diagram.puml` — verified accurate; no changes needed
- `artifacts/sequence_diagram.puml` — verified accurate; no changes needed

### Purpose
Routine diagram maintenance pass. All three PlantUML diagrams were reviewed against the current source code (`src/calculator.py`, `src/__main__.py`, `src/__init__.py`) and test suite (`tests/test_calculator.py`). All diagrams correctly reflect the `Calculator` class with its four operations, the `__main__` entry point, the `__init__` export, and all five test classes (`TestAddition`, `TestSubtraction`, `TestMultiplication`, `TestDivision`, `TestDivisionIncorrectInputs`) with their 30 test methods.

### Risks
- None. No source or test code was modified; only `progress.md` updated.

### Test results
No tests modified; all existing 30 tests remain passing from previous run.

Duration: 37.6s | Cost: $0.161423 USD | Turns: 16

---

## Run: issue-107 — Add factorial to the calculator

- **Branch:** task/issue-107-add-factorial
- **Target PR branch:** exp2/naive-generic
- **Date:** 2026-04-11

### Files changed
- `src/calculator.py` — added `import math` and `factorial(n: int) -> int` method using `math.factorial()`
- `tests/test_calculator.py` — added `TestFactorial` (4 happy-path tests) and `TestFactorialIncorrectInputs` (4 error-case tests)
- `src/__main__.py` — added `calc.factorial(5)` demo call
- `artifacts/class_diagram.puml` — added `factorial` method to `Calculator` class; added `TestFactorial` and `TestFactorialIncorrectInputs` test classes
- `artifacts/activity_diagram.puml` — added factorial activity block with error branch
- `artifacts/sequence_diagram.puml` — added factorial sequence with error/success branches

### Purpose
Implements Issue #107 (V2 Task 3 - Factorial - Naive/generic): adds a `factorial(n)` method to the `Calculator` class backed by `math.factorial()`. The implementation delegates to the standard library to ensure correctness and leverage Python's built-in large-integer arithmetic.

### Risks
- `math.factorial` in Python 3.12 raises `TypeError` (not `ValueError`) for float arguments — tests reflect this actual runtime behavior.
- No new dependencies introduced; `math` is a standard library module.

### Test results
All 38 tests passed (30 pre-existing + 8 new):
- `TestFactorial::test_factorial_zero` — PASSED
- `TestFactorial::test_factorial_one` — PASSED
- `TestFactorial::test_factorial_small_positive` — PASSED
- `TestFactorial::test_factorial_larger_positive` — PASSED
- `TestFactorialIncorrectInputs::test_factorial_negative` — PASSED
- `TestFactorialIncorrectInputs::test_factorial_float` — PASSED
- `TestFactorialIncorrectInputs::test_factorial_string` — PASSED
- `TestFactorialIncorrectInputs::test_factorial_none` — PASSED

Duration: 186.4s | Cost: $0.693774 USD | Turns: 38

---

## Run: diagram-update — Update PlantUML diagrams

- **Branch:** task/issue-107-add-factorial
- **Date:** 2026-04-11

### Files changed
- `artifacts/class_diagram.puml` — verified accurate; no changes needed
- `artifacts/activity_diagram.puml` — verified accurate; no changes needed
- `artifacts/sequence_diagram.puml` — verified accurate; no changes needed

### Purpose
Routine diagram maintenance pass. All three PlantUML diagrams were reviewed against the current source code (`src/calculator.py`, `src/__main__.py`, `src/__init__.py`) and test suite (`tests/test_calculator.py`). All diagrams correctly reflect the `Calculator` class with its five operations (`add`, `subtract`, `multiply`, `divide`, `factorial`), the `__main__` entry point, the `__init__` export, and all seven test classes (`TestAddition`, `TestSubtraction`, `TestMultiplication`, `TestDivision`, `TestDivisionIncorrectInputs`, `TestFactorial`, `TestFactorialIncorrectInputs`) with their 38 test methods.

### Risks
- None. No source or test code was modified; only `progress.md` updated.

### Test results
No tests modified; all existing 38 tests remain passing from previous run.

Duration: 36.5s | Cost: $0.156808 USD | Turns: 15
