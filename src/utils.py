"""
Utility functions: minimal SQLite store for candidate uploads and helper functions
"""
import sqlite3
from pathlib import Path
from typing import Dict, Any
import os

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "candidates.db"


def init_db(db_path=DB_PATH):
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        file_path TEXT,
        score REAL,
        similarity REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()


def insert_candidate(name: str, email: str, file_path: str, score: float, similarity: float, db_path=DB_PATH):
    conn = sqlite3.connect(str(db_path))
    c = conn.cursor()
    c.execute("INSERT INTO candidates (name,email,file_path,score,similarity) VALUES (?,?,?,?,?)",
              (name, email, file_path, score, similarity))
    conn.commit()
    conn.close()


def query_candidates(limit=10, db_path=DB_PATH):
    conn = sqlite3.connect(str(db_path))
    c = conn.cursor()
    c.execute("SELECT id,name,email,file_path,score,similarity,created_at FROM candidates ORDER BY created_at DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return rows
