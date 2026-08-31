import sqlite3

def get_connection():
    # This connects to the database file you already made
    conn = sqlite3.connect("visionqueue.db")
    # This enables WAL so the database doesn't block the camera frames
    conn.execute("PRAGMA journal_mode = WAL;")
    return conn

def add_new_session(session_id, camera_source):
    # This is a function Vijay can use to save a new session!
    conn = get_connection()
    conn.execute(
        "INSERT INTO sessions (session_id, start_time, camera_source, status) VALUES (?, datetime('now'), ?, 'ACTIVE')",
        (session_id, camera_source)
    )
    conn.commit()
    conn.close()
    print(f"Success: Session {session_id} was saved to the database!")

# A quick test to prove it works
if __name__ == "__main__":
    add_new_session("test_001", "camera_front_door")