import subprocess
import sys


def test_cli_calc():
    """Проверяем запуск калькулятора через командную строку."""
    result = subprocess.run(
        [sys.executable, "-m", "toolkit", "calc", "2+2"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "4" in result.stdout

def test_cli_error_code():
    """При ошибке код возврата должен быть 2."""
    result = subprocess.run(
        [sys.executable, "-m", "toolkit", "calc", "2+"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 2
