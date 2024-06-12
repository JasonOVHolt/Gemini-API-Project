from kivymd.app import MDApp
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.properties import StringProperty, ObjectProperty

from gemini import *

from functools import partial

#Horizontal and Vertical Aspect ratio default to 16:9
h_ratio = 450
v_ratio = 800
Window.size = (h_ratio, v_ratio)

sm = ObjectProperty()

class Manager(ScreenManager):
    response = ""

    def Next(*args):
        global sm
        sm = args[0]
        sm.current = 'GenreScreen'
        print(args)


    def Genre(*args):
        global sm
        global PromptGenre
        PromptGenre = args[1]
        sm.current = 'LanguageScreen'

    def Language(*args):
        global sm
        global PromptLanguage
        PromptLanguage = args[1]
        sm.current = 'DifficultyScreen'

    def Difficulty(*args):
        global sm
        global PromptDifficulty
        PromptDifficulty = args[1]
        print("Genre: " + PromptGenre + ", Language: " + PromptLanguage + ", Difficulty: " + str(PromptDifficulty))
        global response
        response = generateStory(PromptGenre,PromptLanguage,PromptDifficulty)
        args[0].ids.prompt_output.text = response
        sm.current = 'PromptScreen'

    
    pass


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