import pytest

from toolkit.converter import convert
from toolkit.errors import IncompatibleUnitsError
from toolkit.errors import TemperatureBelongZero
from toolkit.errors import UnknownUnitError

# ============ ДЛИНА ============

def test_mm_to_cm():
    """Миллиметры в сантиметры."""
    assert convert(10, "mm", "cm") == "1.0 cm"


def test_cm_to_m():
    """Сантиметры в метры."""
    assert convert(100, "cm", "m") == "1.0 m"


def test_m_to_km():
    """Метры в километры."""
    assert convert(1000, "m", "km") == "1.0 km"


def test_km_to_m():
    """Километры в метры."""
    assert convert(1, "km", "m") == "1000.0 m"


def test_mm_to_km():
    """Миллиметры в километры."""
    assert convert(1000000, "mm", "km") == "1.0 km"


# ============ МАССА ============

def test_g_to_kg():
    """Граммы в килограммы."""
    assert convert(1000, "g", "kg") == "1.0 kg"


def test_kg_to_g():
    """Килограммы в граммы."""
    assert convert(1, "kg", "g") == "1000.0 g"


# ============ ТЕМПЕРАТУРА ============

def test_c_to_f():
    """Цельсий в Фаренгейт."""
    assert convert(0, "c", "f") == "32.0 f"


def test_f_to_c():
    """Фаренгейт в Цельсий."""
    assert convert(32, "f", "c") == "0.0 c"


def test_c_to_k():
    """Цельсий в Кельвины."""
    assert convert(0, "c", "k") == "273.0 k"


def test_k_to_c():
    """Кельвины в Цельсий."""
    assert convert(273.15, "k", "c") == "0.0 c"


# ============ ОСОБЫЕ СЛУЧАИ ============

def test_same_unit():
    """Перевод в ту же единицу возвращает исходное значение."""
    assert convert(5, "m", "m") == "5.0 m"


def test_case_insensitive():
    """Регистр единиц не важен."""
    assert convert(10, "MM", "CM") == "1.0 cm"
    assert convert(1, "KG", "G") == "1000.0 g"


def test_float_value():
    """Дробные значения допустимы."""
    assert convert(1.5, "m", "cm") == "150.0 cm"


# ============ НЕГАТИВНЫЕ ТЕСТЫ ============

def test_unknown_unit_start():
    """Неизвестная начальная единица."""
    with pytest.raises(UnknownUnitError):
        convert(1, "abc", "m")


def test_unknown_unit_end():
    """Неизвестная конечная единица."""
    with pytest.raises(UnknownUnitError):
        convert(1, "m", "xyz")


def test_incompatible_units():
    """Нельзя перевести метры в килограммы."""
    with pytest.raises(IncompatibleUnitsError):
        convert(1, "m", "kg")


def test_incompatible_temp_and_length():
    """Температуру нельзя перевести в длину."""
    with pytest.raises(IncompatibleUnitsError):
        convert(1, "c", "m")


def test_below_absolute_zero_c():
    """Температура ниже абсолютного нуля по Цельсию."""
    with pytest.raises(TemperatureBelongZero):
        convert(-300, "c", "k")


def test_below_absolute_zero_k():
    """Отрицательная температура в Кельвинах."""
    with pytest.raises(TemperatureBelongZero):
        convert(-1, "k", "c")


def test_below_absolute_zero_f():
    """Температура ниже абсолютного нуля по Фаренгейту."""
    with pytest.raises(TemperatureBelongZero):
        convert(-500, "f", "c")