# Evolution Log

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
