import json
import sqlite3
from datetime import datetime

class SharedMemory:
    def __init__(self, db_path="shared_memory.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT,
                timestamp TEXT,
                source_type TEXT,
                step TEXT,
                extracted_data TEXT
            )
        """)
        self.conn.commit()

    def log_entry(self, conversation_id, data):
        self.cursor.execute("""
            INSERT INTO memory (conversation_id, timestamp, source_type, step, extracted_data)
            VALUES (?, ?, ?, ?, ?)
        """, (
            conversation_id,
            data.get("timestamp", datetime.now().isoformat()),
            data.get("format", "Unknown"),
            data.get("step", "unspecified"),
            json.dumps(data)
        ))
        self.conn.commit()

    def get_history(self, conversation_id):
        self.cursor.execute("""
            SELECT * FROM memory WHERE conversation_id=?
            ORDER BY timestamp ASC
        """, (conversation_id,))
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]
