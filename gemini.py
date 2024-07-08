import os
import google.generativeai as genai
from gtts import gTTS
import json


PromptGenre = "Road Trip"
PromptLanguage = "Spanish"
PromptDifficulty = 1

prompt = ""
gemini_response = ""

storyData = ""



currentAnswers = list()  


def SaveDataSettings(f,v,k,l):
    print("Saving Settings")
    dictionary = {
        "FirstTime": f,
        "KeyValidity": v,
        "GeminiKey": k,
        "DefaultLang": l
    }

    json_object = json.dumps(dictionary, indent=4)
 

    with open("savedData.json", "w") as outfile:
        outfile.write(json_object)





try:
    f = open('savedData.json')
    data = json.load(f)
except:
    SaveDataSettings(True,False,"L","English")
    f = open('savedData.json')
    data = json.load(f)
    pass




firstTime = data['FirstTime']
VerifiedKey = data['KeyValidity']
defaultLanguage = data['DefaultLang']
geminikey = data['GeminiKey']

if VerifiedKey == True:
    genai.configure(api_key=geminikey) #Configures Gemini API with API Key from environmnet variable


model = genai.GenerativeModel('gemini-1.5-pro') #Selects Gemini Model
chat = model.start_chat(history=[]) #Begins conversation chat with gemini





def setKey(key):
    global data
    data['GeminiKey'] = key
    print(data['GeminiKey'])

    genai.configure(api_key=key) #Configures Gemini API with API Key



def validKey(): #Verifies api key is valid
    global VerifiedKey
    global firstTime
    global data
    global defaultLanguage
    try:
        model.generate_content("Hello") #Sends Simple message to see if an error occurs
    except:
        VerifiedKey = False
        return False
    firstTime = False
    VerifiedKey = True
    SaveDataSettings(firstTime,VerifiedKey,data['GeminiKey'],defaultLanguage)
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

    keyword = [15]   #Formatting response for better output
    keyword = gemini_response.splitlines()
    mKeyword = list()
    mKeyword = list(filter(None,keyword))
    
    mResponse = FormatGeminiJSON(mKeyword)
    with open('CurrentStory.json', 'w') as f:
        for line in mResponse:
            f.write(f"{line}\n")
    f.close()
    myobj = gTTS(text=mResponse[0], lang=language, slow=False, lang_check= False) #Creates text-to-speech with prompt and language code
    myobj.save("prompt.mp3") #Saves text-to-speech file

    global storyData
    f = open('CurrentStory.json')
    storyData = json.load(f)

    return storyData
    ###End loading screen here

        
def BeginStory(*args):

    #Start loading screen here

    generateStory(PromptGenre,PromptLanguage,PromptDifficulty) #Generates story with the genre and language and eventually difficulty 

def Difficulty(genre,language,diff):    #Defines how difficulty effects story generation
    if diff == 1:
        return "Generate a short 6 sentence story about a " + genre + " in " + language + "then generate 5 questions about the story in " + defaultLanguage + " with answers and format it all in json"
    elif diff == 2:
        return "Generate a short 6 sentence story about a " + genre + " in " + language + "then generate 5 questions about the story in " + language + " with answers and format the response like this:\n{Story}\n{Question1}\n{Question1Answer}\n{Question2}\n{Question2Answer}\n{Question3}\n{Question3Answer}\n{Question4}\n{Question4Answer}\n{Question5}\n{Question5Answer}"
    elif diff == 3:
        return "Generate a short 6 sentence story about a " + genre + " in " + language + "then generate 5 questions about the story in " + language + " with answers and format the response like this:\n{Story}\n{Question1}\n{Question1Answer}\n{Question2}\n{Question2Answer}\n{Question3}\n{Question3Answer}\n{Question4}\n{Question4Answer}\n{Question5}\n{Question5Answer}"

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
    global storyData
    AnswerResponse = "Are these answers similar to the answers you gave: " + q1 + "AND " + storyData['questions'][0]['answer'] + ";" + q2 + "AND " + storyData['questions'][1]['answer'] + ";"  + q3 + "AND " + storyData['questions'][2]['answer'] + ";"  + q4 + "AND " + storyData['questions'][3]['answer'] + ";"  + q5 + "AND " + storyData['questions'][4]['answer'] + ". Just say correct or wrong for each question and format it all in json."
    print(chat.send_message(AnswerResponse).text)

def FormatGeminiJSON(response):
    mResponse = list()
    for x in range(len(response)):
        if x == 0 or x == (len(response)-1):
            print("")
        else:
            mResponse.append(response[x])

    return mResponse