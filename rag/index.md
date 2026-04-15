# RAG Index

Master index of summarized files. Updated each evolution cycle.

| File | Purpose | Last Updated (cycle) |
|------|---------|----------------------|
| `README.md` | User and developer documentation: setup, interactive mode, bash CLI, all 12 ops, session files, code structure, test instructions | 13 |
| `src/__init__.py` | Package init; exports `Calculator` and `CalculatorSession` | 11 |
| `src/__main__.py` | Interactive CLI: Normal/Scientific mode switching, menu-driven session loop, retry logic, MAX_ATTEMPTS=5, per-session history, error logging | 14 |
| `src/calculator.py` | `Calculator(BasicOperations, ScientificOperations)` — unified class inheriting all 18 ops from the operations package | 12 |
| `src/operations/__init__.py` | Operations package init; re-exports `BasicOperations` and `ScientificOperations` | 12 |
| `src/operations/basic.py` | `BasicOperations` mixin: add, subtract, multiply, divide | 12 |
| `src/operations/scientific.py` | `ScientificOperations` mixin: factorial, square, cube, square_root, cube_root, power, log, ln, sin, cos, tan, cot, asin, acos (all trig in degrees) | 14 |
| `src/error_logger.py` | Append-mode error logger: log_error(source, message) writes timestamped entries to ERROR_LOG_FILE (error.log) | 9 |
| `src/session.py` | CalculatorSession: operation dispatch + history management; BINARY_OPS/UNARY_OPS/ALL_OPS shared metadata (18 total ops) | 14 |
| `tests/conftest.py` | Pytest autouse fixture isolating error log writes to tmp_path for all tests | 9 |
| `tests/test_calculator.py` | 76-test suite for Calculator; all ops, edge cases, float precision, ZeroDivisionError, factorial/sqrt/log/ln validation | 4 |
| `tests/test_error_logger.py` | 7-test suite for error_logger: file creation, source/message/timestamp format, append, per-line invariant | 9 |
| `tests/test_main.py` | 80+-test suite for the interactive CLI; covers mode switching, NORMAL/SCIENTIFIC ops maps, all 18 ops including trig, retry logic, history, error logging | 14 |
| `tests/test_session.py` | 49-test suite for CalculatorSession: op metadata sets (18 ops), format_entry, execute (all 18 ops + error paths), history tracking, save() | 14 |
| `main.py` | Bash-accessible CLI entry point: `python main.py <op> [a] [b]`; imports op sets from src.session, uses CalculatorSession, exits 0/1, logs errors | 11 |
| `tests/test_cli.py` | 34-test suite for main.py CLI: all 12 ops, arg-count validation, error paths, non-numeric operands, error logging | 9 |
| `src/gui.py` | Tkinter GUI: CalculatorGUI + ModeSelector, OperationSelector, OperandSection, ResultDisplay, HistoryPanel; Normal/Scientific modes; auto-hides Operand B for unary ops | 15 |
| `gui_main.py` | Root-level GUI entry point: `python gui_main.py`; delegates to `src.gui.main()` | 15 |
| `tests/test_gui.py` | GUI test suite (skipped if tkinter absent): _parse_number, each section class, CalculatorGUI integration (calculate, clear, history, mode switch, error display) | 15 |
