from kivymd.app import MDApp
from kivymd.uix.button import MDButton, MDButtonText
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty

from gemini import *

from functools import partial

sm = ScreenManager()


class HomeScreen(Screen):
    def Next(*args):
        global sm
        sm.current = 'GenreScreen'
    pass
    
class GenreScreen(Screen):
    def Next(*args):
        global sm
        global PromptGenre
        PromptGenre = args[1]
        sm.current = 'LanguageScreen'
    pass
class LanguageScreen(Screen):
    def Next(*args):
        global sm
        global PromptLanguage
        PromptLanguage = args[1]
        sm.current = 'DifficultyScreen'
    pass
class DifficultyScreen(Screen):
    def Next(*args):
        global sm
        global PromptDifficulty
        PromptDifficulty = args[1]
        print("Genre: " + PromptGenre + ", Language: " + PromptLanguage + ", Difficulty: " + str(PromptDifficulty))
        PromptScreen.UpdateText(generateStory(PromptGenre,PromptLanguage,PromptDifficulty))
        sm.current = 'PromptScreen'
    pass



class PromptScreen(Screen):
    response = StringProperty("L")

    def UpdateText(gemini):
        print(gemini)
        response = gemini
    pass



class PrototypeApp(MDApp):
    def build(self):
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple"

        Builder.load_file("prototype.kv")

        global sm
        sm.add_widget(HomeScreen(name = 'HomeScreen'))
        sm.add_widget(GenreScreen(name = 'GenreScreen'))
        sm.add_widget(LanguageScreen(name = 'LanguageScreen'))
        sm.add_widget(DifficultyScreen(name = 'DifficultyScreen'))
        sm.add_widget(PromptScreen(name = 'PromptScreen'))        

        return sm
    


PrototypeApp().run()