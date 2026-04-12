# Evolution Log

## Cycle 3 — Issue #214: Add Factorial (2026-04-12)
- **Task:** Add factorial operation to Calculator
- **Branch:** exp3/issue-214-add-factorial
- **Files changed:** src/calculator.py, tests/test_calculator.py
- **Outcome:** Added `Calculator.factorial(n)` via `math.factorial`; 28 tests collected, 28 passed.
- **Key decisions:** Used `math.factorial` from stdlib to delegate validation (raises `ValueError` for negatives), consistent with existing pattern of relying on Python built-in behavior. Added `import math` at module level.
- **Cost:** PENDING
- **Turns:** PENDING

## Cycle 2 — Issue #211: Calculator Test Suite (2026-04-12)
- **Task:** Create comprehensive tests for the Calculator class
- **Branch:** exp3/issue-211-calculator-tests
- **Files changed:** tests/test_calculator.py, progress.md
- **Outcome:** Expanded from 1 test to 23 tests; 23 collected, 23 passed.
- **Key decisions:** Retained existing `test_divide_by_zero_raises`. Added 5 tests per arithmetic operation (add, subtract) and 6 for multiply, 7 for divide — covering positive, negative, mixed-sign, zero, float, and boundary (identity element) inputs. Used `pytest.approx` for float comparisons.
- **Cost:** PENDING
- **Turns:** PENDING

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
