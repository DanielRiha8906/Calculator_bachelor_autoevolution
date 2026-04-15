# Codebase Map

Per-file summaries: purpose, public API surface, key invariants.

---

## `src/__init__.py`
- **Purpose:** Package initializer for the `src` package.
- **Exports:** `Calculator`
- **Invariants:** Re-exports `Calculator` from `calculator.py`; no logic of its own.
- **Last updated:** cycle 0

---

## `src/__main__.py`
- **Purpose:** Interactive CLI entry point for the Calculator with per-session history and error logging.
- **Exports:** `main()`, `display_menu()`, `get_number()`, `get_number_with_retry()`, `format_history_entry()`, `save_history()`, `OPERATIONS`, `MAX_ATTEMPTS`, `HISTORY_FILE`
- **Public API:**
  - `OPERATIONS: dict[str, tuple[str, int]]` — maps menu key to `(operation_name, arity)`; covers all 12 operations
  - `MAX_ATTEMPTS: int` — maximum failed input attempts before session termination (currently 5)
  - `HISTORY_FILE: str` — path where session history is written on session end (default `"history.txt"`)
  - `display_menu() -> None` — prints the numbered operation menu; includes 'h. history' and 'q. quit' options
  - `get_number(prompt, require_int=False) -> int | float` — reads one number from stdin; raises `ValueError` for non-numeric or (when `require_int=True`) non-integer input
  - `get_number_with_retry(prompt, require_int=False) -> int | float` — wraps `get_number` with retry logic; raises `_SessionExpired` after MAX_ATTEMPTS failures; each failed attempt calls `log_error("interactive", ...)`
  - `format_history_entry(name, args, result) -> str` — formats a calculation as `name(arg1, arg2) = result`
  - `save_history(history, path=None) -> None` — writes history list to `path` (or `HISTORY_FILE` if None); overwrites any previous content so each session starts fresh
  - `main() -> None` — runs the interactive session loop until the user enters 'q' or retries are exhausted; on 'h' displays current session history; on quit/expiry writes history to HISTORY_FILE
- **Invariants:**
  - Unary operations (factorial, square, cube, square_root, cube_root, log, ln) prompt for one operand; factorial uses `require_int=True`.
  - Binary operations (add, subtract, multiply, divide, power) prompt for two operands.
  - Successful calculations are appended to `history` as `format_history_entry(name, (a[, b]), result)` entries.
  - 'h' input during the session displays the history list; "No history yet." if empty.
  - `save_history` is called on every exit path (normal quit, max-invalid-ops, `_SessionExpired`).
  - `save_history` reads `HISTORY_FILE` at call time (not as a default arg default) so tests can patch it.
  - Invalid operation selections print the list of available operations and allow retry; after MAX_ATTEMPTS total invalid selections the session ends; each invalid selection logs via `log_error("interactive", ...)`.
  - Invalid operand inputs trigger up to MAX_ATTEMPTS retries per prompt; on exhaustion `_SessionExpired` is raised and the session ends; each failed input attempt logs via `log_error`.
  - `ValueError`, `TypeError`, and `ZeroDivisionError` from calculator operations (not from input parsing) are caught, logged via `log_error("interactive", f"calculation error in {name}: ...")`, and printed as "Error: <msg>"; the session continues.
  - `_SessionExpired` (internal exception, not re-exported) propagates out of operand reading and is caught in `main()` to break the session loop.
- **Last updated:** cycle 9 (issue-253)

---

## `src/calculator.py`
- **Purpose:** Core arithmetic calculator implementation.
- **Public API:**
  - `Calculator.add(a, b) -> float/int` — returns `a + b`
  - `Calculator.subtract(a, b) -> float/int` — returns `a - b`
  - `Calculator.multiply(a, b) -> float/int` — returns `a * b`
  - `Calculator.divide(a, b) -> float/int` — returns `a / b`; raises `ZeroDivisionError` naturally when `b == 0`
  - `Calculator.factorial(n: int) -> int` — returns `n!`; raises `TypeError` for non-integers (including bool/float), raises `ValueError` for negative integers
  - `Calculator.square(x) -> float` — returns `x * x`
  - `Calculator.cube(x) -> float` — returns `x * x * x`
  - `Calculator.square_root(x) -> float` — returns `math.sqrt(x)`; raises `ValueError` for `x < 0`
  - `Calculator.cube_root(x) -> float` — returns real cube root (negative for negative x); uses `-(abs(x)**(1/3))` for negatives
  - `Calculator.power(base, exp) -> float` — returns `base ** exp`
  - `Calculator.log(x) -> float` — returns `math.log10(x)`; raises `ValueError` for `x <= 0`
  - `Calculator.ln(x) -> float` — returns `math.log(x)`; raises `ValueError` for `x <= 0`
- **Key invariants:**
  - Division delegates directly to Python `/` operator; no explicit zero-check.
  - `ZeroDivisionError` is raised by Python runtime when dividing by zero.
  - Factorial validates input type explicitly: booleans are rejected (`isinstance(n, bool)` checked before `isinstance(n, int)` since `bool` is a subclass of `int`).
  - Factorial is computed iteratively; `factorial(0)` and `factorial(1)` both return 1.
  - `square_root` raises `ValueError` for negative inputs (not `math.sqrt`'s `ValueError`; explicit guard for clear messaging).
  - `cube_root` handles negative inputs by computing `-(abs(x)**(1/3))` to stay in real domain.
  - `log` and `ln` raise `ValueError` for `x <= 0` with explicit guard before delegating to `math`.
  - Module imports `math` at the top.
- **Last updated:** cycle 4 (issue-219)

---

## `tests/test_calculator.py`
- **Purpose:** Comprehensive unit test suite for `Calculator`.
- **Current state:** 76 tests covering all twelve operations. Includes normal inputs, edge cases (zero operands, negative values, large numbers), floating-point precision via `pytest.approx`, `ZeroDivisionError` for divide, factorial boundary/rejection, `ValueError` for square_root (negative), log/ln (non-positive), and cube_root negative-input correctness. Uses a `calc` pytest fixture.
- **Exports:** None
- **Last updated:** cycle 4 (issue-219)

---

## `tests/test_main.py`
- **Purpose:** Unit tests for the interactive CLI in `src/__main__.py`.
- **Current state:** 56 tests covering: OPERATIONS mapping invariants (all 12 ops present, correct arities), `get_number` parsing (int, float, require_int, invalid input), quit behaviour (immediate and case-insensitive), all 12 operations end-to-end through mocked stdin/stdout, error paths (divide-by-zero, sqrt negative, log/ln non-positive, factorial negative/float, non-numeric input), unknown operation key, available-operations listing on invalid op, retry-attempts-remaining message, session termination after MAX_ATTEMPTS invalid operand inputs, session termination after MAX_ATTEMPTS invalid operation selections, session-continues-before-max test, multi-calculation sessions, `format_history_entry` (binary/unary/float), `save_history` (writes/empty/overwrites), session history display ('h' key: empty message, after one/multiple calcs, header), history file written on quit/expiry/empty session, new session starts fresh, display_menu includes 'h' option, error logging for unknown operation/calculation error/invalid operand/clean session.
- **Test strategy:** `unittest.mock.patch` on `builtins.input` (side_effect list) and `builtins.print` (capture). Helper `run_main_with_inputs` flattens all printed args into a list of strings. `MAX_ATTEMPTS` and `HISTORY_FILE` imported from `src.__main__`. History file tests patch `src.__main__.HISTORY_FILE` and use `tmp_path` fixture to avoid writing real files. Error log path is redirected via autouse `isolate_error_log` fixture from `tests/conftest.py`.
- **Exports:** None
- **Last updated:** cycle 9 (issue-253)

---

## `main.py`
- **Purpose:** Bash-accessible command-line entry point for the Calculator. Accepts `<operation> [operand1] [operand2]` as positional CLI arguments, computes the result, and prints it to stdout. Not interactive — one invocation, one result.
- **Public API:**
  - `main(argv: list[str] | None = None) -> int` — parses args, runs the operation, prints result; returns exit code (0 success, 1 error)
  - `_parse_operand(value: str, require_int: bool = False)` — converts a string CLI arg to int or float
  - `_BINARY_OPS`, `_UNARY_OPS`, `_ALL_OPS` — sets defining which operations take two vs one operand
- **Invariants:**
  - Binary ops (add, subtract, multiply, divide, power) require exactly 2 operands.
  - Unary ops (factorial, square, cube, square_root, cube_root, log, ln) require exactly 1 operand.
  - factorial uses `require_int=True` in `_parse_operand` to preserve Calculator.factorial's integer contract.
  - All errors (wrong arg count, unknown op, non-numeric operand, computation error) print to stderr, call `log_error("cli", ...)`, and return exit code 1.
  - Result is printed to stdout with `print(result)`.
  - `if __name__ == "__main__": sys.exit(main())` wires exit code to the shell.
- **Last updated:** cycle 9 (issue-253)

---

## `src/error_logger.py`
- **Purpose:** Dedicated error logging module; appends error events from interactive and CLI modes to a local log file, separate from user-facing session history.
- **Exports:** `ERROR_LOG_FILE: str`, `log_error(source: str, message: str) -> None`
- **Public API:**
  - `ERROR_LOG_FILE: str` — path to the error log file (default `"error.log"`); module-level name looked up at call time so tests can patch it.
  - `log_error(source, message) -> None` — appends one timestamped entry in format `YYYY-MM-DDTHH:MM:SS [source] message\n` to `ERROR_LOG_FILE` (opens in append mode).
- **Key invariants:**
  - File is always opened in append mode so entries from multiple invocations accumulate.
  - Each entry ends with `\n`; timestamp uses ISO-8601 local time without timezone.
  - `source` should be `"interactive"` (from `src/__main__.py`) or `"cli"` (from `main.py`).
  - Does NOT interact with Python's `logging` module; uses direct file I/O for simplicity and testability.
- **Last updated:** cycle 9 (issue-253)

---

## `tests/conftest.py`
- **Purpose:** Shared pytest fixtures for the test suite. Provides an autouse `isolate_error_log` fixture that redirects `src.error_logger.ERROR_LOG_FILE` to a temp file for every test, preventing error-path tests from writing to the real `error.log`.
- **Exports:** `isolate_error_log` (pytest fixture, autouse=True, yields tmp log path)
- **Last updated:** cycle 9 (issue-253)

---

## `tests/test_error_logger.py`
- **Purpose:** Unit tests for `src/error_logger.py`.
- **Current state:** 7 tests covering: file creation on first log call, source and message written to file, timestamp format (ISO-8601), append behavior for multiple entries, one-entry-per-line invariant, `ERROR_LOG_FILE` type and extension.
- **Test strategy:** Uses `isolate_error_log` fixture from conftest for file isolation.
- **Exports:** None
- **Last updated:** cycle 9 (issue-253)

---

## `tests/test_cli.py`
- **Purpose:** Unit tests for the bash CLI in `main.py`.
- **Current state:** 34 tests covering: argument-count validation (no args, too few, too many for binary and unary ops), unknown operation, all 12 operations (normal inputs and float variants), error paths (divide-by-zero, sqrt negative, log/ln non-positive, factorial float/negative), non-numeric operand, and 6 error-logging assertions (unknown op, wrong arg count binary/unary, calculation error, non-numeric operand, clean run produces no log).
- **Test strategy:** Call `main(args)` directly with a list of strings; use pytest `capsys` to capture stdout/stderr. Helper `run_cli` returns `(exit_code, stdout, stderr)`. Error log path redirected by autouse `isolate_error_log` fixture from `tests/conftest.py`.
- **Exports:** None
- **Last updated:** cycle 9 (issue-253)
