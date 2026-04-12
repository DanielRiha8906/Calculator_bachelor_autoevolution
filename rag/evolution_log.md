# Evolution Log

Per-cycle entries: task, files changed, outcome, lessons learned.

---

## Cycle 5 — Issue #221: Interactive user input (2026-04-12)

- **Task:** Add interactive user input so the calculator reads the selected operation and required values at runtime; allow the user to continue after each result.
- **Files changed:** `src/__main__.py`, `tests/test_main.py` (new)
- **Outcome:** 91 tests pass (63 existing + 28 new). `src/__main__.py` replaced with a full interactive loop; `tests/test_main.py` added.
- **Key decisions:**
  - Implemented `show_menu()`, `parse_number()`, `parse_int()`, and `run_operation()` as standalone helpers so each concern is testable in isolation.
  - `parse_number` and `parse_int` retry indefinitely on invalid input, printing a clear error message, rather than propagating exceptions — this keeps the UX smooth.
  - `run_operation` catches `ValueError` from Calculator methods and prints it as a user-facing error without crashing the loop.
  - `OPERATIONS` dict maps string keys `"1"`–`"12"` to operation names, keeping the menu and dispatch logic in sync with a single source of truth.
  - Tests use `unittest.mock.patch("builtins.input", side_effect=[...])` to supply canned inputs; `capsys` verifies stdout content.
- **Cost:** PENDING | **Turns:** PENDING

---

## Cycle 4 — Issue #218: Multiple math operations (2026-04-12)

- **Task:** Add square, cube, square_root, cube_root, power, log, and ln as supported Calculator operations with tests.
- **Files changed:** `src/calculator.py`, `tests/test_calculator.py`
- **Outcome:** 63 tests pass. Added 7 new Calculator methods. Added 33 new tests.
- **Key decisions:**
  - `cube_root` uses a sign-preserving trick `-((-a)**(1/3))` for negative inputs, since Python's `a**(1/3)` produces a complex number for negative `a`.
  - `log` validates both `a > 0` and `base > 0 and base != 1` before delegating to `math.log(a, base)`.
  - `ln` is a thin wrapper around `math.log(a)` with a `a > 0` guard.
  - `square` and `cube` are pure `**` expressions — no guards needed.
  - `power` accepts any real exponent via `**`; no special-casing needed.
- **Lessons learned:** Python `(-8)**(1/3)` returns a complex number, not `-2.0`; the sign-preserving `-(abs(a)**(1/3))` idiom is required for real cube roots of negative numbers.
- **Cost:** PENDING | **Turns:** PENDING

---

## Cycle 3 — Issue #215: Factorial operation (2026-04-12)

- **Task:** Add `factorial` as a supported calculator operation with correct input validation and tests.
- **Files changed:** `src/calculator.py`, `tests/test_calculator.py`
- **Outcome:** 30 tests pass. Added `Calculator.factorial(n)` using `math.factorial`; raises `ValueError` for negative or non-integer inputs. Added 6 tests covering zero, small value, large value, negative input, and float input.
- **Key decisions:** Used `math.factorial` from the standard library rather than a manual implementation — it is correct, well-tested, and handles arbitrarily large integers natively. Non-integer (float) inputs are rejected with `isinstance` check before delegating to `math.factorial` since `math.factorial(3.0)` raises `TypeError` in Python 3.12 rather than `ValueError`, which would break the API contract.
- **Lessons learned:** `math.factorial` raises `TypeError` for floats in Python 3.12, so an explicit `isinstance(n, int)` guard is needed to produce a consistent `ValueError` for all invalid input types.

---

## Cycle 2 — Issue #212: Full test suite (2026-04-12)

- **Task:** Create a unit test suite covering all arithmetic operations and verify expected results are valid inputs.
- **Files changed:** `tests/test_calculator.py`
- **Outcome:** 24 tests pass. Added 21 new tests for `add`, `subtract`, `multiply`, and expanded `divide` coverage. No source changes required.
- **Key decisions:** Kept all existing divide tests intact; grouped new tests by operation using comment headers; used `math.isclose` for float assertions to avoid floating-point precision failures.
- **Lessons learned:** Float comparisons require `math.isclose`; identity-element tests (add 0, multiply by 1) are cheap and verify boundary correctness explicitly.

---

## Cycle 1 — Issue #209: ZeroDivisionError (2026-04-12)

- **Task:** Add unit test for division by zero; fix `divide` to handle it correctly.
- **Files changed:** `src/calculator.py`, `tests/test_calculator.py`
- **Outcome:** All 3 tests pass. `divide` now raises `ValueError` on zero divisor.
- **Key decisions:** Raise `ValueError` (not `ZeroDivisionError`) to give a clear, explicit message. Added two additional tests (normal division, negative denominator) alongside the required guard test.
- **Lessons learned:** Raw Python `ZeroDivisionError` is an uncontrolled exception; explicit `ValueError` with message is cleaner for downstream consumers.

---

## Cycle 0 — Bootstrap (2026-04-12)

- **Task:** RAG initialization (no implementation task)
- **Files changed:** rag/index.md, rag/codebase_map.md, rag/evolution_log.md, rag/patterns.md (created)
- **Outcome:** RAG initialized from current state of src/ and tests/
- **Lessons learned:** Initial state — Calculator has no ZeroDivisionError guard in divide().
