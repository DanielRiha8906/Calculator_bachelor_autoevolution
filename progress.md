## Run: Issue #148 — Retry logic for interactive mode (task/issue-148-retry-logic-interactive)

**Date:** 2026-04-11
**Branch:** task/issue-148-retry-logic-interactive
**Target:** exp2/expert-generic

### Files changed

- `src/__main__.py` — added `MAX_RETRIES = 5` constant and `_prompt_number()` helper;
  updated `main()` to track consecutive invalid menu selections (up to MAX_RETRIES before
  terminating) and to use `_prompt_number` for operand input so invalid entries trigger
  a retry with a remaining-attempts message instead of jumping straight back to the menu
- `tests/test_main.py` — updated `test_factorial_float_input_shows_error` to provide a
  valid retry input after the invalid one (matches new retry behavior); added 5 new tests
  covering: available-options display on bad menu choice, session termination after
  MAX_RETRIES invalid menu choices, failure-counter reset on valid choice, operand retry
  succeeding after one bad input, and session termination after MAX_RETRIES bad operands
- `artifacts/class_diagram.puml` — added `MAX_RETRIES` attribute and `_prompt_number`
  method to the `__main__` class; updated notes for `main()` to describe retry policy
- `artifacts/activity_diagram.puml` — added retry-loop and termination branches for
  both invalid menu selections and invalid operand inputs in the interactive partition
- `artifacts/sequence_diagram.puml` — updated interactive-mode sequence to show the
  retry counter increment, available-options message, and per-operand retry loops

### Purpose

Implemented issue #148 (Task 8 — Retry logic — Expert/guided):
- Invalid menu choice: shows error + lists available operation keys; increments a
  consecutive-failure counter; terminates the session after MAX_RETRIES (5) failures
- Valid menu choice resets the failure counter to zero
- Invalid operand (non-parseable string): `_prompt_number` re-prompts up to MAX_RETRIES
  times, printing remaining attempts; returns None when exhausted, causing `main()` to
  terminate with a "Ending session" message
- Bash CLI mode (`main.py`) is unchanged — it already fails fast with stderr + exit 1

### Risks

Low. Changes are confined to `src/__main__.py` input-handling logic. The `Calculator`
class and bash CLI are not touched. Mathematical errors (e.g. divide-by-zero) continue
to show an error and return to the menu rather than consuming retry attempts, preserving
the existing `test_error_does_not_terminate_session` behaviour.

### Test results

138 tests collected; 138 passed; 0 failed; 0 skipped.
No regressions in `test_calculator.py` (75) or `test_cli.py` (30).
`test_main.py` grew from 28 to 33 tests (+5 retry-specific tests).

### PR target

exp2/expert-generic (never main)

Duration: 544.0s | Cost: $1.293858 USD | Turns: 35

---

## Run: Diagram update — PlantUML artifacts (task/issue-145-bash-cli)

**Date:** 2026-04-11
**Branch:** task/issue-145-bash-cli
**Target:** exp2/expert-generic

### Files changed

- `artifacts/class_diagram.puml` — verified accurate; no changes needed
- `artifacts/activity_diagram.puml` — verified accurate; no changes needed
- `artifacts/sequence_diagram.puml` — verified accurate; no changes needed

### Purpose

Reviewed all three PlantUML diagrams against the current state of `src/` and `main.py`.
All twelve Calculator methods and both entry points (interactive `src/__main__.py` and
bash CLI `main.py`) are correctly represented in every diagram. No updates were required.

### Risks

None. No source or test files were modified.

### Test results

N/A — diagram-only run.

### PR target

exp2/expert-generic (never main)

Duration: 48.0s | Cost: $0.207033 USD | Turns: 17

---

## Run: Issue #145 — Add bash CLI (task/issue-145-bash-cli)

**Date:** 2026-04-11
**Branch:** task/issue-145-bash-cli
**Target:** exp2/expert-generic

### Files changed

- `main.py` — new file; bash CLI entry point supporting all 12 Calculator operations via
  command-line arguments (`python main.py <operation> [operand1] [operand2]`)
- `tests/test_cli.py` — new file; 30 tests covering argument validation, all operations
  (happy path and error cases), and correct stdout/stderr/exit-code behaviour
- `artifacts/class_diagram.puml` — added `main` CLI module with `CLI_OPERATIONS`,
  `_parse_operand`, and `main(argv)` with descriptive notes
- `artifacts/activity_diagram.puml` — added Bash CLI partition alongside the existing
  interactive session partition
- `artifacts/sequence_diagram.puml` — added Bash CLI sequence alongside the existing
  interactive session sequence

### Purpose

Implemented a bash CLI per issue #145 (V2 Task 7 - Bash mode - Expert/generic):
- `main.py` at the project root accepts `<operation> [operands]` as argv
- `CLI_OPERATIONS` maps the 12 operation names to `(method_name, arity)` pairs
- `_parse_operand()` parses each argv operand: int for whole-number strings,
  float otherwise; strict int for `factorial` (mirrors `_parse_number` in `__main__`)
- Errors (unknown operation, wrong operand count, bad number format, calculator
  exceptions) are written to stderr and the process exits with code 1
- Successful results are printed to stdout with exit code 0
- The interactive session in `src/__main__.py` is unchanged

### Risks

Minimal. `main.py` is a new file with no modifications to existing source or tests.
The `Calculator` class and both existing test files are untouched. The only runtime
dependency added is `src.calculator.Calculator`, already present in the project.

### Test results

133 tests collected, 133 passed. No regressions (103 pre-existing + 30 new).

### PR target

exp2/expert-generic (never main)

Duration: 363.7s | Cost: $0.893680 USD | Turns: 36

---

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

Duration: 206.8s | Cost: $0.499660 USD | Turns: 19

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

---

## Run: Diagram update — PlantUML artifacts (task/issue-115-user-input)

**Date:** 2026-04-11
**Branch:** task/issue-115-user-input
**Target:** exp2/expert-generic

### Files changed

- `artifacts/class_diagram.puml` — added `OPERATIONS: dict` and `_parse_number()` to `__main__` module; added descriptive notes for each
- `artifacts/activity_diagram.puml` — replaced static linear demo flow with interactive session loop reflecting `main()`: menu display, choice validation, arity-based operand collection via `_parse_number`, error handling, repeat-until-quit structure
- `artifacts/sequence_diagram.puml` — replaced static sequence with interactive loop showing User actor, `_parse_number` calls, arity-based branching, exception alt blocks, and session lifecycle

### Purpose

Updated all three PlantUML diagrams to reflect the interactive session loop introduced in
issue #115. The previous diagrams modelled a static hardcoded demo; they now accurately
represent the menu-driven input loop, `OPERATIONS` dispatch table, `_parse_number` helper,
and per-operation error handling present in the current `src/__main__.py`.

### Risks

None. No source or test files were modified.

### Test results

N/A — diagram-only run.

### PR target

exp2/expert-generic (never main)

Duration: 76.1s | Cost: $0.275522 USD | Turns: 18
