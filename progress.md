
--- 2026-04-08: Issue #37 (exp/expert-generic) — Add square, cube, sqrt, cbrt, power, log, ln ---
Files changed: src/calculator.py (added 7 methods), tests/test_calculator.py (added 36 tests across 7 new test classes)
Purpose: Implement square, cube, square_root, cube_root, power, log (base-10), and ln operations; raise ValueError for invalid domains (sqrt of negative, log/ln of ≤0).
Risks: cube_root uses sign-preserving fractional exponent to handle negative inputs correctly; floating-point results use math.isclose in tests.
Testing: python3 -m pytest tests/test_calculator.py -v — 76 passed, 0 failed.
Duration: PENDING | Cost: PENDING | Turns: PENDING
Branch: task/issue-37-math-functions-expert-generic | PR target: exp/expert-generic

--- 2026-04-08: Issue #25 (exp/expert-generic) — Add factorial operation ---
Files changed: src/calculator.py (added factorial method + import math), tests/test_calculator.py (added TestFactorial with 8 tests)
Purpose: Implement Calculator.factorial(n) for non-negative integers; reject negatives (ValueError) and non-integers including booleans (TypeError).
Risks: None — uses stdlib math.factorial, no new dependencies.
Testing: python -m pytest tests/test_calculator.py -v — 40 passed, 0 failed.
Tokens used: ~6 000 (estimated) | Cost: ~$0.03 | Turns: 1
Branch: task/issue-25-factorial-expert-generic | PR target: exp/expert-generic (PR #27)

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

