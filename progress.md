## Run: 2026-04-09 — Issue #101 V2 Task 1 - Naive/generic

**Branch:** task/naive-generic-division-input-tests  
**PR target:** exp2/naive-generic

**Files changed:**
- `tests/test_calculator.py` — added `TestDivisionIncorrectInputs` class with 6 tests

**Purpose:**
Add tests for incorrect inputs in the `Calculator.divide` method, covering:
- Division by zero (int and float)
- Non-numeric numerator and denominator (string)
- None as numerator and denominator

**Risks:**
- None. The existing `Calculator.divide` implementation relies on Python's built-in arithmetic, which already raises `ZeroDivisionError` and `TypeError` for these inputs. No source code changes were required.

**Test results:** 6 passed, 0 failed

Duration: PENDING | Cost: PENDING | Turns: PENDING
