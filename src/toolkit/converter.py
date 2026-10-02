from .errors import IncompatibleUnitsError
from .errors import InvalidNumberError
from .errors import TemperatureBelongZero
from .errors import UnknownUnitError

LENGTH = ('mm', 'cm', 'm', 'km')
MASS = ('g', 'kg')
TEMP = ('c', 'f', 'k')

def _group(u):
    """"Проверка на приложения величин к одной смысловой группе"""
    if u in LENGTH: return 'length'
    if u in MASS: return 'mass'
    return 'temperature'

def validation(value, start, end):
    """"Валидация. Проверка на ошибки"""
    if start not in LENGTH + MASS + TEMP:
        raise UnknownUnitError(f"Неизвестная единица: {start}")
    if end not in LENGTH + MASS + TEMP:
        raise UnknownUnitError(f"Неизвестная единица: {end}")
    if _group(start) != _group(end):
        raise IncompatibleUnitsError(f"Нельзя перевести {start} в {end}")
    current = ""
    for ch in value:
        if ch in "0123456789.":
            current += ch
        else:
            if current:
                if current.count(".") > 1:
                    raise InvalidNumberError(f"Неверное число: {current}")
                if not any(c.isdigit() for c in current):
                    raise InvalidNumberError(f"Неверное число: {current}")
                current = ""

def convert(value,start, end):
    """Конвертация"""
    value = str(value)
    start = start.lower()
    end = end.lower()

    validation(value, start, end)
    if start == end and start in ('mm', 'cm', 'm', 'km', 'g', 'kg', 'c', 'f', 'k'):
        return f'{float(value)} {start}'

    if start == 'mm':
        if end == "cm":
            return f'{float(value)/10} cm'
        elif end == "m":
            return f'{float(value)/10**3} m'
        elif end == "km":
            return f'{float(value) / 10**6} km'

    if start == 'cm':
        if end == "mm":
            return f'{float(value)*10} mm'
        elif end == "m":
            return f'{float(value)/10**2} m'
        elif end == "km":
            return f'{float(value) / 10**5} km'

    if start == 'm':
        if end == "mm":
            return f'{float(value)*10**3} mm'
        elif end == "cm":
            return f'{float(value)*10**2} cm'
        elif end == "km":
            return f'{float(value) / 10**3} km'

    if start == 'km':
        if end == "mm":
            return f'{float(value)*10**6} mm'
        elif end == "cm":
            return f'{float(value)*10**5} cm'
        elif end == "m":
            return f'{float(value) * 10**3} m'

    if start == 'g' and end == 'kg':
        return f'{float(value) / 10**3} kg'

    if start == 'kg' and end == 'g':
        return f'{float(value) * 10**3} g'
    if start in TEMP:
        if start == 'k' and float(value) >= 0:
            if end == "c":
                return f'{float(value)-273.15} c'
            elif end == "f":
                return f'{(float(value)-273.15)*1.8 + 32} f'

        if start == 'c' and float(value) >= -273:
            if end == "k":
                return f'{float(value)+273
                } k'
            elif end == "f":
                return f'{float(value)*1.8+32} f'

        if start == 'f' and float(value)>-459:
            if end == "c":
                return f'{(float(value) - 32)/1.8} c'
            elif end == "k":
                return f'{(float(value) - 32) / 1.8 + 273} k'
        else:
            raise TemperatureBelongZero("Введенная температура ниже абсолютного нуля")