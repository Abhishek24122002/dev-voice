import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey
import datetime
import random
import numpy as np
import pyttsx3


chatStr = ""
# https://youtu.be/Z3ZAJoi4x6Q


def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Harry: {query}\n Jarvis: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a  try catch block
    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]


def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=0.7,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a  try catch block
    # print(response["choices"][0]["text"])
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    # with open(f"Openai/prompt- {random.randint(1, 2343434356)}", "w") as f:
    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
        f.write(text)


def say(text):
    # Use PowerShell to convert text to speech
    # os.system(f'PowerShell -Command "Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{text}\')"')
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # r.pause_threshold =  0.6
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Jarvis"

def open_vs_code():
    say("Opening vs code")
    os.system(f'start cmd /K "code . "')

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Jarvis"


def open_cmd(app_name):
    say("Opening CMD")
    # Create a path for the new directory by joining the location and app_name
    directory_path = os.path.join("D:\Major Project", app_name)

    # # Create a new directory at the specified location
    os.makedirs(directory_path, exist_ok=True)

    # # Change the working directory to the newly created directory
    os.chdir(directory_path)
    say('Creating React App ')
    # Open a command prompt and run the 'npx create-react-app' command
    os.system(f'start cmd /K "npx create-react-app {app_name}"')
    
    


if __name__ == '__main__':
    print('Welcome to Dev Voice AI')
    say("Dev Voice AI")
    while True:
        print("Listening...")
        say('Listening')
        query = takeCommand()
        # todo: Add more sites
        sites = [["youtube", "https://www.youtube.com"], ["website",
                                                          "https://abhishekthorat.netlify.app/"], ["google", "https://www.google.com"], ]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
        # todo: Add a feature to play a specific song
        if "open music" in query:
            musicPath = "/Users/harry/Downloads/downfall-21371.mp3"
            os.system(f"open {musicPath}")
        

        elif "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            print(f"Sir time is {hour} bajke {min} minutes")
            say(f"Sir time is {hour} bajke {min} minutes")

        elif "open vs code".lower() in query.lower():
         os.system(f"open /Applications/Visual\ Studio\ Code.app/Contents/Resources/app/bin/code")
         

        elif "open pass".lower() in query.lower():
            os.system(f"open /Applications/Passky.app")

        elif "vs code" in query.lower():
            open_vs_code()

        elif "testing".lower() in query.lower():
            ai(prompt=query)

        elif "Jarvis Quit".lower() in query.lower():
            exit()

        elif "reset chat".lower() in query.lower():
            chatStr = ""

        elif "create react app" in query.lower():
            app_name = query.lower().replace("create react app", "").strip()
            open_cmd(app_name)
        elif "dev" in query.lower():
            say('at your service sir')

        elif "answer a question" in query.lower():
            # Prompt the user for a question
            say("Sure, please ask your question.")
            question = takeCommand()
            ai(prompt=question)

        else:
            print("Chatting...")
            say('AI turning off')
            chat(query)

        # say(query)