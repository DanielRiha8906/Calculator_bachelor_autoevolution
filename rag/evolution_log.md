# Evolution Log

Per-cycle entries: task, files changed, outcome, lessons learned.

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
