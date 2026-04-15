import sqlite3
from datetime import datetime, timedelta
import os

DB_PATH = "database.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with tables. Create default admin if it doesn't exist."""
    conn = get_db()
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_locked INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            action TEXT NOT NULL,
            ip TEXT DEFAULT 'N/A',
            status TEXT DEFAULT 'info',
            time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            ip TEXT DEFAULT 'N/A',
            count INTEGER DEFAULT 0,
            last_attempt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Create default admin user if it doesn't exist
    admin_check = cur.execute("SELECT * FROM users WHERE username = ?", ("admin",)).fetchone()
    if not admin_check:
        # Import bcrypt to hash password - default password is 'admin123' (CHANGE THIS IN PRODUCTION!)
        from flask_bcrypt import Bcrypt
        bcrypt = Bcrypt()
        hashed = bcrypt.generate_password_hash("admin123").decode("utf-8")
        cur.execute(
            "INSERT INTO users (full_name, username, email, password, role) VALUES (?,?,?,?,?)",
            ("Administrator", "admin", "admin@cyberguard.local", hashed, "admin")
        )

    conn.commit()
    conn.close()

# ─── Auth helpers ────────────────────────────────────────────────────────────

def get_user_by_username(username):
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return user

def get_user_by_email(email):
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    return user

def create_user(full_name, username, email, hashed_password, role="user"):
    conn = get_db()
    conn.execute(
        "INSERT INTO users (full_name, username, email, password, role) VALUES (?,?,?,?,?)",
        (full_name, username, email, hashed_password, role)
    )
    conn.commit()
    conn.close()

# ─── Attempt helpers ─────────────────────────────────────────────────────────

def get_attempts(username):
    conn = get_db()
    row = conn.execute("SELECT * FROM attempts WHERE username = ?", (username,)).fetchone()
    conn.close()
    return row

def increment_attempt(username, ip):
    conn = get_db()
    existing = conn.execute("SELECT id FROM attempts WHERE username = ?", (username,)).fetchone()
    if existing:
        conn.execute(
            "UPDATE attempts SET count = count + 1, last_attempt = CURRENT_TIMESTAMP, ip = ? WHERE username = ?",
            (ip, username)
        )
    else:
        conn.execute(
            "INSERT INTO attempts (username, ip, count) VALUES (?,?,1)",
            (username, ip)
        )
    conn.commit()
    conn.close()

def reset_attempts(username):
    conn = get_db()
    conn.execute("DELETE FROM attempts WHERE username = ?", (username,))
    conn.commit()
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
    conn.execute(
        "INSERT INTO logs (username, action, ip, status) VALUES (?,?,?,?)",
        (username, action, ip, status)
    )
    conn.commit()
    conn.close()

# ─── Dashboard data helpers ───────────────────────────────────────────────────

def get_all_logs(limit=200):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM logs ORDER BY time DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_user_logs(username, limit=50):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM logs WHERE username = ? ORDER BY time DESC LIMIT ?",
        (username, limit)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_all_users():
    conn = get_db()
    rows = conn.execute("SELECT id, full_name, username, email, role, created_at, is_locked FROM users ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_suspicious_users(threshold=3):
    conn = get_db()
    rows = conn.execute(
        "SELECT username, ip, count, last_attempt FROM attempts WHERE count >= ? ORDER BY count DESC",
        (threshold,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def delete_user(user_id):
    conn = get_db()
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

def get_stats():
    conn = get_db()
    total_users   = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    total_logins  = conn.execute("SELECT COUNT(*) FROM logs WHERE action = 'Login Success'").fetchone()[0]
    failed_logins = conn.execute("SELECT COUNT(*) FROM logs WHERE action = 'Login Failed'").fetchone()[0]
    suspicious    = conn.execute("SELECT COUNT(*) FROM attempts WHERE count >= 3").fetchone()[0]
    conn.close()
    return {
        "total_users": total_users,
        "total_logins": total_logins,
        "failed_logins": failed_logins,
        "suspicious": suspicious,
    }


