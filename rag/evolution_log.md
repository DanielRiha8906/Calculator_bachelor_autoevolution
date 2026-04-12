# Evolution Log

Per-cycle entries: task, files changed, outcome, lessons learned.

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
