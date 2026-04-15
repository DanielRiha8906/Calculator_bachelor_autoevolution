# Codebase Map

## src/__init__.py
- **Purpose:** Package initializer for the `src` module; re-exports Calculator.
- **Exports:** `Calculator`
- **Key invariants:** Re-exports Calculator from `src.calculator` via `__all__`. Has a module-level docstring describing the package purpose.
- **Last updated:** cycle 12

## src/calculator.py
- **Purpose:** Core calculator facade: per-instance history, error logging, and operation dispatch; delegates operation implementations to the `src.operations` sub-package.
- **Imports:** `from .operations import arithmetic, advanced, scientific`
- **Module-level docstring:** Present — describes module role and cross-cutting concerns.
- **Module-level constants:** `UNARY_OPS`, `BINARY_OPS`, `INTEGER_OPS`, `SCIENTIFIC_UNARY_OPS` — sets classifying all operations by arity and type requirements.
- **Module-level helpers:** `_to_int_if_needed(op, value)` — coerces value to int for INTEGER_OPS, raises ValueError for non-whole numbers.
- **Module-level:** `logger = logging.getLogger(__name__)` — logs errors at ERROR level before re-raising.
- **Public API:**
  - `Calculator.__init__()` → initialises `self.history: list[dict]` to `[]`; has docstring
  - `Calculator.get_history()` → returns a shallow copy of `self.history`
  - `Calculator.add(a, b)`, `subtract`, `multiply`, `divide` → arithmetic ops; divide logs ZeroDivisionError
  - `Calculator.factorial(n)`, `square`, `cube`, `square_root`, `cube_root`, `power`, `log`, `ln` → advanced ops; factorial/square_root/log/ln log ValueError
  - `Calculator.sin(x)`, `cos(x)`, `tan(x)` → trigonometric (radians); no error logging needed
  - `Calculator.asin(x)`, `acos(x)` → inverse trig; logs and raises `ValueError` for `|x| > 1`
  - `Calculator.atan(x)`, `sinh(x)`, `cosh(x)`, `tanh(x)`, `exp(x)` → hyperbolic/exponential; no domain errors
  - `Calculator.execute(op, *operands)` → dispatches by op name across BINARY_OPS, UNARY_OPS, SCIENTIFIC_UNARY_OPS; applies _to_int_if_needed for INTEGER_OPS; records history on success; propagates exceptions unchanged; raises ValueError for unknown ops.
- **Key invariants:** History is recorded by `execute()`, not by individual Calculator methods. Each history entry is `{"op": str, "operands": tuple, "result": float|int}`. Failed operations are not recorded. `get_history()` returns a copy — callers cannot mutate internal state. SCIENTIFIC_UNARY_OPS are not in UNARY_OPS (separate set). All scientific ops are unary.
- **Last updated:** cycle 13

## src/operations/__init__.py
- **Purpose:** Operations sub-package initializer; re-exports all arithmetic, advanced, and scientific operation functions for convenience.
- **Exports:** `add`, `subtract`, `multiply`, `divide`, `factorial`, `square`, `cube`, `square_root`, `cube_root`, `power`, `log`, `ln`, `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `sinh`, `cosh`, `tanh`, `exp`
- **Last updated:** cycle 13

## src/operations/arithmetic.py
- **Purpose:** Pure arithmetic operation functions with no side effects.
- **Public API:**
  - `add(a, b)` → `a + b`
  - `subtract(a, b)` → `a - b`
  - `multiply(a, b)` → `a * b`
  - `divide(a, b)` → `a / b` (raises `ZeroDivisionError` natively if `b == 0`)
- **Key invariants:** No logging, no state. All functions are pure.
- **Last updated:** cycle 11

## src/operations/advanced.py
- **Purpose:** Pure advanced mathematical operation functions (power, roots, factorial, logarithms) with no side effects.
- **Imports:** `math`
- **Public API:**
  - `factorial(n)` → `math.factorial(n)` (raises `ValueError` for negative `n`)
  - `square(n)` → `n ** 2`
  - `cube(n)` → `n ** 3`
  - `square_root(n)` → `math.sqrt(n)` (raises `ValueError` for negative `n`)
  - `cube_root(n)` → `math.cbrt(n)` (handles negative inputs; requires Python 3.11+)
  - `power(base, exp)` → `base ** exp`
  - `log(n)` → `math.log10(n)` (raises `ValueError` for `n <= 0`)
  - `ln(n)` → `math.log(n)` (raises `ValueError` for `n <= 0`)
- **Key invariants:** No logging, no state. All functions are pure.
- **Last updated:** cycle 11

## src/operations/scientific.py
- **Purpose:** Pure scientific math operation functions (trigonometric, hyperbolic, exponential) with no side effects. All angle inputs/outputs in radians.
- **Imports:** `math`
- **Public API:**
  - `sin(x)` → `math.sin(x)`
  - `cos(x)` → `math.cos(x)`
  - `tan(x)` → `math.tan(x)`
  - `asin(x)` → `math.asin(x)` (raises `ValueError` for `|x| > 1`)
  - `acos(x)` → `math.acos(x)` (raises `ValueError` for `|x| > 1`)
  - `atan(x)` → `math.atan(x)`
  - `sinh(x)` → `math.sinh(x)`
  - `cosh(x)` → `math.cosh(x)`
  - `tanh(x)` → `math.tanh(x)`
  - `exp(x)` → `math.exp(x)`
- **Key invariants:** No logging, no state. All functions are pure.
- **Last updated:** cycle 13

## src/__main__.py
- **Purpose:** Pure interface layer for the Calculator: bash argv mode and interactive REPL with normal/scientific mode switching, with error logging.
- **Module-level docstring:** Present — documents both CLI and REPL usage modes with examples.
- **Imports from calculator:** `Calculator`, `BINARY_OPS`, `UNARY_OPS`, `SCIENTIFIC_UNARY_OPS`
- **Exports:** `parse_number(prompt, max_attempts)`, `run_operation(calc, op)`, `_format_result(value)`, `_show_history(calc)`, `cli_main(args)`, `main()`
- **Module-level constants:** `MAX_INPUT_ATTEMPTS`, `MENU`, `MENU_MAP`, `SCIENTIFIC_MENU`, `SCIENTIFIC_MENU_MAP`
- **Module-level:** `logger = logging.getLogger(__name__)` — logs caught errors at ERROR level.
- **Key invariants:**
  - `main()` tracks `mode` ("normal" or "scientific"). Pressing 'm' toggles mode and prints a confirmation. Normal mode uses MENU/MENU_MAP; scientific mode uses SCIENTIFIC_MENU/SCIENTIFIC_MENU_MAP.
  - `MENU_MAP` maps "1"–"12" to the 12 standard Calculator ops; unchanged.
  - `SCIENTIFIC_MENU_MAP` maps "1"–"10" to 10 scientific ops (sin, cos, tan, asin, acos, atan, sinh, cosh, tanh, exp).
  - Unknown REPL choice message mentions 'h', 'm', and 'q' as valid non-numeric choices (range differs by mode: 1-12 normal, 1-10 scientific).
  - `cli_main` uses `all_ops = UNARY_OPS | BINARY_OPS | SCIENTIFIC_UNARY_OPS` — scientific ops available without mode switching in CLI.
  - History is shared across normal and scientific mode operations within the same REPL session.
  - `run_operation` works for scientific ops (they're unary, so falls through to the single-operand path correctly).
- **Last updated:** cycle 13

## tests/test_main.py
- **Purpose:** Test suite for src/__main__.py (both interactive REPL and bash CLI mode), including scientific mode.
- **Exports:** 95 test functions. Adds: SCIENTIFIC_MENU_MAP completeness (2), REPL mode switching (4: switch toggle, sin op, unknown choice in sci mode, shared history), run_operation scientific (4: sin, cos, asin-error, exp), cli_main scientific (4: sin, cos, exp, asin-error).
- **Key invariants:** Imports `SCIENTIFIC_MENU_MAP` alongside other names. Scientific REPL tests patch sys.argv to ["prog"] and use 'm' as the first input to enter scientific mode.
- **Last updated:** cycle 13

## tests/test_calculator.py
- **Purpose:** Full test suite for Calculator class, including execute() dispatch, module-level constants, and scientific mode operations.
- **Current state:** 109 tests. Imports: `Calculator, BINARY_OPS, UNARY_OPS, INTEGER_OPS, SCIENTIFIC_UNARY_OPS, _to_int_if_needed`.
- **Exports:** existing 82 tests + `test_scientific_unary_ops_set` (1), scientific method tests: sin(2), cos(2), tan(2), asin(4), acos(4), atan(2), sinh(1), cosh(1), tanh(1), exp(2), execute scientific (3)
- **Last updated:** cycle 13
