# Evolution Log

Per-cycle entries: task, files changed, outcome, lessons learned.

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
