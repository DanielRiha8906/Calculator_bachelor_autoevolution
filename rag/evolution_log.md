# Evolution Log

Per-cycle entries: task, files changed, outcome, lessons learned.

---

## Cycle 9 — Issue #252: Error Logging (2026-04-12)

- **Task:** Add error logging to the calculator so failures and invalid usage are recorded in a local log file (`error.log`), separate from the operation history.
- **Files changed:** `src/__main__.py`, `tests/test_main.py`
- **Outcome:** 147 tests pass (63 calculator + 84 CLI/interactive). All 133 prior tests continue to pass; 14 new tests added.
- **Key decisions:**
  - Added `ERROR_LOG_FILE = "error.log"` module constant alongside `HISTORY_FILE`, using the same `None`-sentinel default pattern so tests can monkeypatch it without touching function signatures.
  - Added `append_to_error_log(message, filepath=None)` which writes `[YYYY-MM-DD HH:MM:SS] message\n` via `datetime.now()`. Append-only — never cleared, persists across sessions (unlike history which is cleared on start).
  - Logging points: invalid number in `parse_number`, invalid integer in `parse_int`, invalid menu choice in interactive loop, unknown operation in `run_operation`, `ValueError` from Calculator in `run_operation`, all `cli_mode` error paths (wrong arg count, non-numeric, calculation errors).
  - Successful operations produce no error log entry (verified by negative tests that check the log file does not exist).
  - Updated `autouse` fixture from `isolate_history` to `isolate_files` to redirect both constants.
- **Lessons learned:** Negative tests (asserting the file does not exist on success) are a clean way to verify that logging is strictly error-only with no false positives.
- **Cost:** PENDING | **Turns:** PENDING

---

## Cycle 8 — Issue #249: Operation history (2026-04-12)

- **Task:** Add operation history to the calculator so calculations performed during the current session are recorded. Keep the history in `history.txt`, allow it to be displayed on request in interactive mode, and do not keep the history between separate sessions.
- **Files changed:** `src/__main__.py`, `tests/test_main.py`
- **Outcome:** 133 tests pass (63 calculator + 70 CLI/interactive). All 117 prior tests continue to pass; 16 new tests added.
- **Key decisions:**
  - Added `HISTORY_FILE = "history.txt"` module constant (relative to cwd) so the path is patchable in tests.
  - Added three focused helpers: `clear_history()`, `append_to_history(entry)`, `show_history()`. All use `None` sentinel defaults that resolve to the module-level `HISTORY_FILE` at call time — critical for test isolation via `monkeypatch.setattr`.
  - `run_operation()` return type changed from `None` to `str | None`: returns a formatted history entry on success, `None` on error or unknown operation. No change to its printing behaviour.
  - `main()` calls `clear_history()` once at interactive session start (wiping any previous session), then `append_to_history(entry)` after each successful `run_operation()`.
  - Added `"h"` branch in the interactive loop before the `OPERATIONS` check; pressing `h` calls `show_history()` and continues the loop.
  - `show_menu()` updated to display the `"h. show history"` option between the numbered operations and `"q. quit"`.
  - CLI mode (`cli_mode`) left unchanged — history is an interactive-only feature.
  - `autouse` fixture in `tests/test_main.py` redirects `HISTORY_FILE` to a `tmp_path` for every test, preventing any file system pollution.
- **Lessons learned:** Python function default arguments are evaluated at definition time, not call time. Using `None` as a sentinel and resolving to the module attribute inside the function body is the correct pattern for making module-level constants patchable by monkeypatch without changing callers.
- **Cost:** PENDING | **Turns:** PENDING

---

## Cycle 7 — Issue #246: Input validation (2026-04-12)

- **Task:** Add input validation to the interactive mode — retry on invalid operation or operand input, stop the session after a fixed number of failed attempts. In CLI mode, invalid input returns a clear error message and exits.
- **Files changed:** `src/__main__.py`, `tests/test_main.py`
- **Outcome:** 117 tests pass (63 existing calculator tests + 54 CLI/interactive tests). All 110 existing tests continue to pass; 7 new tests added.
- **Key decisions:**
  - Added `MAX_ATTEMPTS = 3` constant and `TooManyAttemptsError` custom exception at module level.
  - `parse_number` and `parse_int` changed from unbounded `while True` loops to bounded `for attempt in range(1, max_attempts + 1)` loops; raise `TooManyAttemptsError` on exhaustion.
  - `run_operation` unchanged — `TooManyAttemptsError` propagates naturally (it does not inherit from `ValueError`).
  - `main()` interactive loop now tracks `invalid_op_count`; breaks and prints "Too many invalid choices" when `MAX_ATTEMPTS` consecutive invalid menu choices occur. Also catches `TooManyAttemptsError` from `run_operation` and breaks.
  - `cli_mode` refactored to parse numbers/integers with explicit `try/except` blocks before calling Calculator, giving per-field error messages like `"'abc' is not a valid number."` instead of relying on Python's float/int error text.
  - `argparse` result variable renamed from `parsed` to `namespace` to avoid shadowing the new `parsed: list[float]` local used for two-arg ops.
- **Lessons learned:** `TooManyAttemptsError` not inheriting from `ValueError` is critical — if it did, `run_operation`'s `except ValueError` block would swallow it silently instead of letting it propagate to `main()`.
- **Cost:** PENDING | **Turns:** PENDING

---

## Cycle 6 — Issue #240: CLI mode (2026-04-12)

- **Task:** Add a CLI mode so the calculator can be executed from bash using command-line arguments. Allow the user to provide the operation and required values directly in the command and print the result to the terminal.
- **Files changed:** `src/__main__.py`, `tests/test_main.py`
- **Outcome:** 110 tests pass (63 existing + 28 existing interactive + 19 new cli_mode tests). All previous tests continue to pass.
- **Key decisions:**
  - Added `cli_mode(args: list[str]) -> int` — parses args via `argparse` with `choices=sorted(_ALL_OPS)`, validates arity per operation, delegates to Calculator, prints result to stdout, errors to stderr, returns 0/1.
  - Operations grouped into `_ONE_ARG_OPS`, `_INT_ARG_OPS`, `_TWO_ARG_OPS` constants for arity dispatch; `getattr(calc, op)` used for one-arg and two-arg ops to avoid a 12-branch if/elif.
  - `main()` signature changed to `main(args: list[str] | None = None)` — when `None`, reads `sys.argv[1:]`; non-empty args dispatch to `cli_mode()`; empty list (`[]`) forces interactive mode.
  - Existing interactive tests updated from `main()` to `main([])` to prevent pytest's own `sys.argv` entries from triggering CLI mode.
  - 20 new tests in `tests/test_main.py` cover all 12 cli_mode happy paths, three error paths, two wrong-arity paths, unknown-operation SystemExit, and the main() dispatch integration.
- **Lessons learned:** When `main()` reads `sys.argv` internally, test harnesses that supply their own args (like pytest) will corrupt the call. Making `args` an explicit parameter with a sensible default cleanly separates production entry-point behavior from test usage.
- **Cost:** PENDING | **Turns:** PENDING

---

## Cycle 5 — Issue #221: Interactive user input (2026-04-12)

- **Task:** Add interactive user input so the calculator reads the selected operation and required values at runtime; allow the user to continue after each result.
- **Files changed:** `src/__main__.py`, `tests/test_main.py` (new)
- **Outcome:** 91 tests pass (63 existing + 28 new). `src/__main__.py` replaced with a full interactive loop; `tests/test_main.py` added.
- **Key decisions:**
  - Implemented `show_menu()`, `parse_number()`, `parse_int()`, and `run_operation()` as standalone helpers so each concern is testable in isolation.
  - `parse_number` and `parse_int` retry indefinitely on invalid input, printing a clear error message, rather than propagating exceptions — this keeps the UX smooth.
  - `run_operation` catches `ValueError` from Calculator methods and prints it as a user-facing error without crashing the loop.
  - `OPERATIONS` dict maps string keys `"1"`–`"12"` to operation names, keeping the menu and dispatch logic in sync with a single source of truth.
  - Tests use `unittest.mock.patch("builtins.input", side_effect=[...])` to supply canned inputs; `capsys` verifies stdout content.
- **Cost:** PENDING | **Turns:** PENDING

---

## Cycle 4 — Issue #218: Multiple math operations (2026-04-12)

- **Task:** Add square, cube, square_root, cube_root, power, log, and ln as supported Calculator operations with tests.
- **Files changed:** `src/calculator.py`, `tests/test_calculator.py`
- **Outcome:** 63 tests pass. Added 7 new Calculator methods. Added 33 new tests.
- **Key decisions:**
  - `cube_root` uses a sign-preserving trick `-((-a)**(1/3))` for negative inputs, since Python's `a**(1/3)` produces a complex number for negative `a`.
  - `log` validates both `a > 0` and `base > 0 and base != 1` before delegating to `math.log(a, base)`.
  - `ln` is a thin wrapper around `math.log(a)` with a `a > 0` guard.
  - `square` and `cube` are pure `**` expressions — no guards needed.
  - `power` accepts any real exponent via `**`; no special-casing needed.
- **Lessons learned:** Python `(-8)**(1/3)` returns a complex number, not `-2.0`; the sign-preserving `-(abs(a)**(1/3))` idiom is required for real cube roots of negative numbers.
- **Cost:** PENDING | **Turns:** PENDING

---

## Cycle 3 — Issue #215: Factorial operation (2026-04-12)

- **Task:** Add `factorial` as a supported calculator operation with correct input validation and tests.
- **Files changed:** `src/calculator.py`, `tests/test_calculator.py`
- **Outcome:** 30 tests pass. Added `Calculator.factorial(n)` using `math.factorial`; raises `ValueError` for negative or non-integer inputs. Added 6 tests covering zero, small value, large value, negative input, and float input.
- **Key decisions:** Used `math.factorial` from the standard library rather than a manual implementation — it is correct, well-tested, and handles arbitrarily large integers natively. Non-integer (float) inputs are rejected with `isinstance` check before delegating to `math.factorial` since `math.factorial(3.0)` raises `TypeError` in Python 3.12 rather than `ValueError`, which would break the API contract.
- **Lessons learned:** `math.factorial` raises `TypeError` for floats in Python 3.12, so an explicit `isinstance(n, int)` guard is needed to produce a consistent `ValueError` for all invalid input types.

---

## Cycle 2 — Issue #212: Full test suite (2026-04-12)

- **Task:** Create a unit test suite covering all arithmetic operations and verify expected results are valid inputs.
- **Files changed:** `tests/test_calculator.py`
- **Outcome:** 24 tests pass. Added 21 new tests for `add`, `subtract`, `multiply`, and expanded `divide` coverage. No source changes required.
- **Key decisions:** Kept all existing divide tests intact; grouped new tests by operation using comment headers; used `math.isclose` for float assertions to avoid floating-point precision failures.
- **Lessons learned:** Float comparisons require `math.isclose`; identity-element tests (add 0, multiply by 1) are cheap and verify boundary correctness explicitly.

---

## Cycle 1 — Issue #209: ZeroDivisionError (2026-04-12)

- **Task:** Add unit test for division by zero; fix `divide` to handle it correctly.
- **Files changed:** `src/calculator.py`, `tests/test_calculator.py`
- **Outcome:** All 3 tests pass. `divide` now raises `ValueError` on zero divisor.
- **Key decisions:** Raise `ValueError` (not `ZeroDivisionError`) to give a clear, explicit message. Added two additional tests (normal division, negative denominator) alongside the required guard test.
- **Lessons learned:** Raw Python `ZeroDivisionError` is an uncontrolled exception; explicit `ValueError` with message is cleaner for downstream consumers.

---

## Cycle 0 — Bootstrap (2026-04-12)

- **Task:** RAG initialization (no implementation task)
- **Files changed:** rag/index.md, rag/codebase_map.md, rag/evolution_log.md, rag/patterns.md (created)
- **Outcome:** RAG initialized from current state of src/ and tests/
- **Lessons learned:** Initial state — Calculator has no ZeroDivisionError guard in divide().
