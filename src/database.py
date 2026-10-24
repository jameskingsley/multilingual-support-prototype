import sqlite3
from datetime import datetime

DB_PATH = "data/support_chat.db"


def get_connection():
    """Creates and returns a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes the database and creates the messages table if it doesn't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id TEXT NOT NULL,
            sender_type TEXT NOT NULL,
            original_text TEXT NOT NULL,
            translated_text TEXT NOT NULL,
            source_lang TEXT NOT NULL,
            target_lang TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_message(
    ticket_id: str,
    sender_type: str,
    original_text: str,
    translated_text: str,
    source_lang: str,
    target_lang: str,
):
    """Logs an inbound or outbound message exchange to the database."""
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.utcnow().isoformat()

    cursor.execute(
        """
        INSERT INTO messages (ticket_id, sender_type, original_text, translated_text, source_lang, target_lang, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
        (
            ticket_id,
            sender_type,
            original_text,
            translated_text,
            source_lang,
            target_lang,
            timestamp,
        ),
    )

    conn.commit()
    conn.close()


def get_ticket_history(ticket_id: str):
    """Retrieves all conversation logs for a specific support ticket."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM messages WHERE ticket_id = ? ORDER BY timestamp ASC",
        (ticket_id,),
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]