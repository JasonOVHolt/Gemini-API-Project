import os
import google.generativeai as genai
from gtts import gTTS




def generateStory(genre,language,diff):
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    chat = model.start_chat(history=[])
    chat
    response = chat.send_message("Generate a short story about " + genre + " in " + language)
    print(response.text)

    if language == "Spanish":
        language = "es"


    myobj = gTTS(text=response.text, lang=language, slow=False)
    myobj.save("prompt.mp3")
    print()



def testPrint(*args):
    print(os.environ.get('GEMINI_API_KEY'))
    generateStory("a road trip","Spanish",1)