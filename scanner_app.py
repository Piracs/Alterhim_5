"""Главный модуль логики приложения."""
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.clock import Clock

import threading
import queue
import time

from config import DEFAULT_SAVE_DIR, DEFAULT_BATCH_PREFIX
from utils import clean_mark_code, sanitize_filename, get_timestamp
from excel_manager import ExcelManager
from gui_manager import MainScreen, BatchDialogPopup, InfoPopup

class ScannerApp(App):
    """Главный класс Kivy-приложения."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.batch_prefix = DEFAULT_BATCH_PREFIX
        self.batch_counter = 1
        self.batch_name = ""
        self.count = 0
        self.count_lock = threading.Lock()
        self.running = True
        self.scanned_codes = set()
        self.db_queue = queue.Queue()
        
        self.excel = ExcelManager(DEFAULT_SAVE_DIR)
        
        # Переменные сбора строки данных от HID клавиатуры
        self._keyboard_buffer = []

    def build(self):
        self.icon = 'icon.png'  # Опционально
        self.sm = ScreenManager()
        self.main_screen = MainScreen(name='main')
        self.sm.add_widget(self.main_screen)
        
        # Передача ссылки на App в менеджер для доступа из KV
        self.sm.app = self
        
        # Перехват нажатий клавиатуры (HID режим)
        Window.bind(on_key_down=self._on_keyboard_down)
        
        return self.sm

    def on_start(self):
        # Запуск фонового воркера для записи Excel
        threading.Thread(target=self._excel_worker, daemon=True).start()
        # Запрос первого имени партии
        Clock.schedule_once(lambda dt: self._ask_batch_name(), 0.5)

    def _on_keyboard_down(self, window, key, scancode, codepoint, modifiers):
        """Ловит символы от HID-сканера клавиатуры."""
        if key == 13:  # Код клавиши Enter (финализация штрихкода сканером)
            raw_barcode = "".join(self._keyboard_buffer)
            self._keyboard_buffer.clear()
            if raw_barcode:
                self._process_scanned_code(raw_barcode)
        else:
            if codepoint:
                self._keyboard_buffer.append(codepoint)
        return True

    def _process_scanned_code(self, raw_text: str) -> None:
        code = clean_mark_code(raw_text)
        if not code or len(code) <= 8:
            return

        if code in self.scanned_codes:
            self.main_screen.count_color = "FF0000"
            self.main_screen.count_text = "Успешно отсканировано: Дубль!"
            self.main_screen.status_text = f"Дубликат кода: {code[:40]}..."
            return
        
        self.scanned_codes.add(code)
        with self.count_lock:
            self.count += 1
            current_count = self.count

        timestamp = get_timestamp()
        self.db_queue.put((code, timestamp))

        self.main_screen.count_color = "00FF00"
        self.main_screen.count_text = f"Успешно отсканировано: {current_count}"
        self.main_screen.status_text = f"Последний: {code[:50]}..."

        # Автоматическая проверка лимита, если он задан пользователем (опционально)
        # В данном ТЗ логика завязана на ручное/циклическое подтверждение сборки.

    def _excel_worker(self):
        while self.running:
            try:
                item = self.db_queue.get(timeout=0.5)
                code, timestamp = item
                self.excel.save_code(code, timestamp)
                self.db_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Ошибка сохранения: {e}")
                time.sleep(0.5)

    def update_save_path(self, new_path: str) -> None:
        """Событие изменения директории пользователем."""
        self.excel.update_save_dir(new_path)

    def _ask_batch_name(self) -> None:
        """Вызывает модальное диалоговое окно ввода партии."""
        suggested_name = f"{self.batch_prefix}_{self.batch_counter}"
        popup = BatchDialogPopup(default_name=suggested_name, callback=self._set_batch_name)
        popup.open()

    def _set_batch_name(self, name: str) -> None:
        if not name or name.strip() == "":
            self.batch_name = sanitize_filename(f"{self.batch_prefix}_{self.batch_counter}")
        else:
            self.batch_name = sanitize_filename(name)
            # Извлекаем префикс для сохранения структуры при инкрементировании
            if "_" in self.batch_name:
                parts = self.batch_name.split("_")
                if parts[-1].isdigit():
                    self.batch_prefix = "_".join(parts[:-1])
                    self.batch_counter = int(parts[-1])
                else:
                    self.batch_prefix = self.batch_name
            else:
                self.batch_prefix = self.batch_name

        self.main_screen.batch_text = f"Текущая партия: {self.batch_name}"
        self.scanned_codes.clear()

    def save_and_continue(self) -> None:
        """Обработчик кнопки 'Сохранить и продолжить' и события 'Коробка собрана'."""
        with self.count_lock:
            current_count = self.count

        # Ожидание завершения записи фонового потока
        self.db_queue.join()
        saved_file = self.excel.finalize_file(self.batch_name)

        if saved_file:
            # Отображение информации об успешном сохранении коробки
            info = InfoPopup(title="Коробка собрана", text=f"Партия сохранена:\n{saved_file}\nКодов: {current_count}")
            info.open()
            
            # Инкрементируем счетчик для следующего цикла коробки
            self.batch_counter += 1
            
        with self.count_lock:
            self.count = 0

        # Сброс UI и вызов диалога для новой партии с обновленным номером
        self.main_screen.status_text = "Ожидание сканов..."
        self.main_screen.count_text = "Успешно отсканировано: 0"
        self.main_screen.count_color = "00FF00"
        
        self._ask_batch_name()

    def on_stop(self):
        self.running = False
        # Финализация принудительного закрытия, если были коды
        with self.count_lock:
            if self.count > 0:
                self.db_queue.join()
                self.excel.finalize_file(self.batch_name)
