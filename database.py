import psycopg2
from datetime import datetime, timedelta
import os

def get_db():
    """Connect to Supabase PostgreSQL."""
    try:
        return psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            port=os.getenv("DB_PORT", "5432")
        )
    except Exception as e:
        print(f"Database connection error: {e}")
        raise

def row_to_dict(cursor, row):
    """Convert psycopg2 row to dictionary."""
    if row is None:
        return None
    columns = [desc[0] for desc in cursor.description]
    return dict(zip(columns, row))

# ─── Auth helpers ────────────────────────────────────────────────────────────

def get_user_by_username(username):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        row = cursor.fetchone()
        user = row_to_dict(cursor, row)
        cursor.close()
        conn.close()
        return user
    except Exception as e:
        print(f"Error getting user by username: {e}")
        return None

def get_user_by_email(email):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        row = cursor.fetchone()
        user = row_to_dict(cursor, row)
        cursor.close()
        conn.close()
        return user
    except Exception as e:
        print(f"Error getting user by email: {e}")
        return None

def create_user(full_name, username, email, hashed_password, role="user"):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (full_name, username, email, password, role) VALUES (%s,%s,%s,%s,%s)",
            (full_name, username, email, hashed_password, role)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error creating user: {e}")
        raise

# ─── Attempt helpers ─────────────────────────────────────────────────────────

def get_attempts(username):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM attempts WHERE username = %s", (username,))
        row = cursor.fetchone()
        result = row_to_dict(cursor, row)
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        print(f"Error getting attempts: {e}")
        return None

def increment_attempt(username, ip):
    try:
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
    except Exception as e:
        print(f"Error incrementing attempt: {e}")

def reset_attempts(username):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM attempts WHERE username = %s", (username,))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error resetting attempts: {e}")

def is_account_locked(username):
    try:
        row = get_attempts(username)
        if not row or row.get("count", 0) < 5:
            return False, 0
        
        last = row.get("last_attempt")
        if not last:
            return False, 0
        
        # Handle different datetime formats
        if isinstance(last, str):
            last = datetime.strptime(last, "%Y-%m-%d %H:%M:%S")
        elif hasattr(last, 'tzinfo') and last.tzinfo is not None:
            last = last.replace(tzinfo=None)
        
        # Check if locked (5+ attempts within 10 minutes)
        if datetime.now() - last < timedelta(minutes=10):
            return True, row.get("count", 0)
        return False, 0
    except Exception as e:
        print(f"Error in is_account_locked: {e}")
        return False, 0

# ─── Log helpers ─────────────────────────────────────────────────────────────

def add_log(username, action, ip="N/A", status="info"):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO logs (username, action, ip, status) VALUES (%s,%s,%s,%s)",
            (username, action, ip, status)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error adding log: {e}")

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


