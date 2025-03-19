import speech_recognition as sr  # Library for speech recognition
import pyautogui  # Library for automating key presses
import pyttsx3  # Text-to-speech engine
import pyaudio  # Audio processing

# Initialize speech recognition and text-to-speech
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function to make the AI speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Functions to automate remote actions
def mute_action():
    """Presses the 'mute' key and provides voice feedback."""
    pyautogui.press("mute")
    speak("Muted this scene!")

def skip_action():
    """Presses the 'right arrow' key to skip forward and provides voice feedback."""
    pyautogui.press("right")
    speak("Skipped this scene!")

def undo_action():
    """Presses the 'left arrow' key to rewind and provides voice feedback."""
    pyautogui.press("left")
    speak("Undo last action!")

def pause_action():
    """Presses the 'spacebar' key to pause or play and provides voice feedback."""
    pyautogui.press("space")
    speak("Paused or resumed playback.")

def toggle_filtering():
    """Toggles AI filtering on/off globally."""
    global FILTERING_ENABLED
    FILTERING_ENABLED = not FILTERING_ENABLED
    state = "enabled" if FILTERING_ENABLED else "disabled"
    speak(f"Filtering is now {state}")

# Detect available input devices
def get_valid_microphone():
    """Finds a valid microphone device index."""
    try:
        p = pyaudio.PyAudio()
        for i in range(p.get_device_count()):
            device_info = p.get_device_info_by_index(i)
            if device_info.get('maxInputChannels', 0) > 0:  # Ensures it is an input device
                print(f"Using microphone: {device_info['name']} (Index {i})")
                return i  # Returns the first valid input device found
        print("No valid microphone found!")
    except Exception as e:
        print(f"Error detecting microphone: {e}")
    return None  # Returns None if no device is found

# Main function to listen for commands
def listen_for_commands():
    """Listens for user voice commands and triggers respective actions."""
    mic_index = get_valid_microphone()
    if mic_index is None:
        print("❌ No valid microphone detected! Please connect a mic.")
        return
    
    with sr.Microphone(device_index=mic_index) as source:
        print("🎤 Listening for voice command...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        audio = recognizer.listen(source)
    
    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"🗣 Recognized command: {command}")

        if "mute this scene" in command:
            mute_action()
        elif "skip scene" in command:
            skip_action()
        elif "undo" in command:
            undo_action()
        elif "pause" in command:
            pause_action()
        elif "toggle filtering" in command:
            toggle_filtering()
        else:
            print("❌ Command not recognized.")
    except sr.UnknownValueError:
        print("🔇 Sorry, I couldn't understand that.")
    except sr.RequestError:
        print("❌ Could not request results, check your internet connection.")

# Run voice command system in a loop
if __name__ == "__main__":
    print("✅ Voice command system is active. Say a command!")
    while True:
        listen_for_commands()
        
        