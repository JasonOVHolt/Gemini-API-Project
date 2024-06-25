from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.core.audio import SoundLoader

from gemini import *

#Horizontal and Vertical Aspect ratio default to 16:9
h_ratio = 450
v_ratio = 800
Window.size = (h_ratio, v_ratio)

sm = ObjectProperty()

class Manager(ScreenManager):
    response = list()

    def CheckGemini(*args):
        print(validKey())   #prints whether gemini key is valid

    def SetGeminiKey(*args):
        print("Key set")

    def SubmitAnswers(*args):   #Checkanswers needs to return list of answers to define label text 
        CheckAnswers(args[0].ids.Q1A.text,args[0].ids.Q2A.text,args[0].ids.Q3A.text,args[0].ids.Q4A.text,args[0].ids.Q5A.text)
        sm.current = 'ResponseScreen'
    
    def PlayPrompt(*args):  #Called when play audio button is pressed
        sound = SoundLoader.load("prompt.mp3")  #Loads Generated Text-to-speech
        sound.play()    #Plays Audio clip
        print("Audio Should be Playing")

    def Next(*args):    #Called when button on title screen is pressed
        global sm
        sm = args[0]    #Assigns the screenmanager for later use
        sm.current = 'GenreScreen'  #Switches to genre screen

    def Genre(*args):   #Called when a genre is selected
        global sm
        sm.current = args[1] + 'TopicScreen'    #Switches to selected topic screen

    def Topic(*args):   #Called when topic is selected
        global sm
        global PromptGenre
        PromptGenre = args[1]   #Assigns selected topic to variable used for generating story
        sm.current = 'LanguageScreen'   #Switches to the language screen

    def Language(*args):    #Called when a language is selected
        global sm
        global PromptLanguage
        PromptLanguage = args[1]    #Assigns selected language to variable used for generating story
        sm.current = 'DifficultyScreen'     #Switches to the difficulty screen

    def Difficulty(*args):  #Called when a difficulty is selected
        global sm
        global PromptDifficulty
        PromptDifficulty = args[1]      #Assigns difficultly level to variable used for generating story

        print("Genre: " + PromptGenre + ", Language: " + PromptLanguage + ", Difficulty: " + str(PromptDifficulty))

        global response
        response = generateStory(PromptGenre,PromptLanguage,PromptDifficulty)   #Generates the story with the criteria and assigns to an array

        args[0].ids.prompt_output.text = response[0]    #Outputs story to screen label

        args[0].ids.question_output1.text = response[1]     #Outputs questions to screen labels
        args[0].ids.question_output2.text = response[2]
        args[0].ids.question_output3.text = response[3]
        args[0].ids.question_output4.text = response[4]
        args[0].ids.question_output5.text =  response[5]

        sm.current = 'PromptScreen'     #Switches to the prompt screen


    pass


class PrototypeApp(MDApp):
    

    def build(self):
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style = "Dark"

        kv = Builder.load_file("prototype2.kv")

        return kv



PrototypeApp().run()