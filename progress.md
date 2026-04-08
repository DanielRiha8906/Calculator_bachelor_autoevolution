
--- 2026-04-08: Issue #66 — Error logging (Task 10, Naive/generic) ---
Files changed: src/calculator.py (added `import logging`, module-level `logger = logging.getLogger(__name__)`, and `logger.error(...)` calls before each raise in divide, factorial, square_root, log, and ln), tests/test_calculator.py (added TestCalculatorErrorLogging class, 8 new tests using pytest caplog fixture), artifacts/class_diagram.puml (updated note to mention error logging)
Purpose: Add error logging to the Calculator so that every invalid-input condition (division by zero, bad factorial argument, negative square root, non-positive log/ln domain) is recorded at ERROR level via Python's standard logging module. Successful operations produce no error logs.
Risks: Low — additive change only. No existing behaviour modified; exceptions still propagate unchanged. Uses Python stdlib logging (no new dependency). Existing 118 tests unaffected.
Testing: python3 -m pytest tests/test_calculator.py -v — 126 passed, 0 failed.
Duration: PENDING | Cost: PENDING | Turns: PENDING
Branch: task/issue-66-error-logging. PR target: exp/naive-generic.

--- 2026-04-08: Issue #63 — History of operations (Task 9, Naive/generic) ---
Files changed: src/calculator.py (added __init__, _record, get_history, clear_history; all 13 operation methods updated to call _record on success), src/__main__.py (added HISTORY_OPS constant; run_interactive now handles 'history' and 'clear_history' commands; welcome message updated), tests/test_calculator.py (added TestCalculatorHistory class with 10 tests; added TestRunInteractiveHistory class with 6 tests), artifacts/class_diagram.puml (added _history field and new methods), artifacts/activity_diagram.puml (added history/clear_history branches in interactive flow), artifacts/sequence_diagram.puml (added history/clear_history interactions)
Purpose: Add a history of operations to the Calculator class. Each successful operation is appended to an internal list (_history). The get_history() method returns a copy; clear_history() resets it. In interactive mode, users can type 'history' to see a numbered list of past operations or 'clear_history' to reset it. Failed operations are never recorded.
Risks: Low — additive change. Calculator class now has __init__ (previously relied on implicit object()); all existing tests still pass. run_cli is untouched. get_history() returns a shallow copy to prevent external mutation of the internal list.
Testing: python -m pytest tests/test_calculator.py -v — 118 passed, 0 failed.
Duration: 264.0s | Cost: $0.862664 USD | Turns: 35
Branch: task/issue-63-history. PR target: exp/naive-generic.

--- 2026-04-08: Issue #60 — Input validation with retry logic (Task 8, Naive/generic) ---
Files changed: src/__main__.py (added MAX_INPUT_RETRIES constant and _read_number helper; refactored run_interactive to use per-number retry loop), tests/test_calculator.py (updated 3 existing tests to supply enough inputs for retry; added 3 new tests for retry behavior), artifacts/activity_diagram.puml (updated interactive path to show retry loops), artifacts/sequence_diagram.puml (updated interactive path to show retry loops)
Purpose: When the user enters an invalid number in interactive mode, prompt them again up to MAX_INPUT_RETRIES (3) times before returning to the operation selection menu. CLI mode is unchanged (single-shot, exit code 1 on bad input).
Risks: Low — run_cli is untouched; the Calculator class is untouched. Existing interactive tests updated to provide enough canned inputs to exhaust or satisfy the retry loop. _read_number returns None on exhaustion so the caller uses continue to return to operation selection.
Testing: python -m pytest tests/test_calculator.py -v — 102 passed, 0 failed.
Duration: 236.8s | Cost: $0.597701 USD | Turns: 20
Branch: task/issue-60-input-validation. PR target: exp/naive-generic.

--- 2026-04-08: Issue #45 — Add CLI bash mode (Task 7, Naive/generic) ---
Files changed: src/__main__.py (added run_cli function, updated main to dispatch on sys.argv), tests/test_calculator.py (added TestRunCLI class, 24 new tests), artifacts/activity_diagram.puml (updated to show CLI path), artifacts/sequence_diagram.puml (updated to show CLI vs interactive paths)
Purpose: Expose all Calculator operations as a non-interactive CLI so the calculator can be driven from bash scripts and one-liners (e.g. python -m src add 5 3). When sys.argv has arguments, main() dispatches to run_cli(); when invoked with no arguments the existing interactive REPL is preserved.
Risks: Low — run_cli is additive; run_interactive and Calculator are unchanged. sys.exit is called on the CLI path so callers get a proper exit code.
Testing: python -m pytest tests/test_calculator.py -v — 99 passed, 0 failed.
Duration: 208.7s | Cost: $0.612450 USD | Turns: 24
Branch: task/issue-45-bash-mode. PR target: exp/naive-generic.

--- 2026-04-08: Issue #42 — Add diagrams (Task 6, Naive/generic) ---
Files changed: artifacts/class_diagram.puml (new), artifacts/activity_diagram.puml (new), artifacts/sequence_diagram.puml (new)
Purpose: Create PlantUML class, activity, and sequence diagrams documenting the Calculator class and interactive session flow, as required by CLAUDE.md artifacts policy.
Risks: None — documentation only; no source code or tests modified.
Testing: python3 -m pytest tests/ -v — 75 passed, 0 failed.
Duration: 138.8s | Cost: $0.321491 USD | Turns: 19
Branch: task/issue-42-diagrams. PR target: exp/naive-generic.

--- 2026-04-08: Issue #38 — Add user input to the calculator (Task 5, Naive/generic) ---
Files changed: src/__main__.py (replaced demo main with run_interactive loop), tests/test_calculator.py (added TestRunInteractive class, 19 new tests)
Purpose: Expose all Calculator operations through an interactive REPL so users can enter operations and numbers at runtime instead of hardcoded values.
Risks: None — additive change; calculator.py is untouched. run_interactive accepts injectable input_fn/output_fn for testability.
Testing: python3 -m pytest tests/test_calculator.py -v — 75 passed, 0 failed.
Duration: 153.0s | Cost: $0.416516 USD | Turns: 20
Branch: task/issue-38-user-input. PR target: exp/naive-generic.

--- 2026-04-08: Issue #35 — Add multiple math functions (Task 4, Naive/generic) ---
Files changed: src/calculator.py (import math + 7 new methods: square, cube, square_root, cube_root, power, log, ln), tests/test_calculator.py (7 new test classes, 31 new tests)
Purpose: Extend Calculator with square, cube, square root, cube root, power, base-10 log, and natural log operations.
Risks: None — purely additive; no existing methods modified. square_root and log/ln raise ValueError for invalid domains.
Testing: python -m pytest tests/test_calculator.py -v — 56 passed, 0 failed.
Duration: 111.4s | Cost: $0.297980 USD | Turns: 17
Branch: task/issue-35-math-functions. PR target: exp/naive-generic.

--- 2026-04-08: Issue #9 — Create tests for the calculator (Task 2, Unstructured/gen) ---
Files changed: tests/test_calculator.py (60 lines added — TestAdd x5, TestSubtract x5, TestMultiply x5)
Purpose: Extend the test suite to cover add, subtract, and multiply operations. Previously only divide() was tested.
Risks: None — tests only, no source code modified.
Testing: python -m pytest tests/test_calculator.py -v — 19 passed, 0 failed.
Tokens: n/a (autonomous run). Cost: n/a. Turns: 1.
Branch: task/issue-9-test-suite. PR target: exp/naive-generic (PR #22).

--- 2026-04-08: Issue #23 — Add factorial to the calculator (Task 3, Naive/generic) ---
Files changed: src/calculator.py (factorial method, 9 lines), tests/test_calculator.py (TestFactorial class, 6 tests)
Purpose: Implement Calculator.factorial(n) returning n! for non-negative integers, raising ValueError for negative n and TypeError for non-integers.
Risks: None — additive change, no existing methods modified.
Testing: python -m pytest tests/test_calculator.py -v — 25 passed, 0 failed.
Tokens: n/a (autonomous run). Cost: n/a. Turns: 1.
Branch: task/issue-23-factorial. PR target: exp/naive-generic.

--- 2026-04-08: Issue #3 — Add tests for incorrect inputs in division ---
Files changed: src/calculator.py (raise ValueError on division by zero), tests/test_calculator.py (4 new tests)
Purpose: Make Calculator.divide() raise ValueError with a descriptive message when the divisor is zero, and add tests covering zero denominator with positive, negative, and zero numerator plus a normal-division smoke test.
Risks: Callers that previously caught ZeroDivisionError must now catch ValueError. Minimal blast radius — calculator is only used internally.
Testing: python3 -m pytest tests/test_calculator.py -v — 4 passed, 0 failed.
Tokens: n/a (autonomous run). Cost: n/a. Turns: 1.
Branch: task/issue-3-division-zero-test. PR target: exp/naive-generic (PR #5).
