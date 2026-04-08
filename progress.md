
--- 2026-04-08: Issue #24 — Add factorial operation (structured-generic) ---
Files changed: src/calculator.py, tests/test_calculator.py
Purpose: Added Calculator.factorial(n) method supporting non-negative integers; raises ValueError for negative or non-integer inputs. Added 6 tests covering zero, one, positive values, large values, negative input error, and non-integer input error.
Risks: Minimal — new method only; no existing methods modified.
Testing: python3 -m pytest tests/test_calculator.py — 26 passed, 0 failed.
Tokens used: ~3,000 (estimated). Cost: ~$0.01 (estimated). Turns: 1.
Branch: task/factorial-structured-generic. PR targeting exp/structured-generic.

--- 2026-04-08: Issue #10 — Unit test suite for all arithmetic operations (structured-generic) ---
Files changed: tests/test_calculator.py
Purpose: Expanded the test suite from 1 test (divide-by-zero) to 20 tests covering add, subtract, multiply, and divide with positive, negative, float, and zero inputs; preserves the existing divide-by-zero assertion.
Risks: None — tests only; no source code changed.
Testing: python -m pytest tests/test_calculator.py — 20 passed, 0 failed.
Tokens used: ~3,000 (estimated). Cost: ~$0.01 (estimated). Turns: 1.
Branch: task/test-suite-structured-generic. PR targeting exp/structured-generic.

--- 2026-04-08: Issue #7 — ZeroDivisionError handling (structured-generic) ---
Files changed: src/calculator.py, tests/test_calculator.py
Purpose: Raise ValueError("Cannot divide by zero") explicitly in Calculator.divide instead of propagating Python's raw ZeroDivisionError. Added unit test test_divide_by_zero_raises_value_error to assert the correct exception and message.
Risks: Minimal — only the divide method is touched. Existing callers catching ZeroDivisionError would need to be updated to catch ValueError, but no such callers exist in this codebase.
Testing: python3 -m pytest tests/test_calculator.py — 1 passed, 0 failed.
Tokens used: ~2,000 (estimated). Cost: ~$0.01 (estimated). Turns: 1.
Branch: task/zero-division-error-structured. PR: #12 targeting exp/structured-generic.
