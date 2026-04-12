# RAG Index

Last updated: cycle 7

| File | Purpose | Last Updated Cycle |
|------|---------|-------------------|
| src/__init__.py | Package init, exports Calculator | 0 |
| src/calculator.py | Calculator class with add/subtract/multiply/divide/factorial/square/cube/square_root/cube_root/power/log/ln | 4 |
| src/__main__.py | CLI + interactive REPL: bash argv dispatch (cli_main), numbered menu REPL, parse_number (retry-limited), _format_result | 7 |
| tests/test_calculator.py | Full test suite: 58 tests for all 12 operations | 4 |
| tests/test_main.py | CLI tests: 56 tests covering parse_number (incl. retry-limit), MENU_MAP, run_operation, cli_main (all 12 ops + errors), main dispatch | 7 |

## RAG Files
| RAG File | Purpose |
|----------|---------|
| rag/codebase_map.md | Per-file summaries, public API, invariants |
| rag/evolution_log.md | Per-cycle entries: task, files changed, outcome |
| rag/patterns.md | Recurring patterns and anti-patterns |
