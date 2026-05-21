import sqlite3
import os

DB_PATH = "reports/detections.db"

def init_db():
    os.makedirs("reports", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS detections (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp   TEXT,
            confidence  REAL,
            severity    TEXT,
            lat         REAL,
            lng         REAL,
            image_path  TEXT,
            status      TEXT DEFAULT 'pending'
        )
    """)
    conn.commit()
    conn.close()

def save_detection(d: dict):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        INSERT INTO detections
            (timestamp, confidence, severity, lat, lng, image_path)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (d["timestamp"], d["confidence"], d["severity"],
          d["lat"], d["lng"], d["image_path"]))
    conn.commit()
    conn.close()

def get_all_detections() -> list:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM detections ORDER BY timestamp DESC"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def update_status(detection_id: int, status: str):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "UPDATE detections SET status=? WHERE id=?",
        (status, detection_id)
    )
    conn.commit()
    conn.close()

def get_stats() -> dict:
    conn = sqlite3.connect(DB_PATH)
    stats = {
        "total":   conn.execute("SELECT COUNT(*) FROM detections").fetchone()[0],
        "pending": conn.execute("SELECT COUNT(*) FROM detections WHERE status='pending'").fetchone()[0],
        "fixed":   conn.execute("SELECT COUNT(*) FROM detections WHERE status='fixed'").fetchone()[0],
        "by_severity": dict(conn.execute(
            "SELECT severity, COUNT(*) FROM detections GROUP BY severity"
        ).fetchall())
    }
    conn.close()
    return stats