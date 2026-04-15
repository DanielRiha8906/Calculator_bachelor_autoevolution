# RAG Index

Master index of summarized files. Updated each evolution cycle.

| File | Purpose | Last Updated (cycle) |
|------|---------|----------------------|
| `src/__init__.py` | Package init; exports `Calculator` | 0 |
| `src/__main__.py` | Interactive CLI: menu-driven session loop with retry logic, MAX_ATTEMPTS=5, per-session history, and error logging | 9 |
| `src/calculator.py` | Core `Calculator` class with add/subtract/multiply/divide/factorial/square/cube/square_root/cube_root/power/log/ln | 4 |
| `src/error_logger.py` | Append-mode error logger: log_error(source, message) writes timestamped entries to ERROR_LOG_FILE (error.log) | 9 |
| `tests/conftest.py` | Pytest autouse fixture isolating error log writes to tmp_path for all tests | 9 |
| `tests/test_calculator.py` | 76-test suite for Calculator; all ops, edge cases, float precision, ZeroDivisionError, factorial/sqrt/log/ln validation | 4 |
| `tests/test_error_logger.py` | 7-test suite for error_logger: file creation, source/message/timestamp format, append, per-line invariant | 9 |
| `tests/test_main.py` | 56-test suite for the interactive CLI; covers OPERATIONS map, get_number, retry logic, session termination, all 12 ops, error paths, multi-session, history display, history file write, error logging | 9 |
| `main.py` | Bash-accessible CLI entry point: `python main.py <op> [a] [b]`; dispatches all 12 ops by name, exits 0/1, logs errors | 9 |
| `tests/test_cli.py` | 34-test suite for main.py CLI: all 12 ops, arg-count validation, error paths, non-numeric operands, error logging | 9 |
