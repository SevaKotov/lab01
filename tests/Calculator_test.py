import pytest

from toolkit.calculator import calculate
from toolkit.errors import *

# ============ ОБЫЧНЫЕ ОПЕРАЦИИ ============

def test_simple_addition():
    """Проверяем обычное сложение."""
    assert calculate("2+3") == 5.0


def test_subtraction():
    """Проверяем вычитание."""
    assert calculate("10-4") == 6.0


def test_multiplication():
    """Проверяем умножение."""
    assert calculate("6*7") == 42.0


def test_division():
    """Проверяем деление."""
    assert calculate("20/4") == 5.0


def test_floor_division():
    """Целочисленное деление (доп. задание)."""
    assert calculate("10//3") == 3.0


def test_modulo():
    """Остаток от деления (доп. задание)."""
    assert calculate("10%3") == 1.0


def test_power():
    """Возведение в степень."""
    assert calculate("2^10") == 1024.0


def test_float_numbers():
    """Калькулятор должен работать с дробными числами."""
    assert calculate("1.5+2.5") == 4.0


def test_single_number():
    """Одно число без операций."""
    assert calculate("42") == 42.0


def test_priority_mul_over_add():
    """Умножение выполняется раньше сложения."""
    assert calculate("2+3*4") == 14.0


def test_parentheses():
    """Скобки меняют приоритет."""
    assert calculate("(2+3)*4") == 20.0


def test_nested_parentheses():
    """Вложенные скобки."""
    assert calculate("((2+3)*(4+1))") == 25.0


def test_unary_minus():
    """Унарный минус перед числом."""
    assert calculate("-5+3") == -2.0


def test_double_minus():
    """Два минуса подряд дают плюс."""
    assert calculate("--5") == 5.0


def test_negative_operands():
    """Отрицательные операнды (доп. задание)."""
    assert calculate("-10//3") == -4.0
    assert calculate("2*-3") == -6.0


def test_whitespace_ignored():
    """Пробелы не должны мешать."""
    assert calculate("  2   +   2   ") == 4.0


def test_chain_of_operations():
    """Цепочка операций слева направо."""
    assert calculate("1+2+3+4+5") == 15.0


def test_complex_expression():
    """Сложное выражение со всеми операциями."""
    # 2 + 3*4 - 8/2 = 2 + 12 - 4 = 10
    assert calculate("2+3*4-8/2") == 10.0


# ============ НЕГАТИВНЫЕ ТЕСТЫ ============

def test_empty_expression():
    """Пустая строка — ошибка."""
    with pytest.raises(EmptyExpressionError):
        calculate("")


def test_only_spaces():
    """Строка из одних пробелов — ошибка."""
    with pytest.raises(EmptyExpressionError):
        calculate("    ")


def test_invalid_letter():
    """Буквы в выражении запрещены."""
    with pytest.raises(InvalidCharacterError):
        calculate("2+a")


def test_two_operators_in_a_row():
    """Два оператора подряд — ошибка."""
    with pytest.raises(ConsecutiveOperatorsError):
        calculate("2**3")


def test_division_by_zero():
    """Деление на ноль запрещено."""
    with pytest.raises(DivisionByZeroError):
        calculate("5/0")


def test_invalid_number():
    """Две точки в числе — ошибка."""
    with pytest.raises(InvalidNumberError):
        calculate("2.5.3")


def test_unbalanced_parentheses():
    """Незакрытая скобка — ошибка."""
    with pytest.raises(ToolkitError):
        calculate("(2+3")


def test_operator_at_end():
    """Выражение заканчивается оператором — ошибка."""
    with pytest.raises(ToolkitError):
        calculate("2+")