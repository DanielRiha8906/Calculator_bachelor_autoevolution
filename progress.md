# Progress Log

## Run: Issue #220 — Add User Input (2026-04-12)

- **Branch:** exp3/issue-220-user-input
- **Target PR branch:** exp3/naive-generic
- **Files changed:** src/__main__.py, tests/test_main.py (new)
- **Purpose:** Replaced hardcoded demo values in `__main__.py` with a full interactive REPL. Presents a numbered menu of all 12 Calculator operations. `parse_number` loops until the user enters a valid float. `run_operation` dispatches to the correct Calculator method and catches `ValueError`/`ZeroDivisionError` so the loop never crashes. `factorial` inputs are converted float→int (with an error for non-whole numbers).
- **Risks:** Minimal — no changes to `Calculator` class or existing tests. New code uses only stdlib (`builtins.input`, `getattr`). No new dependencies.
- **Tests passed:** Yes — 84 collected (58 existing + 26 new in tests/test_main.py), 84 passed.
- **RAG entries consulted:** rag/index.md, rag/codebase_map.md, rag/evolution_log.md, rag/patterns.md
Duration: 182.5s | Cost: $0.580864 USD | Turns: 34

## Run: Diagram Update (2026-04-12)

- **Branch:** exp3/issue-217-add-math-functions
- **Files changed:** artifacts/class_diagram.puml, artifacts/activity_diagram.puml, artifacts/sequence_diagram.puml
- **Purpose:** Updated all three PlantUML diagrams to reflect the full 12-method Calculator API (square, cube, square_root, cube_root, power, log, ln were missing from prior diagrams which only showed 5 methods).
- **Risks:** None — diagram-only update, no source code changes.
- **Tests passed:** N/A — no code changes.
- **RAG entries consulted:** rag/index.md, rag/codebase_map.md
Duration: 61.5s | Cost: $0.220107 USD | Turns: 19

## Run: Issue #217 — Add Multiple Math Functions (2026-04-12)

- **Branch:** exp3/issue-217-add-math-functions
- **Target PR branch:** exp3/naive-generic
- **Files changed:** src/calculator.py, tests/test_calculator.py
- **Purpose:** Added 7 new Calculator methods: square, cube, square_root, cube_root, power, log (base-10), ln (natural log). Added 30 new tests covering all seven operations with positive, negative, zero, float, and error-path inputs.
- **Risks:** Minimal — all delegation to stdlib (`math.sqrt`, `math.cbrt`, `math.log10`, `math.log`). `math.cbrt` requires Python 3.11+ which is satisfied by project's Python 3.12 requirement. No new dependencies added.
- **Tests passed:** Yes — 58 collected, 58 passed.
- **RAG entries consulted:** rag/index.md, rag/codebase_map.md, rag/patterns.md
Duration: 127.1s | Cost: $0.470713 USD | Turns: 28

## Run: Issue #208 — ZeroDivisionTest (2026-04-12)

- **Branch:** exp3/issue-208-zero-division-test
- **Target PR branch:** exp3/naive-generic
- **Files changed:** tests/test_calculator.py
- **Purpose:** Added `test_divide_by_zero_raises` to verify that `Calculator.divide` raises `ZeroDivisionError` when divisor is 0, covering incorrect-input handling for division.
- **Risks:** None — test only; no changes to source code.
- **Tests passed:** Yes — 1 collected, 1 passed.
- **RAG entries consulted:** RAG initialized this run; `rag/codebase_map.md` used to confirm `divide` raises ZeroDivisionError natively (no source code changes required).
- Duration: 125.1s | Cost: $0.522137 USD | Turns: 41

## Run: Issue #211 — Calculator Test Suite (2026-04-12)

- **Branch:** exp3/issue-211-calculator-tests
- **Target PR branch:** exp3/naive-generic
- **Files changed:** tests/test_calculator.py
- **Purpose:** Expanded test suite from 1 test to 23 tests covering all four Calculator operations (add, subtract, multiply, divide) with positive, negative, mixed-sign, zero, float, and edge-case inputs.
- **Risks:** None — tests only; no changes to source code.
- **Tests passed:** Yes — 23 collected, 23 passed.
- **RAG entries consulted:** rag/index.md, rag/codebase_map.md, rag/evolution_log.md
- Duration: 92.6s | Cost: $0.318279 USD | Turns: 26

## Run: Issue #214 — Add Factorial (2026-04-12)

- **Branch:** exp3/issue-214-add-factorial
- **Target PR branch:** exp3/naive-generic
- **Files changed:** src/calculator.py, tests/test_calculator.py
- **Purpose:** Added `Calculator.factorial(n)` using `math.factorial`; raises `ValueError` for negative inputs. Added 5 tests: factorial(0), factorial(1), factorial(5), factorial(10), and negative-input error case.
- **Risks:** Minimal — added `import math` at module level; `math` is stdlib so no new dependencies. All existing 23 tests continue to pass.
- **Tests passed:** Yes — 28 collected, 28 passed.
- **RAG entries consulted:** rag/index.md, rag/codebase_map.md, rag/patterns.md
Duration: 100.8s | Cost: $0.384814 USD | Turns: 29

## Run: Diagram Update (2026-04-12)

- **Branch:** exp3/issue-208-zero-division-test
- **Files changed:** artifacts/class_diagram.puml, artifacts/activity_diagram.puml, artifacts/sequence_diagram.puml
- **Purpose:** Created all three required PlantUML diagrams reflecting the current state of `src/` (Calculator class with add/subtract/multiply/divide, __main__ entry point, ZeroDivisionError behaviour on divide).
- **Risks:** None — diagram-only update; no source or test changes.
- **Tests passed:** N/A (no code changes)
- **RAG entries consulted:** rag/codebase_map.md, rag/index.md
- Duration: 48.5s | Cost: $0.181222 USD | Turns: 18

## Run: Diagram Update (2026-04-12)

- **Branch:** exp3/issue-211-calculator-tests
- **Files changed:** artifacts/class_diagram.puml, artifacts/activity_diagram.puml, artifacts/sequence_diagram.puml (verified current; no changes needed)
- **Purpose:** Verified all three PlantUML diagrams remain accurate against current `src/` state. No source code changes since last diagram update; diagrams unchanged.
- **Risks:** None — diagram verification run; no source or test changes.
- **Tests passed:** N/A (no code changes)
- **RAG entries consulted:** rag/index.md, rag/codebase_map.md
- Duration: 35.9s | Cost: $0.152743 USD | Turns: 17

## Run: Diagram Update (2026-04-12)

- **Branch:** exp3/issue-214-add-factorial
- **Files changed:** artifacts/class_diagram.puml, artifacts/activity_diagram.puml, artifacts/sequence_diagram.puml
- **Purpose:** Updated all three PlantUML diagrams to reflect `Calculator.factorial(n)` added in cycle 3. Added `factorial` method to class diagram with ValueError note; noted factorial availability in activity diagram; added factorial sequence with `math` participant in sequence diagram.
- **Risks:** None — diagram-only update; no source or test changes.
- **Tests passed:** N/A (no code changes)
- **RAG entries consulted:** rag/index.md, rag/codebase_map.md
- Duration: 51.0s | Cost: $0.192411 USD | Turns: 19
