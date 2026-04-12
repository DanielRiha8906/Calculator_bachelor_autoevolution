# RAG Index

Master index of summarized files. Updated each evolution cycle.

| File | Purpose | Last Updated (cycle) |
|------|---------|----------------------|
| `src/__init__.py` | Package init; exports `Calculator` | 0 |
| `src/__main__.py` | Interactive CLI: menu-driven session loop for all 12 Calculator operations | 5 |
| `src/calculator.py` | Core `Calculator` class with add/subtract/multiply/divide/factorial/square/cube/square_root/cube_root/power/log/ln | 4 |
| `tests/test_calculator.py` | 76-test suite for Calculator; all ops, edge cases, float precision, ZeroDivisionError, factorial/sqrt/log/ln validation | 4 |
| `tests/test_main.py` | 32-test suite for the interactive CLI; covers OPERATIONS map, get_number, all 12 ops, error paths, multi-session | 5 |
