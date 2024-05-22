import os
import google.generativeai as genai
from gtts import gTTS

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

model = genai.GenerativeModel('gemini-1.5-pro-latest')



def testPrint(*args):
    print("Yo")