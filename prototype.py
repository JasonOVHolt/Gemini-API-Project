from kivymd.app import MDApp
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.properties import StringProperty, ObjectProperty

from gemini import *

from functools import partial

sm = ScreenManager()

#Horizontal and Vertical Aspect ratio default to 16:9
h_ratio = 450
v_ratio = 800
Window.size = (h_ratio, v_ratio)

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
    def Next(self,diff):
        global sm
        global PromptDifficulty
        PromptDifficulty = diff
        print("Genre: " + PromptGenre + ", Language: " + PromptLanguage + ", Difficulty: " + str(PromptDifficulty))
        promptText = "TEST"#generateStory(PromptGenre,PromptLanguage,PromptDifficulty)
        PromptScreen.UpdatePromptText(self,promptText) 
        #print(PromptScreen.response)
        sm.current = 'PromptScreen'
    pass



class PromptScreen(Screen):
    response = StringProperty("L",rebind=True)

    def on_response(self,instance,value):
        print("Value Changed")

    def UpdatePromptText(self,gemini):       
        PromptScreen.response = gemini
        currentApp = MDApp.get_running_app()
        sm.id.prompt_output.text = f'{PromptScreen.response}'



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