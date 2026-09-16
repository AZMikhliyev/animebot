import sqlite3

DB_PATH = "anime.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS anime (
            code TEXT PRIMARY KEY,
            message_id INTEGER NOT NULL,
            title TEXT,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def add_anime(code: str, message_id: int, title: str = None):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT OR REPLACE INTO anime (code, message_id, title) VALUES (?, ?, ?)",
        (code.upper(), message_id, title),
    )
    conn.commit()
    conn.close()


def get_anime(code: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT message_id, title FROM anime WHERE code = ?", (code.upper(),))
    row = cur.fetchone()
    conn.close()
    return row


def delete_anime(code: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM anime WHERE code = ?", (code.upper(),))
    deleted = cur.rowcount > 0
    conn.commit()
    conn.close()
    return deleted


def list_anime():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT code, title FROM anime ORDER BY added_at DESC")
    rows = cur.fetchall()
    conn.close()
    return rows


def count_anime() -> int:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM anime")
    n = cur.fetchone()[0]
    conn.close()
    return n
