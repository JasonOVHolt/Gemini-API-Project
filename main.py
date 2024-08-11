from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screenmanager import MDScreenManager
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.core.audio import SoundLoader
from kivy.core.text import LabelBase, DEFAULT_FONT

from gemini import *

#Horizontal and Vertical Aspect ratio default to 9:16
h_ratio = 540
v_ratio = 960
Window.size = (h_ratio, v_ratio)

sm = ObjectProperty()       #Creates Object Properties for the screen manager and audio playback
audio = ObjectProperty()

isAudioPlaying = False

selectedTopic = ""

t1 = CustomThread()     #Assigns t1 to the custom thread calss



class Manager(MDScreenManager):
    response = list()
    

    def SubmitAnswers(*args):   #Checkanswers needs to return list of answers to define label text 

        global audio
        try:    #Tries to stop audio if audio is currently playing
            audio.stop()    
        except:
            pass

        sm.transition.direction = "right"
        answerData = CheckAnswers(args[0].ids.Q1A.text,args[0].ids.Q2A.text,args[0].ids.Q3A.text,args[0].ids.Q4A.text,args[0].ids.Q5A.text,args[0])     #Assigns the answer response to the variable for later use

        global storyData
        f = open('CurrentStory.json', encoding='utf-8')     #Opens the story data for displaying on results screen
        story = json.load(f)

        args[0].ids.prompt_output2.text = args[0].ids.prompt_output.text    #Shows story and question on the results screen
        args[0].ids.Q1OriginalQuestion.text = story['questions'][0]['question']
        args[0].ids.Q2OriginalQuestion.text = story['questions'][1]['question']
        args[0].ids.Q3OriginalQuestion.text = story['questions'][2]['question']
        args[0].ids.Q4OriginalQuestion.text = story['questions'][3]['question']
        args[0].ids.Q5OriginalQuestion.text = story['questions'][4]['question']


        args[0].ids.Q1OriginalAnswer.text = args[0].ids.Q1A.text    #Checks each question to see if the answers were similar and sets the text color
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
            sm.ids.audioicon.icon = 'pause'
            sm.ids.audiotext.text = 'Pause Audio'
            print("Audio Should be Playing")
        else:
            audio.stop()
            isAudioPlaying = False
            sm.ids.audioicon.icon = 'play'
            sm.ids.audiotext.text = 'Play Audio'
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

    def GoToSettings(*args):    #Called when clicking settings icon
        args[0].current = "SettingsScreen"
        pass


    def CheckKey(*args):        #Checks to see if given key is valid and shows validity
        global VerifiedKey
        setKey(args[0].ids.KeyText.text)
        valid = validKey()      #Sends a message to gemini to see if key is valid

        if valid:       #Shows whether key is valid or not
            VerifiedKey = True
            args[0].ids.KeyValidity.text_color_normal = "green"
            args[0].ids.KeyValidity.text = "Valid"
            args[0].ids.validButton.icon = "check-bold"
            args[0].ids.validButton.text_color = "green"
            pass    
        else:
            args[0].ids.KeyValidity.text_color_normal = "red"
            args[0].ids.KeyValidity.text = "NOT Valid"
            args[0].ids.validButton.icon = "close-thick"
            args[0].ids.validButton.text_color = "red"
            pass    
        pass

    def ContinueSettings(*args):        #Checks if the key given in the settings screen is valid before letting them continue
        global VerifiedKey
        
        if VerifiedKey:
            args[0].current = 'GenreScreen'
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
        sm.ids.loading_gif._coreimage.anim_reset(True) #Resets loading icon animation
        sm.current = 'LoadingScreen'
        global t1

        t1 = CustomThread(target=generateStory,args=(PromptGenre,PromptLanguage,PromptDifficulty,sm))   #Assigns thread to function
        t1.start()

        if PromptDifficulty == 1:   #Configures difficulty to text for loading display
            diff = "easy"
        if PromptDifficulty == 2:
            diff = "medium"
        if PromptDifficulty == 3:
            diff = "hard"

        sm.ids.GenerationID.text = "Now generating a story about " + PromptGenre + " in the " + PromptLanguage + " language with a difficulty of " + diff + "..."   #Displays current

        #t1.join()

    def BackToStart(*args):     #Resets Text fields and unload old audio file
        global sm
        sm.transition.direction = "right"
        args[0].ids.Q1A.text = ""
        args[0].ids.Q2A.text = ""
        args[0].ids.Q3A.text = ""
        args[0].ids.Q4A.text = ""
        args[0].ids.Q5A.text = ""
        global audio

        try:       #Unloads audio
            audio.unload()
        except:
            pass

        sm.current = "HomeScreen"

    def BackTo(*args):      #Sends you screen depending on what augment is giving
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
    

    def build(self):    #Builds app
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style = "Dark"

        with open("ui.kv", encoding='utf-8') as f:   #Loads Kivy file
            kv = Builder.load_string(f.read())

        LabelBase.register(name='Code2000', fn_regular='Code2000.ttf')  #Sets font
        LabelBase.register(DEFAULT_FONT, fn_regular='Code2000.ttf')

        return kv




PrototypeApp().run()