## Run: issue-146 — Add retry logic for bad input in interactive mode

- **Branch:** task/issue-146-retry-logic
- **Target PR branch:** exp2/naive-generic
- **Date:** 2026-04-11

### Files changed
- `src/user_input.py` — added `MAX_RETRIES = 3` constant and two helpers `_get_float()` and `_get_int()` that prompt for valid numeric input and retry up to `MAX_RETRIES` times before raising `ValueError`; replaced bare `input()` calls in `interactive_mode()` with these helpers
- `tests/test_user_input.py` — added 9 new tests across two classes (`TestRetryLogicHelpers`, `TestRetryLogicInInteractiveMode`) covering successful retry after bad input, exhausting all retries, and correct error messages

### Purpose
Implements Issue #146 (V2 Task 8 - Retry logic - Naive/generic): when the user enters invalid input (non-numeric or non-integer) for an operand, the system prints a descriptive error with remaining attempts and prompts again, up to 3 times, before reporting failure and returning to the operation selection menu.

### Risks
- Only operand input has retry logic; operation selection continues to use the existing `continue` path on invalid choice (different UX, already sufficient).
- `MAX_RETRIES = 3` is a module-level constant — easy to adjust, but changing it affects all callers at once.
- No new dependencies introduced.

### Test results
All 123 tests passed (114 pre-existing + 9 new):
- `TestRetryLogicHelpers` (6 tests) — all PASSED
- `TestRetryLogicInInteractiveMode` (3 tests) — all PASSED

Duration: 140.8s | Cost: $0.432757 USD | Turns: 19

---

## Run: issue-143 — Add bash CLI mode to the calculator

- **Branch:** task/issue-143-add-bash-cli
- **Target PR branch:** exp2/naive-generic
- **Date:** 2026-04-11

### Files changed
- `src/cli.py` — new module with `cli_mode()` function implementing argparse-based single-shot CLI for all 12 calculator operations
- `src/__main__.py` — updated to route to `cli_mode()` when command-line arguments are present, or `interactive_mode()` when run with no arguments
- `tests/test_cli.py` — new test file with 25 tests covering all operation types, error cases, operand count validation, and invalid operation handling
- `artifacts/class_diagram.puml` — added `CLI` class and three new test classes
- `artifacts/activity_diagram.puml` — added CLI branch at entry point showing argument parsing and per-operation dispatch
- `artifacts/sequence_diagram.puml` — added CLI participant showing full request/response flow for bash mode

### Purpose
Implements Issue #143 (V2 Task 7 - Bash mode - Naive/generic): adds a non-interactive CLI mode so the calculator can be used from bash scripts and shell pipelines. When `python -m src` is invoked with arguments (`python -m src add 3 5`), it parses the operation and operands via argparse, executes once, prints the result to stdout, and exits with code 0 (success) or 1 (error). Without arguments the existing interactive REPL is unchanged.

### Risks
- `factorial` still requires an integer operand; passing a float string (e.g. `3.5`) will raise `ValueError` and exit with code 1 — consistent with the interactive mode behaviour.
- argparse exits with code 2 for unknown operations or missing required arguments; tests verify `SystemExit` is raised for unknown operations.
- No new dependencies introduced; only `argparse` and `sys` from the standard library are used.

### Test results
All 114 tests passed (89 pre-existing + 25 new):
- `TestCliTwoArgOps` (7 tests) — all PASSED
- `TestCliSingleArgOps` (8 tests) — all PASSED
- `TestCliErrorCases` (10 tests) — all PASSED

Duration: 234.8s | Cost: $0.702941 USD | Turns: 30

---

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

---

## Run: diagram-update — Update PlantUML diagrams

- **Branch:** task/issue-113-add-user-input
- **Date:** 2026-04-11

### Files changed
- `artifacts/class_diagram.puml` — added `UserInput` module class (`OPERATIONS`, `TWO_ARG_OPS`, `INT_OPS`, `_print_menu()`, `interactive_mode()`); added `TestInteractiveMode` with 15 test methods; updated `Main` relationship to reflect it now calls `interactive_mode()` rather than `Calculator` directly
- `artifacts/activity_diagram.puml` — replaced static demo flow with interactive REPL loop: print menu, read choice, dispatch by op type (INT_OPS / TWO_ARG_OPS / single-arg), handle errors, loop until 'q'
- `artifacts/sequence_diagram.puml` — replaced static sequence with interactive flow: `__main__` → `user_input::interactive_mode()` → `Calculator`, showing loop, all three input-arity branches, and error handling

### Purpose
Routine diagram maintenance pass following the addition of `src/user_input.py` (Issue #113). All three PlantUML diagrams now reflect the current codebase: `Calculator` (12 methods), `UserInput` module (interactive REPL), `__main__` entry point, `__init__` export, and all 18 test classes (89 test methods total).

### Risks
- None. No source or test code was modified; only diagram artifacts and `progress.md` updated.

### Test results
No tests modified; all existing 89 tests remain passing from previous run.

Duration: 109.3s | Cost: $0.335366 USD | Turns: 22

---

## Run: diagram-update — Update PlantUML diagrams

- **Branch:** task/issue-143-add-bash-cli
- **Date:** 2026-04-11

### Files changed
- `artifacts/class_diagram.puml` — verified accurate; no changes needed
- `artifacts/activity_diagram.puml` — verified accurate; no changes needed
- `artifacts/sequence_diagram.puml` — verified accurate; no changes needed

### Purpose
Routine diagram maintenance pass following the addition of `src/cli.py` (Issue #143). All three PlantUML diagrams were reviewed against the current source code (`src/calculator.py`, `src/user_input.py`, `src/cli.py`, `src/__main__.py`, `src/__init__.py`) and test suite (`tests/test_calculator.py`, `tests/test_user_input.py`, `tests/test_cli.py`). All diagrams correctly reflect the full codebase: `Calculator` (12 methods), `UserInput` module (interactive REPL), `CLI` module (bash single-shot mode), `__main__` entry point, `__init__` export, and all 21 test classes (114 test methods total).

### Risks
- None. No source or test code was modified; only `progress.md` updated.

### Test results
No tests modified; all existing 114 tests remain passing from previous run.

Duration: 42.4s | Cost: $0.248681 USD | Turns: 21
