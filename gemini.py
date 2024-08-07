import google.generativeai as genai
from gtts import gTTS
import json
from threading import Thread
from kivy.clock import mainthread

PromptGenre = "Road Trip"
PromptLanguage = "Spanish"
PromptDifficulty = 1

prompt = ""
gemini_response = ""

storyData = ""



currentAnswers = list()  


class CustomThread(Thread):     #Custom Thread class for later multi-threaded processes
    def __init__(self,group=None, target=None, name=None, args=(),kwargs={},Verbose=None):
        Thread.__init__(self,group,target,name,args,kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        Thread.join(self)
        return self._return

def SaveDataSettings(f,v,k,l):      #Saves settings to json file
    print("Saving Settings")

    dictionary = {      #uses settings to construct json file
        "FirstTime": f,
        "KeyValidity": v,
        "GeminiKey": k,
        "DefaultLang": l
    }

    json_object = json.dumps(dictionary, indent=4)
 
    with open("savedData.json", "w") as outfile:    #Saves settings to file
        outfile.write(json_object)

try:        #tries to find settings file if doesnt find one, then it creates the file with default values
    f = open('savedData.json')
    data = json.load(f)
except:
    SaveDataSettings(True,False,"L","English")
    f = open('savedData.json')
    data = json.load(f)
    pass

firstTime = data['FirstTime']       #Saves global variables to the settings from the settings file
VerifiedKey = data['KeyValidity']
defaultLanguage = data['DefaultLang']
geminikey = data['GeminiKey']

if VerifiedKey == True:     #Configures key for Gemini API if key was verified
    genai.configure(api_key=geminikey) #Configures Gemini API with API Key from environmnet variable

model = genai.GenerativeModel('gemini-1.5-pro-latest') #Selects Gemini Model
chat = model.start_chat(history=[]) #Begins conversation chat with gemini

def setKey(key):        #Takes in a key and saves key to settings structure
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

def generateStory(g,l,d,m): #Generates the story given the corresponding topic, language and difficulty
    PromptGenre = g
    PromptLanguage = l
    PromptDifficulty = d

    prompt = Difficulty(PromptGenre,PromptLanguage,PromptDifficulty) #Generates the prompt depending on genre, language, and difficulty
    
    global model
    global chat

    
    chat

    try:
        gemini_response = chat.send_message(prompt).text #Sends prompt to Gemini
    except:
        ChangeToError(m)
        return
    
    print(gemini_response)

        

    language = LanguageCode(PromptLanguage) #Converts language into corresponding language code for use with text-to-speech

    keyword = [15]   #Formatting response for better output
    keyword = gemini_response.splitlines()
    mKeyword = list()
    mKeyword = list(filter(None,keyword))
    
    mResponse = FormatGeminiJSON(mKeyword)
    with open('CurrentStory.json', 'w', encoding='utf-8') as f:
        for line in mResponse:
            f.write(f"{line}\n")
    f.close()

    global storyData    #Open story data in utf-8 and assigning it to the variable
    f = open('CurrentStory.json', encoding='utf-8')
    storyData = json.load(f)

    myobj = gTTS(text=storyData['story'], lang=language, slow=False, lang_check= False) #Creates text-to-speech with prompt and language code
    myobj.save("prompt.mp3") #Saves text-to-speech file


    m.ids.prompt_output.text = storyData['story']    #Outputs story to screen label

    m.ids.question_output1.text = storyData['questions'][0]['question']     #Outputs questions to screen labels
    m.ids.question_output2.text = storyData['questions'][1]['question']
    m.ids.question_output3.text = storyData['questions'][2]['question']
    m.ids.question_output4.text = storyData['questions'][3]['question']
    m.ids.question_output5.text = storyData['questions'][4]['question']
    ChangeToPrompt(m)

@mainthread
def ChangeToPrompt(sm):     #Changes screen to the prompt screen in main thread
    sm.current = "PromptScreen"

@mainthread
def ChangeToError(sm):      #Changes screen to the error screen in main thread
    sm.current = "ErrorScreen"

     

def Difficulty(genre,language,diff):    #Defines how difficulty effects story generation
    if diff == 1:
        return "Generate a short 6 sentence story about a " + genre + " in " + language + "then generate 5 questions about the story in " + defaultLanguage + " with answers and format it all in json and make sure all dialog uses single quotes only and each string element should use double quotes only"
    elif diff == 2:
        return "Generate a short 6 sentence story about a " + genre + " in " + language + "then generate 5 questions about the story in " + language + "  with answers and format it all in json and make sure all dialog uses single quotes only and each string element should use double quotes only"
    elif diff == 3:
        return "Generate a short 6 sentence story about a " + genre + " in " + language + "then generate 5 questions about the story in " + language + "  with answers and format it all in json and make sure all dialog uses single quotes only and each string element should use double quotes only"

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

def CheckAnswers(q1,q2,q3,q4,q5,m):   #Will be used to check if the answers are correct
    global storyData
    global  PromptDifficulty
    if PromptDifficulty != 3:
        AnswerResponse = "Are these answers similar to the answers you gave: " + q1 + "AND " + storyData['questions'][0]['answer'] + ";" + q2 + "AND " + storyData['questions'][1]['answer'] + ";"  + q3 + "AND " + storyData['questions'][2]['answer'] + ";"  + q4 + "AND " + storyData['questions'][3]['answer'] + ";"  + q5 + "AND " + storyData['questions'][4]['answer'] + ". Just say correct or wrong for each question and nothing else then format it all in json and label each element as answer"
    else:
        AnswerResponse = "Are these answers similar to the answers you gave: " + q1 + "AND " + storyData['questions'][0]['answer'] + ";" + q2 + "AND " + storyData['questions'][1]['answer'] + ";"  + q3 + "AND " + storyData['questions'][2]['answer'] + ";"  + q4 + "AND " + storyData['questions'][3]['answer'] + ";"  + q5 + "AND " + storyData['questions'][4]['answer'] + ". Just say correct or wrong for each question and nothing else then format it all in json and label each element as answer. if the comparisons are in different languages then mark it wrong"

    response = []
    try:
        response = chat.send_message(AnswerResponse).text.splitlines()
    except:
        m.current = "ErrorScreen"
        return
    answers = FormatGeminiJSON(response)

    with open('AnswerResponse.json', 'w', encoding='utf-8') as f:
        for line in answers:
            f.write(f"{line}\n")
    
    f.close()
    return json.load(open('AnswerResponse.json'))


def FormatGeminiJSON(response):     #Gets rid of text formatting from Gemini response 
    mResponse = list()
    for x in range(len(response)):
        if x == 0 or x == (len(response)-1):
            print("")
        else:
            mResponse.append(response[x])

    return mResponse