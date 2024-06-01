import os
import google.generativeai as genai
from gtts import gTTS


PromptGenre = "Road Trip"
PromptLanguage = "Spanish"
PromptDifficulty = 1
defaultLanguage = "English"

prompt = ""
gemini_response = ""

def generateStory(): #Generates the story given the corresponding topic, language and difficulty

    prompt = Difficulty(PromptGenre,PromptLanguage,PromptDifficulty) #Generates the prompt depending on genre, language, and difficulty

    genai.configure(api_key=os.getenv('GEMINI_API_KEY')) #Configures Gemini API with API Key from environmnet variable

    model = genai.GenerativeModel('gemini-1.5-pro-latest') #Selects Gemini Model
    chat = model.start_chat(history=[]) #Begins conversation chat with gemini
    chat

    gemini_response = chat.send_message(prompt).text #Sends prompt to Gemini
    print(gemini_response)

    language = LanguageCode(PromptLanguage) #Converts language into corresponding language code for use with text-to-speech

    gemini_response.replace("#","") #Gets rid of # when provided in gemini response as Title

    myobj = gTTS(text=gemini_response, lang=language, slow=False, lang_check= False) #Creates text-to-speech with prompt and language code
    myobj.save("prompt.mp3") #Saves text-to-speech file

    ###End loading screen here



def BeginStory(*args):

    #Start loading screen here

    generateStory() #Generates story with the genre and language and eventually difficulty 

def Difficulty(genre,language,diff):
    if diff == 1:
        return "Generate a short 6 sentence story about a " + genre + " in " + language + "then generate 5 questions about the story in " + defaultLanguage
    elif diff == 2:
        return "Generate a short 6 sentence story about a " + genre + " in " + language + "then generate 5 questions about the story in " + language
    elif diff == 3:
        return "Generate a short 6 sentence story about a " + genre + " in " + language + "then generate 5 questions about the story in " + language

def LanguageCode(lang):
    if lang == "Spanish":
        x = "es"
    elif lang == "English":
        x = "en"
    elif lang == "French":
        x = "fr"
    elif lang == "German":
        x = "de"
    elif lang == "Portuguese":
        x = "pt"
    elif lang == "Japanese":
        x = "ja"
    
    return x

   
def changelanguage(*args):
    global PromptLanguage
   
    if PromptLanguage == "Spanish":
        PromptLanguage = "English"
    elif PromptLanguage == "English":
        PromptLanguage = "French"
    elif PromptLanguage == "French":
        PromptLanguage = "German"
    elif PromptLanguage == "German":
        PromptLanguage = "Portuguese"
    elif PromptLanguage == "Portuguese":
        PromptLanguage = "Japanese"
    elif PromptLanguage == "Japanese":
        PromptLanguage = "Spanish"
    print("Current Language: " + PromptLanguage)

def changeDifficulty(*args):
    global PromptDifficulty
    if(PromptDifficulty == 1):
        PromptDifficulty = 2
        print("Current Difficulty: Medium")
    elif(PromptDifficulty == 2):
        PromptDifficulty = 3
        print("Current Difficulty: Hard")
    elif(PromptDifficulty == 3):
        PromptDifficulty = 1
        print("Current Difficulty: Easy")
    

