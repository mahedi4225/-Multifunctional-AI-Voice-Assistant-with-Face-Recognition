import os
import pyttsx3
import pyautogui
import speech_recognition as sr

def software_open():
    # Initialize the speech recognizer and engine
    recognizer = sr.Recognizer()
    engine = pyttsx3.init()

    # Function to speak the given text
    def speak(text):
        engine.say(text)
        engine.runAndWait()

    # Function to open software
    def open_software(software_name):
        try:
            os.startfile(software_name)
            speak(f"Opened {software_name}.")
        except Exception as e:
            speak(f"An error occurred while opening {software_name}. Error: {str(e)}")

    # Function to close software
    def close_software(software_name):
        try:
            os.system(f"TASKKILL /F /IM {software_name}.exe")
            speak(f"Closed {software_name}.")
        except Exception as e:
            speak(f"An error occurred while closing {software_name}. Error: {str(e)}")

    # Function to process the voice command
    def process_command(command):
        if "open" in command and "software" in command:
            software_name = command.split("open ")[-1].split(" software")[0]
            open_software(software_name)
        elif "close" in command and "software" in command:
            software_name = command.split("close ")[-1].split(" software")[0]
            close_software(software_name)
        elif "open" in command:   # EASY METHOD
            query = command.replace("open", "")
            query = query.replace("jarvis", "")
            pyautogui.press("super")
            pyautogui.typewrite(query)
            pyautogui.press("enter")
        elif "close the conversation" in command:
            speak("Closing the conversation.")
            exit()
        else:
            speak("Sorry, I couldn't understand that command.")

    # Main program loop
    while True:
        try:
            # Listen for voice input
            with sr.Microphone() as source:
                print("Listening...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)

            # Convert speech to text
            print("Recognizing...")
            command = recognizer.recognize_google(audio).lower()
            print("Command:", command)

            # Process the command
            process_command(command)

        except sr.UnknownValueError:
            print("Sorry, I couldn't understand audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    software_open()