# Evolution Log

Per-cycle entries: task, files changed, outcome, lessons learned.

---

## Cycle 16 — Issue #303: GUI Look — Expert/generic

- **Task:** Redesign the existing tkinter Calculator GUI to present a clean, structured, visually coherent interface. Preserve all behaviour; improve presentation layer only.
- **Files changed:**
  - `src/gui.py` (modified): introduced `_OperandSection` helper class to own operand-field management; replaced raw `tk` widgets with `ttk` throughout; organized window into six ttk `LabelFrame` sections (Mode, Operation, Operands, Actions, Result, Session History); added unary/binary badge label next to operation combobox; added Clear button; result area uses large centred font; consistent `_PAD_*` constants.
- **Test result:** 278 passed
- **Key decisions:** Extracted `_OperandSection` to separate operand-visibility logic from the main controller. Used ttk for a native consistent look without adding new dependencies. `set_arity` is idempotent to avoid unnecessary re-layout. No changes to `gui_modes.py`, `session.py`, or test files — GUI design is purely a presentation-layer change.
- **Cost:** PENDING
- **Turns:** PENDING

---

## Cycle 15 — Issue #284: GUI — Expert/generic

- **Task:** Add a tkinter-based graphical interface that reuses existing application logic (CalculatorSession) without duplicating it. Use an OOP mode design with a shared CalculatorMode ABC so Simple and Scientific modes share structure while keeping their operation sets separate.
- **Files changed:**
  - `src/gui_modes.py` (new): `CalculatorMode` ABC with `name` and `operations` abstract properties; `SimpleMode` (6 ops); `ScientificMode` (all 18 ops); `parse_number` helper.
  - `src/gui.py` (new): `CalculatorGUI` tkinter controller; imports `CalculatorSession` for all computation; mode switching swaps the active `CalculatorMode` instance; session history displayed in a `ScrolledText` widget.
  - `gui.py` (new): thin root-level launcher (`python gui.py`) mirroring `main.py` style.
  - `tests/test_gui.py` (new): 42 tests covering `CalculatorMode` abstractness, `SimpleMode`/`ScientificMode` operation sets, arity contracts, and `parse_number`; no display required.
- **Test result:** 278 passed
- **Key decisions:** Mode classes extracted to `gui_modes.py` (no tkinter dependency) so they are testable in CI without a display. `gui.py` imports tkinter only at module level so the import fails gracefully when tkinter is absent; tests target `gui_modes.py` directly. `CalculatorGUI` holds no arithmetic logic — all computation goes through `CalculatorSession.execute()`. Factorial operand is converted with `int()` to match `Calculator.factorial`'s integer contract. Both `ValueError`/`TypeError` and `ZeroDivisionError` are caught and shown in the result label; errors are also forwarded to `log_error("gui", ...)` for consistency with CLI modes.
- **Cost:** PENDING
- **Turns:** PENDING

---

## Cycle 14 — Issue #281: Scientific Mode — Expert/generic

- **Task:** Add Normal and Scientific calculator modes to the interactive CLI. Normal mode exposes add, subtract, multiply, divide, square, square_root. Scientific mode extends Normal with cube, cube_root, factorial, power, log, ln, sin, cos, tan, cot, asin, acos (all trig in degrees). Users switch modes with 'm' without restarting the session.
- **Files changed:**
  - `src/operations/scientific.py`: added six trig methods — `sin`, `cos`, `tan`, `cot`, `asin`, `acos` — all in degrees; `tan`/`cot` raise `ValueError` at their undefined points; `asin`/`acos` raise `ValueError` outside `[-1, 1]`.
  - `src/session.py`: added trig ops to `UNARY_OPS`; `ALL_OPS` grows from 12 to 18.
  - `src/__main__.py`: replaced single `OPERATIONS` dict with `NORMAL_OPERATIONS` (6 ops, keys 1-6) and `SCIENTIFIC_OPERATIONS` (18 ops, keys 1-18); `display_menu` gains `operations` and `mode_name` params with defaults; `main()` starts in Normal mode, handles 'm' input for mode selection.
  - `tests/test_main.py`: replaced 56 tests with 80+ tests reflecting mode-based structure; updated all key references; added mode-switching and trig tests.
  - `tests/test_session.py`: updated `UNARY_OPS`/`ALL_OPS` assertions; added 12 trig-operation tests; total now ~49.
- **Test result:** 237 passed
- **Key decisions:** Keys 1-4 (basic arithmetic) and 5-6 (square/sqrt) are identical in both modes so basic-op tests needed no mode-switch prefix. Scientific-only ops start at key 7. Trig functions use degrees (not radians) for user-friendliness. `tan(90°)` and `cot(0°)` raise `ValueError` using a `1e-10` near-zero guard on the co-function value. `OPERATIONS` alias was removed; callers now import `NORMAL_OPERATIONS` or `SCIENTIFIC_OPERATIONS` explicitly.
- **Cost:** PENDING
- **Turns:** PENDING

---

## Cycle 13 — Issue #278: Documentation — Expert/generic

- **Task:** Add written documentation for the calculator application so users and developers can understand how to run, use, and maintain the current version. Document available operations, interactive mode, bash CLI mode, session history and error logging behavior, and the current code structure after the modularization refactor.
- **Files changed:**
  - `README.md`: replaced placeholder (single line) with comprehensive documentation covering setup, both usage modes with examples, full 12-operation reference table, session file behavior, code structure with per-module descriptions, and test instructions.
- **Test result:** 209 passed (unchanged; documentation-only change)
- **Key decisions:** Documentation reflects the post-modularization code structure (cycles 11–12). No source files changed. Kept documentation strictly aligned with actual implementation — no mention of planned future features or idealized behavior. Used markdown tables for operation reference to maximize scannability.
- **Cost:** PENDING
- **Turns:** PENDING

---

## Cycle 12 — Issue #275: Modularization — Expert/generic

- **Task:** Refactor the calculator into multiple modules so core logic, interface handling, session-related behavior, and supporting concerns are organized more cleanly. Introduce a clearer operations structure with an obvious boundary between normal and scientific functionality.
- **Files changed:**
  - `src/operations/__init__.py` (new): package init; re-exports `BasicOperations` and `ScientificOperations`.
  - `src/operations/basic.py` (new): `BasicOperations` mixin with add, subtract, multiply, divide.
  - `src/operations/scientific.py` (new): `ScientificOperations` mixin with factorial, square, cube, square_root, cube_root, power, log, ln.
  - `src/calculator.py`: replaced monolithic implementation with `Calculator(BasicOperations, ScientificOperations)` using multiple inheritance; no methods defined directly.
- **Test result:** 209 passed (unchanged; no tests added or modified)
- **Key decisions:** Used a `src/operations/` package so the file names themselves communicate the structural boundary. `Calculator` is a thin class that inherits both mixins, giving it the same public API as before. No session, CLI, or test files required modification. Multiple inheritance chosen over composition because the mixin approach keeps each class independently usable without coupling through a container. `ScientificOperations` is not yet a "mode" — it is the structural home for future scientific-mode work.
- **Cost:** PENDING
- **Turns:** PENDING

---

## Cycle 11 — Issue #271: Logic separation — Expert/generic

- **Task:** Refactor the calculator so core calculation logic is separated from interface concerns (guided interactive input, bash CLI handling, output formatting, session control). Improve OO responsibility boundaries so calculator operations can be reused independently of the user interface.
- **Files changed:**
  - `src/session.py` (new): `CalculatorSession` class with `execute()`, `format_entry()`, `history()`, `save()`; and `BINARY_OPS`/`UNARY_OPS`/`ALL_OPS` frozensets as the single authoritative source of operation arity metadata.
  - `src/__init__.py`: added `CalculatorSession` to exports.
  - `src/__main__.py`: now imports and uses `CalculatorSession` for operation dispatch and history management; `format_history_entry` delegates to `CalculatorSession.format_entry` (preserved for test backward compatibility); `main()` no longer manages the history list directly.
  - `main.py`: removed own `_BINARY_OPS`/`_UNARY_OPS`/`_ALL_OPS` definitions; imports `BINARY_OPS`, `ALL_OPS`, `CalculatorSession` from `src.session`; uses `CalculatorSession.execute()` for dispatch.
  - `tests/test_session.py` (new): 37 tests for `CalculatorSession` and operation metadata.
- **Test result:** 209 passed (was 173)
- **Key decisions:** `CalculatorSession` is the abstraction boundary: it knows which Calculator method to call and owns history tracking; interfaces (interactive menu, CLI args) only handle I/O. `format_history_entry` kept as a module-level wrapper in `__main__.py` so 56 existing tests import without change. `save_history` also kept in `__main__.py` since it handles the `HISTORY_FILE` default — that's interface config, not session logic. Operation metadata (`BINARY_OPS`/`UNARY_OPS`) moved to `session.py` eliminating the duplication that existed between `__main__.py` and `main.py`. No test deletions; all 173 prior tests continue to pass.
- **Cost:** PENDING
- **Turns:** PENDING

---

## Cycle 9 — Issue #253: Error logging for invalid usage and calculation failures

- **Task:** Add error logging to the calculator so that invalid usage and calculation failures are recorded in a dedicated local log file (`error.log`). Cover both interactive mode (`src/__main__.py`) and bash CLI mode (`main.py`). Log: unsupported operations, invalid operand input, incorrect argument counts, runtime calculation errors (ZeroDivisionError, ValueError, TypeError). Keep error logging separate from user-facing session history.
- **Files changed:**
  - `src/error_logger.py` (new): `ERROR_LOG_FILE` constant, `log_error(source, message)` function using append-mode file I/O with ISO-8601 timestamps.
  - `src/__main__.py`: added `from .error_logger import log_error`; added `log_error` calls in `get_number_with_retry` (invalid operand), unknown operation branch, and `(ValueError, TypeError, ZeroDivisionError)` catch block.
  - `main.py`: added `from src.error_logger import log_error`; added `log_error` calls for no-args, unknown op, wrong arg count (binary/unary), and calculation/operand-parse errors.
  - `tests/conftest.py` (new): autouse `isolate_error_log` fixture patches `src.error_logger.ERROR_LOG_FILE` to `tmp_path` for every test.
  - `tests/test_error_logger.py` (new): 7 tests for the logger module.
  - `tests/test_main.py`: added 4 error-logging tests (unknown op logged, calculation error logged, invalid operand logged, clean session no log entries).
  - `tests/test_cli.py`: added 6 error-logging tests (unknown op, wrong arg count binary/unary, calculation error, non-numeric operand, clean run).
- **Test result:** 173 passed (was 156)
- **Key decisions:** Used direct file append I/O rather than Python's `logging` module to keep the implementation simple, consistent with `save_history`, and easy to patch in tests. Module-level `ERROR_LOG_FILE` constant (looked up at call time) enables `patch("src.error_logger.ERROR_LOG_FILE", ...)` in tests. Autouse conftest fixture isolates log writes without requiring individual tests to be modified. Error logging is strictly additive — no changes to user-facing output or history behaviour.
- **Cost:** PENDING
- **Turns:** PENDING

---

## Cycle 8 — Issue #250: Session history for interactive CLI

- **Task:** Add operation history to the calculator so calculations performed during the current session are tracked and can be shown on request. Record entries in function-style format (`name(args) = result`). Write history to `history.txt` on session end; start each new session with a fresh history.
- **Files changed:** `src/__main__.py` (added `HISTORY_FILE`, `format_history_entry()`, `save_history()`; updated `display_menu()` to include 'h'; updated `main()` to maintain history list, record each successful result, display on 'h', write file on all exit paths), `tests/test_main.py` (updated imports; added 15 new tests; total 52 tests)
- **Test result:** 156 passed
- **Key decisions:** `save_history` uses `path=None` with a runtime lookup of `HISTORY_FILE` (instead of a default-arg capture) so tests can cleanly patch the module-level constant via `patch("src.__main__.HISTORY_FILE", ...)`. History is only appended on successful calculation; error paths (ValueError, etc.) do not add entries. 'h' is not counted as an invalid operation for retry purposes — it is checked before the unknown-op branch.
- **Cost:** PENDING
- **Turns:** PENDING

---

## Cycle 7 — Issue #247: Input validation with retry logic (interactive CLI)

- **Task:** Add input validation with retry logic to the interactive CLI. Invalid operation selections show the list of available operations and allow retry; after MAX_ATTEMPTS (5) total invalid selections the session terminates. Invalid operand inputs retry up to MAX_ATTEMPTS times per prompt before ending the session. CLI (main.py) already fails fast — no changes needed there.
- **Files changed:** `src/__main__.py` (added `MAX_ATTEMPTS`, `_SessionExpired`, `get_number_with_retry`; updated `main` to track invalid op attempts and use retry for operand reads), `tests/test_main.py` (updated 2 tests with adjusted input sequences; added 4 new tests covering retry and termination paths; total 37 tests)
- **Test result:** 141 passed
- **Key decisions:** `_SessionExpired` (internal exception) propagates out of `get_number_with_retry` and is caught in `main()` to break the loop — this keeps the termination logic cleanly separated from the normal `ValueError`/`TypeError`/`ZeroDivisionError` error-display path. Invalid operation attempts are tracked as a running session total (no reset on valid selection) so abusive or confused input terminates the session regardless of interspersed valid operations. The "remaining attempts" message is printed on each non-final failure so the user knows how many tries they have left.
- **Cost:** PENDING
- **Turns:** PENDING

---

## Cycle 6 — Issue #243: CLI mode (bash argument-based access)

- **Task:** Add a command-line interface so the calculator can be used from bash by passing the operation and operand values as arguments (`python main.py add 5 7`, `python main.py factorial 5`). Support all 12 existing operations with correct arity handling. Print errors to stderr and use exit codes.
- **Files changed:** `main.py` (new file; `main()`, `_parse_operand()`, operation sets), `tests/test_cli.py` (new file; 28 tests)
- **Test result:** 136 passed (108 existing + 28 new)
- **Key decisions:** Created `main.py` at repo root rather than modifying `src/__main__.py`, keeping interactive and argument-based CLIs cleanly separated. `_parse_operand` mirrors the `get_number` approach from the interactive CLI but operates on string args rather than stdin. factorial uses `require_int=True` to preserve Calculator.factorial's integer contract. All errors go to stderr with exit code 1; success prints to stdout with exit code 0.
- **Cost:** PENDING
- **Turns:** PENDING

---

## Cycle 5 — Issue #222: Interactive user input for CLI

- **Task:** Replace the hardcoded demo in `src/__main__.py` with a menu-driven interactive session. The loop reads the user's operation choice and the required operands, computes the result, displays it, and continues until the user enters 'q'. Unary ops prompt for one number (factorial requires int); binary ops prompt for two.
- **Files changed:** `src/__main__.py` (full rewrite; added `OPERATIONS`, `display_menu`, `get_number`, updated `main`), `tests/test_main.py` (new file; 32 tests)
- **Test result:** 108 passed (76 existing + 32 new)
- **Key decisions:** `get_number` with `require_int=True` is used only for factorial to preserve Calculator.factorial's integer-only contract. `ValueError`, `TypeError`, and `ZeroDivisionError` are caught in the session loop so errors display a message without terminating the session. Unknown menu keys are handled with a warning, not a crash.
- **Cost:** PENDING
- **Turns:** PENDING

---

## Cycle 4 — Issue #219: Add multiple math operations

- **Task:** Add square, cube, square_root, cube_root, power, log (base-10), and ln as Calculator methods. Handle edge cases: negative inputs for square_root, log, ln raise `ValueError`; cube_root accepts negative inputs and returns negative real results.
- **Files changed:** `src/calculator.py` (added 7 methods + `import math`), `tests/test_calculator.py` (added 38 tests; total now 76)
- **Test result:** 76 passed
- **Key decisions:** cube_root uses `-(abs(x)**(1/3))` for negatives to avoid Python's inability to raise negative floats to fractional powers. Explicit `ValueError` guards in square_root, log, and ln provide clear error messages before delegating to `math`. square and cube use simple multiplication rather than `math.pow` to avoid float coercion for integer inputs.
- **Cost:** PENDING
- **Turns:** PENDING

---

## Cycle 3 — Issue #216: Add factorial operation

- **Task:** Add `factorial` as a supported calculator operation with proper input validation.
- **Files changed:** `src/calculator.py` (added `factorial` method), `tests/test_calculator.py` (added 10 factorial tests; total now 38)
- **Test result:** 38 passed
- **Key decisions:** Rejected booleans explicitly (`isinstance(n, bool)` guard before `isinstance(n, int)`) since `bool` is a subclass of `int` in Python. Implemented iteratively to avoid recursion overhead. Raises `TypeError` for non-integer types, `ValueError` for negatives.
- **Cost:** PENDING
- **Turns:** PENDING

---

## Cycle 2 — Issue #213: Comprehensive test suite

- **Task:** Create a unit test suite for all Calculator operations covering normal inputs and edge cases.
- **Files changed:** `tests/test_calculator.py` (expanded from 1 to 28 tests; added fixture, full add/subtract/multiply/divide coverage with float, zero, negative, and large-number cases)
- **Test result:** 28 passed
- **Key decisions:** Used `pytest.approx` for float comparisons; kept existing `test_divide_by_zero_raises` intact and added `test_divide_by_zero_float_raises`; no source changes required.
- **Cost:** PENDING
- **Turns:** PENDING

---

## Cycle 1 — Issue #210: ZeroDivisionError test coverage

- **Task:** Add focused test asserting `Calculator.divide` raises `ZeroDivisionError` when divisor is zero.
- **Files changed:** `tests/test_calculator.py` (added `test_divide_by_zero_raises`)
- **Test result:** 1 passed
- **Key decisions:** Implementation already raises correctly via Python `/` operator; no source change needed. Test is additive only.
- **Cost:** PENDING
- **Turns:** PENDING

---

## Cycle 0 — Bootstrap (RAG initialization)

- **Task:** Initial RAG setup; no code changes.
- **Files changed:** `rag/index.md`, `rag/codebase_map.md`, `rag/evolution_log.md`, `rag/patterns.md`
- **Test result:** N/A
- **Key decisions:** Summarized existing src/ and tests/ into RAG. `tests/test_calculator.py` has imports but no test bodies.
- **Cost:** N/A
- **Turns:** N/A
