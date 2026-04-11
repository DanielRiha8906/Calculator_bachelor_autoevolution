"""Tests for CLI (bash) mode of the Calculator."""

import logging
import pytest
from src.cli import cli_mode


class TestCliTwoArgOps:
    """Tests for two-operand operations via CLI."""

    def test_add(self, capsys):
        exit_code = cli_mode(["add", "3", "5"])
        assert exit_code == 0
        assert capsys.readouterr().out.strip() == "8.0"

    def test_subtract(self, capsys):
        exit_code = cli_mode(["subtract", "10", "3"])
        assert exit_code == 0
        assert capsys.readouterr().out.strip() == "7.0"

    def test_multiply(self, capsys):
        exit_code = cli_mode(["multiply", "4", "5"])
        assert exit_code == 0
        assert capsys.readouterr().out.strip() == "20.0"

    def test_divide(self, capsys):
        exit_code = cli_mode(["divide", "10", "2"])
        assert exit_code == 0
        assert capsys.readouterr().out.strip() == "5.0"

    def test_power(self, capsys):
        exit_code = cli_mode(["power", "2", "3"])
        assert exit_code == 0
        assert capsys.readouterr().out.strip() == "8.0"

    def test_add_floats(self, capsys):
        exit_code = cli_mode(["add", "1.5", "2.5"])
        assert exit_code == 0
        assert capsys.readouterr().out.strip() == "4.0"

    def test_add_negative(self, capsys):
        exit_code = cli_mode(["add", "-3", "5"])
        assert exit_code == 0
        assert capsys.readouterr().out.strip() == "2.0"


class TestCliSingleArgOps:
    """Tests for single-operand operations via CLI."""

    def test_factorial(self, capsys):
        exit_code = cli_mode(["factorial", "5"])
        assert exit_code == 0
        assert capsys.readouterr().out.strip() == "120"

    def test_factorial_zero(self, capsys):
        exit_code = cli_mode(["factorial", "0"])
        assert exit_code == 0
        assert capsys.readouterr().out.strip() == "1"

    def test_square(self, capsys):
        exit_code = cli_mode(["square", "4"])
        assert exit_code == 0
        assert capsys.readouterr().out.strip() == "16.0"

    def test_cube(self, capsys):
        exit_code = cli_mode(["cube", "3"])
        assert exit_code == 0
        assert capsys.readouterr().out.strip() == "27.0"

    def test_square_root(self, capsys):
        exit_code = cli_mode(["square_root", "9"])
        assert exit_code == 0
        assert capsys.readouterr().out.strip() == "3.0"

    def test_cube_root(self, capsys):
        exit_code = cli_mode(["cube_root", "27"])
        assert exit_code == 0
        captured = capsys.readouterr()
        assert pytest.approx(float(captured.out.strip()), abs=1e-9) == 3.0

    def test_log(self, capsys):
        exit_code = cli_mode(["log", "100"])
        assert exit_code == 0
        captured = capsys.readouterr()
        assert pytest.approx(float(captured.out.strip()), abs=1e-9) == 2.0

    def test_ln(self, capsys):
        import math
        exit_code = cli_mode(["ln", "1"])
        assert exit_code == 0
        captured = capsys.readouterr()
        assert pytest.approx(float(captured.out.strip()), abs=1e-9) == 0.0


class TestCliErrorCases:
    """Tests for error handling in CLI mode."""

    def test_divide_by_zero_returns_error(self, capsys):
        exit_code = cli_mode(["divide", "10", "0"])
        assert exit_code == 1
        assert "Error:" in capsys.readouterr().err

    def test_square_root_negative_returns_error(self, capsys):
        exit_code = cli_mode(["square_root", "-1"])
        assert exit_code == 1
        assert "Error:" in capsys.readouterr().err

    def test_factorial_negative_returns_error(self, capsys):
        exit_code = cli_mode(["factorial", "-1"])
        assert exit_code == 1
        assert "Error:" in capsys.readouterr().err

    def test_log_zero_returns_error(self, capsys):
        exit_code = cli_mode(["log", "0"])
        assert exit_code == 1
        assert "Error:" in capsys.readouterr().err

    def test_ln_negative_returns_error(self, capsys):
        exit_code = cli_mode(["ln", "-5"])
        assert exit_code == 1
        assert "Error:" in capsys.readouterr().err

    def test_two_arg_op_with_one_operand_returns_error(self, capsys):
        exit_code = cli_mode(["add", "5"])
        assert exit_code == 1
        assert "Error:" in capsys.readouterr().err

    def test_two_arg_op_with_three_operands_returns_error(self, capsys):
        exit_code = cli_mode(["add", "1", "2", "3"])
        assert exit_code == 1
        assert "Error:" in capsys.readouterr().err

    def test_single_arg_op_with_two_operands_returns_error(self, capsys):
        exit_code = cli_mode(["square", "4", "9"])
        assert exit_code == 1
        assert "Error:" in capsys.readouterr().err

    def test_factorial_with_two_operands_returns_error(self, capsys):
        exit_code = cli_mode(["factorial", "5", "3"])
        assert exit_code == 1
        assert "Error:" in capsys.readouterr().err

    def test_invalid_operation_raises_system_exit(self):
        with pytest.raises(SystemExit):
            cli_mode(["invalid_op", "5"])


class TestCliErrorLogging:
    """Tests that errors are logged at ERROR level in CLI mode."""

    def test_divide_by_zero_logs_error(self, caplog):
        with caplog.at_level(logging.ERROR, logger="src.cli"):
            exit_code = cli_mode(["divide", "10", "0"])
        assert exit_code == 1
        assert any("divide" in r.message for r in caplog.records)

    def test_wrong_operand_count_logs_error(self, caplog):
        with caplog.at_level(logging.ERROR, logger="src.cli"):
            exit_code = cli_mode(["add", "1", "2", "3"])
        assert exit_code == 1
        assert len(caplog.records) == 1
        assert "requires exactly 2 operands" in caplog.records[0].message

    def test_successful_operation_does_not_log_error(self, caplog):
        with caplog.at_level(logging.ERROR, logger="src.cli"):
            exit_code = cli_mode(["add", "3", "5"])
        assert exit_code == 0
        assert len(caplog.records) == 0
