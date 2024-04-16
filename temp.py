import requests
from bs4 import BeautifulSoup
import pyttsx3
import speech_recognition as sr

def temp_def():
    # Initialize the speech recognizer and engine
    recognizer = sr.Recognizer()
    engine = pyttsx3.init()

    # Function to speak the given text
    def speak(text):
        engine.say(text)
        engine.runAndWait()

    # Function to process the voice command
    def process_command(command):
        if "temperature" in command:
            speak("Sure, please provide the location.")
            location = get_voice_input()
            if location:
                search = f"temperature in {location}"
                url = f"https://www.google.com/search?q={search}"
                r = requests.get(url)
                data = BeautifulSoup(r.text, "html.parser")
                temp = data.find("div", class_="BNeawe").text
                speak(f"The current temperature in {location} is {temp}")

        elif "weather" in command:
            speak("Sure, please provide the location.")
            location = get_voice_input()
            if location:
                search = f"weather in {location}"
                url = f"https://www.google.com/search?q={search}"
                r = requests.get(url)
                data = BeautifulSoup(r.text, "html.parser")
                weather_info = data.find("div", class_="BNeawe").text
                speak(f"The current weather in {location} is {weather_info}")

        elif "close the conversation" in command:
            speak("Closing the conversation.")
            exit()
        else:
            speak("Wait a minute!")

    # Function to get voice input
    def get_voice_input():
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio).lower()
            print("User Input:", query)
            return query
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand audio.")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return ""

    # Main program loop
    while True:
        try:
            # Listen for voice input
            command = get_voice_input()

            # Process the command
            process_command(command)

        except KeyboardInterrupt:
            break

# Call the voice_assistant function
if __name__ == "__main__":
     temp_def()
