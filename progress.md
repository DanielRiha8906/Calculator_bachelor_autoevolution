
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
