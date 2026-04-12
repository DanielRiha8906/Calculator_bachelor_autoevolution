# Evolution Log

## Cycle 1 — Issue #208: ZeroDivisionTest (2026-04-12)
- **Task:** Add test for incorrect inputs in division (ZeroDivisionError)
- **Branch:** exp3/issue-208-zero-division-test
- **Files changed:** tests/test_calculator.py
- **Outcome:** Added `test_divide_by_zero_raises`; 1 test collected, 1 passed.
- **Key decisions:** Used `pytest.raises(ZeroDivisionError)` to assert built-in Python behavior — no changes needed to Calculator itself since `divide` already raises natively.
- **Cost:** PENDING
- **Turns:** PENDING

## Cycle 0 — Bootstrap (2026-04-12)
- **Task:** RAG initialization
- **Files changed:** rag/index.md, rag/codebase_map.md, rag/evolution_log.md, rag/patterns.md
- **Outcome:** RAG knowledge base created from current state of src/ and tests/
- **Lessons learned:** Project is minimal — one Calculator class with four arithmetic ops, and an empty test file.
- **Cost:** N/A (initialization)
- **Turns:** N/A
