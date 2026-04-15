# RAG Index

Master index of summarized files. `last-updated` is the cycle number when the summary was last written.

| File | One-line purpose | Last-updated |
|------|-----------------|--------------|
| src/__init__.py | Package init — exports Calculator class | 12 |
| src/calculator.py | Calculator class delegating to operations sub-modules + execute dispatch | 12 |
| src/operations/__init__.py | Operations sub-package init | 11 |
| src/operations/basic.py | Pure functions: add, subtract, multiply, divide | 11 |
| src/operations/scientific.py | Pure functions: factorial, square, cube, square_root, cube_root, power, log, ln | 11 |
| src/interface/__init__.py | Interface sub-package init | 11 |
| src/interface/history.py | HISTORY_FILE/ERROR_LOG_FILE constants + history and error-log file helpers | 11 |
| src/interface/interactive.py | Interactive menu mode: TooManyAttemptsError, NORMAL_MODE_OPERATIONS, SCIENTIFIC_MODE_OPERATIONS, OPERATIONS, arity sets, show_menu(operations, mode), parse_number, parse_int, run_operation | 13 |
| src/interface/cli.py | Non-interactive CLI mode: cli_mode function | 11 |
| src/__main__.py | Thin entry point: main() with normal/scientific/GUI mode toggle + re-exports from interface sub-package | 14 |
| src/interface/gui.py | tkinter GUI: CalculatorApp (normal/scientific mode, calculate, inline history panel, full history viewer) + launch_gui() entry-point | 15 |
| tests/test_calculator.py | Full unit test suite for Calculator — 68 tests covering all operations including execute | 10 |
| tests/test_main.py | Unit tests for interactive CLI and cli_mode — 92 tests with mocked input; monkeypatches target src.interface.history | 14 |
| tests/test_gui.py | Headless GUI tests — 38 tests using dependency-injected MagicMock tkinter; covers mode switching, _compute, history | 15 |
