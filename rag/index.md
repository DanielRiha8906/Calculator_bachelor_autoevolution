# RAG Index

Last updated: cycle 9

| File | Purpose | Last Updated Cycle |
|------|---------|-------------------|
| src/__init__.py | Package init, exports Calculator | 0 |
| src/calculator.py | Calculator class with add/subtract/multiply/divide/factorial/square/cube/square_root/cube_root/power/log/ln; history list and get_history(); error logging via module-level logger | 9 |
| src/__main__.py | CLI + interactive REPL: bash argv dispatch (cli_main), numbered menu REPL, parse_number (retry-limited), _format_result, _show_history, 'h' history choice; error logging via module-level logger | 9 |
| tests/test_calculator.py | Full test suite: 67 tests for all 12 operations + history invariants + error logging (caplog) | 9 |
| tests/test_main.py | CLI tests: 75 tests covering parse_number (incl. retry-limit), MENU_MAP, run_operation (incl. history recording + error logging), _show_history, cli_main (all 12 ops + errors + error logging), main dispatch, history REPL flow | 9 |

## RAG Files
| RAG File | Purpose |
|----------|---------|
| rag/codebase_map.md | Per-file summaries, public API, invariants |
| rag/evolution_log.md | Per-cycle entries: task, files changed, outcome |
| rag/patterns.md | Recurring patterns and anti-patterns |
