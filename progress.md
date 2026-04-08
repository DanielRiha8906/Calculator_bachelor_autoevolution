
--- 2026-04-08: Issue #7 — ZeroDivisionError handling (structured-generic) ---
Files changed: src/calculator.py, tests/test_calculator.py
Purpose: Raise ValueError("Cannot divide by zero") explicitly in Calculator.divide instead of propagating Python's raw ZeroDivisionError. Added unit test test_divide_by_zero_raises_value_error to assert the correct exception and message.
Risks: Minimal — only the divide method is touched. Existing callers catching ZeroDivisionError would need to be updated to catch ValueError, but no such callers exist in this codebase.
Testing: python3 -m pytest tests/test_calculator.py — 1 passed, 0 failed.
Tokens used: ~2,000 (estimated). Cost: ~$0.01 (estimated). Turns: 1.
Branch: task/zero-division-error-structured. PR: #12 targeting exp/structured-generic.
