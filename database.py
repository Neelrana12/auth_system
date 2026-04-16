import sqlite3
import os
from datetime import datetime, timedelta

# SQLite database file
DB_PATH = "cyberguard.db"

def get_db():
    """Connect to SQLite Database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with required tables."""
    conn = get_db()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            is_locked INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create attempts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            ip TEXT,
            count INTEGER DEFAULT 1,
            last_attempt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create logs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            action TEXT NOT NULL,
            ip TEXT DEFAULT 'N/A',
            status TEXT DEFAULT 'info',
            time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

def row_to_dict(row):
    """Convert sqlite3.Row to dictionary."""
    if row is None:
        return None
    return dict(row)

# ─── Auth helpers ────────────────────────────────────────────────────────────

def get_user_by_username(username):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = row_to_dict(cursor.fetchone())
    cursor.close()
    conn.close()
    return user

def get_user_by_email(email):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = row_to_dict(cursor.fetchone())
    cursor.close()
    conn.close()
    return user

def create_user(full_name, username, email, hashed_password, role="user"):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (full_name, username, email, password, role) VALUES (?,?,?,?,?)",
        (full_name, username, email, hashed_password, role)
    )
    conn.commit()
    cursor.close()
    conn.close()

# ─── Attempt helpers ─────────────────────────────────────────────────────────

def get_attempts(username):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attempts WHERE username = ?", (username,))
    result = row_to_dict(cursor.fetchone())
    cursor.close()
    conn.close()
    return result

def increment_attempt(username, ip):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM attempts WHERE username = ?", (username,))
    existing = cursor.fetchone()
    if existing:
        cursor.execute(
            "UPDATE attempts SET count = count + 1, last_attempt = CURRENT_TIMESTAMP, ip = ? WHERE username = ?",
            (ip, username)
        )
    else:
        cursor.execute(
            "INSERT INTO attempts (username, ip, count) VALUES (?,?,1)",
            (username, ip)
        )
    conn.commit()
    cursor.close()
    conn.close()

def reset_attempts(username):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM attempts WHERE username = ?", (username,))
    conn.commit()
    cursor.close()
    conn.close()

def is_account_locked(username):
    row = get_attempts(username)
    if row and row["count"] >= 5:
        last = datetime.strptime(str(row["last_attempt"]), "%Y-%m-%d %H:%M:%S")
        if datetime.now() - last < timedelta(minutes=10):
            return True, row["count"]
    return False, 0

# ─── Log helpers ─────────────────────────────────────────────────────────────

def add_log(username, action, ip="N/A", status="info"):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO logs (username, action, ip, status) VALUES (?,?,?,?)",
        (username, action, ip, status)
    )
    conn.commit()
    cursor.close()
    conn.close()

# ─── Dashboard data helpers ───────────────────────────────────────────────────

def get_all_logs(limit=200):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM logs ORDER BY time DESC LIMIT ?", (limit,)
    )
    rows = cursor.fetchall()
    result = [row_to_dict(r) for r in rows]
    cursor.close()
    conn.close()
    return result

def get_user_logs(username, limit=50):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM logs WHERE username = ? ORDER BY time DESC LIMIT ?",
        (username, limit)
    )
    rows = cursor.fetchall()
    result = [row_to_dict(r) for r in rows]
    cursor.close()
    conn.close()
    return result

def get_all_users():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, full_name, username, email, role, created_at, is_locked FROM users ORDER BY created_at DESC")
    rows = cursor.fetchall()
    result = [row_to_dict(r) for r in rows]
    cursor.close()
    conn.close()
    return result

def get_suspicious_users(threshold=3):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT username, ip, count, last_attempt FROM attempts WHERE count >= ? ORDER BY count DESC",
        (threshold,)
    )
    rows = cursor.fetchall()
    result = [row_to_dict(r) for r in rows]
    cursor.close()
    conn.close()
    return result

def delete_user(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()

def get_stats():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM logs WHERE action = 'Login Success'")
    total_logins = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM logs WHERE action = 'Login Failed'")
    failed_logins = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM attempts WHERE count >= 3")
    suspicious = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return {
        "total_users": total_users,
        "total_logins": total_logins,
        "failed_logins": failed_logins,
        "suspicious": suspicious,
    }


