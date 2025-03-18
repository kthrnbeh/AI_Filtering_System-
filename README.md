# AI_Filtering_System-
Letting good things come 
# AI Filtering System

This AI-powered content filtering system provides real-time moderation for videos by automatically **muting, skipping, or logging** objectionable content. Users can customize filtering settings through a **Flask-based admin dashboard** and even control the AI via **voice commands**.

## Features
✅ **Admin Dashboard** – Manage user profiles & view filtering analytics.
✅ **Real-Time AI Analytics** – See how many times filtering was triggered.
✅ **Voice Commands** – Control actions by saying "Mute this scene!".
✅ **Multiple Profiles** – Different filtering settings for different users.
✅ **Speech Recognition & Voice Feedback** – AI confirms actions aloud.
✅ **SQLite Database** – Stores user settings, logs, and profiles.

---

## Installation
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/YOUR-REPO/AI_Filtering_System.git
cd AI_Filtering_System
```

### **2️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3️⃣ Initialize the Database**
```bash
python database.py
```

### **4️⃣ Run the Admin Dashboard**
```bash
python admin_dashboard.py
```
- Open **`http://localhost:5000`** in your browser.

### **5️⃣ Enable Voice Commands**
```bash
python voice_commands.py
```
- Speak **"Mute this scene!"** or **"Skip scene!"** to control the AI.

---

## Folder Structure
```
📂 AI_Filtering_System/
│── 📜 ai_filtering_system.py       # Main AI Filtering Script (Coming Soon)
│── 📜 admin_dashboard.py            # Flask Admin Dashboard
│── 📜 database.py                  # SQLite Database Initialization
│── 📜 voice_commands.py             # Voice Command System
│── 📂 templates/
│   │── 📜 dashboard.html           # HTML for Web Dashboard
│── 📂 static/
│   │── 📜 filter_chart.png         # Graph Image for Dashboard
│── 📜 requirements.txt              # Required Python Libraries
│── 📜 README.md                     # Setup Instructions
```

---

## To-Do (Future Features)
- [ ] **Real-Time Dashboard Updates** – Auto-refresh logs.
- [ ] **AI Smart Recommendations** – Suggest filters based on history.
- [ ] **Multi-Language Support** – Enable filtering in multiple languages.

🚀 **Enjoy AI-powered content filtering!**