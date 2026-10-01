import pytest

from toolkit.calculator import calculate
from toolkit.errors import *

# ============ ЦЕЛОЧИСЛЕННОЕ ДЕЛЕНИЕ (//) ============

class TestIntegerDivision:
    def test_simple(self):
        assert calculate("10//3") == 3.0

    def test_exact_division(self):
        assert calculate("10//2") == 5.0

    def test_less_than_divisor(self):
        assert calculate("2//5") == 0.0

    def test_large_numbers(self):
        assert calculate("1000000//7") == 142857.0

    def test_with_float_operands(self):
        # 7.5 // 2 = 3.0
        assert calculate("7.5//2") == 3.0

    def test_negative_dividend(self):
        # В Python: -10 // 3 == -4 (округление вниз, не к нулю!)
        assert calculate("-10//3") == -4.0

    def test_negative_divisor(self):
        # 10 // -3 == -4
        assert calculate("10//-3") == -4.0

    def test_both_negative(self):
        # -10 // -3 == 3
        assert calculate("-10//-3") == 3.0

    def test_priority_over_addition(self):
        # 2 + 10 // 3 = 2 + 3 = 5
        assert calculate("2+10//3") == 5.0

    def test_same_priority_as_multiplication(self):
        # 10 // 2 * 3: слева направо → (10 // 2) * 3 = 15
        assert calculate("10//2*3") == 15.0

    def test_with_parentheses(self):
        assert calculate("(20+10)//3") == 10.0


class TestIntegerDivisionErrors:
    def test_division_by_zero(self):
        with pytest.raises(DivisionByZeroError):
            calculate("10//0")

    def test_division_by_zero_expression(self):
        with pytest.raises(DivisionByZeroError):
            calculate("10//(3-3)")


# ============ ОСТАТОК ОТ ДЕЛЕНИЯ (%) ============

class TestModulo:
    def test_simple(self):
        assert calculate("10%3") == 1.0

    def test_exact_division(self):
        assert calculate("10%5") == 0.0

    def test_less_than_divisor(self):
        assert calculate("2%5") == 2.0

    def test_large_numbers(self):
        assert calculate("1000000%7") == 1.0

    def test_with_float_operands(self):
        assert calculate("7.5%2") == 1.5

    def test_negative_dividend(self):
        assert calculate("-10%3") == 2.0

    def test_negative_divisor(self):
        assert calculate("10%-3") == -2.0

    def test_both_negative(self):
        assert calculate("-10%-3") == -1.0

    def test_priority_over_addition(self):
        assert calculate("2+10%3") == 3.0

    def test_same_priority_as_multiplication(self):
        assert calculate("20%6*2") == 4.0

    def test_with_parentheses(self):
        assert calculate("(20+10)%7") == 2.0


class TestModuloErrors:
    def test_division_by_zero(self):
        with pytest.raises(DivisionByZeroError):
            calculate("10%0")

    def test_division_by_zero_expression(self):
        with pytest.raises(DivisionByZeroError):
            calculate("10%(3-3)")


# ============ КОМБИНАЦИИ ============

class TestCombinations:
    def test_floor_div_and_modulo(self):
        # (10 // 3) + (10 % 3) = 3 + 1 = 4
        assert calculate("10//3+10%3") == 4.0

    def test_all_four_operations(self):
        # 20 // 3 + 20 % 3 - 4 * 2 = 6 + 2 - 8 = 0
        assert calculate("20//3+20%3-4*2") == 0.0

    def test_nested_parentheses_with_both(self):
        # (17 // 5) * (17 % 5) = 3 * 2 = 6
        assert calculate("(17//5)*(17%5)") == 6.0

    def test_negative_in_complex_expression(self):
        # 2 * (-10 // 3) = 2 * (-4) = -8
        assert calculate("2*(-10//3)") == -8.0

class TestSingleOperations:
    def test_single_number(self):
        assert calculate("42") == 42.0

    def test_single_float(self):
        assert calculate("3.14") == 3.14

    def test_single_negative(self):
        assert calculate("-7") == -7.0

    def test_single_zero(self):
        assert calculate("0") == 0.0

    def test_addition(self):
        assert calculate("2+3") == 5.0

    def test_subtraction(self):
        assert calculate("10-4") == 6.0

    def test_multiplication(self):
        assert calculate("6*7") == 42.0

    def test_division(self):
        assert calculate("20/4") == 5.0

    def test_floor_division(self):
        assert calculate("20//6") == 3.0

    def test_modulo(self):
        assert calculate("20%6") == 2.0

    def test_power(self):
        assert calculate("2^10") == 1024.0


# ============ ЦЕПОЧКИ ОДНОТИПНЫХ ОПЕРАТОРОВ ============

class TestChains:
    def test_many_additions(self):
        assert calculate("1+2+3+4+5") == 15.0

    def test_many_subtractions(self):
        assert calculate("100-10-20-30") == 40.0

    def test_many_multiplications(self):
        assert calculate("2*3*4*5") == 120.0

    def test_many_divisions(self):
        assert calculate("1000/10/10/2") == 5.0

    def test_mixed_add_sub(self):
        assert calculate("10+5-3+8-4") == 16.0

    def test_mixed_mul_div(self):
        assert calculate("100*2/4*3") == 150.0

    def test_alternating_operators(self):
        assert calculate("2+3*4-5/5") == 13.0


# ============ ПРИОРИТЕТ ОПЕРАТОРОВ ============

class TestPrecedence:
    def test_mul_before_add(self):
        assert calculate("2+3*4") == 14.0

    def test_mul_before_sub(self):
        assert calculate("10-2*3") == 4.0

    def test_div_before_add(self):
        assert calculate("2+10/5") == 4.0

    def test_div_before_sub(self):
        assert calculate("10-8/4") == 8.0

    def test_all_four_levels(self):
        # 2 + 3 * 4 - 8 / 2 = 2 + 12 - 4 = 10
        assert calculate("2+3*4-8/2") == 10.0

    def test_power_highest_priority(self):
        # 2 * 3 ^ 2 = 2 * 9 = 18
        assert calculate("2*3^2") == 18.0

    def test_power_right_associative(self):
        # 2 ^ 3 ^ 2 обычно правоассоциативно: 2 ^ 9 = 512
        # (если ваша реализация левоассоциативна — будет 64)
        result = calculate("2^3^2")
        assert result in (512.0, 64.0)  # допускаем оба варианта


# ============ СКОБКИ ============

class TestParentheses:
    def test_simple_override(self):
        assert calculate("(2+3)*4") == 20.0

    def test_division_by_group(self):
        assert calculate("100/(2+3)") == 20.0

    def test_nested(self):
        assert calculate("((2+3)*(4+1))") == 25.0

    def test_deep_nested(self):
        assert calculate("(((1+1)))") == 2.0

    def test_double_nested(self):
        assert calculate("((2+3)*2+(4+6)*3)") == 40.0

    def test_parentheses_with_priority(self):
        # 2 * (3 + 4) * 5 = 70
        assert calculate("2*(3+4)*5") == 70.0

    def test_redundant_parentheses(self):
        assert calculate("((((42))))") == 42.0

    def test_negative_inside_parentheses(self):
        assert calculate("(-5)*2") == -10.0

    def test_negative_result_inside(self):
        assert calculate("(3-10)") == -7.0


# ============ УНАРНЫЙ МИНУС ============

class TestUnaryMinus:
    def test_double_minus(self):
        assert calculate("--5") == 5.0

    def test_leading(self):
        assert calculate("-5+3") == -2.0

    def test_after_operator(self):
        assert calculate("2*-3") == -6.0

    def test_after_open_paren(self):
        assert calculate("(-5)*2") == -10.0

    def test_minus_plus_combination(self):
        assert calculate("-+5") == -5.0

    def test_plus_minus_combination(self):
        assert calculate("+-5") == -5.0

    def test_minus_before_parenthesis(self):
        assert calculate("-(2+3)") == -5.0

    def test_complex_with_unary(self):
        assert calculate("3 + -2 * 4") == -5.0

    def test_unary_in_middle(self):
        assert calculate("5 * -2 + 1") == -9.0


# ============ ВЕЩЕСТВЕННЫЕ ЧИСЛА ============

class TestFloats:
    def test_simple_float(self):
        assert calculate("1.5+2.5") == 4.0

    def test_float_multiplication(self):
        assert calculate("0.5*4") == 2.0

    def test_float_division(self):
        assert calculate("1.5/0.5") == 3.0

    def test_zero_point_five(self):
        assert calculate("0.5+0.5") == 1.0

    def test_many_decimals(self):
        assert calculate("3.14159*2") == pytest.approx(6.28318, rel=1e-5)

    def test_float_plus_integer(self):
        assert calculate("1.5+2") == 3.5

    def test_float_precision(self):
        assert calculate("0.1+0.2") == pytest.approx(0.3, rel=1e-9)

    def test_ten_times_point_one(self):
        expr = "0.1+0.1+0.1+0.1+0.1+0.1+0.1+0.1+0.1+0.1"
        assert calculate(expr) == pytest.approx(1.0, rel=1e-9)

    def test_scientific_like(self):
        # 0.0001 * 0.0001 = 1e-8
        assert calculate("0.0001*0.0001") == pytest.approx(1e-8, rel=1e-9)


# ============ БОЛЬШИЕ И МАЛЫЕ ЧИСЛА ============

class TestExtremeValues:
    def test_million_squared(self):
        assert calculate("1000000*1000000") == 1e12

    def test_billion_plus(self):
        assert calculate("1000000000+1000000000") == 2e9

    def test_small_numbers(self):
        assert calculate("0.000001+0.000002") == pytest.approx(3e-6, rel=1e-9)

    def test_very_large_division(self):
        assert calculate("1000000000000/1000000") == 1e6

    def test_power_of_two_ten(self):
        assert calculate("2^10") == 1024.0

    def test_power_of_two_twenty(self):
        assert calculate("2^20") == 1048576.0


# ============ ПРОБЕЛЫ И ФОРМАТИРОВАНИЕ ============

class TestWhitespace:
    def test_no_spaces(self):
        assert calculate("2+2") == 4.0

    def test_spaces_around_operators(self):
        assert calculate("2 + 2") == 4.0

    def test_many_spaces(self):
        assert calculate("  2   +   2   ") == 4.0

    def test_spaces_inside_parens(self):
        assert calculate("( 2 + 3 ) * 4") == 20.0

    def test_tabs(self):
        assert calculate("2\t+\t2") == 4.0

    def test_mixed_whitespace(self):
        assert calculate("  2  *  3  +  4  ") == 10.0

# ============ СЛОЖНЫЕ СОСТАВНЫЕ ВЫРАЖЕНИЯ ============

class TestComplexExpressions:
    def test_physics_formula(self):
        # E = m * c^2, m=2, c=3
        assert calculate("2*3^2") == 18.0

    def test_quadratic_discriminant(self):
        # D = b^2 - 4*a*c, a=1, b=5, c=6
        # D = 25 - 24 = 1
        assert calculate("5^2-4*1*6") == 1.0

    def test_average(self):
        # (10+20+30+40) / 4 = 25
        assert calculate("(10+20+30+40)/4") == 25.0

    def test_percentage_of(self):
        # 15% от 200 = 30
        assert calculate("200*15/100") == 30.0

    def test_compound_expression_1(self):
        # 1 + 2 * 3 - 4 / 2 + 5 = 1 + 6 - 2 + 5 = 10
        assert calculate("1+2*3-4/2+5") == 10.0

    def test_compound_expression_2(self):
        # (2+3)*(4-1)/(1+4) = 5*3/5 = 3
        assert calculate("(2+3)*(4-1)/(1+4)") == 3.0

    def test_compound_expression_3(self):
        # 10 - 2 * (3 + 4) / 7 = 10 - 2 = 8
        assert calculate("10-2*(3+4)/7") == 8.0

    def test_compound_expression_4(self):
        # 100 / (5 * (2 + 2)) = 100 / 20 = 5
        assert calculate("100/(5*(2+2))") == 5.0

    def test_all_operators_together(self):
        # 2 + 3 * 4 - 5 / 5 + 6 % 4 + 2 ^ 3 - 10 // 3
        # = 2 + 12 - 1 + 2 + 8 - 3 = 20
        assert calculate("2+3*4-5/5+6%4+2^3-10//3") == 20.0

    def test_nested_with_all_operators(self):
        # (2^3 + 4) * 3 - 12 // 5 + 7 % 3
        # = (8 + 4) * 3 - 2 + 1 = 36 - 2 + 1 = 35
        assert calculate("(2^3+4)*3-12//5+7%3") == 35.0


# ============ НЕГАТИВНЫЕ ТЕСТЫ ============

class TestErrors:
    def test_empty(self):
        with pytest.raises(EmptyExpressionError):
            calculate("")

    def test_only_spaces(self):
        with pytest.raises(EmptyExpressionError):
            calculate("     ")

    def test_invalid_letter(self):
        with pytest.raises(InvalidCharacterError):
            calculate("2+a")

    def test_invalid_symbol(self):
        with pytest.raises(InvalidCharacterError):
            calculate("2#2")

    def test_two_binary_operators(self):
        with pytest.raises(ConsecutiveOperatorsError):
            calculate("2**3")

    def test_operator_plus_star(self):
        with pytest.raises(ConsecutiveOperatorsError):
            calculate("2+*3")

    def test_division_by_zero(self):
        with pytest.raises(DivisionByZeroError):
            calculate("5/0")

    def test_modulo_by_zero(self):
        with pytest.raises(DivisionByZeroError):
            calculate("5%0")

    def test_floor_division_by_zero(self):
        with pytest.raises(DivisionByZeroError):
            calculate("5//0")

    def test_two_dots(self):
        with pytest.raises(InvalidNumberError):
            calculate("2.5.3")

    def test_only_dot(self):
        with pytest.raises(InvalidNumberError):
            calculate(".")

    def test_unbalanced_open(self):
        with pytest.raises(ToolkitError):
            calculate("(2+3")

    def test_unbalanced_close(self):
        with pytest.raises(ToolkitError):
            calculate("2+3)")

    def test_empty_parentheses(self):
        with pytest.raises(ToolkitError):
            calculate("()")

    def test_operator_at_end(self):
        with pytest.raises(ToolkitError):
            calculate("2+")

    def test_two_numbers_in_a_row(self):
        with pytest.raises(ToolkitError):
            calculate("2 2")
