import sqlite3

def init_db():
    conn = sqlite3.connect("filtering.db")
    cursor = conn.cursor()
    
    # Create profiles table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            filtering_enabled BOOLEAN DEFAULT TRUE
        )
    """)
    
    # Create logs table
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

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")