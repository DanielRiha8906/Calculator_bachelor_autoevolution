# RAG Index

Last updated: cycle 11

| File | Purpose | Last Updated Cycle |
|------|---------|-------------------|
| src/__init__.py | Package init, exports Calculator | 0 |
| src/calculator.py | Calculator class delegating to operations sub-package; UNARY_OPS/BINARY_OPS/INTEGER_OPS constants; _to_int_if_needed(); history via execute(); error logging | 11 |
| src/__main__.py | Pure interface layer: CLI + interactive REPL; imports op-set constants from calculator; run_operation/cli_main delegate to calc.execute(); parse_number, _format_result, _show_history | 10 |
| src/operations/__init__.py | Operations sub-package init; re-exports all arithmetic and advanced operation functions | 11 |
| src/operations/arithmetic.py | Pure functions: add, subtract, multiply, divide | 11 |
| src/operations/advanced.py | Pure functions: factorial, square, cube, square_root, cube_root, power, log, ln | 11 |
| src/operations/scientific.py | Placeholder stub for future scientific mode operations | 11 |
| tests/test_calculator.py | Full test suite: 82 tests for all 12 operations + history + error logging + execute() dispatch + module-level constants/helpers | 10 |
| tests/test_main.py | CLI tests: 75 tests covering parse_number (incl. retry-limit), MENU_MAP, run_operation (incl. history recording + error logging), _show_history, cli_main (all 12 ops + errors + error logging), main dispatch, history REPL flow | 9 |

## RAG Files
| RAG File | Purpose |
|----------|---------|
| rag/codebase_map.md | Per-file summaries, public API, invariants |
| rag/evolution_log.md | Per-cycle entries: task, files changed, outcome |
| rag/patterns.md | Recurring patterns and anti-patterns |
