import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey
import datetime
import random
import numpy as np
import pyttsx3
import pygame


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

def play_music(file_name):
    pygame.init()
    pygame.mixer.init()

    try:
        pygame.mixer.music.load(file_name)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except pygame.error as e:
        print(f"An error occurred while playing the music: {e}")

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
        try:
            print("Still Listening...")
            audio = r.listen(source, timeout=10)  # Set a timeout for listening

            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query

        except sr.WaitTimeoutError:
            print("Listening timed out. Please try again.")
            return "Listening timed out"

        except Exception as e:
            print(f"An error occurred: {e}")
            return "Some Error Occurred. Sorry from Jarvis"

def save_tasks_to_file(tasks):
    with open("todays_tasks.txt", "w") as file:
        for task in tasks:
            file.write(task + "\n")

def read_tasks_from_file():
    try:
        with open("todays_tasks.txt", "r") as file:
            tasks = file.readlines()
            return tasks
    except FileNotFoundError:
        return []
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
    say("Sir Welcome to Dev Voice AI")
    todays_tasks = read_tasks_from_file()
    while True:
        print("Listening...")
        say('Listening')
        query = takeCommand()
        # todo: Add more sites
        sites = [["youtube", "https://www.youtube.com"], ["my website",
                                                          "https://abhishekthorat.netlify.app/"], ["google", "https://www.google.com"], ["github", "https://github.com/Abhishek24122002"],]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
        # todo: Add a feature to play a specific song
        if "play music" in query:
            music_file = "relax.mp3"
            say("Playing Music sir")
            play_music(music_file)

        elif "stop music" in query.lower():
            pygame.mixer.music.stop()
            print("Music stopped.")
            say("music Stopped")
        

        elif "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            print(f"Sir time is {hour}  {min} minutes")
            say(f"Sir time is {hour} {min} minutes")

        elif "open vs code".lower() in query.lower():
         os.system(f"open /Applications/Visual\ Studio\ Code.app/Contents/Resources/app/bin/code")

        elif "Today's task" in query.lower():
            # Extract the tasks from the query
            tasks = query.split("task")[1].strip().split(", ")
            
            # Add tasks to the list of today's tasks
            todays_tasks.extend(tasks)

            # Save tasks to the file
            save_tasks_to_file(todays_tasks)

            say("Tasks saved successfully!")

        elif "pending work" in query.lower():
            if todays_tasks:
                say("Your today's tasks are:")
                for task in todays_tasks:
                    say(task)
                    print(task)

            else:
                say("You haven't added any tasks for today.")

        if "quit" in query.lower() in query.lower():
            print("Exiting...")
            say("Exiting. Goodbye!")
            break

        if "stop music" in query.lower():
            if music_playing:
                stop_music()
                print("Stop music command received.")
                say("Stop music command received.")
            else:
                print("No music is currently playing.")
                say("No music is currently playing.")
            continue  # Skip the rest of the loop
         

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
            

        elif "quit" in query.lower():
            print("Exiting...")
            say("Exiting. Goodbye!")
            break


        else:
            print("Chatting...")
            say('AI turning off')
            chat(query)


            