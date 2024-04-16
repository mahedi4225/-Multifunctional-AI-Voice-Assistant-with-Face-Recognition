import pyttsx3
import speech_recognition as sr
import datetime
import wolframalpha
import sympy
import requests
import spacy
from Automation.email_assistant import email_automation
from Features.searchInternet import search_control
from Features.Brain import AIbrain
from Automation.Software_open import software_open
from temp import temp_def


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Set the desired voice

# Load the spaCy English model
nlp = spacy.load('en_core_web_sm')


def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.......")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=10, phrase_time_limit=10)

    try:
        print("Recognizing.....")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        if query.lower() == "exit" or "quit" in query.lower():
            speak("Goodbye Sir!")
            return False
        elif "find temperature" in query.lower():
            temp_def()
            speak("Temperature Mode Activated")  # Call the temp_def() function from Code1
        elif "activate email mode" in query.lower():
            speak("Email Mode Activated!")
            email_automation()
        elif "activate search mode" in query.lower():
            speak("Search Mode Activated!")
            search_control()
        elif "activate chat mode" in query.lower():
            speak("Chat Mode Activated")
            AIbrain()
        elif "activate software" in query.lower():
            speak("Software Automation Mode Activated")
            software_open()

    except Exception as e:
        speak("Say That Again Sir!")
        return True
    return True

def wish_me():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak("Good Morning Sir!")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Sir!")

    else:
        speak("Good Evening Sir!")

    speak("I am your AI assistant. How can I assist you?")

def WolframeAlpha(query):
    api_key = "T9KXP5-W996EKAUX7"
    requester = wolframalpha.Client(api_key)
    requested = requester.query(query)
    
    try:
        # Check if the query has a direct answer
        Answer = next(requested.results).text
        speak(Answer)

    except StopIteration:
        try:
            # Check if the query has a result that can be computed
            pods = requested.pods
            result = next(pod for pod in pods if pod["@id"] == "Result")
            Answer = result.subpod.plaintext
            speak(Answer)

        except StopIteration:
            try:
                # Check if the query has an image result
                pods = requested.pods
                image = next(pod for pod in pods if pod["@id"] == "Image")
                url = image["subpod"]["img"]["@src"]
                speak(f"You can see the result at this url: {url}")

            except StopIteration:
                # No answer found, try to solve math problems
                try:
                    Answer = sympy.simplify(query)
                    speak(str(Answer))
                except:
                    speak('Not Found Sir!')



    
def mainT():
    wish_me()
    while takecommand():
        
        pass

if __name__ == "__main__":
    mainT()