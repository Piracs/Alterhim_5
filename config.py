"""Модуль конфигурации приложения."""
import os

EXCEL_FILE: str = "Mark_fail.xlsx"
COLUMN: str = "A"

# Начальные настройки для инкрементирования сессий коробки
DEFAULT_BATCH_PREFIX: str = "Партия"
DEFAULT_SAVE_DIR: str = os.path.expanduser("~")
