from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager

# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.

# Declare both screens
class MenuScreen(MDScreen):

        MDScreen(
        
            )
             

class SettingsScreen(MDScreen):
    pass

class TestApp(MDApp):

    def build(self):
        # Create the screen manager
        sm = MDScreenManager()
        sm.add_widget(MenuScreen(name='Home'))
        sm.add_widget(SettingsScreen(name='settings'))

        return sm


