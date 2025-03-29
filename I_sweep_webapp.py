from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
import os
from ai_filtering_system import filter_content  # Import your filtering logic

app = Flask(__name__)
app.secret_key = 'secretkey'  # Change this in production
login_manager = LoginManager()
login_manager.init_app(app)

# --- Database Setup ---
DB_PATH = 'isweep.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT,
                    tier TEXT,
                    total_paid REAL DEFAULT 0.0
                )''')
    conn.commit()
    conn.close()

init_db()

# --- User Loader ---
class User(UserMixin):
    def __init__(self, id, username, tier, total_paid):
        self.id = id
        self.username = username
        self.tier = tier
        self.total_paid = total_paid

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, username, tier, total_paid FROM users WHERE id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return User(*row)
    return None

# --- Routes ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT id, username, tier, total_paid FROM users WHERE username = ? AND password = ?", (username, password))
        row = c.fetchone()
        conn.close()
        if row:
            user = User(*row)
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        tier = request.form['tier']
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password, tier) VALUES (?, ?, ?)", (username, password, tier))
            conn.commit()
        except sqlite3.IntegrityError:
            return "Username already exists."
        conn.close()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/start_filtering', methods=['POST'])
@login_required
def start_filtering():
    video = request.files.get('video')
    audio = request.files.get('audio')
    subtitles = request.files.get('subtitles')
    youtube_url = request.form.get('youtube_url')
    categories = request.form.getlist('categories[]')
    mode = request.form.get('mode')

    # Save files if they exist
    video_path = os.path.join('uploads', video.filename) if video else None
    audio_path = os.path.join('uploads', audio.filename) if audio else None
    subtitles_path = os.path.join('uploads', subtitles.filename) if subtitles else None

    if video:
        video.save(video_path)
    if audio:
        audio.save(audio_path)
    if subtitles:
        subtitles.save(subtitles_path)

    # Run filtering logic
    result = filter_content(
        video=video_path,
        audio=audio_path,
        subtitles=subtitles_path,
        categories=categories,
        mode=mode
    )

    return jsonify({"status": "Filtering complete", "result": result})

@app.route('/subscribe')
@login_required
def subscribe():
    return render_template('subscribe.html', user=current_user)

# --- Sample Users Setup (Run Once) ---
def create_sample_users():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    sample_users = [
        ('freeuser', 'pass', 'free', 0.0),
        ('flexuser', 'pass', 'subscription', 42.0),
        ('owneruser', 'pass', 'owner', 350.0),
    ]
    for u in sample_users:
        try:
            c.execute("INSERT INTO users (username, password, tier, total_paid) VALUES (?, ?, ?, ?)", u)
        except sqlite3.IntegrityError:
            continue
    conn.commit()
    conn.close()

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    if not os.path.exists(DB_PATH):
        init_db()
        create_sample_users()
    app.run(debug=True)
