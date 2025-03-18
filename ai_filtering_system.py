import os
import sqlite3
import json
import pyttsx3
import pyautogui
import speech_recognition as sr
import matplotlib.pyplot as plt
import pandas as pd
from flask import Flask, render_template, request, redirect

# Initialize Flask App
app = Flask(__name__)

# Initialize SQLite Database
def init_db():
    conn = sqlite3.connect("filtering.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            filtering_enabled BOOLEAN DEFAULT TRUE
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            timestamp TEXT,
            action TEXT,
            content TEXT,
            user_feedback TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Function to log filtering actions
def log_filter_action(action, content, user_feedback=""):
    conn = sqlite3.connect("filtering.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs VALUES (?, ?, ?, ?)", 
                   (pd.Timestamp.now(), action, content, user_feedback))
    conn.commit()
    conn.close()

# Flask Route: Dashboard
def get_filter_logs():
    conn = sqlite3.connect("filtering.db")
    df = pd.read_sql_query("SELECT action, COUNT(*) as count FROM logs GROUP BY action", conn)
    conn.close()
    return df

@app.route("/")
def index():
    df = get_filter_logs()
    
    # Generate a bar chart
    plt.figure(figsize=(6, 4))
    plt.bar(df["action"], df["count"], color=["red", "blue"])
    plt.xlabel("Filtering Action")
    plt.ylabel("Count")
    plt.title("Filtering Actions Frequency")
    plt.savefig("static/filter_chart.png")  # Save the graph
    plt.close()

    return render_template("dashboard.html", img_url="/static/filter_chart.png")

# Flask Route: Add/Delete User Profiles
def get_profiles():
    conn = sqlite3.connect("filtering.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profiles")
    profiles = cursor.fetchall()
    conn.close()
    return profiles

@app.route("/add_profile", methods=["POST"])
def add_profile():
    name = request.form["name"]
    conn = sqlite3.connect("filtering.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO profiles (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/delete_profile/<int:id>")
def delete_profile(id):
    conn = sqlite3.connect("filtering.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM profiles WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

# Voice Feedback System
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

# Voice Command System
recognizer = sr.Recognizer()
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
    app.run(debug=True, host="0.0.0.0", port=5000)
