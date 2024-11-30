import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import datetime
import os
import pyjokes
import requests

# Pip install pocketSphinx

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    # Convert text to speech.
    engine.say(text)
    engine.runAndWait()

def get_weather(city):
    # api_key = "ae787ae3e27c4079b6e154730242011"
    url = f"https://api.weatherapi.com/v1/current.json?key=ae787ae3e27c4079b6e154730242011&q={city}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description']
        temperature = data['main']['temp']
        return( f"The weather in {city} is {weather} with a temperature of {temperature} degrees Celsius.")
    else:
        return "Sorry , I couldn't response the weather details right now."

def processCommand(c):
    if "open google" in c.lower():
        speak("Opening Google")
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        speak("Opening Youtube")
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        speak("Opening Linkedin")
        webbrowser.open("https://www.linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        if song in musicLibrary.music:
          link = musicLibrary.music[song]
          speak(f"playing {song}")
          webbrowser.open(link)
        else:
            speak(f"Sorry, I couldn't find the song {song}.")
    elif "what time" in c.lower():
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
    elif "what date" in c.lower():
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {current_date}")
    elif "search for" in c.lower():
        query = c.lower().replace("search for", "").strip()
        speak(f"Searching Google for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")
    elif "tell me a joke" in c.lower():
        joke = pyjokes.get_joke()
        speak(joke)
    elif "weather in" in c.lower():
        city = c.lower().split("in")[1].strip()
        weather_details = get_weather(city)
        speak(weather_details)
    elif "volume up" in c.lower():
        os.system("amixer set Master 10%+")
        speak("Volume increased")
    elif "volume down" in c.lower():
        os.system("amixer set Master 10%-")
        speak("Volume decreased")
    elif "set reminder" in c.lower():
        reminder = c.lower().replace("set reminder", "").strip()
        speak(f"Reminder set for {reminder}")
        with open("reminders.txt", "a") as f:
            f.write(f"{reminder}\n")
    elif "exit" in c.lower() or "goodbye" in c.lower():
        speak("Goodbye! Have a nice day!")
        exit()              
    else:
        speak("Sorry, I didn't understand the command")


def listenForCommand(timeout=5, phrase_time_limit=5):
    """Listen for a command and return it."""
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Dynamically adjust energy threshold
        print("Listening for command...")
        audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
    return recognizer.recognize_google(audio)

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        try:
            print("Listening....")
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for noise levels
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=2)
                wake_word = recognizer.recognize_google(audio).lower()

            if wake_word == "jarvis":
                print("recognizing....")
                speak("Hello, how can I help you?")
                try:
                    command = listenForCommand()
                    processCommand(command)
                except sr.UnknownValueError:
                    speak("Sorry, I couldn't understand your command. Please try again.")
                except sr.RequestError as e:
                    speak("There seems to be an issue with the speech recognition service.")
                except Exception as e:
                    speak(f"An error occurred: {e}")

        except sr.UnknownValueError:
            print("No recognizable speech detected.")
        except sr.RequestError as e:
            print(f"Speech recognition service error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
