import os

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
