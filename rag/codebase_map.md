# Codebase Map

Per-file summaries: purpose, public API surface, key invariants.

---

## `src/__init__.py`
- **Purpose:** Package initializer for the `src` package.
- **Exports:** `Calculator`, `CalculatorSession`
- **Invariants:** Re-exports `Calculator` from `calculator.py` and `CalculatorSession` from `session.py`; no logic of its own.
- **Last updated:** cycle 11 (issue-271)

---

## `src/__main__.py`
- **Purpose:** Interactive CLI entry point for the Calculator with Normal/Scientific mode switching, per-session history, and error logging.
- **Exports:** `main()`, `display_menu()`, `get_number()`, `get_number_with_retry()`, `format_history_entry()`, `save_history()`, `NORMAL_OPERATIONS`, `SCIENTIFIC_OPERATIONS`, `MAX_ATTEMPTS`, `HISTORY_FILE`
- **Public API:**
  - `NORMAL_OPERATIONS: dict[str, tuple[str, int]]` — maps menu key to `(operation_name, arity)` for Normal mode: add(1), subtract(2), multiply(3), divide(4), square(5), square_root(6)
  - `SCIENTIFIC_OPERATIONS: dict[str, tuple[str, int]]` — full 18-operation set for Scientific mode; keys 1-4 are the same as Normal; adds cube(8), cube_root(9), factorial(7), power(10), log(11), ln(12), sin(13), cos(14), tan(15), cot(16), asin(17), acos(18)
  - `MAX_ATTEMPTS: int` — maximum failed input attempts before session termination (currently 5)
  - `HISTORY_FILE: str` — path where session history is written on session end (default `"history.txt"`)
  - `display_menu(operations=None, mode_name="Normal") -> None` — prints mode name and available operations; includes 'm. switch mode', 'h. history', 'q. quit'
  - `get_number(prompt, require_int=False) -> int | float` — reads one number from stdin; raises `ValueError` for non-numeric or (when `require_int=True`) non-integer input
  - `get_number_with_retry(prompt, require_int=False) -> int | float` — wraps `get_number` with retry logic; raises `_SessionExpired` after MAX_ATTEMPTS failures; each failed attempt calls `log_error("interactive", ...)`
  - `format_history_entry(name, args, result) -> str` — delegates to `CalculatorSession.format_entry`
  - `save_history(history, path=None) -> None` — writes history list to `path` (or `HISTORY_FILE` if None); overwrites any previous content so each session starts fresh
  - `main() -> None` — runs the interactive session loop; starts in Normal mode; 'm' prompts mode selection (1=Normal, 2=Scientific); 'h' displays history; 'q' or max-attempts exits; delegates computation and history to `CalculatorSession`
- **Invariants:**
  - Session starts in Normal mode; mode switch does not reset session history.
  - Unknown mode choice in the mode-select prompt prints a warning and retains the current mode.
  - `main()` creates a `CalculatorSession` to handle all operation dispatch and history recording; does not interact with `Calculator` directly.
  - `save_history` is called on every exit path (normal quit, max-invalid-ops, `_SessionExpired`).
  - `save_history` reads `HISTORY_FILE` at call time (not as a default arg default) so tests can patch it.
- **Last updated:** cycle 14 (issue-281)

---

## `src/calculator.py`
- **Purpose:** Unified `Calculator` class combining basic and scientific operations via multiple inheritance.
- **Public API:** All 12 operations inherited from `BasicOperations` and `ScientificOperations` — see those modules for per-method contracts.
- **Key invariants:**
  - `Calculator` adds no methods of its own; it exists to provide a single named type for the rest of the application.
  - MRO: `Calculator → BasicOperations → ScientificOperations → object`.
  - Public API is identical to the pre-modularization `Calculator`; no callers required updating.
- **Last updated:** cycle 12 (issue-275)

---

## `src/operations/__init__.py`
- **Purpose:** Package init for `src/operations/`; re-exports `BasicOperations` and `ScientificOperations`.
- **Exports:** `BasicOperations`, `ScientificOperations`
- **Last updated:** cycle 12 (issue-275)

---

## `src/operations/basic.py`
- **Purpose:** `BasicOperations` mixin class; the four standard arithmetic operations that form the foundation shared by all calculator modes.
- **Public API:**
  - `BasicOperations.add(a, b)` — `a + b`
  - `BasicOperations.subtract(a, b)` — `a - b`
  - `BasicOperations.multiply(a, b)` — `a * b`
  - `BasicOperations.divide(a, b)` — `a / b`; raises `ZeroDivisionError` when `b == 0` via Python's `/` operator.
- **Key invariants:**
  - No `math` import; only Python built-in operators used.
  - Division has no explicit zero guard — ZeroDivisionError comes from the runtime.
- **Last updated:** cycle 12 (issue-275)

---

## `src/operations/scientific.py`
- **Purpose:** `ScientificOperations` mixin class; advanced operations beyond basic arithmetic, including trigonometric functions (all in degrees).
- **Public API:**
  - `ScientificOperations.factorial(n: int) -> int` — `n!`; raises `TypeError` for non-int/bool, `ValueError` for negative.
  - `ScientificOperations.square(x) -> float` — `x * x`
  - `ScientificOperations.cube(x) -> float` — `x * x * x`
  - `ScientificOperations.square_root(x) -> float` — `math.sqrt(x)`; raises `ValueError` for `x < 0`.
  - `ScientificOperations.cube_root(x) -> float` — real cube root; negative input returns negative result via `-(abs(x)**(1/3))`.
  - `ScientificOperations.power(base, exp) -> float` — `base ** exp`
  - `ScientificOperations.log(x) -> float` — `math.log10(x)`; raises `ValueError` for `x <= 0`.
  - `ScientificOperations.ln(x) -> float` — `math.log(x)`; raises `ValueError` for `x <= 0`.
  - `ScientificOperations.sin(x) -> float` — `math.sin(radians(x))`; input in degrees.
  - `ScientificOperations.cos(x) -> float` — `math.cos(radians(x))`; input in degrees.
  - `ScientificOperations.tan(x) -> float` — `math.tan(radians(x))`; raises `ValueError` when `cos(x) ≈ 0` (odd multiples of 90°).
  - `ScientificOperations.cot(x) -> float` — `cos(x)/sin(x)`; raises `ValueError` when `sin(x) ≈ 0` (multiples of 180°).
  - `ScientificOperations.asin(x) -> float` — `degrees(math.asin(x))`; raises `ValueError` for `|x| > 1`.
  - `ScientificOperations.acos(x) -> float` — `degrees(math.acos(x))`; raises `ValueError` for `|x| > 1`.
- **Key invariants:**
  - All trig inputs/outputs are in degrees; `math.radians`/`math.degrees` handle conversion.
  - Domain guards use `abs(val) < 1e-10` threshold for tan/cot to catch floating-point near-zero.
  - Factorial guards bool before int (since `bool` is a subclass of `int` in Python).
- **Last updated:** cycle 14 (issue-281)

---

## `README.md`
- **Purpose:** User and developer documentation for the calculator application. Covers setup, interactive mode usage, bash CLI usage, all 12 operations, session file behavior (history.txt, error.log), code structure overview, and how to run the test suite.
- **Exports:** N/A (documentation file)
- **Key invariants:** Reflects the actual implementation as of cycle 13 (post-modularization). Does not describe planned future behavior.
- **Last updated:** cycle 13 (issue-278)

---

## `tests/test_calculator.py`
- **Purpose:** Comprehensive unit test suite for `Calculator`.
- **Current state:** 76 tests covering all twelve operations. Includes normal inputs, edge cases (zero operands, negative values, large numbers), floating-point precision via `pytest.approx`, `ZeroDivisionError` for divide, factorial boundary/rejection, `ValueError` for square_root (negative), log/ln (non-positive), and cube_root negative-input correctness. Uses a `calc` pytest fixture.
- **Exports:** None
- **Last updated:** cycle 4 (issue-219)

---

## `tests/test_main.py`
- **Purpose:** Unit tests for the interactive CLI in `src/__main__.py`.
- **Current state:** 80+ tests covering: NORMAL_OPERATIONS/SCIENTIFIC_OPERATIONS mapping invariants, mode switching (normal→scientific, scientific→normal, unknown mode choice, mode persistence across calculations), all 18 operations end-to-end through mocked stdin/stdout, trig operations (sin, cos, tan, cot, asin, acos), error paths, unknown operation key, retry logic, multi-calculation sessions, format_history_entry, save_history, session history display, history file written on all exit paths, display_menu options (mode/history/switch), error logging.
- **Test strategy:** `unittest.mock.patch` on `builtins.input` (side_effect list) and `builtins.print` (capture). Helper `run_main_with_inputs` flattens all printed args. Scientific mode tests prefix inputs with `["m", "2", ...]` to switch mode before operation. Keys 1-4 (add/subtract/multiply/divide) are stable across both modes. Key "5"=square, "6"=square_root in both modes; scientific-only ops start at key "7".
- **Exports:** None
- **Last updated:** cycle 14 (issue-281)

---

## `main.py`
- **Purpose:** Bash-accessible command-line entry point for the Calculator. Accepts `<operation> [operand1] [operand2]` as positional CLI arguments, computes the result, and prints it to stdout. Not interactive — one invocation, one result.
- **Public API:**
  - `main(argv: list[str] | None = None) -> int` — parses args, runs the operation via `CalculatorSession`, prints result; returns exit code (0 success, 1 error)
  - `_parse_operand(value: str, require_int: bool = False)` — converts a string CLI arg to int or float
- **Imports:**
  - `BINARY_OPS`, `ALL_OPS` from `src.session` (operation arity metadata; no longer duplicated here)
  - `CalculatorSession` from `src.session` for operation dispatch
- **Invariants:**
  - Binary ops (add, subtract, multiply, divide, power) require exactly 2 operands.
  - Unary ops (factorial, square, cube, square_root, cube_root, log, ln) require exactly 1 operand.
  - factorial uses `require_int=True` in `_parse_operand` to preserve Calculator.factorial's integer contract.
  - All errors (wrong arg count, unknown op, non-numeric operand, computation error) print to stderr, call `log_error("cli", ...)`, and return exit code 1.
  - Result is printed to stdout with `print(result)`.
  - `if __name__ == "__main__": sys.exit(main())` wires exit code to the shell.
- **Last updated:** cycle 11 (issue-271)

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

## `src/session.py`
- **Purpose:** Centralises operation dispatch, session history management, and operation arity metadata. Introduced in cycle 11 to separate computation from interface concerns.
- **Exports:** `CalculatorSession`, `BINARY_OPS`, `UNARY_OPS`, `ALL_OPS`
- **Public API:**
  - `BINARY_OPS: frozenset[str]` — `{"add", "subtract", "multiply", "divide", "power"}`
  - `UNARY_OPS: frozenset[str]` — `{"factorial", "square", "cube", "square_root", "cube_root", "log", "ln", "sin", "cos", "tan", "cot", "asin", "acos"}` (18 total with BINARY_OPS)
  - `ALL_OPS: frozenset[str]` — union of `BINARY_OPS` and `UNARY_OPS`; 18 operations total
  - `CalculatorSession.__init__()` — creates a private `Calculator` instance and empty history list
  - `CalculatorSession.execute(name, *args)` — dispatches `getattr(calc, name)(*args)`, appends formatted entry to history, returns result; propagates `ValueError`/`TypeError`/`ZeroDivisionError` without recording failed calls
  - `CalculatorSession.format_entry(name, args, result) -> str` — static method; returns `"name(arg1, arg2) = result"`
  - `CalculatorSession.history() -> list[str]` — returns a copy of the history list
  - `CalculatorSession.save(path: str) -> None` — writes history to file, overwriting previous content
- **Key invariants:**
  - Failed `execute()` calls (any exception) do not append to history.
  - `history()` returns a defensive copy; mutations of the returned list do not affect the session.
  - `BINARY_OPS` and `UNARY_OPS` are disjoint; `ALL_OPS` is their union.
- **Last updated:** cycle 14 (issue-281)

---

## `tests/conftest.py`
- **Purpose:** Shared pytest fixtures for the test suite. Provides an autouse `isolate_error_log` fixture that redirects `src.error_logger.ERROR_LOG_FILE` to a temp file for every test, preventing error-path tests from writing to the real `error.log`.
- **Exports:** `isolate_error_log` (pytest fixture, autouse=True, yields tmp log path)
- **Last updated:** cycle 9 (issue-253)

---

## `tests/test_session.py`
- **Purpose:** Unit tests for `src/session.py`.
- **Current state:** 49 tests covering: `BINARY_OPS`/`UNARY_OPS`/`ALL_OPS` set contents (updated to 18 total ops) and disjointness, `format_entry` static method (binary/unary/float), `execute` for all 18 operations including trig (normal inputs + error paths), history lifecycle (empty on init, accumulates on success, not updated on error, defensive copy), `save` (writes entries, empty session, overwrites).
- **Test strategy:** `session` fixture creates a fresh `CalculatorSession` for each test; `tmp_path` for file I/O tests. Uses `isolate_error_log` autouse fixture from conftest.
- **Exports:** None
- **Last updated:** cycle 14 (issue-281)

---

## `src/gui_modes.py`
- **Purpose:** Calculator mode abstractions for the GUI; no tkinter dependency so these can be imported and tested without a display.
- **Exports:** `CalculatorMode`, `SimpleMode`, `ScientificMode`, `parse_number`
- **Public API:**
  - `CalculatorMode(ABC)` — abstract base class; subclasses must implement `name: str` and `operations: dict[str, tuple[str, int]]` as abstract properties.
  - `SimpleMode` — 6 operations: add, subtract, multiply, divide, square, square_root.
  - `ScientificMode` — 18 operations: all SimpleMode ops plus factorial, cube, cube_root, power, log, ln, sin, cos, tan, cot, asin, acos.
  - `parse_number(raw: str)` — parses a string to int (if whole number) or float; raises `ValueError` for non-numeric input.
- **Key invariants:**
  - `ScientificMode.operations` is a strict superset of `SimpleMode.operations`.
  - All operation names in both modes are members of `BINARY_OPS | UNARY_OPS` from `src.session`.
  - `operations` property returns a fresh dict each call (no shared mutable state).
- **Last updated:** cycle 15 (issue-284)

---

## `src/gui.py`
- **Purpose:** Tkinter GUI controller for the Calculator. Delegates all computation to `CalculatorSession`; contains no arithmetic logic.
- **Exports:** `CalculatorGUI`, `main`, re-exports `CalculatorMode`, `SimpleMode`, `ScientificMode`
- **Public API:**
  - `_OperandSection(parent)` — inner helper class; owns first/second operand entry widgets, manages `set_arity(arity)` to show/hide the second operand row, exposes `read_a()`/`read_b()`/`clear()`/`focus_a()`.
  - `CalculatorGUI(root: tk.Tk)` — builds the full widget tree using ttk-based LabelFrame sections; holds a `CalculatorSession` and a list of `CalculatorMode` instances; mode switching swaps `_current_mode`.
  - `main() -> None` — creates a `Tk` root, instantiates `CalculatorGUI`, and calls `mainloop()`.
- **Layout sections (top-to-bottom):** Mode (radio buttons), Operation (combobox + unary/binary badge), Operands (_OperandSection), Actions (Calculate + Clear buttons), Result (large centred label), Session History (scrolled text).
- **Key invariants:**
  - All computation goes through `CalculatorSession.execute()`; no direct `Calculator` interaction.
  - Factorial input is parsed with `int()` to preserve Calculator.factorial's integer contract.
  - Errors (`ValueError`, `TypeError`, `ZeroDivisionError`) are shown in the result label and forwarded to `log_error("gui", ...)`.
  - Session history persists across mode switches within the same window lifetime.
  - `_OperandSection.set_arity` is idempotent — no re-layout when arity is unchanged.
  - Requires a display/tkinter; not importable in headless CI — use `src.gui_modes` for testable logic.
- **Last updated:** cycle 16 (issue-303)

---

## `gui.py` (root)
- **Purpose:** Thin GUI launcher at project root; mirrors `main.py` style. Run with `python gui.py`.
- **Exports:** N/A (script only)
- **Last updated:** cycle 15 (issue-284)

---

## `tests/test_gui.py`
- **Purpose:** Tests for `src/gui_modes.py`; no display required.
- **Current state:** 42 tests covering: `CalculatorMode` cannot be instantiated directly, `SimpleMode` name/op-count/valid-op-names/arity/contents, `ScientificMode` name/op-count/valid-op-names/arity/coverage of all 18 ops, `parse_number` for int/float/negative/scientific-notation/invalid/empty, mode contract parametrized across both classes.
- **Test strategy:** Imports `src.gui_modes` directly (not `src.gui`) to avoid tkinter dependency.
- **Exports:** None
- **Last updated:** cycle 15 (issue-284)

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
