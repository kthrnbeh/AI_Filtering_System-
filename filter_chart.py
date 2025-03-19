import mss
import cv2
import numpy as np
import pygetwindow as gw
import pyautogui
import pytesseract
import speech_recognition as sr
import pyttsx3
import tkinter as tk
from tkinter import messagebox

# Configure OCR for subtitle detection
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Change path for Mac/Linux

# List of words to mute or skip
MUTE_KEYWORDS = [
    "fuck", "shit", "bitch", "damn", "cunt", "asshole", "bastard", "suck", 
    "jesus christ", "goddamn", "oh my god", "hell"
]  # List of words that trigger muting
SKIP_KEYWORDS = ["violence", "blood", "scary"]  # List of words that trigger scene skipping

# Initialize text-to-speech engine for voice feedback
engine = pyttsx3.init()

def speak(text):
    """Speaks the given text aloud using TTS engine."""
    engine.say(text)
    engine.runAndWait()

# Global variable to enable/disable filtering
FILTERING_ENABLED = True  

def toggle_filtering():
    """Toggles the filtering system on or off."""
    global FILTERING_ENABLED
    FILTERING_ENABLED = not FILTERING_ENABLED
    state = "enabled" if FILTERING_ENABLED else "disabled"
    messagebox.showinfo("Filtering Status", f"Filtering is now {state}")
    print(f"Filtering is now {state}")

def capture_screen():
    """Captures and processes the streaming video window in real-time."""
    with mss.mss() as sct:
        while True:
            # Identify an active streaming service window
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

            # Capture screen area of detected window
            x, y, width, height = window[0]._rect
            screenshot = sct.grab({"top": y, "left": x, "width": width, "height": height})
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

            # Process the captured frame to analyze subtitles
            process_frame(frame)

            if not FILTERING_ENABLED:
                continue

    cv2.destroyAllWindows()

def process_frame(frame):
    """Processes the frame to detect inappropriate content using subtitles."""
    if not FILTERING_ENABLED:
        return

    # Extract subtitles using OCR (bottom part of the screen)
    h, w, _ = frame.shape
    subtitle_region = frame[int(h * 0.8):, :]  # Focus on the bottom 20% of the screen
    subtitle_gray = cv2.cvtColor(subtitle_region, cv2.COLOR_BGR2GRAY)
    subtitle_gray = cv2.threshold(subtitle_gray, 128, 255, cv2.THRESH_BINARY)[1]
    subtitle_text = pytesseract.image_to_string(subtitle_gray, config="--psm 6").lower()
    print("Detected subtitles:", subtitle_text)

    # Check subtitles for words that require muting
    for word in MUTE_KEYWORDS:
        if word in subtitle_text:
            pyautogui.press("mute")  # Mutes the video/audio
            speak(f"Muted scene due to: {word}")

    # Check subtitles for words that trigger scene skipping
    for word in SKIP_KEYWORDS:
        if word in subtitle_text:
            pyautogui.press("right")  # Skips to the next scene
            speak(f"Skipped scene due to: {word}")

def create_gui():
    """Creates a simple GUI for enabling/disabling filtering."""
    root = tk.Tk()
    root.title("AI Filtering System")
    root.geometry("300x200")
    
    # Label for the filtering options
    tk.Label(root, text="Select Filtering Options:", font=("Arial", 12)).pack(pady=10)
    
    # Button to toggle filtering ON/OFF
    toggle_button = tk.Button(root, text="Toggle Filtering", font=("Arial", 10), command=toggle_filtering)
    toggle_button.pack(pady=5)
    
    # Button to exit the application
    exit_button = tk.Button(root, text="Exit", font=("Arial", 10), command=root.quit)
    exit_button.pack(pady=5)
    
    # Launch the GUI window
    root.mainloop()

if __name__ == "__main__":
    create_gui()  # Start the GUI when the script is run