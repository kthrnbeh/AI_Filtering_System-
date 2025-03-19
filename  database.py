import sqlite3

# Function to initialize the database and create necessary tables
def init_db():
    conn = sqlite3.connect("filtering.db")  # Connect to the SQLite database (creates file if not exists)
    cursor = conn.cursor()
    
    # Create profiles table to store user settings
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique ID for each profile
            name TEXT UNIQUE,                      -- Unique profile name
            filtering_enabled BOOLEAN DEFAULT TRUE -- Toggle for enabling/disabling filtering
        )
    """)
    
    # Create logs table to store filtering actions and user feedback
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT, -- Unique ID for each log entry
            timestamp TEXT,                       -- Timestamp of the filtering action
            action TEXT,                          -- Type of action performed (mute/skip)
            content TEXT,                         -- Detected content that triggered the action
            user_feedback TEXT                    -- User feedback on the filtering accuracy
        )
    """)
    
    conn.commit()  # Save changes
    conn.close()   # Close connection

# Run the function to ensure the database is set up when the script is executed
if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")