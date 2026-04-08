
--- 2026-04-08: Issue #67 — Error logging (structured-generic) ---
Files changed: src/__main__.py, tests/test_main.py, artifacts/class_diagram.puml, artifacts/activity_diagram.puml, artifacts/sequence_diagram.puml
Purpose: Added error logging to the calculator. Failures and invalid-usage events (invalid operation choice, invalid operands, unsupported operations, and calculation errors) are now appended as timestamped lines to calculator_errors.log. The log is separate from history.txt so normal operation history is never mixed with errors. Implementation uses a single _log_error(path, message) helper consistent with the existing _append_history pattern. Added ERROR_LOG_FILE constant and error_log_file parameter to run_calculator() and run_bash_mode() for test isolation. Added 7 new tests covering: invalid choice logging, calc error logging in interactive mode, bash unknown operation, bash calc error, bash invalid input, bash wrong arg count, and absence of log file on success.
Risks: Minimal — Calculator class unchanged. The only new I/O is file appends to calculator_errors.log. Existing tests unaffected because they do not pass error_log_file, so errors are written to the default path in the test working directory (not asserted). New tests use tmp_path for isolation.
Testing: python -m pytest tests/ — 115 passed, 0 failed.
Duration: PENDING | Cost: PENDING | Turns: PENDING
Branch: task/issue-67-error-logging-structured-generic. PR targeting exp/structured-generic.

--- 2026-04-08: Issue #64 — History (structured-generic) ---
Files changed: src/__main__.py, tests/test_main.py, artifacts/class_diagram.puml, artifacts/activity_diagram.puml, artifacts/sequence_diagram.puml, .gitignore
Purpose: Added session history to the interactive calculator. Each successful operation is recorded in history.txt (format: "op(operands) = result"). The file is cleared at the start of every session so history never persists between runs. Users can type 'h' at the operation prompt to display all calculations from the current session; 'h' does not consume a retry attempt. Bash mode is unaffected. Added HISTORY_FILE constant and three private helpers (_clear_history, _append_history, _show_history). Added history_file parameter to run_calculator() for test isolation. Added five new tests covering empty history, single-operation recording, multi-operation accumulation, session clearing, and 'h' not consuming an attempt. Updated all three PlantUML diagrams to reflect the new history flow. Added history.txt to .gitignore.
Risks: Minimal — Calculator class unchanged; bash mode unchanged. The only new I/O is file writes to history.txt in the working directory. Tests use tmp_path so no cross-test file contamination.
Testing: python3 -m pytest tests/ — 108 passed, 0 failed.
Duration: 446.2s | Cost: $0.924571 USD | Turns: 26
Branch: task/issue-64-history-structured-generic. PR targeting exp/structured-generic.

--- 2026-04-08: Issue #61 — Input validation with retry logic (structured-generic) ---
Files changed: src/__main__.py, tests/test_main.py, artifacts/activity_diagram.puml, artifacts/sequence_diagram.puml
Purpose: Added MAX_ATTEMPTS=3 retry loop to the interactive mode so invalid operation choice and invalid operand input prompt the user to try again instead of crashing or looping indefinitely. After exhausting all retries the session ends with a clear "Ending session" message. Added _parse_float() helper used by both modes to emit "'<val>' is not a valid number" instead of Python's raw float() error. Fixed three existing tests that assumed single-attempt error handling; added six new tests covering retry-then-success, max-attempt exhaustion, and bash-mode non-numeric input. Updated activity and sequence diagrams to document the retry paths.
Risks: Minimal — no Calculator class changes; behaviour change is confined to run_calculator() and run_bash_mode(). MAX_ATTEMPTS is a module-level constant, easy to adjust.
Testing: python -m pytest tests/ — 103 passed, 0 failed.
Duration: 580.4s | Cost: $1.223240 USD | Turns: 32
Branch: task/issue-61-input-validation. PR targeting exp/structured-generic.

--- 2026-04-08: Issue #48 — Bash mode CLI (structured-generic) ---
Files changed: src/__main__.py, tests/test_main.py, artifacts/activity_diagram.puml, artifacts/sequence_diagram.puml, artifacts/class_diagram.puml
Purpose: Added run_bash_mode() to __main__.py so the calculator can be invoked non-interactively from the command line: python -m src <operation> <value1> [<value2>]. If arguments are present, main() dispatches to bash mode and exits with code 0 (success) or 1 (error); no arguments falls through to the existing interactive loop. Added 20 new tests covering all 12 operations in bash mode, error paths (unknown op, wrong arg count, math errors, factorial validation).
Risks: Minimal — interactive loop unchanged; bash mode is an additive dispatch path in main(). sys.exit() is only called from main(), not from run_bash_mode(), so tests remain independent.
Testing: python -m pytest tests/ — 97 passed, 0 failed.
Duration: PENDING | Cost: PENDING | Turns: PENDING
Branch: task/issue-48-bash-mode. PR targeting exp/structured-generic.

--- 2026-04-08: Issue #43 — Add PlantUML diagrams (structured-generic) ---
Files changed: artifacts/class_diagram.puml, artifacts/activity_diagram.puml, artifacts/sequence_diagram.puml
Purpose: Created three PlantUML documentation diagrams in artifacts/ covering the Calculator class structure (class diagram), the interactive calculator loop (activity diagram), and the component interaction flow (sequence diagram).
Risks: Docs-only change; no source or test files modified.
Testing: No executable tests needed — diagram syntax is declarative PlantUML. Existing 77 tests unaffected (not re-run since no source changed).
Duration: 98.2s | Cost: $0.282727 USD | Turns: 13
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
