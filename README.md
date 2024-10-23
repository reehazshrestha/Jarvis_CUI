# Voice Assistant with Ollama

This project implements a voice assistant using the `Ollama` model. It listens to your questions and responds using text-to-speech.

## Requirements

Before running this project, ensure you have the following:

- Python 3.x
- Required libraries (see below)
- [Ollama](https://ollama.com/) installed to run the model

## Installation

To install the necessary libraries, run:

```bash
pip install pyttsx3 SpeechRecognition langchain_ollama langchain_core slowprint
```

Additionally, make sure to install Ollama by following the instructions on their official website.

## Usage:

Here's how the code works:

1.It listens to the microphone input and recognizes the spoken questions. 
2.It processes the input using the Ollama language model to generate responses. 
3.The assistant responds with text-to-speech. 

## Code Explanation:

```
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
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model
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
```
## Note:

The response to your prompt might be delayed depending on the processing time.

Feel free to explore and modify the code to suit your needs!


You can customize it further based on your preferences or add more details as needed!
