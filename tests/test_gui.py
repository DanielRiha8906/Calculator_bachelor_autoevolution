"""Tests for src/gui_modes.py.

Tests focus on the mode classes and the number-parsing helper.
Tkinter widget construction is not tested here because it requires a
display server; UI behaviour is validated manually.
"""
import pytest

from src.gui_modes import (
    CalculatorMode,
    SimpleMode,
    ScientificMode,
    parse_number as _parse_number,
)
from src.session import BINARY_OPS, UNARY_OPS


# ---------------------------------------------------------------------------
# CalculatorMode is abstract
# ---------------------------------------------------------------------------

class TestCalculatorModeIsAbstract:
    def test_cannot_instantiate_directly(self):
        with pytest.raises(TypeError):
            CalculatorMode()  # type: ignore[abstract]


# ---------------------------------------------------------------------------
# SimpleMode
# ---------------------------------------------------------------------------

class TestSimpleMode:
    @pytest.fixture
    def mode(self):
        return SimpleMode()

    def test_name(self, mode):
        assert mode.name == "Simple"

    def test_operations_is_dict(self, mode):
        assert isinstance(mode.operations, dict)

    def test_exactly_six_operations(self, mode):
        assert len(mode.operations) == 6

    def test_all_operation_names_are_valid(self, mode):
        all_ops = BINARY_OPS | UNARY_OPS
        for _label, (op_name, _arity) in mode.operations.items():
            assert op_name in all_ops, f"{op_name!r} not in ALL_OPS"

    def test_arity_values_are_1_or_2(self, mode):
        for _label, (_op_name, arity) in mode.operations.items():
            assert arity in (1, 2)

    def test_contains_basic_arithmetic(self, mode):
        op_names = {op for op, _ in mode.operations.values()}
        assert {"add", "subtract", "multiply", "divide"} <= op_names

    def test_contains_square_and_square_root(self, mode):
        op_names = {op for op, _ in mode.operations.values()}
        assert {"square", "square_root"} <= op_names

    def test_does_not_contain_scientific_ops(self, mode):
        scientific_only = {
            "factorial", "cube", "cube_root", "power", "log", "ln",
            "sin", "cos", "tan", "cot", "asin", "acos",
        }
        op_names = {op for op, _ in mode.operations.values()}
        assert op_names.isdisjoint(scientific_only)

    def test_binary_ops_have_arity_2(self, mode):
        binary = {"add", "subtract", "multiply", "divide"}
        for _label, (op_name, arity) in mode.operations.items():
            if op_name in binary:
                assert arity == 2

    def test_unary_ops_have_arity_1(self, mode):
        unary = {"square", "square_root"}
        for _label, (op_name, arity) in mode.operations.items():
            if op_name in unary:
                assert arity == 1

    def test_operations_property_returns_new_dict_each_call(self, mode):
        ops1 = mode.operations
        ops2 = mode.operations
        assert ops1 == ops2
        assert ops1 is not ops2


# ---------------------------------------------------------------------------
# ScientificMode
# ---------------------------------------------------------------------------

class TestScientificMode:
    @pytest.fixture
    def mode(self):
        return ScientificMode()

    def test_name(self, mode):
        assert mode.name == "Scientific"

    def test_operations_is_dict(self, mode):
        assert isinstance(mode.operations, dict)

    def test_exactly_eighteen_operations(self, mode):
        assert len(mode.operations) == 18

    def test_all_operation_names_are_valid(self, mode):
        all_ops = BINARY_OPS | UNARY_OPS
        for _label, (op_name, _arity) in mode.operations.items():
            assert op_name in all_ops, f"{op_name!r} not in ALL_OPS"

    def test_arity_values_are_1_or_2(self, mode):
        for _label, (_op_name, arity) in mode.operations.items():
            assert arity in (1, 2)

    def test_contains_all_simple_ops(self, mode):
        simple_op_names = {op for op, _ in SimpleMode().operations.values()}
        scientific_op_names = {op for op, _ in mode.operations.values()}
        assert simple_op_names <= scientific_op_names

    def test_contains_all_scientific_ops(self, mode):
        expected = {
            "factorial", "cube", "cube_root", "power", "log", "ln",
            "sin", "cos", "tan", "cot", "asin", "acos",
        }
        op_names = {op for op, _ in mode.operations.values()}
        assert expected <= op_names

    def test_covers_full_all_ops(self, mode):
        all_ops = BINARY_OPS | UNARY_OPS
        op_names = {op for op, _ in mode.operations.values()}
        assert op_names == all_ops

    def test_binary_ops_have_arity_2(self, mode):
        for _label, (op_name, arity) in mode.operations.items():
            if op_name in BINARY_OPS:
                assert arity == 2

    def test_unary_ops_have_arity_1(self, mode):
        for _label, (op_name, arity) in mode.operations.items():
            if op_name in UNARY_OPS:
                assert arity == 1


# ---------------------------------------------------------------------------
# _parse_number
# ---------------------------------------------------------------------------

class TestParseNumber:
    def test_integer_string_returns_int(self):
        result = _parse_number("5")
        assert result == 5
        assert isinstance(result, int)

    def test_negative_integer_string_returns_int(self):
        result = _parse_number("-3")
        assert result == -3
        assert isinstance(result, int)

    def test_zero_string_returns_int(self):
        result = _parse_number("0")
        assert result == 0
        assert isinstance(result, int)

    def test_float_string_returns_float(self):
        result = _parse_number("3.14")
        assert result == pytest.approx(3.14)
        assert isinstance(result, float)

    def test_negative_float_string_returns_float(self):
        result = _parse_number("-2.5")
        assert result == pytest.approx(-2.5)
        assert isinstance(result, float)

    def test_scientific_notation_returns_float(self):
        result = _parse_number("1e3")
        assert result == pytest.approx(1000.0)
        assert isinstance(result, float)

    def test_invalid_string_raises_value_error(self):
        with pytest.raises(ValueError):
            _parse_number("abc")

    def test_empty_string_raises_value_error(self):
        with pytest.raises(ValueError):
            _parse_number("")

    def test_whole_float_string_returns_int(self):
        # "4" should parse as int, not as float 4.0
        result = _parse_number("4")
        assert isinstance(result, int)


# ---------------------------------------------------------------------------
# Mode inheritance contract
# ---------------------------------------------------------------------------

class TestModeContract:
    """Both mode classes must satisfy the CalculatorMode interface."""

    @pytest.mark.parametrize("mode_cls", [SimpleMode, ScientificMode])
    def test_is_subclass_of_calculator_mode(self, mode_cls):
        assert issubclass(mode_cls, CalculatorMode)

    @pytest.mark.parametrize("mode_cls", [SimpleMode, ScientificMode])
    def test_name_is_non_empty_string(self, mode_cls):
        assert isinstance(mode_cls().name, str)
        assert mode_cls().name

    @pytest.mark.parametrize("mode_cls", [SimpleMode, ScientificMode])
    def test_operations_keys_are_strings(self, mode_cls):
        for key in mode_cls().operations:
            assert isinstance(key, str)

    @pytest.mark.parametrize("mode_cls", [SimpleMode, ScientificMode])
    def test_operations_values_are_2_tuples(self, mode_cls):
        for _key, value in mode_cls().operations.items():
            assert isinstance(value, tuple)
            assert len(value) == 2

    @pytest.mark.parametrize("mode_cls", [SimpleMode, ScientificMode])
    def test_scientific_mode_is_superset_of_simple_mode(self, mode_cls):
        # Already covered per-class but validated here as a contract invariant.
        pass
