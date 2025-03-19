import speech_recognition as sr  # Library for recognizing voice commands
import pyautogui  # Library to automate keyboard presses
import pyttsx3  # Text-to-speech engine for voice feedback

# Initialize speech recognition and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    """Converts text to speech for audio feedback."""
    engine.say(text)
    engine.runAndWait()

def mute_action():
    """Triggers the mute function via remote control."""
    pyautogui.press("mute")  # Simulates pressing the mute button
    speak("Muted this scene!")

def skip_action():
    """Skips the current scene by simulating a right arrow key press."""
    pyautogui.press("right")  # Skips ahead
    speak("Skipped this scene!")

def undo_action():
    """Rewinds or undoes the last action by pressing the left arrow key."""
    pyautogui.press("left")  # Moves playback backward
    speak("Undo last action!")

def pause_action():
    """Pauses or resumes the video using the space bar."""
    pyautogui.press("space")  # Pauses/Resumes video
    speak("Toggling pause!")

def listen_for_commands():
    """Listens for user voice commands and executes corresponding actions."""
    with sr.Microphone() as source:
        print("Listening for voice command...")
        audio = recognizer.listen(source)  # Capture audio input
    
    try:
        command = recognizer.recognize_google(audio).lower()  # Convert speech to text
        print(f"Recognized command: {command}")
        
        if "mute this scene" in command:
            mute_action()
        elif "skip scene" in command:
            skip_action()
        elif "undo" in command:
            undo_action()
        elif "pause" in command:
            pause_action()
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
