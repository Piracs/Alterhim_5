"""Модуль контроллеров экранов Kivy."""
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
import os

class MainScreen(Screen):
    """Главный экран сканирования товаров."""
    status_text = StringProperty("Ожидание сканов...")
    count_text = StringProperty("Успешно отсканировано: 0")
    batch_text = StringProperty("Текущая партия: Не задана")
    save_path = StringProperty(os.path.expanduser("~"))
    count_color = StringProperty("00FF00")

    def choose_directory(self) -> None:
        """Открывает модальное окно выбора папки сохранения."""
        content = BoxLayout(orientation='vertical')
        filechooser = FileChooserListView(dirselect=True, filters=[lambda folder, filename: os.path.isdir(os.path.join(folder, filename))])
        
        btn_layout = BoxLayout(size_hint_y=None, height=40)
        btn_close = Button(text="Отмена")
        btn_select = Button(text="Выбрать")
        
        btn_layout.add_widget(btn_close)
        btn_layout.add_widget(btn_select)
        content.add_widget(filechooser)
        content.add_widget(btn_layout)
        
        popup = Popup(title="Выберите папку сохранения", content=content, size_hint=(0.9, 0.9))
        
        btn_close.bind(on_release=popup.dismiss)
        
        def on_select(instance):
            if filechooser.selection:
                self.save_path = filechooser.selection[0]
            else:
                self.save_path = filechooser.path
            self.manager.app.update_save_path(self.save_path)
            popup.dismiss()
            
        btn_select.bind(on_release=on_select)
        popup.open()


class BatchDialogPopup(Popup):
    """Диалог ввода имени новой партии штрихкодов."""
    def __init__(self, default_name: str, callback, **kwargs):
        super().__init__(**kwargs)
        self.title = "Имя партии"
        self.size_hint = (0.9, 0.4)
        self.auto_dismiss = False
        self.callback = callback
        self.ids.batch_input.text = default_name

    def submit(self) -> None:
        """Передает введенное имя в callback."""
        name = self.ids.batch_input.text.strip()
        self.callback(name)
        self.dismiss()


class InfoPopup(Popup):
    """Универсальное информационное всплывающее окно."""
    def __init__(self, title: str, text: str, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.size_hint = (0.9, 0.4)
        self.ids.info_label.text = text
