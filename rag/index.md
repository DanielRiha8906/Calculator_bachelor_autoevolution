# RAG Index

Last updated: cycle 15

| File | Purpose | Last Updated Cycle |
|------|---------|-------------------|
| src/__init__.py | Package init, exports Calculator | 12 |
| src/calculator.py | Calculator class; UNARY_OPS/BINARY_OPS/INTEGER_OPS/SCIENTIFIC_UNARY_OPS constants; 22 ops total; execute() dispatch; error logging | 13 |
| src/__main__.py | Interface layer: GUI (--gui flag), CLI + interactive REPL with normal/scientific mode switching ('m'); MENU_MAP, SCIENTIFIC_MENU_MAP | 14 |
| src/gui.py | Tkinter GUI: CalculatorGUI class + launch_gui(); all 22 ops; modern dark theme with hover via _make_button(); sci panel toggle; history dialog | 15 |
| src/operations/__init__.py | Operations sub-package init; re-exports all arithmetic, advanced, and scientific functions | 13 |
| src/operations/arithmetic.py | Pure functions: add, subtract, multiply, divide | 11 |
| src/operations/advanced.py | Pure functions: factorial, square, cube, square_root, cube_root, power, log, ln | 11 |
| src/operations/scientific.py | Pure functions: sin, cos, tan, asin, acos, atan, sinh, cosh, tanh, exp (all in radians) | 13 |
| tests/test_calculator.py | Full test suite: 109 tests; adds scientific op tests and SCIENTIFIC_UNARY_OPS constant test | 13 |
| tests/test_main.py | CLI tests: 96 tests; adds --gui flag test for main() | 14 |
| tests/test_gui.py | GUI tests: 46 tests; tkinter mocked via sys.modules injection; covers all CalculatorGUI logic methods | 14 |

## RAG Files
| RAG File | Purpose |
|----------|---------|
| rag/codebase_map.md | Per-file summaries, public API, invariants |
| rag/evolution_log.md | Per-cycle entries: task, files changed, outcome |
| rag/patterns.md | Recurring patterns and anti-patterns |
