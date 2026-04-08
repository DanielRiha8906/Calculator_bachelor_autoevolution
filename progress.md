
--- 2026-04-08: Issue #43 — Add PlantUML diagrams (structured-generic) ---
Files changed: artifacts/class_diagram.puml, artifacts/activity_diagram.puml, artifacts/sequence_diagram.puml
Purpose: Created three PlantUML documentation diagrams in artifacts/ covering the Calculator class structure (class diagram), the interactive calculator loop (activity diagram), and the component interaction flow (sequence diagram).
Risks: Docs-only change; no source or test files modified.
Testing: No executable tests needed — diagram syntax is declarative PlantUML. Existing 77 tests unaffected (not re-run since no source changed).
Duration: PENDING | Cost: PENDING | Turns: PENDING
Branch: task/issue-43-add-diagrams. PR targeting exp/structured-generic.

--- 2026-04-08: Issue #39 — Add interactive user input (structured-generic) ---
Files changed: src/__main__.py, tests/test_main.py
Purpose: Replaced hardcoded demo in __main__.py with an interactive loop. Users can select any of the 12 calculator operations by number, enter the required operands, see the result, and choose to continue or quit. Invalid input and math errors are shown as messages; the loop offers "Continue? (y/n)" after each operation. Added tests/test_main.py with 20 tests covering all operations, error paths, invalid choice, continue loop, and quit.
Risks: Minimal — Calculator class unchanged; only the entry point and a new test file added.
Testing: python3 -m pytest tests/ — 77 passed, 0 failed.
Duration: PENDING | Cost: PENDING | Turns: PENDING
Branch: task/user-input-structured-generic. PR targeting exp/structured-generic.

--- 2026-04-08: Issue #36 — Add square, cube, sqrt, cbrt, power, log, ln (structured-generic) ---
Files changed: src/calculator.py, tests/test_calculator.py
Purpose: Added 7 new Calculator methods: square, cube, sqrt, cbrt, power, log (base 10), ln. sqrt, log, and ln raise ValueError for invalid inputs (negative/non-positive). Added 31 tests covering normal values, edge cases, and error paths for each new method.
Risks: Minimal — new methods only; no existing methods modified. math.cbrt requires Python 3.11+; project uses Python 3.12.
Testing: python -m pytest tests/test_calculator.py — 57 passed, 0 failed.
Duration: 127.4s | Cost: $0.33351364999999994 USD | Turns: 16
Branch: task/add-math-functions-structured-generic. PR targeting exp/structured-generic.

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
