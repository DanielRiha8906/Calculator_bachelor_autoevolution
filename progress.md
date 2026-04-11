## Run: issue-113 — Add user input to the calculator

- **Branch:** task/issue-113-add-user-input
- **Target PR branch:** exp2/naive-generic
- **Date:** 2026-04-11

### Files changed
- `src/user_input.py` — new module with `interactive_mode()` function implementing an interactive CLI REPL for the calculator
- `src/__main__.py` — updated to call `interactive_mode()` instead of the static demo
- `tests/test_user_input.py` — new test file with 15 tests covering quit, menu display, all operation types, invalid input, and error handling

### Purpose
Implements Issue #113 (V2 Task 5 - User input - Naive/generic): adds an interactive command-line interface that lets users select an operation from a menu, enter operands, and see the result. The loop repeats until the user quits with 'q'. All 12 calculator operations are accessible; errors (ZeroDivisionError, ValueError, TypeError) are displayed without crashing.

### Risks
- None. `interactive_mode()` is a pure I/O wrapper over the existing `Calculator` class; no calculator logic was modified.
- Factorial requires integer input — the function parses with `int()` for that operation and `float()` for all others.

### Test results
All 89 tests passed (74 pre-existing + 15 new):
- `TestInteractiveMode::test_quit_immediately` — PASSED
- `TestInteractiveMode::test_menu_is_printed` — PASSED
- `TestInteractiveMode::test_add_two_numbers` — PASSED
- `TestInteractiveMode::test_subtract_two_numbers` — PASSED
- `TestInteractiveMode::test_multiply_two_numbers` — PASSED
- `TestInteractiveMode::test_divide_two_numbers` — PASSED
- `TestInteractiveMode::test_factorial_integer` — PASSED
- `TestInteractiveMode::test_square_number` — PASSED
- `TestInteractiveMode::test_cube_number` — PASSED
- `TestInteractiveMode::test_square_root` — PASSED
- `TestInteractiveMode::test_power_operation` — PASSED
- `TestInteractiveMode::test_invalid_choice_shows_error` — PASSED
- `TestInteractiveMode::test_divide_by_zero_shows_error` — PASSED
- `TestInteractiveMode::test_square_root_negative_shows_error` — PASSED
- `TestInteractiveMode::test_multiple_operations_in_session` — PASSED

Duration: 192.8s | Cost: $0.583849 USD | Turns: 21

---

## Run: issue-110 — Add more math functions to the calculator

- **Branch:** task/issue-110-add-math-functions
- **Target PR branch:** exp2/naive-generic
- **Date:** 2026-04-11

### Files changed
- `src/calculator.py` — added `square`, `cube`, `square_root`, `cube_root`, `power`, `log`, `ln` methods
- `tests/test_calculator.py` — added 11 test classes (36 new test cases) covering all 7 new methods
- `src/__main__.py` — added demo calls for all 7 new functions
- `artifacts/class_diagram.puml` — added 7 new methods to `Calculator` and 11 new test classes
- `artifacts/activity_diagram.puml` — added activity blocks for all 7 new operations
- `artifacts/sequence_diagram.puml` — added sequence interactions for all 7 new operations

### Purpose
Implements Issue #110 (V2 Task 4 - More functions - Naive/generic): adds `square(x)`, `cube(x)`, `square_root(x)`, `cube_root(x)`, `power(base, exp)`, `log(x)`, and `ln(x)` to the `Calculator` class. All implementations delegate to the Python `math` standard library (`math.sqrt`, `math.cbrt`, `math.pow`, `math.log10`, `math.log`) for correctness, with `square` and `cube` using direct Python operators.

### Risks
- `math.cbrt` was introduced in Python 3.11 — compatible with this project's Python 3.12 requirement.
- `log` is implemented as `math.log10` (common/base-10 logarithm); `ln` uses `math.log` (natural logarithm).
- `power` uses `math.pow` which always returns a float and raises `ValueError` for domain errors (e.g., negative base with fractional exponent).
- No new dependencies introduced; all functions use the standard library `math` module already imported.

### Test results
All 74 tests passed (38 pre-existing + 36 new):
- `TestSquare` (5 tests) — all PASSED
- `TestCube` (5 tests) — all PASSED
- `TestSquareRoot` (4 tests) — all PASSED
- `TestSquareRootIncorrectInputs` (1 test) — PASSED
- `TestCubeRoot` (4 tests) — all PASSED
- `TestPower` (5 tests) — all PASSED
- `TestLog` (4 tests) — all PASSED
- `TestLogIncorrectInputs` (2 tests) — all PASSED
- `TestLn` (4 tests) — all PASSED
- `TestLnIncorrectInputs` (2 tests) — all PASSED

Duration: 259.0s | Cost: $0.802687 USD | Turns: 35

---

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

---

## Run: diagram-update — Update PlantUML diagrams

- **Branch:** task/issue-110-add-math-functions
- **Date:** 2026-04-11

### Files changed
- `artifacts/class_diagram.puml` — verified accurate; no changes needed
- `artifacts/activity_diagram.puml` — verified accurate; no changes needed
- `artifacts/sequence_diagram.puml` — verified accurate; no changes needed

### Purpose
Routine diagram maintenance pass. All three PlantUML diagrams were reviewed against the current source code (`src/calculator.py`, `src/__main__.py`, `src/__init__.py`) and test suite. All diagrams correctly reflect the `Calculator` class with its 12 operations (`add`, `subtract`, `multiply`, `divide`, `factorial`, `square`, `cube`, `square_root`, `cube_root`, `power`, `log`, `ln`), the `__main__` entry point, the `__init__` export, and all 17 test classes with their full set of test methods.

### Risks
- None. No source or test code was modified; only `progress.md` updated.

### Test results
No tests modified; all existing 74 tests remain passing from previous run.

Duration: 25.1s | Cost: $0.125089 USD | Turns: 12
