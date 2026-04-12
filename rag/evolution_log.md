# Evolution Log

Per-cycle entries: task, files changed, outcome, lessons learned.

---

## Cycle 2 — Issue #213: Comprehensive unit test suite

- **Task:** Create a full unit test suite covering all Calculator operations with normal inputs and edge cases.
- **Files changed:** `tests/test_calculator.py` (replaced 1-test file with 24-test suite in 4 classes)
- **Test result:** 24 passed
- **Key decisions:** Used `math.isclose` for float comparisons to avoid precision issues. Used `None` as invalid type for `multiply` since `None * int` raises `TypeError` (unlike `str * int` which is valid Python). Organized by operation class for readability.
- **Cost:** PENDING
- **Turns:** PENDING

---

## Cycle 1 — Issue #210: ZeroDivisionError test coverage

- **Task:** Add focused test asserting `Calculator.divide` raises `ZeroDivisionError` when divisor is zero.
- **Files changed:** `tests/test_calculator.py` (added `test_divide_by_zero_raises`)
- **Test result:** 1 passed
- **Key decisions:** Implementation already raises correctly via Python `/` operator; no source change needed. Test is additive only.
- **Cost:** PENDING
- **Turns:** PENDING

---

## Cycle 0 — Bootstrap (RAG initialization)

- **Task:** Initial RAG setup; no code changes.
- **Files changed:** `rag/index.md`, `rag/codebase_map.md`, `rag/evolution_log.md`, `rag/patterns.md`
- **Test result:** N/A
- **Key decisions:** Summarized existing src/ and tests/ into RAG. `tests/test_calculator.py` has imports but no test bodies.
- **Cost:** N/A
- **Turns:** N/A
