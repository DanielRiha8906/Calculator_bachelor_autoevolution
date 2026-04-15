# Evolution Log

## Cycle 14 — Issue #282: GUI (2026-04-15)
- **Task:** Add a tkinter GUI for the calculator app while keeping existing CLI/REPL functionality
- **Branch:** exp3/issue-282-gui-tkinter
- **Files changed:** src/gui.py (new), src/__main__.py, tests/test_gui.py (new)
- **Outcome:** Created `src/gui.py` with `CalculatorGUI` class: a tkinter window with digit buttons, basic binary ops (+−×÷), common unary ops (x², √, n!, x³, ∛, log, ln, xʸ), a toggleable scientific panel (sin–exp), and a history dialog. All computation goes through `Calculator.execute()`. Added `--gui` flag to `main()` in `__main__.py` via lazy import of `launch_gui`. Added 46 tests in `tests/test_gui.py` that mock tkinter via sys.modules injection (no display needed). 234 tests collected, 234 passed.
- **Key decisions:** tkinter not installed in CI — must inject fake tkinter into sys.modules before importing src.gui. Used `side_effect=_FakeStringVar` for StringVar mocks to get testable in-memory storage. Used `Frame.side_effect = lambda: MagicMock()` to give display_frame and sci_frame independent mocks (so toggle_mode grid call counts can be asserted independently). `--gui` flag uses a lazy `from .gui import launch_gui` inside main() so CLI/REPL paths never incur the tkinter import cost.
- **Cost:** PENDING
- **Turns:** PENDING

## Cycle 13 — Issue #279: Scientific Mode (2026-04-15)
- **Task:** Add scientific mode to the calculator with interactive mode switching
- **Branch:** exp3/issue-279-scientific-mode
- **Files changed:** src/operations/scientific.py, src/operations/__init__.py, src/calculator.py, src/__main__.py, tests/test_calculator.py, tests/test_main.py
- **Outcome:** Implemented 10 scientific operations (sin, cos, tan, asin, acos, atan, sinh, cosh, tanh, exp; all in radians) in scientific.py. Added SCIENTIFIC_UNARY_OPS constant and Calculator methods with error logging for domain-violating ops (asin, acos). Added SCIENTIFIC_MENU/SCIENTIFIC_MENU_MAP and 'm' mode toggle to the interactive REPL. CLI mode accepts scientific ops without mode switching. 188 tests collected, 188 passed.
- **Key decisions:** SCIENTIFIC_UNARY_OPS is a separate constant from UNARY_OPS to avoid breaking existing tests that assert exact set membership. Scientific ops are all unary so they fall through run_operation's unary path without changes to that function. History is shared between modes within a REPL session.
- **Cost:** PENDING
- **Turns:** PENDING

## Cycle 12 — Issue #276: Documentation (2026-04-15)
- **Task:** Add documentation for the calculator application
- **Branch:** exp3/issue-276-documentation
- **Files changed:** src/__init__.py, src/calculator.py, src/__main__.py, README.md
- **Outcome:** Added module-level docstrings to src/__init__.py, src/calculator.py, and src/__main__.py. Added class docstring and __init__ docstring to Calculator. Added method docstrings to all 12 Calculator operation methods that lacked them. Added main() docstring. Expanded README.md from a placeholder title to a full user guide (installation, CLI/REPL usage examples, operations table, project structure, test instructions). 149 tests collected, 149 passed.
- **Key decisions:** Docstrings follow the existing short-sentence style already used in arithmetic.py and advanced.py. README documents both usage modes (CLI and interactive REPL) with concrete examples. No logic was changed — purely additive documentation.
- **Cost:** PENDING
- **Turns:** PENDING

## Cycle 11 — Issue #273: Modularization (2026-04-15)
- **Task:** Refactor the calculator into more modules and prepare the structure for a future scientific mode
- **Branch:** exp3/issue-273-modularization
- **Files changed:** src/calculator.py, src/operations/__init__.py (new), src/operations/arithmetic.py (new), src/operations/advanced.py (new), src/operations/scientific.py (new)
- **Outcome:** Created `src/operations/` sub-package. Extracted pure arithmetic functions (add/subtract/multiply/divide) into `arithmetic.py` and pure advanced functions (factorial/square/cube/square_root/cube_root/power/log/ln) into `advanced.py`. Added `scientific.py` as a placeholder stub for future scientific mode. Calculator methods now delegate to these pure functions; error logging and history recording remain in the Calculator layer. 149 tests collected, 149 passed.
- **Key decisions:** Operation functions are pure (no logging, no state) — this keeps the operations modules reusable and testable in isolation. Calculator retains logging/history as cross-cutting concerns. scientific.py is an empty stub with a docstring; it signals intent without adding speculative logic. Public Calculator API is unchanged, so all existing tests pass without modification.
- **Cost:** PENDING
- **Turns:** PENDING

## Cycle 10 — Issue #269: Logic Separation (2026-04-15)
- **Task:** Separate calculator logic from the interface layer
- **Branch:** exp3/issue-269-logic-separation
- **Files changed:** src/calculator.py, src/__main__.py, tests/test_calculator.py
- **Outcome:** Moved UNARY_OPS, BINARY_OPS, INTEGER_OPS constants and _to_int_if_needed() from __main__.py to calculator.py. Added Calculator.execute() method that handles operation dispatch, integer coercion, and history recording — keeping history tracking fully within the logic layer. __main__.py now imports these symbols from calculator and uses execute() in run_operation/cli_main instead of calling getattr(calc, op)() + calc.history.append() directly. Added 15 new tests for execute() and the new module-level symbols. 149 tests collected, 149 passed.
- **Key decisions:** execute() records history on success and propagates exceptions unchanged — so run_operation/cli_main still catch and log errors at the interface layer. Interface module retains MENU_MAP, MAX_INPUT_ATTEMPTS, MENU, parse_number, _format_result, _show_history, run_operation, cli_main, main as pure I/O concerns. No tests were removed or changed in logic; one stale comment in test_calculator.py was updated.
- **Cost:** PENDING
- **Turns:** PENDING

## Cycle 9 — Issue #251: Error Logging (2026-04-12)
- **Task:** Add error logging to the calculator
- **Branch:** exp3/issue-251-add-error-logging
- **Files changed:** src/calculator.py, src/__main__.py, tests/test_calculator.py, tests/test_main.py
- **Outcome:** Added module-level `logger = logging.getLogger(__name__)` to both src/calculator.py and src/__main__.py. Wrapped divide, factorial, square_root, log, and ln in Calculator with try/except/raise to log at ERROR level before re-raising. Added `logger.error(...)` calls in `run_operation` and `cli_main` where exceptions are caught. Configured `logging.basicConfig(level=ERROR)` in `main()`. Added 9 new tests using `caplog` fixture. 134 tests collected, 134 passed.
- **Key decisions:** Logging is done at the point of catch/re-raise rather than by restructuring exception flow — exceptions continue to propagate unchanged, preserving existing caller behavior. `logging.basicConfig` is only called in `main()` (the entry point), not in library code, following Python logging best practices. Library code (calculator.py, __main__ module-level) only creates loggers, never configures them.
- **Cost:** PENDING
- **Turns:** PENDING

## Cycle 8 — Issue #248: History (2026-04-12)
- **Task:** Add history of operations to the calculator
- **Branch:** exp3/issue-248-add-history
- **Files changed:** src/calculator.py, src/__main__.py, tests/test_calculator.py, tests/test_main.py
- **Outcome:** Added `self.history: list[dict]` and `get_history()` to Calculator; `run_operation` appends `{"op", "operands", "result"}` on success (errors are not recorded); added `_show_history(calc)` helper; REPL 'h' choice displays history; MENU updated to show 'h' option. 125 tests collected, 125 passed.
- **Key decisions:** History is recorded externally (in `run_operation`) rather than inside Calculator methods — keeps computation methods side-effect-free. Only successful operations are recorded (failed inputs/domain errors produce no entry). `get_history()` returns a copy to prevent external mutation of internal state.
- **Cost:** PENDING
- **Turns:** PENDING

## Cycle 7 — Issue #245: Input Validation (2026-04-12)
- **Task:** Add validation for bad input and let the user retry a few times
- **Branch:** exp3/issue-245-input-validation
- **Files changed:** src/__main__.py, tests/test_main.py
- **Outcome:** Added `MAX_INPUT_ATTEMPTS = 3` constant; changed `parse_number` from infinite-loop to a bounded retry loop with remaining-attempts feedback; on exhaustion raises `ValueError` which `run_operation` already catches. Added 4 new tests (retry exhaustion, remaining count, run_operation error path). 113 tests collected, 113 passed.
- **Key decisions:** Used a simple `for` loop instead of `while True` to enforce the limit naturally. Kept `max_attempts` as an optional parameter (defaulting to `MAX_INPUT_ATTEMPTS`) so tests can override it without patching the constant. The `ValueError` raised on exhaustion reuses the existing `run_operation` catch clause — no additional handler was needed.
- **Cost:** PENDING
- **Turns:** PENDING

## Cycle 6 — Issue #239: CLI Mode (2026-04-12)
- **Task:** Add CLI mode so the calculator can be used from bash
- **Branch:** exp3/issue-239-cli-mode
- **Files changed:** src/__main__.py, tests/test_main.py
- **Outcome:** Added `cli_main(args)` and `_format_result(value)` to `__main__.py`. `main()` dispatches to `cli_main` when `sys.argv` has arguments, else runs the REPL. 110 tests collected, 110 passed.
- **Key decisions:** Used `sys.argv` check in `main()` rather than argparse — interface is simple enough (operation + operands) that stdlib-only dispatch suffices. `_format_result` converts whole floats to integer strings for cleaner bash output. Fixed three existing `main()` tests that needed `patch("sys.argv", ["prog"])` after the argv check was added.
- **Cost:** PENDING
- **Turns:** PENDING

## Cycle 5 — Issue #220: Add User Input (2026-04-12)
- **Task:** Add user input to the calculator (interactive CLI)
- **Branch:** exp3/issue-220-user-input
- **Files changed:** src/__main__.py, tests/test_main.py (new)
- **Outcome:** Replaced hardcoded demo in `__main__.py` with a full interactive REPL. 84 tests collected, 84 passed.
- **Key decisions:** `parse_number` loops on invalid input rather than crashing. `factorial` inputs are converted float→int to satisfy `math.factorial`; non-whole inputs raise `ValueError`. `run_operation` catches `ValueError`/`ZeroDivisionError` so the REPL never exits on bad operands. MENU_MAP maps "1"–"12" to all 12 Calculator operations.
- **Cost:** PENDING
- **Turns:** PENDING

## Cycle 4 — Issue #217: Add Multiple Math Functions (2026-04-12)
- **Task:** Add square, cube, square root, cube root, power, log and ln to Calculator
- **Branch:** exp3/issue-217-add-math-functions
- **Files changed:** src/calculator.py, tests/test_calculator.py
- **Outcome:** Added 7 new methods; 58 tests collected, 58 passed.
- **Key decisions:** Used `math.cbrt` (Python 3.11+, project targets 3.12) for cube root to correctly handle negative inputs. Used `math.sqrt` for square root (raises ValueError for negative). Implemented `log` as base-10 via `math.log10`, `ln` as natural log via `math.log`. Both log/ln raise ValueError for domain violations via stdlib delegation. `power` uses `**` operator directly.
- **Cost:** PENDING
- **Turns:** PENDING

## Cycle 3 — Issue #214: Add Factorial (2026-04-12)
- **Task:** Add factorial operation to Calculator
- **Branch:** exp3/issue-214-add-factorial
- **Files changed:** src/calculator.py, tests/test_calculator.py
- **Outcome:** Added `Calculator.factorial(n)` via `math.factorial`; 28 tests collected, 28 passed.
- **Key decisions:** Used `math.factorial` from stdlib to delegate validation (raises `ValueError` for negatives), consistent with existing pattern of relying on Python built-in behavior. Added `import math` at module level.
- **Cost:** PENDING
- **Turns:** PENDING

## Cycle 2 — Issue #211: Calculator Test Suite (2026-04-12)
- **Task:** Create comprehensive tests for the Calculator class
- **Branch:** exp3/issue-211-calculator-tests
- **Files changed:** tests/test_calculator.py, progress.md
- **Outcome:** Expanded from 1 test to 23 tests; 23 collected, 23 passed.
- **Key decisions:** Retained existing `test_divide_by_zero_raises`. Added 5 tests per arithmetic operation (add, subtract) and 6 for multiply, 7 for divide — covering positive, negative, mixed-sign, zero, float, and boundary (identity element) inputs. Used `pytest.approx` for float comparisons.
- **Cost:** PENDING
- **Turns:** PENDING

## Cycle 1 — Issue #208: ZeroDivisionTest (2026-04-12)
- **Task:** Add test for incorrect inputs in division (ZeroDivisionError)
- **Branch:** exp3/issue-208-zero-division-test
- **Files changed:** tests/test_calculator.py
- **Outcome:** Added `test_divide_by_zero_raises`; 1 test collected, 1 passed.
- **Key decisions:** Used `pytest.raises(ZeroDivisionError)` to assert built-in Python behavior — no changes needed to Calculator itself since `divide` already raises natively.
- **Cost:** PENDING
- **Turns:** PENDING

## Cycle 0 — Bootstrap (2026-04-12)
- **Task:** RAG initialization
- **Files changed:** rag/index.md, rag/codebase_map.md, rag/evolution_log.md, rag/patterns.md
- **Outcome:** RAG knowledge base created from current state of src/ and tests/
- **Lessons learned:** Project is minimal — one Calculator class with four arithmetic ops, and an empty test file.
- **Cost:** N/A (initialization)
- **Turns:** N/A
