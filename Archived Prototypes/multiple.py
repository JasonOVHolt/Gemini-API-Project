from kivymd.app import MDApp
from kivymd.uix.button import MDButton, MDButtonText
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

class HomeScreen(Screen):
    pass
    
class OtherScreen(Screen):
    pass

class MultipleApp(MDApp):
    def build(self):
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple"

        Builder.load_file("ui.kv")

        sm = ScreenManager()
        sm.add_widget(HomeScreen(name = 'HomeScreen'))
        sm.add_widget(OtherScreen(name = 'OtherScreen'))

        return sm
    

MultipleApp().run()