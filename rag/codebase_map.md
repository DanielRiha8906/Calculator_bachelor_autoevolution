# Codebase Map

Per-file summaries: purpose, public API surface, key invariants.

---

## src/__init__.py
- **Purpose:** Python package initializer for `src/`.
- **Exports:** `Calculator` (re-exported from `src.calculator`)
- **Invariants:** Must always export `Calculator` so external imports work.

---

## src/calculator.py
- **Purpose:** Defines the `Calculator` class — the core computation unit.
- **Last updated:** cycle 4
- **Public API:**
  - `Calculator.add(a, b)` → `a + b`
  - `Calculator.subtract(a, b)` → `a - b`
  - `Calculator.multiply(a, b)` → `a * b`
  - `Calculator.divide(a, b)` → `a / b`; raises `ValueError("Division by zero is not allowed")` when `b == 0`
  - `Calculator.factorial(n: int) -> int` → `n!`; raises `ValueError` for negative `n` or non-integer `n`
  - `Calculator.square(a)` → `a ** 2`
  - `Calculator.cube(a)` → `a ** 3`
  - `Calculator.square_root(a)` → `math.sqrt(a)`; raises `ValueError` for `a < 0`
  - `Calculator.cube_root(a)` → real cube root; supports negative input via sign-preserving `(-abs(a))**(1/3)` trick
  - `Calculator.power(a, b)` → `a ** b`
  - `Calculator.log(a, base)` → `math.log(a, base)`; raises `ValueError` for `a <= 0` or `base <= 0` or `base == 1`
  - `Calculator.ln(a)` → `math.log(a)`; raises `ValueError` for `a <= 0`
- **Invariants:** No state — all methods are pure functions of their arguments. Imports `math` at module level.

---

## src/__main__.py
- **Purpose:** CLI entry point for manual smoke-testing the calculator.
- **Exports:** `main()` function; executed when `python -m src` is run.
- **Invariants:** Only calls `Calculator` methods; no side effects beyond stdout.

---

## tests/test_calculator.py
- **Purpose:** Unit test suite for `Calculator` — full coverage of all twelve operations.
- **Last updated:** cycle 4
- **Tests (63 total):**
  - **add (5):** positive numbers, negative numbers, mixed sign, zero identity, floats
  - **subtract (6):** positive numbers, negative numbers, mixed sign, zero, floats, same-number-gives-zero
  - **multiply (6):** positive numbers, negative numbers, mixed sign, zero, identity (×1), floats
  - **divide (7):** divide-by-zero `ValueError`, normal, negative denominator, negative numerator, both negative, floats, fractional result
  - **factorial (6):** zero, one, small (5!), large (10!), negative raises `ValueError`, float raises `ValueError`
  - **square (4):** positive, negative, zero, float
  - **cube (4):** positive, negative, zero, float
  - **square_root (4):** positive, zero, float, negative raises `ValueError`
  - **cube_root (4):** positive, negative, zero, float
  - **power (5):** positive exponent, zero exponent, one exponent, negative exponent, float base
  - **log (7):** base 10, base 2, base e, non-positive `a` raises, negative `a` raises, base==1 raises, base==0 raises
  - **ln (5):** ln(e)==1, ln(1)==0, ln(e³)==3, zero raises `ValueError`, negative raises `ValueError`
- **Invariants:** Must import from `src.calculator`, not from the package root; uses `math.isclose` for float comparisons.
