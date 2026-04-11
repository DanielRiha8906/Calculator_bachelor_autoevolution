import math
import pytest
import sys
from unittest.mock import patch

from src.cli import build_parser, cli_main, _dispatch
from src.controller import CalculatorController


@pytest.fixture
def calc():
    return CalculatorController()


@pytest.fixture
def parser():
    return build_parser()


# --- build_parser: argument parsing ---

def test_parser_add(parser):
    args = parser.parse_args(["add", "3", "4"])
    assert args.operation == "add"
    assert args.a == 3.0
    assert args.b == 4.0


def test_parser_subtract(parser):
    args = parser.parse_args(["subtract", "10", "3"])
    assert args.operation == "subtract"
    assert args.a == 10.0
    assert args.b == 3.0


def test_parser_multiply(parser):
    args = parser.parse_args(["multiply", "3", "4"])
    assert args.operation == "multiply"
    assert args.a == 3.0
    assert args.b == 4.0


def test_parser_divide(parser):
    args = parser.parse_args(["divide", "10", "2"])
    assert args.operation == "divide"
    assert args.a == 10.0
    assert args.b == 2.0


def test_parser_power(parser):
    args = parser.parse_args(["power", "2", "10"])
    assert args.operation == "power"
    assert args.base == 2.0
    assert args.exp == 10.0


def test_parser_square(parser):
    args = parser.parse_args(["square", "4"])
    assert args.operation == "square"
    assert args.a == 4.0


def test_parser_cube(parser):
    args = parser.parse_args(["cube", "3"])
    assert args.operation == "cube"
    assert args.a == 3.0


def test_parser_sqrt(parser):
    args = parser.parse_args(["sqrt", "9"])
    assert args.operation == "sqrt"
    assert args.a == 9.0


def test_parser_cbrt(parser):
    args = parser.parse_args(["cbrt", "27"])
    assert args.operation == "cbrt"
    assert args.a == 27.0


def test_parser_ln(parser):
    args = parser.parse_args(["ln", str(math.e)])
    assert args.operation == "ln"
    assert args.a == pytest.approx(math.e)


def test_parser_log_default_base(parser):
    args = parser.parse_args(["log", "100"])
    assert args.operation == "log"
    assert args.a == 100.0
    assert args.base == 10.0


def test_parser_log_custom_base(parser):
    args = parser.parse_args(["log", "8", "--base", "2"])
    assert args.operation == "log"
    assert args.a == 8.0
    assert args.base == 2.0


def test_parser_factorial(parser):
    args = parser.parse_args(["factorial", "5"])
    assert args.operation == "factorial"
    assert args.n == 5


def test_parser_requires_subcommand(parser):
    with pytest.raises(SystemExit):
        parser.parse_args([])


# --- _dispatch: operation routing ---

def test_dispatch_add(calc, parser):
    args = parser.parse_args(["add", "3", "4"])
    assert _dispatch(calc, args) == "7.0"


def test_dispatch_subtract(calc, parser):
    args = parser.parse_args(["subtract", "10", "3"])
    assert _dispatch(calc, args) == "7.0"


def test_dispatch_multiply(calc, parser):
    args = parser.parse_args(["multiply", "3", "4"])
    assert _dispatch(calc, args) == "12.0"


def test_dispatch_divide(calc, parser):
    args = parser.parse_args(["divide", "10", "2"])
    assert _dispatch(calc, args) == "5.0"


def test_dispatch_divide_by_zero_raises(calc, parser):
    args = parser.parse_args(["divide", "10", "0"])
    with pytest.raises(ZeroDivisionError):
        _dispatch(calc, args)


def test_dispatch_power(calc, parser):
    args = parser.parse_args(["power", "2", "10"])
    assert _dispatch(calc, args) == "1024.0"


def test_dispatch_square(calc, parser):
    args = parser.parse_args(["square", "4"])
    assert _dispatch(calc, args) == "16.0"


def test_dispatch_cube(calc, parser):
    args = parser.parse_args(["cube", "3"])
    assert _dispatch(calc, args) == "27.0"


def test_dispatch_sqrt(calc, parser):
    args = parser.parse_args(["sqrt", "9"])
    assert _dispatch(calc, args) == "3.0"


def test_dispatch_sqrt_negative_raises(calc, parser):
    args = parser.parse_args(["sqrt", "-4"])
    with pytest.raises(ValueError):
        _dispatch(calc, args)


def test_dispatch_cbrt(calc, parser):
    args = parser.parse_args(["cbrt", "27"])
    result = float(_dispatch(calc, args))
    assert result == pytest.approx(3.0)


def test_dispatch_ln(calc, parser):
    args = parser.parse_args(["ln", str(math.e)])
    result = float(_dispatch(calc, args))
    assert result == pytest.approx(1.0)


def test_dispatch_ln_non_positive_raises(calc, parser):
    args = parser.parse_args(["ln", "0"])
    with pytest.raises(ValueError):
        _dispatch(calc, args)


def test_dispatch_log_default_base(calc, parser):
    args = parser.parse_args(["log", "100"])
    result = float(_dispatch(calc, args))
    assert result == pytest.approx(2.0)


def test_dispatch_log_custom_base(calc, parser):
    args = parser.parse_args(["log", "8", "--base", "2"])
    result = float(_dispatch(calc, args))
    assert result == pytest.approx(3.0)


def test_dispatch_log_non_positive_raises(calc, parser):
    args = parser.parse_args(["log", "0"])
    with pytest.raises(ValueError):
        _dispatch(calc, args)


def test_dispatch_factorial(calc, parser):
    args = parser.parse_args(["factorial", "5"])
    assert _dispatch(calc, args) == "120"


def test_dispatch_factorial_zero(calc, parser):
    args = parser.parse_args(["factorial", "0"])
    assert _dispatch(calc, args) == "1"


def test_dispatch_factorial_negative_raises(calc, parser):
    args = parser.parse_args(["factorial", "-1"])
    with pytest.raises(ValueError):
        _dispatch(calc, args)


# --- cli_main: end-to-end output ---

def test_cli_main_add(capsys):
    with patch("sys.argv", ["prog", "add", "3", "4"]):
        cli_main()
    assert capsys.readouterr().out.strip() == "7.0"


def test_cli_main_subtract(capsys):
    with patch("sys.argv", ["prog", "subtract", "10", "3"]):
        cli_main()
    assert capsys.readouterr().out.strip() == "7.0"


def test_cli_main_multiply(capsys):
    with patch("sys.argv", ["prog", "multiply", "3", "4"]):
        cli_main()
    assert capsys.readouterr().out.strip() == "12.0"


def test_cli_main_divide(capsys):
    with patch("sys.argv", ["prog", "divide", "10", "2"]):
        cli_main()
    assert capsys.readouterr().out.strip() == "5.0"


def test_cli_main_divide_by_zero_exits_with_error(capsys):
    with patch("sys.argv", ["prog", "divide", "10", "0"]):
        with pytest.raises(SystemExit) as exc_info:
            cli_main()
    assert exc_info.value.code == 1
    assert "Error:" in capsys.readouterr().err


def test_cli_main_power(capsys):
    with patch("sys.argv", ["prog", "power", "2", "10"]):
        cli_main()
    assert capsys.readouterr().out.strip() == "1024.0"


def test_cli_main_square(capsys):
    with patch("sys.argv", ["prog", "square", "4"]):
        cli_main()
    assert capsys.readouterr().out.strip() == "16.0"


def test_cli_main_cube(capsys):
    with patch("sys.argv", ["prog", "cube", "3"]):
        cli_main()
    assert capsys.readouterr().out.strip() == "27.0"


def test_cli_main_sqrt(capsys):
    with patch("sys.argv", ["prog", "sqrt", "9"]):
        cli_main()
    assert capsys.readouterr().out.strip() == "3.0"


def test_cli_main_sqrt_negative_exits_with_error(capsys):
    with patch("sys.argv", ["prog", "sqrt", "-4"]):
        with pytest.raises(SystemExit) as exc_info:
            cli_main()
    assert exc_info.value.code == 1
    assert "Error:" in capsys.readouterr().err


def test_cli_main_cbrt(capsys):
    with patch("sys.argv", ["prog", "cbrt", "27"]):
        cli_main()
    result = float(capsys.readouterr().out.strip())
    assert result == pytest.approx(3.0)


def test_cli_main_ln(capsys):
    with patch("sys.argv", ["prog", "ln", str(math.e)]):
        cli_main()
    result = float(capsys.readouterr().out.strip())
    assert result == pytest.approx(1.0)


def test_cli_main_log_default_base(capsys):
    with patch("sys.argv", ["prog", "log", "100"]):
        cli_main()
    result = float(capsys.readouterr().out.strip())
    assert result == pytest.approx(2.0)


def test_cli_main_log_custom_base(capsys):
    with patch("sys.argv", ["prog", "log", "8", "--base", "2"]):
        cli_main()
    result = float(capsys.readouterr().out.strip())
    assert result == pytest.approx(3.0)


def test_cli_main_factorial(capsys):
    with patch("sys.argv", ["prog", "factorial", "5"]):
        cli_main()
    assert capsys.readouterr().out.strip() == "120"


def test_cli_main_factorial_negative_exits_with_error(capsys):
    with patch("sys.argv", ["prog", "factorial", "-1"]):
        with pytest.raises(SystemExit) as exc_info:
            cli_main()
    assert exc_info.value.code == 1
    assert "Error:" in capsys.readouterr().err
