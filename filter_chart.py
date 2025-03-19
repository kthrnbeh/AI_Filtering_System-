import mss
import cv2
import numpy as np
import pygetwindow as gw
import pyautogui
import pytesseract
import speech_recognition as sr
import pyttsx3

# Configure OCR for subtitle detection
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Change path for Mac/Linux

# Define keywords to mute or skip
MUTE_KEYWORDS = [
    "fuck", "shit", "bitch", "damn", "cunt", "asshole", "bastard", "suck", 
    "jesus christ", "goddamn", "oh my god", "hell"
]  # Add words to mute
SKIP_KEYWORDS = ["violence", "blood", "scary"]

# Initialize voice engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

FILTERING_ENABLED = True  # Global toggle
def toggle_filtering():
    global FILTERING_ENABLED
    FILTERING_ENABLED = not FILTERING_ENABLED
    state = "enabled" if FILTERING_ENABLED else "disabled"
    print(f"Filtering is now {state}")

def capture_screen():
    """Captures the streaming video window and processes it in real-time."""
    with mss.mss() as sct:
        while True:
            streaming_services = ["Netflix", "YouTube", "Hulu", "Disney+", "Amazon Prime"]
            window = None
            for service in streaming_services:
                win = gw.getWindowsWithTitle(service)
                if win:
                    window = win
                    break
            
            if not window:
                print("No streaming window detected. Waiting...")
                continue

            x, y, width, height = window[0]._rect
            screenshot = sct.grab({"top": y, "left": x, "width": width, "height": height})
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

            process_frame(frame)

            if not FILTERING_ENABLED:
                continue

    cv2.destroyAllWindows()

def process_frame(frame):
    """Processes the video frame to detect objectionable content."""
    if not FILTERING_ENABLED:
        return

    h, w, _ = frame.shape
    subtitle_region = frame[int(h * 0.8):, :]
    subtitle_gray = cv2.cvtColor(subtitle_region, cv2.COLOR_BGR2GRAY)
    subtitle_gray = cv2.threshold(subtitle_gray, 128, 255, cv2.THRESH_BINARY)[1]
    subtitle_text = pytesseract.image_to_string(subtitle_gray, config="--psm 6").lower()
    print("Detected subtitles:", subtitle_text)

    for word in MUTE_KEYWORDS:
        if word in subtitle_text:
            pyautogui.press("mute")
            speak(f"Muted scene due to: {word}")

    for word in SKIP_KEYWORDS:
        if word in subtitle_text:
            pyautogui.press("right")
            speak(f"Skipped scene due to: {word}")

def rewind_action():
    pyautogui.press("left")
    speak("Rewinding scene!")

def pause_action():
    pyautogui.press("space")
    speak("Toggling pause!")

def listen_for_commands():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for voice command...")
        audio = recognizer.listen(source)
    
    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"Recognized command: {command}")
        
        if "mute this scene" in command:
            pyautogui.press("mute")
        elif "skip scene" in command:
            pyautogui.press("right")
        elif "undo" in command:
            pyautogui.press("left")
        elif "rewind" in command:
            rewind_action()
        elif "pause" in command:
            pause_action()
        elif "toggle filtering" in command:
            toggle_filtering()
        else:
            print("Command not recognized.")
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
    except sr.RequestError:
        print("Could not request results, check your internet connection.")

if __name__ == "__main__":
    print("Starting AI filter for streaming services...")
    capture_screen()
