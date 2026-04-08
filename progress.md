
--- 2026-04-08: Issue #3 — Add tests for incorrect inputs in division ---
Files changed: src/calculator.py (raise ValueError on division by zero), tests/test_calculator.py (4 new tests)
Purpose: Make Calculator.divide() raise ValueError with a descriptive message when the divisor is zero, and add tests covering zero denominator with positive, negative, and zero numerator plus a normal-division smoke test.
Risks: Callers that previously caught ZeroDivisionError must now catch ValueError. Minimal blast radius — calculator is only used internally.
Testing: python3 -m pytest tests/test_calculator.py -v — 4 passed, 0 failed.
Tokens: n/a (autonomous run). Cost: n/a. Turns: 1.
Branch: task/issue-3-division-zero-test. PR target: exp/naive-generic (PR #5).
