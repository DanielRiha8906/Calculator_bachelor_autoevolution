# Evolution Log

Per-cycle entries: task, files changed, outcome, lessons learned.

---

## Cycle 3 — Issue #216: Add factorial operation

- **Task:** Add `factorial` as a supported calculator operation with proper input validation.
- **Files changed:** `src/calculator.py` (added `factorial` method), `tests/test_calculator.py` (added 10 factorial tests; total now 38)
- **Test result:** 38 passed
- **Key decisions:** Rejected booleans explicitly (`isinstance(n, bool)` guard before `isinstance(n, int)`) since `bool` is a subclass of `int` in Python. Implemented iteratively to avoid recursion overhead. Raises `TypeError` for non-integer types, `ValueError` for negatives.
- **Cost:** PENDING
- **Turns:** PENDING

---

## Cycle 2 — Issue #213: Comprehensive test suite

- **Task:** Create a unit test suite for all Calculator operations covering normal inputs and edge cases.
- **Files changed:** `tests/test_calculator.py` (expanded from 1 to 28 tests; added fixture, full add/subtract/multiply/divide coverage with float, zero, negative, and large-number cases)
- **Test result:** 28 passed
- **Key decisions:** Used `pytest.approx` for float comparisons; kept existing `test_divide_by_zero_raises` intact and added `test_divide_by_zero_float_raises`; no source changes required.
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
