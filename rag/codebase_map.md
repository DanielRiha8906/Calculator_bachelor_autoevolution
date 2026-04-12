# Codebase Map

## src/__init__.py
- **Purpose:** Package initializer for the `src` module.
- **Exports:** `Calculator`
- **Key invariants:** Re-exports Calculator from `src.calculator` via `__all__`.
- **Last updated:** cycle 0

## src/calculator.py
- **Purpose:** Core arithmetic calculator class.
- **Public API:**
  - `Calculator.add(a, b)` → `a + b`
  - `Calculator.subtract(a, b)` → `a - b`
  - `Calculator.multiply(a, b)` → `a * b`
  - `Calculator.divide(a, b)` → `a / b` (raises `ZeroDivisionError` if `b == 0`, Python built-in behavior)
  - `Calculator.factorial(n)` → `math.factorial(n)` (raises `ValueError` for negative `n`)
  - `Calculator.square(n)` → `n ** 2`
  - `Calculator.cube(n)` → `n ** 3`
  - `Calculator.square_root(n)` → `math.sqrt(n)` (raises `ValueError` for negative `n`)
  - `Calculator.cube_root(n)` → `math.cbrt(n)` (handles negative inputs; requires Python 3.11+)
  - `Calculator.power(base, exp)` → `base ** exp`
  - `Calculator.log(n)` → `math.log10(n)` (raises `ValueError` for `n <= 0`)
  - `Calculator.ln(n)` → `math.log(n)` (raises `ValueError` for `n <= 0`)
- **Key invariants:** No input validation except where delegated to stdlib. `divide` raises `ZeroDivisionError` on zero divisor; `factorial` raises `ValueError` for negative inputs; `square_root`, `log`, `ln` raise `ValueError` for invalid domain inputs.
- **Last updated:** cycle 4

## src/__main__.py
- **Purpose:** CLI entry point; demonstrates basic Calculator usage.
- **Exports:** `main()` function
- **Key invariants:** Calls all four operations with hardcoded values (10, 5).
- **Last updated:** cycle 0

## tests/test_calculator.py
- **Purpose:** Full test suite for Calculator class.
- **Current state:** 58 tests covering all 12 operations — add, subtract, multiply, divide, factorial, square, cube, square_root, cube_root, power, log, ln — with positive, negative, mixed-sign, zero, float, and boundary inputs. Includes `test_divide_by_zero_raises` (ZeroDivisionError), `test_factorial_negative_raises` (ValueError), `test_square_root_negative_raises` (ValueError), `test_log_non_positive_raises`, `test_log_negative_raises`, `test_ln_non_positive_raises`, `test_ln_negative_raises` (all ValueError).
- **Exports:** `test_add_*` (5), `test_subtract_*` (5), `test_multiply_*` (6), `test_divide_*` (7), `test_factorial_*` (5), `test_square_*` (4), `test_cube_*` (4), `test_square_root_*` (4), `test_cube_root_*` (4), `test_power_*` (4), `test_log_*` (5), `test_ln_*` (5)
- **Last updated:** cycle 4
