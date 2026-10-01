import pytest

from toolkit.converter import convert
from toolkit.errors import (
    IncompatibleUnitsError,
    UnknownUnitError,
)

# ============ ДЛИНА ============

class TestLength:
    def test_mm_to_cm(self):
        assert convert(10, "mm", "cm") == "1.0 cm"

    def test_mm_to_m(self):
        assert convert(1000, "mm", "m") == "1.0 m"

    def test_mm_to_km(self):
        assert convert(1_000_000, "mm", "km") == "1.0 km"

    def test_cm_to_mm(self):
        assert convert(1, "cm", "mm") == "10.0 mm"

    def test_cm_to_m(self):
        assert convert(100, "cm", "m") == "1.0 m"

    def test_cm_to_km(self):
        assert convert(100_000, "cm", "km") == "1.0 km"

    def test_m_to_mm(self):
        assert convert(1, "m", "mm") == "1000.0 mm"

    def test_m_to_cm(self):
        assert convert(1, "m", "cm") == "100.0 cm"

    def test_m_to_km(self):
        assert convert(1000, "m", "km") == "1.0 km"

    def test_km_to_mm(self):
        assert convert(1, "km", "mm") == "1000000.0 mm"

    def test_km_to_cm(self):
        assert convert(1, "km", "cm") == "100000.0 cm"

    def test_km_to_m(self):
        assert convert(1, "km", "m") == "1000.0 m"

    def test_zero_length(self):
        assert convert(0, "km", "mm") == "0.0 mm"

    def test_negative_length(self):
        assert convert(-5, "m", "cm") == "-500.0 cm"

    def test_fractional_length(self):
        assert convert(1.5, "m", "cm") == "150.0 cm"


# ============ МАССА ============

class TestMass:
    def test_g_to_kg(self):
        assert convert(1000, "g", "kg") == "1.0 kg"

    def test_kg_to_g(self):
        assert convert(1, "kg", "g") == "1000.0 g"

    def test_half_kilo(self):
        assert convert(500, "g", "kg") == "0.5 kg"

    def test_zero_mass(self):
        assert convert(0, "kg", "g") == "0.0 g"

    def test_negative_mass(self):
        assert convert(-1, "kg", "g") == "-1000.0 g"

    def test_fractional_mass(self):
        assert convert(0.5, "kg", "g") == "500.0 g"


# ============ ТЕМПЕРАТУРА ============

class TestTemperature:
    def test_c_to_f_freezing(self):
        assert convert(0, "c", "f") == "32.0 f"

    def test_c_to_f_boiling(self):
        assert convert(100, "c", "f") == "212.0 f"

    def test_c_to_k_zero(self):
        assert convert(0, "c", "k") == "273.15 k"

    def test_c_to_k_boiling(self):
        assert convert(100, "c", "k") == "373.15 k"

    def test_k_to_f(self):
        assert convert(273.15, "k", "f") == "32.0 f"

    def test_f_to_c_freezing(self):
        assert convert(32, "f", "c") == "0.0 c"

    def test_f_to_c_boiling(self):
        assert convert(212, "f", "c") == "100.0 c"

    def test_f_to_k_freezing(self):
        assert convert(32, "f", "k") == "273.15 k"

    def test_negative_celsius(self):
        assert convert(-40, "c", "f") == "-40.0 f"

    def test_minus_forty_equivalence_c_to_f(self):
        assert convert(-40, "c", "f") == "-40.0 f"

    def test_minus_forty_equivalence_f_to_c(self):
        assert convert(-40, "f", "c") == "-40.0 c"


# ============ РЕГИСТР ============

class TestCaseInsensitivity:
    def test_uppercase_length(self):
        assert convert(100, "CM", "M") == "1.0 m"

    def test_mixed_case_length(self):
        assert convert(100, "Cm", "m") == "1.0 m"

    def test_uppercase_mass(self):
        assert convert(1000, "G", "KG") == "1.0 kg"

    def test_uppercase_temperature(self):
        assert convert(0, "C", "F") == "32.0 f"

    def test_mixed_case_temperature(self):
        assert convert(0, "c", "K") == "273.15 k"


# ============ ТОЖДЕСТВЕННАЯ КОНВЕРТАЦИЯ ============

class TestIdentity:
    def test_mm_to_mm(self):
        assert convert(42, "mm", "mm") == "42.0 mm"

    def test_cm_to_cm(self):
        assert convert(42, "cm", "cm") == "42.0 cm"

    def test_m_to_m(self):
        assert convert(42, "m", "m") == "42.0 m"

    def test_km_to_km(self):
        assert convert(42, "km", "km") == "42.0 km"

    def test_g_to_g(self):
        assert convert(42, "g", "g") == "42.0 g"

    def test_kg_to_kg(self):
        assert convert(42, "kg", "kg") == "42.0 kg"

    def test_c_to_c(self):
        assert convert(42, "c", "c") == "42.0 c"

    def test_f_to_f(self):
        assert convert(42, "f", "f") == "42.0 f"

    def test_k_to_k(self):
        assert convert(42, "k", "k") == "42.0 k"

    def test_identity_uppercase(self):
        assert convert(42, "M", "M") == "42.0 m"


# ============ НЕИЗВЕСТНАЯ ЕДИНИЦА ============

class TestUnknownUnit:
    def test_unknown_from(self):
        with pytest.raises(UnknownUnitError):
            convert(1, "xyz", "m")

    def test_unknown_to(self):
        with pytest.raises(UnknownUnitError):
            convert(1, "m", "ft")

    def test_unknown_both(self):
        with pytest.raises(UnknownUnitError):
            convert(1, "abc", "xyz")

    def test_unknown_miles(self):
        with pytest.raises(UnknownUnitError):
            convert(1, "miles", "km")

    def test_unknown_pounds(self):
        with pytest.raises(UnknownUnitError):
            convert(1, "lb", "kg")

    def test_empty_unit(self):
        with pytest.raises(UnknownUnitError):
            convert(1, "", "m")


# ============ НЕСОВМЕСТИМЫЕ ЕДИНИЦЫ ============

class TestIncompatibleUnits:
    def test_length_to_mass(self):
        with pytest.raises(IncompatibleUnitsError):
            convert(1, "m", "kg")

    def test_length_to_temperature(self):
        with pytest.raises(IncompatibleUnitsError):
            convert(1, "cm", "c")

    def test_mass_to_length(self):
        with pytest.raises(IncompatibleUnitsError):
            convert(1, "g", "km")

    def test_mass_to_temperature(self):
        with pytest.raises(IncompatibleUnitsError):
            convert(1, "kg", "f")

    def test_temperature_to_length(self):
        with pytest.raises(IncompatibleUnitsError):
            convert(20, "c", "m")

    def test_temperature_to_mass(self):
        with pytest.raises(IncompatibleUnitsError):
            convert(20, "f", "kg")
