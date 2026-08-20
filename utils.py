"""Вспомогательные функции для обработки данных."""
import re
import time

def clean_mark_code(raw: str) -> str:
    """Очищает полученную строку штрихкода от префиксов и непечатных символов."""
    if not raw:
        return ""
    code = raw.strip()
    prefixes = [']d2', ']D2', '\x1D', '\x02', '\x03', '\x1E', '\x04', '\x00']
    for p in prefixes:
        code = code.replace(p, '')
    code = ''.join(c for c in code if c.isprintable())
    return code.strip()

def sanitize_filename(name: str) -> str:
    """Удаляет недопустимые символы из имени файла."""
    return re.sub(r'[<>:"/\\|?*]', '_', name).strip()

def get_timestamp() -> str:
    """Возвращает текущую временную метку."""
    return time.strftime("%Y-%m-%d %H:%M:%S")
