import sqlite3

def init_db():
    with sqlite3.connect("mentor.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mentors (
                id INTEGER PRIMARY KEY,
                name TEXT,
                username TEXT
            )
        """)
        conn.commit() 


def register_mentor(mentor_id: int, name: str, username: str):
    with sqlite3.connect("mentor.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO mentors (id, name, username)
            VALUES (?, ?, ?)
        """, (mentor_id, name, username)) 
        conn.commit()

def is_mentor_registered(mentor_id: int) -> bool:
    with sqlite3.connect("mentor.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM mentors WHERE id = ?", (mentor_id,))
        return cursor.fetchone() is not None
        