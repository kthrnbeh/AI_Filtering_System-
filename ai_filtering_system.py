import os
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Only import PyAutoGUI if a display is available
if "DISPLAY" in os.environ or os.name == "nt":
    import pyautogui
else:
    print("Warning: No display detected! Disabling PyAutoGUI features.")

# Safe function replacement if PyAutoGUI is not available
def safe_press(key):
    if "pyautogui" in globals():
        pyautogui.press(key)
    else:
        print(f"Simulated key press: {key}")

# Replace pyautogui.press with safe_press in your code
# Add this at the bottom of your ai_filtering_system.py file

def filter_content(video=None, audio=None, subtitles=None, categories=None, mode=None):
    print("🧠 Running AI Filtering System...")
    print(f"Video: {video}")
    print(f"Audio: {audio}")
    print(f"Subtitles: {subtitles}")
    print(f"Categories: {categories}")
    print(f"Mode: {mode}")
    
    # 👇 You can integrate your actual filtering logic here later
    # For now, this just simulates a result
    return {
        "message": "Filtering complete!",
        "filtered_categories": categories,
        "mode_used": mode
    }
