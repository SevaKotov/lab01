from fractions import Fraction

from .errors import *


def validation(example):
    """"Проверка исходного выражения на базовые ошибки"""
    if not example or not example.strip():
        raise EmptyExpressionError("Пустая строка")

    allowed = "0123456789.+-*/^%() \t"
    for ch in example:
        if ch not in allowed:
            raise InvalidCharacterError(f"Недопустимый символ: {ch!r}")

    i = 0
    while i < len(example):
        if example[i] in "0123456789.":
            j = i
            while j < len(example) and example[j] in "0123456789.":
                j += 1
            k = j
            while k < len(example) and example[k] in " \t":
                k += 1
            if k > j and k < len(example) and example[k] in "0123456789.":
                raise MissingOperandError(
                    f"Пропущен оператор между числами: {example[i:k].strip()}"
                )
            i = j
        else:
            i += 1

    current = ""
    for ch in example + " ":
        if ch in "0123456789.":
            current += ch
        else:
            if current:
                if current.count(".") > 1:
                    raise InvalidNumberError(f"Неверное число: {current}")
                if not any(c.isdigit() for c in current):
                    raise InvalidNumberError(f"Неверное число: {current}")
                current = ""

    ops = "+-*/^%"
    for i in range(len(example) - 1):
        cur, nxt = example[i], example[i + 1]
        if cur in ops and nxt in ops and nxt not in "+-" and cur+nxt != "//":
            raise ConsecutiveOperatorsError(f"Два оператора подряд: {cur}{nxt}")

    if example[0] in "*/^%":
        raise MissingOperandError(f"Пропущен операнд перед: {example[0]}")
    if example[-1] in ops:
        raise MissingOperandError(f"Пропущен операнд после: {example[-1]}")

    if "()" in example:
        raise MissingOperandError("Пустые скобки")
    for i, ch in enumerate(example):
        if ch == "(" and i + 1 < len(example) and example[i + 1] in "*/^%":
            raise MissingOperandError("Пропущен операнд после '('")
        if ch == ")" and i > 0 and example[i - 1] in ops:
            raise MissingOperandError("Пропущен операнд перед ')'")

    balance = 0
    for ch in example:
        if ch == "(":
            balance += 1
        elif ch == ")":
            balance -= 1
            if balance < 0:
                raise UnbalancedParenthesesError("Лишняя закрывающая скобка")
    if balance != 0:
        raise UnbalancedParenthesesError("Не закрыта открывающая скобка")

    current = ""
    for ch in example:
        if ch in "0123456789.":
            current += ch
        else:
            if current:
                if current.count(".") > 1:
                    raise InvalidNumberError(f"Неверное число: {current}")
                if not any(c.isdigit() for c in current):
                    raise InvalidNumberError(f"Неверное число: {current}")
                current = ""

def safe_pow(base, exp):
    """"Безопасное возведение в степень"""
    if base >= 0:
        return base ** exp
    frac = Fraction(exp).limit_denominator()
    if frac.denominator % 2 == 0:
        raise InvalidNumberError(f"Число {base} возводится в {exp}-ю степень")
    if frac.numerator % 2 != 0:
        return -(abs(base) ** exp)
    else:
        return abs(base) ** exp

def IsOp(s):
    """"Проверка элемента на принадлежность к операциям"""
    return str(s) in '+-*/^%'

def find_num(example, i):
    """"Нахождение всего числа (всей его длинны включая дробную часть)"""
    num = ''
    while i < len(example) and (example[i] in '0123456789' or example[i] == '.'):
        num += example[i]
        i+=1
    return num, i

def tokenization(example):
    """"Преобразование в польскую запись"""
    while any(p in example for p in ("--", "++", "+-", "-+")):
        example = example.replace("--", "+").replace("++", "+").replace("+-", "-").replace("-+", "-")

    validation(example)
    example = example.replace(" ", "").replace("\t", "")

    while "-(" in example:
        example = example.replace("-(", "-1*(")
    while "+(" in example:
        example = example.replace("+(", "+1*(")

    order = {
        "(":-1,
        "+":0,
        "-":0,
        "*":1,
        "/":1,
        "//":1,
        "^":2,
        "%":2
    }
    example+=')'
    token = []
    stack = ['(']
    i = 0
    if example[0] == '+':
        example = example[1:]

    while i < len(example):
        char = example[i]
        if char in '0123456789':
            num_str, i = find_num(example, i)
            token.append(float(num_str))
            continue

        if char == '-' and (i == 0 or example[i-1] == '(' or IsOp(example[i-1])):
            num, i = find_num(example, i+1)
            num = -1*float(num)
            token.append(num)
            continue

        if char == "/" and example[i+1] == '/':
            stack.append('//')
            i+=2
            continue

        if IsOp(char):
            while order.get(char) <= order.get(stack[-1]):
                token.append(stack.pop(-1))
            stack.append(char)
            i+=1
            continue

        if char == ')':
            while stack[-1] != '(':
                token.append(stack.pop(-1))
            stack.pop(-1)
            i+=1
            continue

        if char == '(':
            stack.append(char)
            i+=1
            continue

    return token

def calculate(example):
    """"Процесс вычисления"""
    token = tokenization(example)
    i = -1
    if len(token)>1:
        if len(token)==2:
            return token[1]
        while i < len(token):
            i+=1
            char = token[i]

            if char == '//':
                if token[i - 1] == 0:
                    raise DivisionByZeroError("Деление на ноль")
                token[i] = token[i - 2] // token[i - 1]
                del token[i - 2:i]
                i = 1
                if len(token) == 1:
                    break
                continue

            if IsOp(char):
                if char == '+':
                    token[i] = token[i-2] + token[i-1]
                    del token[i-2:i]
                    i = 1
                    if len(token) == 1:
                        break
                    continue

                if char == '-':
                    token[i] = token[i-2] - token[i-1]
                    del token[i-2:i]
                    i = 1
                    if len(token) == 1:
                        break
                    continue

                if char == '*':
                    token[i] = token[i-2] * token[i-1]
                    del token[i-2:i]
                    i = 1
                    if len(token) == 1:
                        break
                    continue

                if char == '^':
                    base = token[i - 2]
                    exp = token[i - 1]
                    token[i] = safe_pow(base, exp)
                    del token[i - 2:i]
                    i = 1
                    if len(token) == 1:
                        break
                    continue


                if char == '%':
                    if token[i - 1] == 0:
                        raise DivisionByZeroError("Деление на ноль")
                    token[i] = token[i-2] % token[i-1]
                    del token[i-2:i]
                    i = 1
                    if len(token) == 1:
                        break
                    continue

                if char == '/':
                    if token[i - 1] == 0:
                        raise DivisionByZeroError("Деление на ноль")
                    token[i] = token[i-2] / token[i-1]
                    del token[i-2:i]
                    i = 1
                    if len(token) == 1:
                        break
                    continue
    return token[0]
