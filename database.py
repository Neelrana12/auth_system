import psycopg2
from datetime import datetime, timedelta
import os

def get_db():
    """Connect to Supabase PostgreSQL."""
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        port=os.getenv("DB_PORT", "5432")
    )

def row_to_dict(cursor, row):
    """Convert psycopg2 row to dictionary."""
    if row is None:
        return None
    columns = [desc[0] for desc in cursor.description]
    return dict(zip(columns, row))

# ─── Auth helpers ────────────────────────────────────────────────────────────

def get_user_by_username(username):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    row = cursor.fetchone()
    user = row_to_dict(cursor, row)
    cursor.close()
    conn.close()
    return user

def get_user_by_email(email):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    row = cursor.fetchone()
    user = row_to_dict(cursor, row)
    cursor.close()
    conn.close()
    return user

def create_user(full_name, username, email, hashed_password, role="user"):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (full_name, username, email, password, role) VALUES (%s,%s,%s,%s,%s)",
        (full_name, username, email, hashed_password, role)
    )
    conn.commit()
    cursor.close()
    conn.close()

# ─── Attempt helpers ─────────────────────────────────────────────────────────

def get_attempts(username):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attempts WHERE username = %s", (username,))
    row = cursor.fetchone()
    result = row_to_dict(cursor, row)
    cursor.close()
    conn.close()
    return result

def increment_attempt(username, ip):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM attempts WHERE username = %s", (username,))
    existing = cursor.fetchone()
    if existing:
        cursor.execute(
            "UPDATE attempts SET count = count + 1, last_attempt = NOW(), ip = %s WHERE username = %s",
            (ip, username)
        )
    else:
        cursor.execute(
            "INSERT INTO attempts (username, ip, count) VALUES (%s,%s,1)",
            (username, ip)
        )
    conn.commit()
    cursor.close()
    conn.close()

def reset_attempts(username):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM attempts WHERE username = %s", (username,))
    conn.commit()
    cursor.close()
    conn.close()

def is_account_locked(username):
    row = get_attempts(username)
    if row and row["count"] >= 5:
        last = row["last_attempt"]
        if isinstance(last, str):
            last = datetime.strptime(last, "%Y-%m-%d %H:%M:%S")
        if datetime.now() - last < timedelta(minutes=10):
            return True, row["count"]
    return False, 0

# ─── Log helpers ─────────────────────────────────────────────────────────────

def add_log(username, action, ip="N/A", status="info"):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO logs (username, action, ip, status) VALUES (%s,%s,%s,%s)",
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
        "SELECT * FROM logs ORDER BY time DESC LIMIT %s", (limit,)
    )
    rows = cursor.fetchall()
    result = [row_to_dict(cursor, r) for r in rows]
    cursor.close()
    conn.close()
    return result

def get_user_logs(username, limit=50):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM logs WHERE username = %s ORDER BY time DESC LIMIT %s",
        (username, limit)
    )
    rows = cursor.fetchall()
    result = [row_to_dict(cursor, r) for r in rows]
    cursor.close()
    conn.close()
    return result

def get_all_users():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, full_name, username, email, role, created_at, is_locked FROM users ORDER BY created_at DESC")
    rows = cursor.fetchall()
    result = [row_to_dict(cursor, r) for r in rows]
    cursor.close()
    conn.close()
    return result

def get_suspicious_users(threshold=3):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT username, ip, count, last_attempt FROM attempts WHERE count >= %s ORDER BY count DESC",
        (threshold,)
    )
    rows = cursor.fetchall()
    result = [row_to_dict(cursor, r) for r in rows]
    cursor.close()
    conn.close()
    return result

def delete_user(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
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


