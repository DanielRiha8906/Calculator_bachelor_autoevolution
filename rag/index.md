# RAG Index

Master index of summarized files. Updated each evolution cycle.

| File | Purpose | Last Updated (cycle) |
|------|---------|----------------------|
| `src/__init__.py` | Package init; exports `Calculator` | 0 |
| `src/__main__.py` | Interactive CLI: menu-driven session loop for all 12 Calculator operations | 5 |
| `src/calculator.py` | Core `Calculator` class with add/subtract/multiply/divide/factorial/square/cube/square_root/cube_root/power/log/ln | 4 |
| `tests/test_calculator.py` | 76-test suite for Calculator; all ops, edge cases, float precision, ZeroDivisionError, factorial/sqrt/log/ln validation | 4 |
| `tests/test_main.py` | 32-test suite for the interactive CLI; covers OPERATIONS map, get_number, all 12 ops, error paths, multi-session | 5 |
| `main.py` | Bash-accessible CLI entry point: `python main.py <op> [a] [b]`; dispatches all 12 ops by name, exits 0/1 | 6 |
| `tests/test_cli.py` | 28-test suite for main.py CLI: all 12 ops, arg-count validation, error paths, non-numeric operands | 6 |
