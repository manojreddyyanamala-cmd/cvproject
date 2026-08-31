import sqlite3
import queue
import threading
import os
import time

# 1. Environment Config & Global Connection
DB_PATH = os.getenv("DB_PATH", "visionqueue.db")
_conn = None
db_queue = queue.Queue()

def get_connection():
    global _conn
    if _conn is None:
        # check_same_thread=False allows our background worker to use it
        _conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        _conn.execute("PRAGMA journal_mode = WAL;")
    return _conn

# 2. Asynchronous Worker Thread
def db_writer_thread():
    while True:
        task = db_queue.get()
        if task[0] == "insert_session":
            session_id, camera_source = task[1], task[2]
            conn = get_connection()
            
            # 3. Error Handling & Transaction Safety
            try:
                with conn: 
                    conn.execute(
                        "INSERT INTO sessions (session_id, start_time, camera_source, status) VALUES (?, datetime('now'), ?, 'ACTIVE')",
                        (session_id, camera_source)
                    )
                print(f"Success: Session {session_id} saved asynchronously!")
            except sqlite3.Error as e:
                print(f"Database error: {e}")
        
        db_queue.task_done()

# Start the background worker immediately
threading.Thread(target=db_writer_thread, daemon=True).start()

def add_new_session(session_id, camera_source):
    # 4. Non-blocking Queue Put (Keeps camera frames fast)
    db_queue.put(("insert_session", session_id, camera_source))

if __name__ == "__main__":
    add_new_session("test_async_001", "camera_main")
    # Pause briefly so the background thread has time to finish before the script closes
    time.sleep(1)