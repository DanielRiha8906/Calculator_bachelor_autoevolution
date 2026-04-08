
--- 2026-04-08: Issue #44 (exp/expert-generic) — Add PlantUML diagrams ---
Files changed: artifacts/class_diagram.puml (new), artifacts/activity_diagram.puml (new), artifacts/sequence_diagram.puml (new)
Purpose: Document the calculator's structure and user interaction with three PlantUML diagrams: class diagram for the Calculator class and __main__ module, activity diagram for the user interaction loop, and sequence diagram for a typical session including error paths.
Risks: None — documentation only, no source code modified.
Testing: python -m pytest — 94 passed, 0 failed (no code changes, existing suite still green).
Duration: PENDING | Cost: PENDING | Turns: PENDING
Branch: task/issue-44-add-diagrams-expert-generic | PR target: exp/expert-generic

--- 2026-04-08: Issue #40 (exp/expert-generic) — Add interactive user input ---
Files changed: src/__main__.py (replaced hardcoded demo with interactive session loop), tests/test_calculator.py (added TestMain class with 18 tests)
Purpose: Replace the hardcoded demo in __main__.py with a menu-driven REPL that reads operation choice and operands at runtime. Handles one-operand operations (factorial, square, cube, sqrt, cbrt, log, ln) and two-operand operations (add, subtract, multiply, divide, power) with appropriate prompts. Session loops until user enters 0. Errors (ValueError, ZeroDivisionError, TypeError) are caught and displayed without crashing the session.
Risks: factorial input is accepted as float from _read_number and then validated as a whole number before conversion to int — input like "5.5" is rejected cleanly.
Testing: python3.12 -m pytest tests/test_calculator.py -v — 94 passed, 0 failed (76 original + 18 new TestMain tests).
Duration: 200.7s | Cost: $0.502824 USD | Turns: 19
Branch: task/issue-40-user-input-expert-generic | PR target: exp/expert-generic

--- 2026-04-08: Issue #37 (exp/expert-generic) — Add square, cube, sqrt, cbrt, power, log, ln ---
Files changed: src/calculator.py (added 7 methods), tests/test_calculator.py (added 36 tests across 7 new test classes)
Purpose: Implement square, cube, square_root, cube_root, power, log (base-10), and ln operations; raise ValueError for invalid domains (sqrt of negative, log/ln of ≤0).
Risks: cube_root uses sign-preserving fractional exponent to handle negative inputs correctly; floating-point results use math.isclose in tests.
Testing: python3 -m pytest tests/test_calculator.py -v — 76 passed, 0 failed.
Duration: 131.4s | Cost: $0.327596 USD | Turns: 15
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

