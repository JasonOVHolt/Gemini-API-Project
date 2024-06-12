from kivymd.app import MDApp
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.properties import StringProperty

from gemini import *

from functools import partial

#Horizontal and Vertical Aspect ratio default to 16:9
h_ratio = 450
v_ratio = 800
Window.size = (h_ratio, v_ratio)


class Manager(ScreenManager):

    def Genre(*args):
        global sm
        sm.current = 'GenreScreen'

    def Language(*args):
        global sm
        sm.current = 'GenreScreen'

    def Difficulty(*args):
        global sm
        sm.current = 'GenreScreen'
    pass

    sm = ScreenManager()

class PrototypeApp(MDApp):
    

    def build(self):
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple"

        kv = Builder.load_file("prototype2.kv")
        

        return kv
    
    def Next(self):
        print("Epic")


PrototypeApp().run()