# AI Filtering System

### Letting Good Things Come ✨

## Overview
This AI-powered content filtering system provides real-time moderation for streaming videos by automatically **muting, skipping, or logging** objectionable content based on user preferences. Users can customize filtering settings through a **Flask-based admin dashboard** and even control the AI via **voice commands**.

## Features 🔥
✅ **Admin Dashboard** – Manage user profiles & view filtering analytics.
✅ **Real-Time AI Analytics** – Track how often filtering actions are triggered.
✅ **Voice Commands** – Control actions using commands like "Mute this scene!".
✅ **Multiple Profiles** – Different filtering settings for different users.
✅ **Speech Recognition & Voice Feedback** – AI confirms actions aloud.
✅ **SQLite Database** – Stores user settings, logs, and filtering history.
✅ **OCR-Based Subtitle Detection** – Extracts subtitles for keyword filtering.
✅ **Works on Streaming Platforms** – Applies filtering in real time to Netflix, Hulu, YouTube, etc.

---

## Installation ⚙️

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/YOUR-REPO/AI_Filtering_System.git
cd AI_Filtering_System
```

### **2️⃣ Install Dependencies**
Ensure you have **Python 3.8+** installed, then run:
```bash
pip install -r requirements.txt
```

### **3️⃣ Initialize the Database**
```bash
python database_setup.py
```
- This will create the `filtering.db` SQLite database for storing profiles and logs.

### **4️⃣ Start the Admin Dashboard**
```bash
python admin_dashboard.py
```
- Open **`http://localhost:5000`** in your browser to manage settings.

### **5️⃣ Enable Voice Commands**
```bash
python voice_commands.py
```
- Speak **"Mute this scene!"** or **"Skip scene!"** to control the AI.

### **6️⃣ Run AI Filtering System**
```bash
python ai_filtering_system.py
```
- The system will start monitoring streaming windows for objectionable content.

---

## Folder Structure 📁
```
📂 AI_Filtering_System/
│── 📜 ai_filtering_system.py       # Main AI Filtering Script (Live Filtering for Streaming)
│── 📜 admin_dashboard.py           # Flask Admin Dashboard for User Management
│── 📜 database_setup.py            # SQLite Database Initialization & Schema Setup
│── 📜 voice_commands.py            # Voice Command System for AI Control
│── 📂 templates/
│   │── 📜 dashboard.html           # HTML for Web Dashboard
│── 📂 static/
│   │── 📜 filter_chart.png         # Graph Image for Dashboard
│── 📜 requirements.txt             # Required Python Libraries
│── 📜 README.md                    # Setup & Usage Instructions
```

---

## How It Works 🎬
### **1️⃣ Subtitle-Based Filtering**
- The AI captures subtitles from streaming services using **OCR (Optical Character Recognition)**.
- It scans for **predefined objectionable words** (e.g., profanity, violence, horror-related terms).
- When a match is found, it triggers the appropriate **remote control action** (mute, skip, rewind, etc.).

### **2️⃣ Real-Time Monitoring**
- The system runs continuously in the background, **detecting streaming video windows**.
- It integrates with services like **Netflix, Hulu, YouTube, Amazon Prime**, and more.
- Uses **MSS (screen capture) & OpenCV** to analyze video content in real-time.

### **3️⃣ Voice Control**
- Users can issue voice commands like:
  - **"Mute this scene!"** → Mutes audio temporarily.
  - **"Skip scene!"** → Jumps forward to avoid unwanted content.
  - **"Undo"** → Rewinds to restore playback.
- Uses **SpeechRecognition + pyttsx3** for speech processing and feedback.

### **4️⃣ Admin Dashboard**
- A web-based dashboard built with **Flask & Bootstrap**.
- Allows users to:
  - **Create/Edit/Delete profiles** with different filtering settings.
  - **View logs & analytics** on how often filtering actions were triggered.
  - **Toggle filtering ON/OFF** dynamically.

---

## To-Do List (Future Features) 🚀
- [ ] **Real-Time Dashboard Updates** – Auto-refresh logs as actions occur.
- [ ] **AI Smart Recommendations** – Suggest filters based on viewing history.
- [ ] **Multi-Language Support** – Enable filtering in different languages.
- [ ] **Adaptive Learning** – AI refines filtering decisions based on user feedback.
- [ ] **Mobile & Browser Extension Support** – Apply filtering on more platforms.

**Enjoy AI-powered content filtering for a safer viewing experience! 🎥**

