## Run: PlantUML diagram update

**Branch:** task/issue-147-retry-logic
**Date:** 2026-04-11

### Files changed
- `artifacts/class_diagram.puml` — Added `TooManyAttemptsError` exception class with `Exception` inheritance; updated `get_number()` and `get_integer()` signatures to include `max_attempts: int` parameter; added dependency arrows from both to `TooManyAttemptsError`
- `artifacts/activity_diagram.puml` — Reviewed; accurately reflects current `src/` state (no update needed)
- `artifacts/sequence_diagram.puml` — Reviewed; accurately reflects current `src/` state (no update needed)

### Purpose
Update PlantUML diagrams to reflect the retry logic additions from issue #147. The class diagram was missing `TooManyAttemptsError` and the updated `get_number`/`get_integer` signatures that include the `max_attempts` parameter. Activity and sequence diagrams already captured these changes in the previous run.

### Risks
- None; no source code was modified.

### Test results
N/A — diagram-only run.

Duration: 74.6s | Cost: $0.253398 USD | Turns: 18

---

## Run: Issue #147 — Retry logic with max attempts

**Branch:** task/issue-147-retry-logic
**Target branch:** exp2/structured-generic
**Date:** 2026-04-11

### Files changed
- `src/__main__.py` — Added `MAX_INPUT_ATTEMPTS = 3` constant and `TooManyAttemptsError` exception. Modified `get_number()` and `get_integer()` to accept a `max_attempts` parameter (default `MAX_INPUT_ATTEMPTS`) and raise `TooManyAttemptsError` after exhausting all attempts, with a countdown message on each failed retry. Modified `main()` to track consecutive invalid operation choices and terminate after `MAX_INPUT_ATTEMPTS` consecutive invalid choices; also catches `TooManyAttemptsError` from `perform_operation` and terminates the session gracefully.
- `tests/test_main.py` — Updated imports to include `TooManyAttemptsError` and `MAX_INPUT_ATTEMPTS`. Added 9 new tests covering max-attempt exhaustion, last-attempt success, countdown message display, invalid-choice counter, counter reset on valid choice, and session exit on too many invalid operands.
- `artifacts/activity_diagram.puml` — Updated interactive mode branch to show the `consecutive_invalid_choices` counter, the max-attempts guard for invalid choices, and the operand retry loop with countdown and exhaustion exit.
- `artifacts/sequence_diagram.puml` — Updated the interactive-mode note to document the two new termination paths: too many invalid choices, and `TooManyAttemptsError` from operand input.

### Purpose
Add bounded retry logic to the interactive calculator mode (issue #147, V2 Task 8 — Structured/generic). Previously `get_number()` and `get_integer()` retried indefinitely on invalid input, and invalid operation choices were silently ignored without limit. Now both operand input and operation selection are bounded by `MAX_INPUT_ATTEMPTS = 3`. CLI mode already terminates on invalid input via argparse and domain-error handling; no CLI changes were needed.

### Risks
- `MAX_INPUT_ATTEMPTS = 3` is a module-level constant. Tests that call `get_number()` or `get_integer()` with fewer than 3 valid inputs and no invalid inputs are unaffected. Tests that relied on infinite retry (passing exactly one invalid then one valid input) continue to pass because one retry is within the 3-attempt limit.
- `TooManyAttemptsError` is not a subclass of `ValueError` or `ZeroDivisionError`, so it propagates past the existing error handler in `main()` and is caught by the dedicated `except TooManyAttemptsError` clause.

### Test results
All 148 tests passed: 148 passed in 0.29s (139 existing + 9 new)

### Intended PR target
exp2/structured-generic

Duration: 368.0s | Cost: $1.145991 USD | Turns: 41

---

## Run: PlantUML diagram update

**Branch:** task/issue-144-bash-cli-mode
**Date:** 2026-04-11

### Files changed
- `artifacts/class_diagram.puml` — Reviewed; accurately reflects current `src/` state (no update needed)
- `artifacts/activity_diagram.puml` — Reviewed; accurately reflects current `src/` state (no update needed)
- `artifacts/sequence_diagram.puml` — Reviewed; accurately reflects current `src/` state (no update needed)

### Purpose
Verify and maintain PlantUML diagrams against the current source code. All three diagrams (class, activity, sequence) correctly represent the `Calculator` class with all 12 operations, the interactive `__main__` module (display_menu, get_number, get_integer, perform_operation, main), and the bash CLI module (build_parser, _dispatch, cli_main) as introduced in issue #144.

### Risks
- None; no source code was modified.

### Test results
N/A — diagram-only run.

Duration: 31.3s | Cost: $0.163883 USD | Turns: 15

---

## Run: Issue #144 — Bash CLI mode

**Branch:** task/issue-144-bash-cli-mode
**Target branch:** exp2/structured-generic
**Date:** 2026-04-11

### Files changed
- `src/cli.py` — New module; implements argparse-based CLI with `build_parser()`, `_dispatch()`, and `cli_main()`. Supports all 12 operations (add, subtract, multiply, divide, power, square, cube, sqrt, cbrt, ln, log, factorial) as subcommands with positional operand arguments; `log` accepts an optional `--base` flag (default 10)
- `src/__main__.py` — Updated entry point: if `sys.argv[1:]` is non-empty, delegates to `cli_main()` (bash mode); otherwise runs the existing interactive `main()` (no change to interactive behaviour)
- `tests/test_cli.py` — New test file with 49 tests covering argument parsing (`build_parser`), operation routing (`_dispatch`), and end-to-end output (`cli_main`) including error cases (exit code 1 + stderr message)
- `artifacts/class_diagram.puml` — Added `cli` package with `build_parser`, `_dispatch`, and `cli_main` functions and their relationships; added mode-dispatch note on main
- `artifacts/activity_diagram.puml` — Added bash CLI mode branch (parse args → dispatch → print result / print error + exit 1) alongside existing interactive mode branch
- `artifacts/sequence_diagram.puml` — Added "Bash CLI Mode" section showing `User → cli_main → _dispatch → Calculator → stdout` interaction

### Purpose
Add bash CLI mode so the calculator can be invoked with a single command from the terminal, providing the operation and operands as arguments and reading the result from stdout (issue #144, V2 Task 7 - Structured/generic experiment). Interactive mode is preserved unchanged when no arguments are supplied.

### Risks
- The `factorial` subcommand uses `type=int` in argparse, so passing a float (e.g., `5.0`) will fail at parse time with a usage error. This is intentional — factorial only accepts integers.
- Error messages go to stderr; stdout receives only the result. This enables scripting (`result=$(python -m src add 3 4)`).
- The `__main__.py` entry-point check (`sys.argv[1:]`) is standard practice; it does not affect how `main()` is tested (tests call it directly).

### Test results
All 139 tests passed: 139 passed in 0.20s (90 existing + 49 new)

### Intended PR target
exp2/structured-generic

Duration: 320.8s | Cost: $0.986884 USD | Turns: 38

---

## Run: PlantUML diagram update

**Branch:** task/issue-114-user-input
**Date:** 2026-04-11

### Files changed
- `artifacts/class_diagram.puml` — Reviewed; accurately reflects current `src/` state (no update needed)
- `artifacts/activity_diagram.puml` — Reviewed; accurately reflects current `src/` state (no update needed)
- `artifacts/sequence_diagram.puml` — Reviewed; accurately reflects current `src/` state (no update needed)

### Purpose
Verify and maintain PlantUML diagrams against the current source code. All three diagrams (class, activity, sequence) correctly represent the `Calculator` class with all 12 operations and the interactive `__main__` module (display_menu, get_number, get_integer, perform_operation, main) as introduced in issue #114.

### Risks
- None; no source code was modified.

### Test results
N/A — diagram-only run.

Duration: 45.3s | Cost: $0.154416 USD | Turns: 14

---

## Run: Issue #114 — Interactive user input

**Branch:** task/issue-114-user-input
**Target branch:** exp2/structured-generic
**Date:** 2026-04-11

### Files changed
- `src/__main__.py` — Replaced static demo with interactive loop; added `display_menu()`, `get_number()`, `get_integer()`, `perform_operation()`, and updated `main()` to a `while True` session loop
- `tests/test_main.py` — New test file with 33 tests covering all interactive helpers and the main loop (mocked I/O via `unittest.mock.patch`)
- `artifacts/activity_diagram.puml` — Updated to show interactive loop flow with menu, dispatch, error handling
- `artifacts/sequence_diagram.puml` — Updated to show User/main/perform_operation/Calculator interaction in a loop
- `artifacts/class_diagram.puml` — Updated `__main__` package to reflect all four new functions and their relationships

### Purpose
Add interactive user input to the calculator so the user can select an operation and supply operands at runtime, see the result, and continue using the calculator without restarting (issue #114, V2 Task 5 - Structured/generic experiment). Input validation retries on bad values; errors from the Calculator (ValueError, ZeroDivisionError) are caught and displayed without crashing the session.

### Risks
- `get_integer` uses `int(raw)` which rejects floats like `"2.5"` — intentional, as factorial only accepts integers.
- `log` base input uses a separate `input()` call (not `get_number`) so the user can press Enter for the default; an invalid base falls back to 10 with a warning rather than looping.
- The type hint `str | None` in `perform_operation` uses a string literal for Python < 3.10 compatibility (`"str | None"`).

### Test results
All 90 tests passed: 90 passed in 0.13s (57 existing + 33 new)

### Intended PR target
exp2/structured-generic

Duration: 457.0s | Cost: $1.042459 USD | Turns: 36

---

## Run: PlantUML diagram update

**Branch:** task/issue-111-more-functions
**Date:** 2026-04-11

### Files changed
- `artifacts/class_diagram.puml` — Reviewed; accurately reflects current `src/` state (no update needed)
- `artifacts/activity_diagram.puml` — Reviewed; accurately reflects current `src/` state (no update needed)
- `artifacts/sequence_diagram.puml` — Reviewed; accurately reflects current `src/` state (no update needed)

### Purpose
Verify and maintain PlantUML diagrams against the current source code. All three diagrams (class, activity, sequence) correctly represent the `Calculator` class and `main()` flow as they exist in `src/`, including all 12 operations: add, subtract, multiply, divide, factorial, square, cube, square_root, cube_root, power, log, ln.

### Risks
- None; no source code was modified.

### Test results
N/A — diagram-only run.

Duration: 32.5s | Cost: $0.153726 USD | Turns: 13

---

## Run: Issue #111 — Add more calculator operations

**Branch:** task/issue-111-more-functions
**Target branch:** exp2/structured-generic
**Date:** 2026-04-11

### Files changed
- `src/calculator.py` — Added 7 new methods: `square`, `cube`, `square_root`, `cube_root`, `power`, `log`, `ln`
- `tests/test_calculator.py` — Added 30 tests covering all 7 new operations including error cases
- `src/__main__.py` — Added demonstration calls for all 7 new operations
- `artifacts/class_diagram.puml` — Added all 7 new methods and error notes for `square_root`, `log`, `ln`
- `artifacts/activity_diagram.puml` — Added activity forks for all 7 new operations with validation guards
- `artifacts/sequence_diagram.puml` — Added interaction sequences for all 7 new operations and extended error note

### Purpose
Add square, cube, square root, cube root, power, log, and ln as supported calculator operations (issue #111, V2 Task 4 - Structured/generic experiment). All operations delegate to Python built-ins (`math.sqrt`, `math.log`) where applicable; `square_root` raises `ValueError` for negative inputs; `log` and `ln` raise `ValueError` for non-positive inputs.

### Risks
- `cube_root` of negative numbers uses `-((-a) ** (1/3))` to handle negatives correctly, since Python's `**` with fractional exponent does not support negative bases.
- `log(a, base)` delegates to `math.log(a, base)` — floating-point precision applies.

### Test results
All 57 tests passed: 57 passed in 0.07s

### Intended PR target
exp2/structured-generic

Duration: 159.0s | Cost: $0.454938 USD | Turns: 24

---

## Run: PlantUML diagram update

**Branch:** task/issue-108-factorial
**Date:** 2026-04-11

### Files changed
- `artifacts/class_diagram.puml` — Reviewed; accurately reflects current `src/` state (no update needed)
- `artifacts/activity_diagram.puml` — Reviewed; accurately reflects current `src/` state (no update needed)
- `artifacts/sequence_diagram.puml` — Reviewed; accurately reflects current `src/` state (no update needed)

### Purpose
Verify and maintain PlantUML diagrams against the current source code. All three diagrams (class, activity, sequence) correctly represent the `Calculator` class and `main()` flow as they exist in `src/`, including the `factorial` method added in the previous run.

### Risks
- None; no source code was modified.

### Test results
N/A — diagram-only run.

Duration: 28.1s | Cost: $0.114785 USD | Turns: 13

---

## Run: Issue #108 — Add factorial operation

**Branch:** task/issue-108-factorial
**Target branch:** exp2/structured-generic
**Date:** 2026-04-11

### Files changed
- `src/calculator.py` — Added `factorial(n)` method using `math.factorial`; raises `ValueError` for negative or non-integer inputs
- `tests/test_calculator.py` — Added 6 tests for factorial: zero, one, positive, large value, negative raises, non-integer raises
- `src/__main__.py` — Added `factorial(5)` demonstration call
- `artifacts/class_diagram.puml` — Added `factorial(n) : int` to Calculator class and error note
- `artifacts/activity_diagram.puml` — Added factorial fork branch with input-validation guard
- `artifacts/sequence_diagram.puml` — Added `factorial(5)` → `120` interaction and extended note

### Purpose
Add factorial as a supported calculator operation (issue #108, V2 Task 3 - Structured/generic experiment). The implementation delegates to `math.factorial` and validates that the input is a non-negative integer before delegating.

### Risks
- Factorial only accepts integers; passing a float raises `ValueError`. This is intentional — factorial is not defined for non-integers in this implementation.
- `math.factorial` handles arbitrarily large integers natively; no overflow risk.

### Test results
All 27 tests passed: 27 passed in 0.04s

### Intended PR target
exp2/structured-generic

Duration: 157.9s | Cost: $0.535234 USD | Turns: 34

---

## Run: PlantUML diagram update

**Branch:** task/issue-105-unit-test-suite
**Date:** 2026-04-11

### Files changed
- `artifacts/class_diagram.puml` — Reviewed; accurately reflects current `src/` state (no update needed)
- `artifacts/activity_diagram.puml` — Reviewed; accurately reflects current `src/` state (no update needed)
- `artifacts/sequence_diagram.puml` — Reviewed; accurately reflects current `src/` state (no update needed)

### Purpose
Verify and maintain PlantUML diagrams against the current source code. All three diagrams (class, activity, sequence) correctly represent the `Calculator` class and `main()` flow as they exist in `src/`.

### Risks
- None; no source code was modified.

### Test results
N/A — diagram-only run.

Duration: 31.1s | Cost: $0.122905 USD | Turns: 14

---

## Run: Issue #105 — Unit test suite for all arithmetic operations

**Branch:** task/issue-105-unit-test-suite
**Target branch:** exp2/structured-generic
**Date:** 2026-04-11

### Files changed
- `tests/test_calculator.py` — Expanded from 1 test to 21 tests covering add, subtract, multiply, and divide

### Purpose
Create a comprehensive unit test suite for the calculator's existing arithmetic operations (issue #105, V2 Task 2 - structured/generic experiment). Tests cover positive/negative/float inputs, zero edge cases, and the ZeroDivisionError guard in divide.

### Risks
- No source code changed; risk is minimal.
- Tests use a shared `calc` fixture via `@pytest.fixture` which is standard pytest practice.

### Test results
All 21 tests passed: 21 passed in 0.02s

### Intended PR target
exp2/structured-generic

Duration: 124.5s | Cost: $0.330308 USD | Turns: 17

---

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
