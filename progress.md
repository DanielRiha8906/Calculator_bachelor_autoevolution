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
