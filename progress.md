
--- 2026-04-03: Issue #12 — User input for calculator ---
Files changed: src/calculator.py (added run_interactive()), tests/test_calculator.py (added TestRunInteractive with 11 tests), artifacts/calculator_sequence_diagram.puml (revised), artifacts/calculator_activity_diagram.puml (created)
Purpose: Replace hardcoded __main__ block with an interactive loop (run_interactive()) that prompts the user for an operation and two numbers, displays the result, and asks whether to continue or quit. Supports all four operations and handles invalid input gracefully.
Risks: No changes to the Calculator class itself — purely additive. The interactive function uses built-in input(), which is easily mocked in tests.
Testing: python -m pytest tests/ — 69 passed, 0 failed (58 original + 11 new interactive tests).

--- 2026-04-03: Issue #10 — Fix sequence diagram termination (PR #11 review) ---
Files changed: artifacts/calculator_sequence_diagram.puml (revised)
Purpose: Add explicit create/destroy lifecycle markers and an alt block showing both the valid-divisor and divide-by-zero paths. Adds a termination note clarifying the program runs once and exits — addressing reviewer question about how the sequence ends.
Risks: Documentation-only change; no production code or tests modified.
Testing: python -m pytest tests/ — 58 passed, 0 failed.

--- 2026-04-03: Issue #10 — Development artifacts in PlantUML ---
Files changed: artifacts/calculator_class_diagram.puml (created), artifacts/calculator_sequence_diagram.puml (created)
Purpose: Add PlantUML artifacts for the Calculator class. Includes a class diagram documenting all four public methods and their signatures, and a sequence diagram illustrating typical usage including the divide-by-zero error case.
Risks: Documentation-only change; no production code or tests modified.
Testing: python3 -m pytest tests/ — 58 passed, 0 failed.

--- 2026-04-03: Issue #7 — Development artifacts folder ---
Files changed: artifacts/calculator_class_diagram.md (created)
Purpose: Add artifacts/ folder with a Mermaid class diagram for calculator.py. The diagram documents all public methods of the Calculator class and must be kept in sync with future additions to the file.
Risks: Documentation-only change; no production code or tests modified.
Testing: python -m pytest tests/ — 58 passed, 0 failed.

--- 2026-04-03: Issue #4 — Complete test suite for calculator.py ---
Files changed: src/test_calculator.py (expanded from 1 test to 58 tests)
Purpose: Add comprehensive unit tests for all four Calculator methods (add, subtract, multiply, divide). Each method now has tests for standard behavior, edge cases, invalid input, and large/precision values.
Risks: No production code was modified. calculator.py is unchanged.
Testing: python -m pytest src/test_calculator.py — 58 passed, 0 failed.

--- 2026-04-02: Issue #2 — Add division by zero test ---
Files changed: src/test_calculator.py (created)
Purpose: Add unit test asserting Calculator.divide raises ValueError when denominator is 0.
Risks: None — no production code was modified.
Testing: pytest src/test_calculator.py — 1 passed, 0 failed.
