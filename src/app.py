# Answer to your prompt might be late !!

import pyttsx3.voice
import speech_recognition
import pyttsx3
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from slowprint.slowprint import *
import threading

template = """
Answer the question below.

Here is the conversation history: {context}

Question: {question}

Answer:
"""
model = OllamaLLM(model="llama3.2")
promt = ChatPromptTemplate.from_template(template)
chain = promt | model
recognizer = speech_recognition.Recognizer()


context = ""

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[3].id)
    engine.say(text)
    engine.runAndWait()

def print_and_say(text):
    thread = threading.Thread(target=speak, args=(text,))
    thread.start()
    
    slowprint(f"Jarvis: {result}", 0.2)   

while True:
    try:
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            print("Listening...")
            audio = recognizer.listen(mic)

            user_input = recognizer.recognize_google(audio)
            print("You:", user_input)

            result = chain.invoke({"context": context, "question": user_input})
            
            print_and_say(result)
           
            context += f"\nUser: {user_input}\nJarvis: {result}"
            

    except speech_recognition.UnknownValueError:
        print("Could not understand that !!")
    except speech_recognition.RequestError as e:
        print(f"Request error {e}")
    except Exception as e:
        print(f"Error: {e}")

            