import speech_recognition as sr
import pyautogui
import pyttsx3

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def mute_action():
    pyautogui.press("mute")
    speak("Muted this scene!")

def skip_action():
    pyautogui.press("right")
    speak("Skipped this scene!")

def undo_action():
    pyautogui.press("left")
    speak("Undo last action!")

def listen_for_commands():
    with sr.Microphone() as source:
        print("Listening for voice command...")
        audio = recognizer.listen(source)
    
    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"Recognized command: {command}")
        
        if "mute this scene" in command:
            mute_action()
        elif "skip scene" in command:
            skip_action()
        elif "undo" in command:
            undo_action()
        else:
            print("Command not recognized.")
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
    except sr.RequestError:
        print("Could not request results, check your internet connection.")

if __name__ == "__main__":
    print("Voice command system is active. Say a command!")
    while True:
        listen_for_commands()