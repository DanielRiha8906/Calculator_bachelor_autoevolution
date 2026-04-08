
--- 2026-04-08: Issue #13 (exp/expert-generic) — Comprehensive unit test suite ---
Files changed: tests/test_calculator.py (expanded from 1 to 32 tests)
Purpose: Add full test coverage for add, subtract, multiply, divide — normal inputs and edge cases (floats, negatives, zero, large numbers, division-by-zero).
Risks: None — no production code modified.
Testing: python3 -m pytest tests/test_calculator.py -v — 32 passed, 0 failed.
Tokens used: ~5 000 (estimated) | Cost: ~$0.02 | Turns: 1
Branch: task/issue-13-test-suite-expert-generic | PR target: exp/expert-generic (PR #21)

--- 2026-04-08: Issue #8 (exp/expert-generic) — Division by zero test ---
Files changed: tests/test_calculator.py (added test_divide_by_zero_raises)
Purpose: Assert that Calculator.divide(1, 0) raises ZeroDivisionError. No implementation change needed — Python's / operator already raises ZeroDivisionError natively.
Risks: None — no production code modified.
Testing: python -m pytest tests/test_calculator.py -v — 1 passed, 0 failed.
Tokens used: ~3 000 (estimated) | Cost: ~$0.01 | Turns: 1
Branch: task/issue-8-division-by-zero | PR target: exp/expert-generic (PR #11)

