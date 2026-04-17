# Supabase Migration Guide

## 1. Environment Setup

Create a `.env` file in your project root:

```
DB_HOST=your-project.supabase.co
DB_NAME=postgres
DB_USER=postgres
DB_PASS=your_password
DB_PORT=5432
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Key changes:
- ✅ Replaced `pyodbc` → `psycopg2-binary`
- ✅ Added `python-dotenv` for environment variables

## 3. Quick Examples

### Example 1: Insert User

```python
from database import get_db

conn = get_db()
cursor = conn.cursor()

cursor.execute(
    "INSERT INTO users (full_name, username, email, password, role) VALUES (%s,%s,%s,%s,%s)",
    ("John Doe", "johndoe", "john@example.com", "hashed_password_here", "user")
)

conn.commit()
cursor.close()
conn.close()

print("User inserted successfully!")
```

### Example 2: Login Query

```python
from database import get_user_by_username

user = get_user_by_username("johndoe")

if user:
    print(f"Found user: {user['username']}")
    print(f"Email: {user['email']}")
    print(f"Role: {user['role']}")
else:
    print("User not found")
```

### Example 3: Track Failed Login Attempt

```python
from database import increment_attempt

increment_attempt("johndoe", "192.168.1.1")
print("Failed attempt logged")
```

### Example 4: Add Log Entry

```python
from database import add_log

add_log("johndoe", "Login Success", "192.168.1.1", "info")
print("Log entry added")
```

## 4. Key Changes from Azure SQL → Supabase/PostgreSQL

| Feature | Azure SQL (pyodbc) | Supabase/PostgreSQL (psycopg2) |
|---------|-------------------|--------------------------------|
| Placeholder | `?` | `%s` |
| Timestamp | `CURRENT_TIMESTAMP` | `NOW()` |
| Connection String | Driver-based | Host-based |
| Password | In code | `.env` file |

## 5. Running Your App

```bash
python app.py
```

Your Flask routes in `routes/auth.py` and `routes/dashboard.py` will work **without any changes**.

## 6. Supabase Connection String Example

From Supabase Dashboard → Settings → Database:
```
Server: your-project.supabase.co
Username: postgres
Password: (your password)
Port: 5432
Database: postgres
```

All these values go into your `.env` file.

## ✅ All Features Working

- ✅ Register user
- ✅ Login
- ✅ Attempts tracking (brute force protection)
- ✅ Logs
- ✅ Dashboard (admin/user views)
- ✅ Account lockout (5 failed attempts = 10 min lockout)

No route changes needed!
