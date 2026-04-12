# RAG Index

Last updated: cycle 5

| File | Purpose | Last Updated Cycle |
|------|---------|-------------------|
| src/__init__.py | Package init, exports Calculator | 0 |
| src/calculator.py | Calculator class with add/subtract/multiply/divide/factorial/square/cube/square_root/cube_root/power/log/ln | 4 |
| src/__main__.py | Interactive CLI REPL: numbered menu for all 12 ops, user input, error handling | 5 |
| tests/test_calculator.py | Full test suite: 58 tests for all 12 operations | 4 |
| tests/test_main.py | CLI tests: 26 tests for parse_number, MENU_MAP, run_operation (all 12 ops + error paths), main loop | 5 |

## RAG Files
| RAG File | Purpose |
|----------|---------|
| rag/codebase_map.md | Per-file summaries, public API, invariants |
| rag/evolution_log.md | Per-cycle entries: task, files changed, outcome |
| rag/patterns.md | Recurring patterns and anti-patterns |
