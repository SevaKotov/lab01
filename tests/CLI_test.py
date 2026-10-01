import subprocess
import sys


def run_cli(*args, cwd=None):
    """Запускает toolkit как подпроцесс и возвращает результат."""
    return subprocess.run(
        [sys.executable, "-m", "toolkit", *args],
        capture_output=True,
        text=True,
        cwd=cwd,
        check=False
    )


# ============ --help ============

class TestCLIHelp:
    def test_help_exits_zero(self):
        result = run_cli("--help")
        assert result.returncode == 0
        assert "calc" in result.stdout
        assert "convert" in result.stdout

    def test_help_goes_to_stdout(self):
        result = run_cli("--help")
        assert result.stdout != ""
        assert result.stderr == ""

    def test_no_args_does_not_crash(self):
        result = run_cli()
        assert result.returncode == 0


# ============ calc: успешные случаи ============

class TestCLICalcSuccess:
    def test_simple_addition(self):
        result = run_cli("calc", "2+2")
        assert result.returncode == 0
        assert result.stdout.strip() == "4.0"

    def test_subtraction(self):
        result = run_cli("calc", "10-3")
        assert result.returncode == 0
        assert result.stdout.strip() == "7.0"

    def test_multiplication(self):
        result = run_cli("calc", "6*7")
        assert result.returncode == 0
        assert result.stdout.strip() == "42.0"

    def test_division(self):
        result = run_cli("calc", "20/4")
        assert result.returncode == 0
        assert result.stdout.strip() == "5.0"

    def test_priority(self):
        result = run_cli("calc", "2+3*4")
        assert result.returncode == 0
        assert result.stdout.strip() == "14.0"

    def test_with_parentheses(self):
        result = run_cli("calc", "(2+3)*4")
        assert result.returncode == 0
        assert result.stdout.strip() == "20.0"

    def test_float_operands(self):
        result = run_cli("calc", "1.5+2.5")
        assert result.returncode == 0
        assert result.stdout.strip() == "4.0"

    def test_nested_parentheses(self):
        result = run_cli("calc", "((2+3)*(4-1))")
        assert result.returncode == 0
        assert result.stdout.strip() == "15.0"

    def test_floor_division(self):
        result = run_cli("calc", "10//3")
        assert result.returncode == 0
        assert result.stdout.strip() == "3.0"

    def test_modulo(self):
        result = run_cli("calc", "10%3")
        assert result.returncode == 0
        assert result.stdout.strip() == "1.0"

    def test_power(self):
        result = run_cli("calc", "2^10")
        assert result.returncode == 0
        assert result.stdout.strip() == "1024.0"

    def test_unary_minus_with_dashdash(self):
        # Выражение, начинающееся с минуса, требует разделителя --
        result = run_cli("calc", "--", "-5+3")
        assert result.returncode == 0
        assert result.stdout.strip() == "-2.0"

    def test_unary_minus_with_parens(self):
        result = run_cli("calc", "--", "-(5+3)")
        assert result.returncode == 0
        assert result.stdout.strip() == "-8.0"


# ============ calc: ошибки ============

class TestCLICalcErrors:
    def test_empty_expression(self):
        result = run_cli("calc", "")
        assert result.returncode == 2
        assert result.stderr != ""
        assert result.stdout == ""

    def test_invalid_character(self):
        result = run_cli("calc", "2 + abc")
        assert result.returncode == 2
        assert result.stderr != ""

    def test_division_by_zero(self):
        result = run_cli("calc", "5/0")
        assert result.returncode == 2
        assert result.stderr != ""
        assert result.stdout == ""

    def test_modulo_by_zero(self):
        result = run_cli("calc", "5%0")
        assert result.returncode == 2
        assert result.stderr != ""

    def test_floor_division_by_zero(self):
        result = run_cli("calc", "5//0")
        assert result.returncode == 2
        assert result.stderr != ""

    def test_two_operators_in_a_row(self):
        result = run_cli("calc", "2**3")
        assert result.returncode == 2
        assert result.stderr != ""

    def test_two_dots_in_number(self):
        result = run_cli("calc", "2.5.3")
        assert result.returncode == 2
        assert result.stderr != ""

    def test_error_goes_to_stderr_not_stdout(self):
        result = run_cli("calc", "5/0")
        assert result.stdout == ""
        assert result.stderr != ""


# ============ convert: успешные случаи ============

class TestCLIConvertSuccess:
    def test_length_cm_to_m(self):
        result = run_cli("convert", "100", "--from", "cm", "--to", "m")
        assert result.returncode == 0
        assert result.stdout.strip() == "1.0 m"

    def test_length_mm_to_cm(self):
        result = run_cli("convert", "10", "--from", "mm", "--to", "cm")
        assert result.returncode == 0
        assert result.stdout.strip() == "1.0 cm"

    def test_length_km_to_m(self):
        result = run_cli("convert", "1", "--from", "km", "--to", "m")
        assert result.returncode == 0
        assert result.stdout.strip() == "1000.0 m"

    def test_mass_g_to_kg(self):
        result = run_cli("convert", "1000", "--from", "g", "--to", "kg")
        assert result.returncode == 0
        assert result.stdout.strip() == "1.0 kg"

    def test_temperature_c_to_f(self):
        result = run_cli("convert", "0", "--from", "c", "--to", "f")
        assert result.returncode == 0
        assert result.stdout.strip() == "32.0 f"

    def test_temperature_c_to_k(self):
        result = run_cli("convert", "0", "--from", "c", "--to", "k")
        assert result.returncode == 0
        assert result.stdout.strip() == "273.15 k"

    def test_case_insensitive_units(self):
        result = run_cli("convert", "100", "--from", "CM", "--to", "M")
        assert result.returncode == 0
        assert result.stdout.strip() == "1.0 m"

    def test_identity_conversion(self):
        result = run_cli("convert", "42", "--from", "m", "--to", "m")
        assert result.returncode == 0
        assert result.stdout.strip() == "42.0 m"

    def test_negative_celsius_allowed(self):
        result = run_cli("convert", "-40", "--from", "c", "--to", "f")
        assert result.returncode == 0
        assert result.stdout.strip() == "-40.0 f"


# ============ convert: ошибки ============

class TestCLIConvertErrors:
    def test_unknown_unit_from(self):
        result = run_cli("convert", "1", "--from", "xyz", "--to", "m")
        assert result.returncode == 2
        assert result.stderr != ""

    def test_unknown_unit_to(self):
        result = run_cli("convert", "1", "--from", "m", "--to", "ft")
        assert result.returncode == 2
        assert result.stderr != ""

    def test_incompatible_units_length_to_mass(self):
        result = run_cli("convert", "1", "--from", "m", "--to", "kg")
        assert result.returncode == 2
        assert result.stderr != ""

    def test_incompatible_units_mass_to_temperature(self):
        result = run_cli("convert", "1", "--from", "g", "--to", "c")
        assert result.returncode == 2
        assert result.stderr != ""

    def test_missing_from_flag(self):
        result = run_cli("convert", "100", "--to", "m")
        assert result.returncode == 2

    def test_missing_to_flag(self):
        result = run_cli("convert", "100", "--from", "cm")
        assert result.returncode == 2

    def test_invalid_value(self):
        result = run_cli("convert", "abc", "--from", "m", "--to", "cm")
        assert result.returncode == 2


# ============ Проверка потоков вывода ============

class TestCLIStreams:
    def test_success_writes_to_stdout(self):
        result = run_cli("calc", "2+2")
        assert result.stdout.strip() == "4.0"
        assert result.stderr == ""

    def test_error_writes_to_stderr(self):
        result = run_cli("calc", "5/0")
        assert result.stdout == ""
        assert result.stderr != ""

    def test_exit_code_success(self):
        result = run_cli("calc", "2+2")
        assert result.returncode == 0

    def test_exit_code_error(self):
        result = run_cli("calc", "5/0")
        assert result.returncode == 2