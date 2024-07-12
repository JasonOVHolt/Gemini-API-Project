from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.core.audio import SoundLoader
from kivy.clock import Clock

from gemini import *

#Horizontal and Vertical Aspect ratio default to 9:16
h_ratio = 450
v_ratio = 800
Window.size = (h_ratio, v_ratio)

sm = ObjectProperty()
audio = ObjectProperty()
isAudioPlaying = False

selectedTopic = ""

class Manager(ScreenManager):
    response = list()

    def SubmitAnswers(*args):   #Checkanswers needs to return list of answers to define label text 
        global audio
        audio.stop()
        sm.transition.direction = "right"
        answerData = CheckAnswers(args[0].ids.Q1A.text,args[0].ids.Q2A.text,args[0].ids.Q3A.text,args[0].ids.Q4A.text,args[0].ids.Q5A.text)
        global response

        args[0].ids.prompt_output2.text = args[0].ids.prompt_output.text
        args[0].ids.Q1OriginalQuestion.text = response['questions'][0]['question']
        args[0].ids.Q2OriginalQuestion.text = response['questions'][1]['question']
        args[0].ids.Q3OriginalQuestion.text = response['questions'][2]['question']
        args[0].ids.Q4OriginalQuestion.text = response['questions'][3]['question']
        args[0].ids.Q5OriginalQuestion.text = response['questions'][4]['question']


        args[0].ids.Q1OriginalAnswer.text = args[0].ids.Q1A.text
        if answerData['answer1'] == "correct":
            args[0].ids.Q1OriginalAnswer.text_color = "green"
        else:
            args[0].ids.Q1OriginalAnswer.text_color = "red"

        args[0].ids.Q2OriginalAnswer.text = args[0].ids.Q2A.text
        if answerData['answer2'] == "correct":
            args[0].ids.Q2OriginalAnswer.text_color = "green"
        else:
            args[0].ids.Q2OriginalAnswer.text_color = "red"
        
        args[0].ids.Q3OriginalAnswer.text = args[0].ids.Q3A.text
        if answerData['answer3'] == "correct":
            args[0].ids.Q3OriginalAnswer.text_color = "green"
        else:
            args[0].ids.Q3OriginalAnswer.text_color = "red"

        args[0].ids.Q4OriginalAnswer.text = args[0].ids.Q4A.text
        if answerData['answer4'] == "correct":
            args[0].ids.Q4OriginalAnswer.text_color = "green"
        else:
            args[0].ids.Q4OriginalAnswer.text_color = "red"

        args[0].ids.Q5OriginalAnswer.text = args[0].ids.Q5A.text
        if answerData['answer5'] == "correct":
            args[0].ids.Q5OriginalAnswer.text_color = "green"
        else:
            args[0].ids.Q5OriginalAnswer.text_color = "red"


        sm.current = 'ResponseScreen'
    
    def PlayPrompt(*args):  #Called when play audio button is pressed
        global audio
        global isAudioPlaying
        try:
            if audio.state == "stop":
                isAudioPlaying = False
        except:
            pass

        if isAudioPlaying == False:
            audio = SoundLoader.load("prompt.mp3")  #Loads Generated Text-to-speech
            audio.play()    #Plays Audio clip
            isAudioPlaying = True
            print("Audio Should be Playing")
        else:
            audio.stop()
            isAudioPlaying = False
            print("Audio Should have Stopped")

    def Next(*args):    #Called when button on title screen is pressed
        global sm
        
        sm = args[0]    #Assigns the screenmanager for later use
        sm.transition.direction = "left"
        global firstTime
        if firstTime == False and VerifiedKey == True:
            sm.current = 'GenreScreen'  #Switches to genre screen
        else:
            sm.current = 'SettingsScreen'

    def CheckKey(*args):        #Checks to see if given key is valid and shows validity

        setKey(args[0].ids.KeyText.text)
        valid = validKey()      #Sends a message to gemini to see if key is valid

        if valid:       #Shows whether key is valid or not
            args[0].ids.KeyValidity.text_color_normal = "green"
            args[0].ids.KeyValidity.text = "Valid"
            pass    
        else:
            args[0].ids.KeyValidity.text_color_normal = "red"
            args[0].ids.KeyValidity.text = "NOT Valid"
            pass    
        pass

    def ContinueSettings(*args):        #Checks if the key given in the settings screen is valid before letting them continue
        global VerifiedKey
        if VerifiedKey:
            sm.current = 'GenreScreen'
        else:
            pass

    def Genre(*args):   #Called when a genre is selected
        
        global sm
        global selectedTopic
        sm.transition.direction = "left"
        selectedTopic = args[1] + 'TopicScreen'
        sm.current = selectedTopic    #Switches to selected topic screen

    def Topic(*args):   #Called when topic is selected
        
        global sm
        sm.transition.direction = "left"
        global PromptGenre
        PromptGenre = args[1]   #Assigns selected topic to variable used for generating story
        sm.current = 'LanguageScreen'   #Switches to the language screen

    def Language(*args):    #Called when a language is selected
        
        global sm
        sm.transition.direction = "left"
        global PromptLanguage
        PromptLanguage = args[1]    #Assigns selected language to variable used for generating story
        sm.current = 'DifficultyScreen'     #Switches to the difficulty screen

    def Difficulty(*args):  #Called when a difficulty is selected
        
        global sm
        sm.transition.direction = "left"
        global PromptDifficulty
        PromptDifficulty = args[1]      #Assigns difficultly level to variable used for generating story

        print("Genre: " + PromptGenre + ", Language: " + PromptLanguage + ", Difficulty: " + str(PromptDifficulty))

        global response
        response = generateStory(PromptGenre,PromptLanguage,PromptDifficulty)   #Generates the story with the criteria and assigns to an array


        args[0].ids.prompt_output.text = response['story']    #Outputs story to screen label

        args[0].ids.question_output1.text = response['questions'][0]['question']     #Outputs questions to screen labels
        args[0].ids.question_output2.text = response['questions'][1]['question']
        args[0].ids.question_output3.text = response['questions'][2]['question']
        args[0].ids.question_output4.text = response['questions'][3]['question']
        args[0].ids.question_output5.text = response['questions'][4]['question']

        sm.current = 'PromptScreen'     #Switches to the prompt screen


    def BackToStart(*args):     #Resets Text fields and unload old audio file
        global sm
        sm.transition.direction = "right"
        args[0].ids.Q1A.text = ""
        args[0].ids.Q2A.text = ""
        args[0].ids.Q3A.text = ""
        args[0].ids.Q4A.text = ""
        args[0].ids.Q5A.text = ""
        global audio
        audio.unload()

        sm.current = "HomeScreen"


    def BackTo(*args):
        global sm
        global selectedTopic
        sm.transition.direction = "right"
        if args[1] == "Topic":
            sm.current = selectedTopic
        else:
            sm.current = args[1]
        
        pass

    pass


class PrototypeApp(MDApp):
    

    def build(self):
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style = "Dark"

        with open("ui.kv", encoding='utf-8') as f:
            kv = Builder.load_string(f.read())


        return kv



PrototypeApp().run()