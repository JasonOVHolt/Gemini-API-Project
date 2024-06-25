import os
import google.generativeai as genai
from gtts import gTTS


PromptGenre = "Road Trip"
PromptLanguage = "Spanish"
PromptDifficulty = 1
defaultLanguage = "English"

prompt = ""
gemini_response = ""

genai.configure(api_key=os.getenv('GEMINI_API_KEY')) #Configures Gemini API with API Key from environmnet variable
model = genai.GenerativeModel('gemini-1.5-pro-latest') #Selects Gemini Model
chat = model.start_chat(history=[]) #Begins conversation chat with gemini

def validKey(): #Verifies api key is valid
    try:
        model.generate_content("Hello") #Sends Simple message to see if an error occurs
    except:
        return False
    return True

def generateStory(g,l,d): #Generates the story given the corresponding topic, language and difficulty
    PromptGenre = g
    PromptLanguage = l
    PromptDifficulty = d

    prompt = Difficulty(PromptGenre,PromptLanguage,PromptDifficulty) #Generates the prompt depending on genre, language, and difficulty
    
    global model
    global chat

    chat

    gemini_response = chat.send_message(prompt).text #Sends prompt to Gemini
    print(gemini_response)

    language = LanguageCode(PromptLanguage) #Converts language into corresponding language code for use with text-to-speech

    keyword = [5]   #Formatting response for better output
    keyword = gemini_response.splitlines()
    mKeyword = list()
    mKeyword = list(filter(None,keyword))
    
    mResponse = FormatPrompt(mKeyword)
    
    myobj = gTTS(text=mResponse[0], lang=language, slow=False, lang_check= False) #Creates text-to-speech with prompt and language code
    myobj.save("prompt.mp3") #Saves text-to-speech file


    return mResponse
    ###End loading screen here

def FormatPrompt(keyword):      #Determines wheater item is a question or not
    modifiedResponse = list()
    for x in range(len(keyword)):
        if keyword[x][0] == "#":
            print("")
        elif keyword[x][0] == "1" or keyword[x][0] == "2" or keyword[x][0] == "3" or keyword[x][0] == "4" or keyword[x][0] == "5":
           modifiedResponse.append(keyword[x]) 
        else:
            modifiedResponse.append(keyword[x])
    
    return modifiedResponse
        


def BeginStory(*args):

    #Start loading screen here

    generateStory(PromptGenre,PromptLanguage,PromptDifficulty) #Generates story with the genre and language and eventually difficulty 

def Difficulty(genre,language,diff):    #Defines how difficulty effects story generation
    if diff == 1:
        return "Generate a short 6 sentence story about a " + genre + " in " + language + "then generate 5 questions about the story in " + defaultLanguage
    elif diff == 2:
        return "Generate a short 6 sentence story about a " + genre + " in " + language + "then generate 5 questions about the story in " + language
    elif diff == 3:
        return "Generate a short 6 sentence story about a " + genre + " in " + language + "then generate 5 questions about the story in " + language

def LanguageCode(lang):     #Converts language into lang code for text-to-speech generation
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
    elif lang == "Italian":
        x = "it"
    elif lang == "Chinese":
        x = "zh"
    
    return x

def CheckAnswers(q1,q2,q3,q4,q5):   #Will be used to check if the answers are correct
    AnswerResponse = "Are these answers correct: " + q1 + ", " + q2 + ", " + q3 + ", " + q4 + ", " + q5
    print(chat.send_message(AnswerResponse).text)