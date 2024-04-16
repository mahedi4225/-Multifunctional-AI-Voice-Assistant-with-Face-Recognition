import speech_recognition as sr
import pyttsx3
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Initialize the speech recognition and text-to-speech engines
recognizer = sr.Recognizer()
engine = pyttsx3.init()
driver = None  # Initialize the driver object

def search_control():
    # Function to recognize speech
    def recognize_speech():
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio)
            print("You said:", query)
            return query.lower()
        except sr.UnknownValueError:
            print("Sorry, I could not understand.")
            return ""
        except sr.RequestError:
            print("Sorry, there was an issue with the speech recognition service.")
            return ""

    # Function to speak the given text
    def speak(text):
        engine.say(text)
        engine.runAndWait()
    
    # Function to search on YouTube
    def search_on_youtube(query):
        url = "https://www.youtube.com/results?search_query=" + query.replace(" ", "+")
        webbrowser.open(url)

    # Main program loop
    while True:
        command = recognize_speech()

        if "search" in command and "youtube" in command:
            speak("What video would you like to search for?")
            query = recognize_speech()
            search_on_youtube(query)
        elif "play" in command and "video" in command:
            speak("Which video would you like to play? Please specify the number.")
            number = recognize_speech()

            # Convert the number word to an integer
            number_map = {"first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5}  # Add more number mappings if needed
            video_number = number_map.get(number, 1)  # Default to the first video if the number is not recognized

            # Open the YouTube search results and play the specified video
            driver = webdriver.Chrome()
            driver.get("https://www.youtube.com/results?search_query=" + query.replace(" ", "+"))

            # Play the specified video
            try:
                videos = driver.find_elements(By.CSS_SELECTOR, "#contents ytd-video-renderer")
                if videos:
                    video = videos[video_number - 1]
                    link_element = video.find_element(By.TAG_NAME, "a")
                    link_element.click()
                else:
                    speak("No videos found in the search results.")
            except IndexError:
                speak("Sorry, the specified video number is not available.")

        elif "pause" in command or "pause video" in command:
            if driver:
                driver.execute_script("document.getElementsByTagName('video')[0].pause()")
        elif "close" in command and "video" in command:
            if driver:
                driver.quit()
                speak("Video closed.")
        elif "increase sound" in command or "increase volume" in command:
            if driver:
                driver.execute_script("document.getElementsByTagName('video')[0].volume += 0.4")
        elif "decrease sound" in command or "decrease volume" in command:
            if driver:
                driver.execute_script("document.getElementsByTagName('video')[0].volume -= 0.4")
        elif "mute" in command:
            if driver:
                driver.execute_script("document.getElementsByTagName('video')[0].muted = true")
        elif "unmute" in command:
            if driver:
                driver.execute_script("document.getElementsByTagName('video')[0].muted = false")
        elif "scroll up" in command:
            if driver:
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_UP)
        elif "scroll down" in command:
            if driver:
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)

        elif "exit" in command or "quit" in command:
            if driver:
                driver.quit()
            break

# Call the function to start YouTube voice control
if __name__ == "__main__":
     search_control()
