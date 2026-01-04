import sqlite3
import hashlib
import json
import pandas as pd
from datetime import datetime

DB_NAME = "chatguard.db"

def init_db():
    """Initialize the database with users and history tables."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Users Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Scan History Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS scan_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            target_model TEXT,
            score REAL,
            pass_rate REAL,
            scan_data TEXT,  -- JSON string of full results
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    
    conn.commit()
    
    # Pre-seed admin account if it doesn't exist
    try:
        admin_hash = hashlib.sha256("admin123".encode()).hexdigest()
        c.execute('INSERT OR IGNORE INTO users (username, password_hash) VALUES (?, ?)', 
                  ("admin", admin_hash))
        conn.commit()
    except:
        pass
    
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', 
                  (username, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT id FROM users WHERE username = ? AND password_hash = ?', 
              (username, hash_password(password)))
    user = c.fetchone()
    conn.close()
    return user[0] if user else None

def save_scan(user_id, target_model, score, pass_rate, results_list):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    json_data = json.dumps(results_list)
    c.execute('''
        INSERT INTO scan_history (user_id, target_model, score, pass_rate, scan_data)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, target_model, score, pass_rate, json_data))
    conn.commit()
    conn.close()

def get_user_history(user_id):
    conn = sqlite3.connect(DB_NAME)
    query = "SELECT id, timestamp, target_model, score, pass_rate FROM scan_history WHERE user_id = ? ORDER BY timestamp DESC"
    df = pd.read_sql_query(query, conn, params=(user_id,))
    conn.close()
    return df

def get_scan_details(scan_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT scan_data FROM scan_history WHERE id = ?", (scan_id,))
    data = c.fetchone()
    conn.close()
    return json.loads(data[0]) if data else []
