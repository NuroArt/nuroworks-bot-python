"""
Tiny SQLite layer for tracking leads and follow-up state.
No external DB needed — the file lives alongside the bot.
"""

import sqlite3
from datetime import datetime, timezone

DB_PATH = "nuroworks_bot.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            chat_id INTEGER PRIMARY KEY,
            username TEXT,
            first_seen TEXT,
            got_checklist INTEGER DEFAULT 0,
            viewed_product INTEGER DEFAULT 0,
            started_service INTEGER DEFAULT 0,
            followup_sent INTEGER DEFAULT 0,
            opted_out INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


def touch_user(chat_id: int, username: str | None):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """INSERT INTO users (chat_id, username, first_seen)
           VALUES (?, ?, ?)
           ON CONFLICT(chat_id) DO NOTHING""",
        (chat_id, username, datetime.now(timezone.utc).isoformat()),
    )
    conn.commit()
    conn.close()


def mark_event(chat_id: int, field: str):
    """field must be one of the known columns, e.g. 'got_checklist'"""
    allowed = {"got_checklist", "viewed_product", "started_service",
               "followup_sent", "opted_out"}
    if field not in allowed:
        raise ValueError(f"Unknown field: {field}")
    conn = sqlite3.connect(DB_PATH)
    conn.execute(f"UPDATE users SET {field} = 1 WHERE chat_id = ?", (chat_id,))
    conn.commit()
    conn.close()


def get_user(chat_id: int):
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute(
        "SELECT * FROM users WHERE chat_id = ?", (chat_id,)
    ).fetchone()
    conn.close()
    return row


def users_needing_followup(cutoff_iso: str):
    """Leads/product-viewers, no purchase started, no followup sent, not opted out,
    who first appeared before the cutoff time."""
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        """SELECT chat_id FROM users
           WHERE (got_checklist = 1 OR viewed_product = 1)
           AND started_service = 0
           AND followup_sent = 0
           AND opted_out = 0
           AND first_seen < ?""",
        (cutoff_iso,),
    ).fetchall()
    conn.close()
    return [r[0] for r in rows]
