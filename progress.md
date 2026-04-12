# Progress Log

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

Duration: PENDING | Cost: PENDING | Turns: PENDING

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
