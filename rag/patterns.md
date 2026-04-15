# Patterns and Anti-Patterns

## Patterns

### Use pytest.raises for exception testing
When testing that Calculator methods raise exceptions for invalid inputs, use `pytest.raises(<ExceptionType>)` as a context manager. This is the idiomatic pytest approach for asserting expected exceptions.

### Use pytest.approx for float comparisons
When asserting equality of floating-point results, use `pytest.approx(expected)` instead of `==` to avoid false failures due to floating-point rounding (e.g., `0.1 + 0.2 != 0.3` exactly in IEEE 754).

### Float-to-int conversion for stdlib functions expecting integers
When user input arrives as `float` (via `parse_number`) but a Calculator method requires `int` (e.g., `factorial` which calls `math.factorial`), check `value != int(value)` and raise `ValueError` for non-whole numbers before casting. This avoids a confusing `TypeError: 'float' object cannot be interpreted as an integer` from the stdlib.

### Patch sys.argv in tests that call main() directly
When `main()` branches on `sys.argv` length, tests that call it directly must patch `sys.argv` to control which path is taken. Use `patch("sys.argv", ["prog"])` for REPL tests and `patch("sys.argv", ["prog", "op", ...])` for CLI dispatch tests. Failing to do so causes pytest's own argv (e.g. `["tests/"]`) to trigger unintended CLI dispatch.

### Dual-mode entry point via sys.argv
When a module needs both a non-interactive (scripting) mode and an interactive mode, check `len(sys.argv) > 1` at the top of `main()` and dispatch to a separate function (`cli_main`) that takes the argument list explicitly. This keeps the two modes independently testable and avoids coupling the interactive REPL to argument parsing.

### Bounded retry with optional max_attempts parameter
When a user-input helper (e.g., `parse_number`) must limit retries, convert the `while True` loop to a `for attempt in range(max_attempts)` loop and raise `ValueError` on exhaustion. Expose `max_attempts` as an optional parameter (defaulting to a module-level constant) so tests can override it without patching the constant. Callers that already catch `ValueError` get the retry-exhaustion error for free — no extra handler needed.

### Module-level logger with basicConfig only in entry points
Library modules (e.g., `calculator.py`, `__main__.py` at import time) should only create loggers: `logger = logging.getLogger(__name__)`. Never call `logging.basicConfig()` in library code. Only call it in the actual entry point (`main()`) so library loggers do not unexpectedly configure the root logger for callers. Tests use the `caplog` fixture — no basicConfig needed there.

### Log-then-re-raise for Calculator errors
When a Calculator method catches an exception to emit a log record (e.g., `ZeroDivisionError`, `ValueError`), always re-raise the original exception unchanged. This keeps logging as a side-effect-only concern: callers retain the same exception contract and tests that use `pytest.raises` are unaffected.

### Named-dispatch execute() method for logic/interface separation
When a class has multiple operations that share cross-cutting concerns (history recording, input coercion), add an `execute(op, *operands)` method that dispatches by name, applies the shared logic (coercion, history), and propagates exceptions unchanged. The interface layer calls `execute()` with pre-parsed values rather than calling individual methods directly and then applying concerns like history tracking itself. This keeps the interface as pure I/O and the class as the authority on all operation semantics.

### Operations sub-package for separation of pure math from calculator logic
When the Calculator class grows to hold many operations, extract the operation implementations into a dedicated `src/operations/` sub-package with separate modules by category (arithmetic, advanced, scientific). Operation functions in the sub-modules are pure (no logging, no state). The Calculator class retains ownership of cross-cutting concerns (history recording, error logging, type coercion) and delegates computation to the sub-modules. This prepares for a future scientific mode by providing a named stub module (`scientific.py`) that can be filled incrementally without touching other files.

## Anti-Patterns

### Infinite retry loops without limit
Looping forever on invalid user input (e.g., `while True: ... except ValueError: print(...)`) makes the REPL impossible to escape from non-interactively and is harder to test reliably. Prefer bounded loops with a configurable `max_attempts` constant.
