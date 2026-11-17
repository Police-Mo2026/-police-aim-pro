from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.storage.jsonstore import JsonStore

Window.clearcolor = (0.035, 0.045, 0.065, 1)

PRESETS = {
    "متوازن": {"Camera": 100, "ADS": 90, "Gyro": 250},
    "سريع": {"Camera": 120, "ADS": 105, "Gyro": 300},
    "هادئ": {"Camera": 85, "ADS": 75, "Gyro": 200},
}

class AimApp(App):
    def build(self):
        self.title = "POLICE AIM PRO"
        self.store = JsonStore("aim_settings.json")
        root = BoxLayout(orientation="vertical", padding=dp(14), spacing=dp(10))

        title = Label(text="[b]POLICE AIM PRO[/b]", markup=True, font_size="25sp",
                      size_hint_y=None, height=dp(48), color=(0.25, 0.85, 1, 1))
        root.add_widget(title)
        subtitle = Label(text="مساعد إعدادات التصويب | PUBG Mobile",
                         size_hint_y=None, height=dp(28), font_size="14sp")
        root.add_widget(subtitle)

        scroll = ScrollView()
        body = BoxLayout(orientation="vertical", spacing=dp(12),
                         size_hint_y=None, padding=(dp(2), dp(8)))
        body.bind(minimum_height=body.setter("height"))

        self.values = {}
        for key, label, default, maximum in [
            ("Camera", "حساسية الكاميرا", 100, 200),
            ("ADS", "حساسية أثناء الإطلاق (ADS)", 90, 200),
            ("Gyro", "حساسية الجيروسكوب", 250, 400),
        ]:
            card = BoxLayout(orientation="vertical", size_hint_y=None,
                             height=dp(100), padding=dp(8), spacing=dp(4))
            row = BoxLayout(size_hint_y=None, height=dp(28))
            row.add_widget(Label(text=label, halign="right"))
            value_label = Label(text=str(default), size_hint_x=None, width=dp(55))
            row.add_widget(value_label)
            card.add_widget(row)
            slider = Slider(min=0, max=maximum, value=default)
            slider.bind(value=lambda instance, value, out=value_label: setattr(out, "text", str(int(value))))
            card.add_widget(slider)
            self.values[key] = slider
            body.add_widget(card)

        body.add_widget(Label(text="إعدادات مقترحة كبداية — عدّلها تدريجياً حسب راحتك.",
                              size_hint_y=None, height=dp(42), halign="center"))
        scroll.add_widget(body)
        root.add_widget(scroll)

        buttons = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(8))
        save = Button(text="حفظ الإعدادات", background_normal="", background_color=(0.05, 0.48, 0.68, 1))
        save.bind(on_release=self.save_settings)
        reset = Button(text="إعادة ضبط", background_normal="", background_color=(0.25, 0.28, 0.34, 1))
        reset.bind(on_release=self.reset_settings)
        buttons.add_widget(save)
        buttons.add_widget(reset)
        root.add_widget(buttons)

        note = Label(text="لا يتصل التطبيق باللعبة ولا يغيّر ملفاتها أو يتحكم بالتصويب تلقائياً.",
                     size_hint_y=None, height=dp(45), font_size="11sp",
                     color=(0.7, 0.75, 0.82, 1), halign="center")
        root.add_widget(note)

        if self.store.exists("settings"):
            saved = self.store.get("settings")
            for key, slider in self.values.items():
                if key in saved:
                    slider.value = saved[key]
        return root

    def save_settings(self, *_):
        data = {key: int(slider.value) for key, slider in self.values.items()}
        self.store.put("settings", **data)
        Popup(title="تم الحفظ", content=Label(text="تم حفظ إعداداتك على هذا الجهاز."),
              size_hint=(0.8, 0.3)).open()

    def reset_settings(self, *_):
        defaults = {"Camera": 100, "ADS": 90, "Gyro": 250}
        for key, value in defaults.items():
            self.values[key].value = value
        self.save_settings()

if __name__ == "__main__":
    AimApp().run()
