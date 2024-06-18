from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import *

Builder.load_string("""
<MainScreen>:                
    BoxLayout:
        canvas.before:
            Color:
                rgba: 0, 1, 0, 1
            Rectangle:
                pos: self.pos
                size: self.size
        Button:
            canvas.after:
                Color:
                    rgba: 1, 0, 0, .1
                Rectangle:
                    pos: self.pos
                    size: self.size
            text: 'GoTo Settings'
            on_press: 
                root.manager.transition.direction = 'left'
                root.manager.current = 'settings'
                
        Button:
            text: 'Quit'

<SettingsScreen>:
    BoxLayout:
        Button:
            text: 'Settings Button'
        Button:
            text: 'Back to menu'
            on_press: 
                root.manager.transition.direction = 'right'
                root.manager.current = 'main'
                
""")                    



class MainScreen(Screen):
    pass
class SettingsScreen(Screen):
    pass
class TestApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(SettingsScreen(name='settings'))    
        return sm

if __name__ == '__main__':
    TestApp().run()

