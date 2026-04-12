## Run: issue-210 — ZeroDivisionError test coverage

- **Branch:** exp3/issue-210-zerodivision-test
- **PR target:** exp3/expert-generic
- **Files changed:**
  - `tests/test_calculator.py` — added `test_divide_by_zero_raises` asserting `ZeroDivisionError` on `divide(1, 0)`
- **Purpose:** Add focused test coverage asserting that `Calculator.divide` raises `ZeroDivisionError` when divisor is zero. Implementation already raises correctly via Python's `/` operator; no source change required.
- **Risks:** None — additive test only, no logic modified.
- **Tests passed:** Yes — `1 passed in 0.01s`
- **RAG entries consulted:** `rag/codebase_map.md` (codebase map, initialized this run), `rag/index.md`
- **Duration:** PENDING | Cost: PENDING | Turns: PENDING
