# Progress Log

---

## Run: Issue #270 — Logic Separation (2026-04-15)

- **Branch:** exp3/issue-270-logic-separation
- **PR target:** exp3/structured-generic
- **Files changed:**
  - `src/calculator.py` — added `Calculator.execute(operation, *args)` method: dispatches to the named Calculator method via `getattr`; raises `ValueError` for unknown or non-callable names. This is the logic layer's unified dispatch point.
  - `src/__main__.py` — added `_OP_PROMPTS` dict mapping each operation name to its interactive prompt tuple (UI layer); refactored `run_operation` to replace the 12-branch if/elif chain with arity-group dispatch (`_INT_ARG_OPS` / `_ONE_ARG_OPS` / else) + `calc.execute(operation, *args)`; replaced `calc.factorial(n)` and `getattr(calc, op)(...)` in `cli_mode` with `calc.execute(op, ...)`.
  - `tests/test_calculator.py` — added 5 tests for `Calculator.execute`: two-arg dispatch, one-arg dispatch, int-arg dispatch, ValueError propagation, unknown operation raises ValueError.
- **Purpose:** Separate calculation logic from user interaction. `Calculator` now owns all computation and dispatch via `execute`; `__main__.py` owns all input collection and display. `run_operation` no longer mixes prompting and calculation within the same if/elif branches.
- **Risks:** None — external behavior of all existing functions is identical; all 147 prior tests pass unchanged.
- **All tests passed:** Yes — 152 tests (68 calculator + 84 CLI/interactive, including 5 new execute tests).
- **RAG entries consulted:** `rag/index.md`, `rag/codebase_map.md`, `rag/evolution_log.md`, `rag/patterns.md`
- **Tokens used:** PENDING | **Cost:** PENDING | **Turns:** PENDING

Duration: PENDING | Cost: PENDING | Turns: PENDING

---

## Run: Diagram update (2026-04-12)

- **Branch:** exp3/issue-252-add-error-logging
- **Files changed:**
  - `artifacts/class_diagram.puml` — added `ERROR_LOG_FILE` constant and `append_to_error_log` function to `__main__` class; added notes for both; updated notes for `parse_number`, `parse_int`, `run_operation`, `cli_mode`, and `main` to describe error-logging behaviour.
  - `artifacts/activity_diagram.puml` — added `append_to_error_log(...)` action labels at every error exit in `cli_mode`; added error-log call before `invalid_op_count` increment in the interactive menu loop; updated parse-step labels inside `run_operation` to note per-attempt error logging; updated `ValueError` exit in `run_operation` to show error-log call.
  - `artifacts/sequence_diagram.puml` — added `error.log` participant; added `append_to_error_log` write calls at all validation and calculation error points in both `cli_mode` and interactive mode (invalid menu choice, each parse failure, each Calculator ValueError).
- **Purpose:** Reflect cycle 9 (issue #252) changes — error logging feature — in all three PlantUML diagrams.
- **Risks:** None — diagram-only change; no source code modified.
- **All tests passed:** N/A (no code changes)
- **RAG entries consulted:** `rag/index.md`, `rag/codebase_map.md`
- **Tokens used:** PENDING | **Cost:** PENDING | **Turns:** PENDING

Duration: 239.4s | Cost: $0.739317 USD | Turns: 25

---

## Run: Issue #252 — Error Logging (2026-04-12)

- **Branch:** exp3/issue-252-add-error-logging
- **Files changed:**
  - `src/__main__.py` — added `ERROR_LOG_FILE` constant; added `append_to_error_log(message, filepath=None)` helper; added error log calls in `parse_number`, `parse_int`, `run_operation` (unknown op + ValueError), interactive loop (invalid menu choice), and all `cli_mode` error paths.
  - `tests/test_main.py` — updated `isolate_history` fixture to also redirect `ERROR_LOG_FILE` (renamed to `isolate_files`); imported `append_to_error_log` and `ERROR_LOG_FILE`; added 14 new tests covering error log append, timestamp format, module-constant usage, logging from parse functions, run_operation, main() interactive loop, and cli_mode; added negative tests verifying successful operations do not produce log entries.
- **Purpose:** Record failures and invalid usage in a local `error.log` file, separate from the operation history, so that debugging and audit of error conditions is possible without mixing them with normal history.
- **Risks:** None — additive change only; error logging uses the same `None`-sentinel pattern as history helpers for safe test isolation.
- **All tests passed:** Yes — 147 tests (63 calculator + 84 CLI/interactive, including 14 new).
- **Current branch:** exp3/issue-252-add-error-logging
- **Intended PR target:** exp3/structured-generic
- **RAG entries consulted:** `rag/index.md`, `rag/codebase_map.md`, `rag/evolution_log.md`, `rag/patterns.md`
- **Tokens used:** PENDING | **Cost:** PENDING | **Turns:** PENDING

Duration: 315.0s | Cost: $1.212037 USD | Turns: 46

---

## Run: Diagram update (2026-04-12)

- **Branch:** exp3/issue-249-operation-history
- **Files changed:**
  - `artifacts/class_diagram.puml` — added `HISTORY_FILE` constant; added `clear_history`, `append_to_history`, `show_history` helper functions; updated `run_operation` return type to `str | None`; updated notes for `main` and `cli_mode`.
  - `artifacts/activity_diagram.puml` — added `clear_history()` call at session start; added `"h"` choice branch (show_history); added `append_to_history(entry)` call after successful operation; updated `show_menu` label; updated `run_operation` partition to show return values.
  - `artifacts/sequence_diagram.puml` — added `history.txt` participant; added `clear_history()` call at session start; added `"h"` choice branch with `show_history()` / file read interaction; added `append_to_history(entry)` call on success; updated error branch note (run_operation returns None, no history written).
- **Purpose:** Reflect Cycle 8 (issue #249) changes — operation history feature — in all three PlantUML diagrams.
- **Risks:** None — diagram-only change, no source code modified.
- **All tests passed:** N/A (no code changes)
- **RAG entries consulted:** `rag/index.md`, `rag/codebase_map.md`, `rag/evolution_log.md`
- **Tokens used:** PENDING | **Cost:** PENDING | **Turns:** PENDING

Duration: 123.0s | Cost: $0.443561 USD | Turns: 20

---

## Run: Issue #249 — Operation history (2026-04-12)

- **Branch:** exp3/issue-249-operation-history
- **Target branch:** exp3/structured-generic
- **Files changed:**
  - `src/__main__.py` — added `HISTORY_FILE` constant; `clear_history()`, `append_to_history()`, `show_history()` helpers with None-sentinel defaults; `show_menu()` gains `"h. show history"` line; `run_operation()` return type changed to `str | None` (history entry on success, None on failure); `main()` clears history at session start, handles `"h"` choice, appends successful entries to file.
  - `tests/test_main.py` — added `autouse` fixture to redirect `HISTORY_FILE` to `tmp_path`; imported new public names; added 16 new tests covering history helpers, run_operation return values, and interactive history flow. Total: 133 tests.
- **Purpose:** Record all successful calculations during a session to `history.txt`; clear the file on each new session so history never persists across sessions; expose `"h"` menu option to display current session history.
- **Risks:** None significant. `history.txt` is written in cwd; path is configurable via `HISTORY_FILE` constant.
- **All tests passed:** Yes (133/133)
- **RAG entries consulted:** `rag/index.md`, `rag/codebase_map.md`, `rag/evolution_log.md`, `rag/patterns.md`
- **Tokens used:** PENDING | **Cost:** PENDING | **Turns:** PENDING

Duration: 408.3s | Cost: $1.351955 USD | Turns: 49

---

## Run: Issue #246 — Input validation (2026-04-12)

- **Branch:** exp3/issue-246-input-validation
- **Target branch:** exp3/structured-generic
- **Files changed:**
  - `src/__main__.py` — added `MAX_ATTEMPTS = 3`, `TooManyAttemptsError`; `parse_number` and `parse_int` now use bounded retry loop and raise `TooManyAttemptsError` on exhaustion; `main()` interactive loop tracks `invalid_op_count` and breaks on too many bad choices; catches `TooManyAttemptsError` from `run_operation`; `cli_mode` gains explicit per-field number/int validation with clear error messages; argparse result renamed `namespace` to avoid shadowing.
  - `tests/test_main.py` — added `TooManyAttemptsError`, `MAX_ATTEMPTS` imports; added 7 new tests covering: parse_number raises after max attempts, parse_int raises after max attempts, interactive session ends on too many invalid choices, interactive session ends on too many invalid operands, CLI non-numeric two-arg error, CLI non-numeric one-arg error, CLI non-integer factorial error.
- **Purpose:** Prevent interactive mode from looping indefinitely on invalid input; provide a fixed retry limit and clean session termination. Improve CLI error messages for non-numeric values.
- **Risks:** Minimal — MAX_ATTEMPTS=3 is a constant, easy to change; TooManyAttemptsError not inheriting from ValueError ensures it is never accidentally swallowed by run_operation's except block.
- **Tests passed:** Yes — 117/117 (63 calculator + 54 main; all pass)
- **RAG entries consulted:** `rag/index.md`, `rag/codebase_map.md`, `rag/evolution_log.md`, `rag/patterns.md`
Duration: 292.9s | Cost: $1.036777 USD | Turns: 39

---

## Run: Issue #240 — CLI mode (2026-04-12)

- **Branch:** exp3/issue-240-cli-mode
- **Target branch:** exp3/structured-generic
- **Files changed:**
  - `src/__main__.py` — added `cli_mode(args)`, `_ONE_ARG_OPS`, `_INT_ARG_OPS`, `_TWO_ARG_OPS`, `_ALL_OPS`; updated `main(args=None)` signature to dispatch to CLI mode when args are present
  - `tests/test_main.py` — updated 5 interactive `main()` calls to `main([])`; added 20 new cli_mode tests (12 happy-path + 8 error/edge cases)
- **Purpose:** Add non-interactive CLI mode so the calculator can be called from bash with operation and values as arguments (`python -m src add 3 4` → prints `7.0`).
- **Risks:** Minimal — interactive mode unchanged; `main()` signature change is backward compatible via default `args=None`; existing tests required only call-site update from `main()` to `main([])`.
- **Tests passed:** Yes — 110/110 (63 calculator + 48 main; all pass)
- **RAG entries consulted:** `rag/index.md`, `rag/codebase_map.md`, `rag/patterns.md`, `rag/evolution_log.md`
Duration: 317.8s | Cost: $0.946621 USD | Turns: 37

---

## Run: Issue #221 — Interactive user input (2026-04-12)

- **Branch:** exp3/issue-221-interactive-input
- **Target branch:** exp3/structured-generic
- **Files changed:**
  - `src/__main__.py` — replaced static demo with interactive menu loop; added `show_menu()`, `parse_number()`, `parse_int()`, `run_operation()`, and updated `main()` to loop until "q"
  - `tests/test_main.py` — new file with 28 tests covering all helpers, all 12 operations, and main loop scenarios
- **Purpose:** Add runtime user input so the calculator reads the selected operation and values interactively, shows results, and allows continued use after each result.
- **Risks:** None — `src/calculator.py` and `tests/test_calculator.py` unchanged; change is purely additive to the CLI layer.
- **Tests passed:** Yes — 91/91 (63 existing + 28 new)
- **RAG entries consulted:** `rag/index.md`, `rag/codebase_map.md`, `rag/evolution_log.md`, `rag/patterns.md`
Duration: 203.6s | Cost: $0.699409 USD | Turns: 36

---

## Run: Issue #218 — Multiple math operations (2026-04-12)

- **Branch:** exp3/issue-218-add-math-operations
- **Target branch:** exp3/structured-generic
- **Files changed:**
  - `src/calculator.py` — added `square`, `cube`, `square_root`, `cube_root`, `power`, `log`, `ln` methods with input validation
  - `tests/test_calculator.py` — added 33 tests for new operations (4 for square, 4 for cube, 4 for square_root, 4 for cube_root, 5 for power, 7 for log, 5 for ln)
- **Purpose:** Add seven new math operations to the Calculator class as required by issue #218.
- **Risks:** None — purely additive; no existing methods modified.
- **Tests passed:** Yes — 63/63
- **RAG entries consulted:** `rag/index.md`, `rag/codebase_map.md`, `rag/evolution_log.md`, `rag/patterns.md`
Duration: 144.3s | Cost: $0.644819 USD | Turns: 36

---

## Run: Issue #215 — Factorial operation (2026-04-12)

- **Branch:** exp3/issue-215-add-factorial
- **Target branch:** exp3/structured-generic
- **Files changed:**
  - `src/calculator.py` — added `import math` and `Calculator.factorial(n)` method with input validation
  - `tests/test_calculator.py` — added 6 factorial tests (zero, one, small, large, negative raises, float raises)
- **Purpose:** Add factorial as a supported calculator operation with correct validation and test coverage.
- **Risks:** None — purely additive change; no existing methods modified.
- **Tests passed:** Yes — 30/30
- **RAG entries consulted:** `rag/index.md`, `rag/codebase_map.md`, `rag/evolution_log.md`, `rag/patterns.md`
- Duration: 97.4s | Cost: $0.349491 USD | Turns: 26

---

## Run: Issue #209 — ZeroDivisionError (2026-04-12)

- **Branch:** exp3/issue-209-zero-division
- **Target branch:** exp3/structured-generic
- **Files changed:**
  - `src/calculator.py` — added zero-check in `divide`; raises `ValueError("Division by zero is not allowed")` when `b == 0`
  - `tests/test_calculator.py` — added `test_divide_by_zero_raises`, `test_divide_normal`, `test_divide_negative_denominator`
- **Purpose:** Guard `Calculator.divide` against zero divisor and provide test coverage.
- **Risks:** None — purely additive change; no existing behavior altered for non-zero inputs.
- **Tests passed:** Yes — 3/3 (`test_divide_by_zero_raises`, `test_divide_normal`, `test_divide_negative_denominator`)
- **RAG entries consulted:** RAG initialized this run; `rag/codebase_map.md` and `rag/evolution_log.md` updated after implementation.
- Duration: 150.2s | Cost: $0.524147 USD | Turns: 41

---

## Run: Issue #212 — Full test suite (2026-04-12)

- **Branch:** exp3/issue-212-test-suite
- **Target branch:** exp3/structured-generic
- **Files changed:**
  - `tests/test_calculator.py` — expanded from 3 divide-only tests to 24 tests covering add (5), subtract (6), multiply (6), divide (7)
- **Purpose:** Create a complete unit test suite for all Calculator arithmetic operations as required by issue #212.
- **Risks:** None — test-only change; no source code modified.
- **Tests passed:** Yes — 24/24
- **RAG entries consulted:** `rag/index.md`, `rag/codebase_map.md`, `rag/evolution_log.md`
- Duration: 129.4s | Cost: $0.446993 USD | Turns: 33

---

## Run: Diagram update (2026-04-12)

- **Branch:** exp3/issue-209-zero-division
- **Files changed:**
  - `artifacts/class_diagram.puml` — created; covers `Calculator` class and its four arithmetic methods, `__main__` dependency
  - `artifacts/activity_diagram.puml` — created; shows main execution flow including zero-division guard in `divide`
  - `artifacts/sequence_diagram.puml` — created; shows interactions between `__main__` and `Calculator` for all four operations
- **Purpose:** Generate up-to-date PlantUML diagrams reflecting current state of `src/` after issue-209 fix.
- **Risks:** None — diagram-only change; no source code modified.
- **Tests passed:** N/A (no source changes)
- **RAG entries consulted:** `rag/codebase_map.md` (via prior run; not re-read this run)
- Duration: 46.3s | Cost: $0.195395 USD | Turns: 15

---

## Run: Diagram update (2026-04-12)

- **Branch:** exp3/issue-212-test-suite
- **Files changed:**
  - `artifacts/class_diagram.puml` — verified accurate; no source changes since last diagram run
  - `artifacts/activity_diagram.puml` — verified accurate; no source changes since last diagram run
  - `artifacts/sequence_diagram.puml` — verified accurate; no source changes since last diagram run
- **Purpose:** Verify and re-commit PlantUML diagrams on current experiment branch; source unchanged since last diagram update so content is still valid.
- **Risks:** None — diagram-only run; no source code modified.
- **Tests passed:** N/A (no source changes)
- **RAG entries consulted:** `rag/index.md`, `rag/codebase_map.md`
- Duration: 39.8s | Cost: $0.177952 USD | Turns: 16

---

## Run: Diagram update (2026-04-12)

- **Branch:** exp3/issue-215-add-factorial
- **Files changed:**
  - `artifacts/class_diagram.puml` — added `factorial(n: int): int` to `Calculator` class with note describing ValueError conditions
  - `artifacts/activity_diagram.puml` — added factorial validation flow (type check, negativity check, delegate to math.factorial)
  - `artifacts/sequence_diagram.puml` — added `factorial(5)` call showing `math` module delegation and error alt path
- **Purpose:** Update PlantUML diagrams to reflect factorial method added to Calculator in cycle 3 (issue #215).
- **Risks:** None — diagram-only change; no source code modified.
- **Tests passed:** N/A (no source changes)
- **RAG entries consulted:** `rag/index.md`, `rag/codebase_map.md`
- Duration: 61.3s | Cost: $0.214985 USD | Turns: 19

---

## Run: Diagram update (2026-04-12)

- **Branch:** exp3/issue-218-add-math-operations
- **Files changed:**
  - `artifacts/class_diagram.puml` — added `square`, `cube`, `square_root`, `cube_root`, `power`, `log`, `ln` to `Calculator` class with notes for ValueError conditions
  - `artifacts/activity_diagram.puml` — added validation and execution flow for all seven new operations
  - `artifacts/sequence_diagram.puml` — added interaction sequences for all seven new operations including math module delegation and error alt paths
- **Purpose:** Update PlantUML diagrams to reflect seven new math operations added to Calculator in cycle 4 (issue #218).
- **Risks:** None — diagram-only change; no source code modified.
- **Tests passed:** N/A (no source changes)
- **RAG entries consulted:** `rag/index.md`, `rag/codebase_map.md`
Duration: 54.5s | Cost: $0.237316 USD | Turns: 18

---

## Run: Diagram update (2026-04-12)

- **Branch:** exp3/issue-221-interactive-input
- **Files changed:**
  - `artifacts/class_diagram.puml` — updated `__main__` class to expose all five functions (`show_menu`, `parse_number`, `parse_int`, `run_operation`, `main`) and the `OPERATIONS` constant with notes describing retry behaviour and error handling
  - `artifacts/activity_diagram.puml` — rewritten to show the full interactive CLI loop: show menu → read choice → validate → run_operation (dispatch by argument count) → print result or error
  - `artifacts/sequence_diagram.puml` — restructured to add `User` actor, wrap all interactions in a `loop` frame, and show input prompting via `parse_number`/`parse_int`; per-operation groups retained for all 12 operations
- **Purpose:** Update PlantUML diagrams to reflect the interactive CLI layer added to `src/__main__.py` in cycle 5 (issue #221).
- **Risks:** None — diagram-only change; no source code modified.
- **Tests passed:** N/A (no source changes)
- **RAG entries consulted:** `rag/index.md`, `rag/codebase_map.md`
Duration: 154.7s | Cost: $0.404612 USD | Turns: 19

---

## Run: Diagram update (2026-04-12)

- **Branch:** exp3/issue-240-cli-mode
- **Files changed:**
  - `artifacts/class_diagram.puml` — added `_ONE_ARG_OPS`, `_INT_ARG_OPS`, `_TWO_ARG_OPS`, `_ALL_OPS` constants and `cli_mode(args: list[str]) -> int` to `__main__`; updated `main()` signature to `main(args: list[str] | None = None) -> None`
  - `artifacts/activity_diagram.puml` — added top-level branch for CLI mode (argparse dispatch with arity validation, result/error output, exit codes) vs interactive mode loop
  - `artifacts/sequence_diagram.puml` — wrapped existing interactive loop in `alt` frame; added CLI mode alt showing argparse dispatch, per-arity Calculator calls, stdout result / stderr error, and exit codes
- **Purpose:** Update PlantUML diagrams to reflect the non-interactive CLI mode added to `src/__main__.py` in cycle 6 (issue #240).
- **Risks:** None — diagram-only change; no source code modified.
- **Tests passed:** N/A (no source changes)
- **RAG entries consulted:** `rag/index.md`, `rag/codebase_map.md`
Duration: 108.0s | Cost: $0.330687 USD | Turns: 21

---

## Run: Diagram update (2026-04-12)

- **Branch:** exp3/issue-246-input-validation
- **Files changed:**
  - `artifacts/class_diagram.puml` — added `TooManyAttemptsError` class with note; added `MAX_ATTEMPTS : int = 3` to `__main__`; updated `parse_number`/`parse_int` signatures to include `max_attempts` param; updated notes for `parse_number`, `parse_int`, `run_operation`, `main`, and `cli_mode` to reflect bounded retry, TooManyAttemptsError propagation, invalid_op_count tracking, and per-field CLI validation
  - `artifacts/activity_diagram.puml` — updated interactive mode to show `invalid_op_count` tracking and session termination on too many invalid menu choices; updated parse steps to show bounded retry (MAX_ATTEMPTS=3) and TooManyAttemptsError exit path; updated CLI mode to show per-field integer/number validation with specific error messages
  - `artifacts/sequence_diagram.puml` — added `invalid_op_count` tracking note; updated parse_number/parse_int note to show bounded retry and TooManyAttemptsError; added alt frame for TooManyAttemptsError session termination; added per-field validation alts in CLI mode
- **Purpose:** Update PlantUML diagrams to reflect input validation changes added in cycle 7 (issue #246): bounded retry with TooManyAttemptsError, invalid_op_count tracking, and per-field CLI validation.
- **Risks:** None — diagram-only change; no source code modified.
- **Tests passed:** N/A (no source changes)
- **RAG entries consulted:** `rag/index.md`, `rag/codebase_map.md`
Duration: 216.1s | Cost: $0.502483 USD | Turns: 19
