import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser


# Initialize speech recognition and text-to-speech
recognizer = sr.Recognizer()
engine = pyttsx3.init()


def speak(text):
    """Convert text to speech."""
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()


def listen():
    """Listen to the user's voice and convert it to text."""
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)

        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            command = recognizer.recognize_google(audio)
            print("You:", command)
            return command.lower()

        except sr.WaitTimeoutError:
            speak("I did not hear anything. Please try again.")
            return ""

        except sr.UnknownValueError:
            speak("Sorry, I didn't understand. Please repeat.")
            return ""

        except sr.RequestError:
            speak("Sorry, the speech recognition service is unavailable.")
            return ""


def process_command(command):

    # Greeting
    if "hello" in command or "hi" in command:
        speak("Hello! How can I help you?")

    # Time
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak("The current time is " + current_time)

    # Date
    elif "date" in command or "today" in command:
        current_date = datetime.datetime.now().strftime("%d %B %Y")
        speak("Today's date is " + current_date)

    # Web search
    elif "search" in command:
        search_query = command.replace("search", "").strip()

        if search_query:
            speak("Searching for " + search_query)
            url = "https://www.google.com/search?q=" + search_query.replace(" ", "+")
            webbrowser.open(url)
        else:
            speak("Please tell me what you want to search.")

    # Exit
    elif "exit" in command or "stop" in command or "quit" in command:
        speak("Goodbye!")
        return False

    else:
        speak("Sorry, I don't know that command.")

    return True


def main():
    speak("Voice assistant started. How can I help you?")

    running = True

    while running:
        command = listen()

        if command:
            running = process_command(command)


if __name__ == "__main__":
    main()