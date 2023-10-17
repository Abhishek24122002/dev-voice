import speech_recognition as sr
import subprocess

def execute_command(command):
    if "assistant" in command:
        subprocess.run(["python", "D:\\Downloads\\JarvisAI-YouTube-main\\JarvisAI-YouTube-main\\main.py"])

    elif "exit" in command:
        exit()

# Initialize recognizer
recognizer = sr.Recognizer()

while True:
    with sr.Microphone() as source:
        print("Listening for command...")
        audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio).lower()
            execute_command(command)
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand the audio.")
        except sr.RequestError:
            print("Sorry, there was an error with the speech recognition service.")
